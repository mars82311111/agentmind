"""
Twitter Bot with SuperMemory
发推时记住历史表现，持续优化
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.agent_memory import twitter_memory
from datetime import datetime

class TwitterBot:
    def __init__(self):
        self.username = "mars_ai_agent"
        self.last_tweet_time = None
        
    def should_post(self):
        """检查是否应该发推（避免过度 posting）"""
        history = twitter_memory.recall("last_tweet", limit=20)
        if len(history) < 5:
            return True
        # 检查最近1小时是否发过
        recent = [h for h in history[-5:] 
                  if datetime.now().isoformat() < h["timestamp"]]
        return len(recent) < 3
    
    def post(self, content):
        """发推并记忆"""
        # 调用opencli发推
        os.system(f'opencli twitter post "{content}" 2>/dev/null')
        
        twitter_memory.remember("last_tweet", {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "char_count": len(content)
        })
        
        print(f"✓ Posted: {content[:50]}...")
        return True
    
    def analyze_engagement(self):
        """分析历史推文表现"""
        history = twitter_memory.recall("engagement", limit=50)
        if not history:
            return {"avg_likes": 0, "avg_replies": 0}
        
        total_likes = sum(h["value"].get("likes", 0) for h in history)
        total_replies = sum(h["value"].get("replies", 0) for h in history)
        
        return {
            "avg_likes": total_likes / len(history),
            "avg_replies": total_replies / len(history),
            "total_analyzed": len(history)
        }
    
    def generate_content_idea(self):
        """基于记忆生成内容策略"""
        stats = self.analyze_engagement()
        learnings = twitter_memory.memory.get("learnings", [])
        
        # 找出表现好的类型
        good_topics = [l for l in learnings if "high" in str(l["result"]).lower()]
        
        if good_topics:
            topic = good_topics[-1]["event"]
            return f"继续聊 {topic}，因为之前表现好"
        
        return "测试新内容方向"

if __name__ == "__main__":
    bot = TwitterBot()
    if bot.should_post():
        idea = bot.generate_content_idea()
        bot.post(f"AI Agent 正在学习如何赚钱。{idea}")
