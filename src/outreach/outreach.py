"""
Cold Outreach System with SuperMemory
记住联系过谁，避免重复，持续优化话术
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.agent_memory import outreach_memory
from datetime import datetime

class OutreachSystem:
    def __init__(self):
        self.already_contacted = set()
        self._load_history()
    
    def _load_history(self):
        """加载历史联系记录"""
        history = outreach_memory.recall("contacted", limit=1000)
        for h in history:
            self.already_contacted.add(h["value"].get("email", ""))
    
    def should_contact(self, business):
        """检查是否应该联系（避免重复）"""
        email = business.get("email", "")
        if email in self.already_contacted:
            return False, "Already contacted"
        
        # 检查最近是否联系过同类商家
        recent = outreach_memory.recall(f"category_{business.get('category')}", limit=5)
        if len(recent) >= 3:
            return False, "Recently contacted same category"
        
        return True, "OK"
    
    def contact(self, business, channel="email"):
        """联系商家并记忆"""
        email = business.get("email")
        name = business.get("name")
        category = business.get("category", "unknown")
        
        # 记忆联系过
        outreach_memory.remember("contacted", {
            "email": email,
            "name": name,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "channel": channel
        })
        
        # 记忆同类商家联系次数
        outreach_memory.remember(f"category_{category}", {
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"✓ Contacted: {name} ({email}) via {channel}")
        return True
    
    def learn_result(self, email, result):
        """记忆联系结果（是否回复、成交等）"""
        outreach_memory.learn(f"outreach_to_{email}", result)
        print(f"  → Learned: {result}")
    
    def get_best_category(self):
        """找出最容易成功的商家类别"""
        learnings = outreach_memory.memory.get("learnings", [])
        results = [l for l in learnings if "outreach_to_" in l["event"]]
        
        categories = {}
        for r in results:
            if "success" in r["result"].lower():
                cat = r["event"].split("_")[-1]
                categories[cat] = categories.get(cat, 0) + 1
        
        if categories:
            best = max(categories.items(), key=lambda x: x[1])
            return best[0], best[1]
        return None, 0
    
    def suggest_next_category(self):
        """建议下一个联系的商家类别"""
        best_cat, best_count = self.get_best_category()
        if best_cat:
            return f"继续联系 {best_cat} 类商家（成功率最高）"
        return "测试新类别商家"

if __name__ == "__main__":
    outreach = OutreachSystem()
    
    # 测试
    test_business = {
        "email": "test@restaurant.com",
        "name": "Test Restaurant",
        "category": "restaurant"
    }
    
    should, reason = outreach.should_contact(test_business)
    print(f"Should contact: {should} ({reason})")
    
    if should:
        outreach.contact(test_business)
        outreach.learn_result(test_business["email"], "no_response")
    
    print(f"Best category: {outreach.get_best_category()}")
