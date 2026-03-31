"""
MoneyPrinterV2 + SuperMemory
24/7 自动赚钱系统
"""
import time
import random
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from twitter.twitter_bot import TwitterBot
from outreach.outreach import OutreachSystem
from memory.agent_memory import content_memory

class MoneyPrinterV2:
    def __init__(self):
        self.twitter = TwitterBot()
        self.outreach = OutreachSystem()
        self.running = True
        self.iteration = 0
        
    def log(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    
    def generate_content_with_memory(self):
        """基于记忆生成内容"""
        # 检查之前什么内容表现好
        learnings = content_memory.memory.get("learnings", [])
        good_content = [l for l in learnings if "good" in l["result"].lower()]
        
        topics = [
            "AI自动化正在改变做生意的方式",
            "24/7无人值守的AI团队",
            "一个人如何用AI运营跨国公司",
            "SuperMemory让AI记住一切",
            "AI Agent团队协作实战"
        ]
        
        # 如果有好的历史主题，继续用
        if good_content:
            last_good = good_content[-1]["event"]
            return f"深入聊：{last_good}"
        
        return random.choice(topics)
    
    def run_twitter_task(self):
        """执行Twitter任务"""
        if self.twitter.should_post():
            topic = self.generate_content_with_memory()
            tweet = f"🚀 {topic}\n\n#AI #自动化 #创业"
            self.twitter.post(tweet)
            content_memory.learn("twitter_post", "posted")
            self.log("Twitter task completed")
            return True
        else:
            self.log("Twitter: waiting (recently posted)")
            return False
    
    def run_outreach_task(self):
        """执行外联任务"""
        # 模拟商家数据库（实际会从网上抓取）
        potential_businesses = [
            {"email": "info@restaurant1.com", "name": "Restaurant A", "category": "restaurant"},
            {"email": "owner@cafe1.com", "name": "Cafe B", "category": "cafe"},
            {"email": "contact@shop1.com", "name": "Shop C", "category": "retail"},
        ]
        
        for biz in potential_businesses:
            should, reason = self.outreach.should_contact(biz)
            if should:
                self.outreach.contact(biz)
                # 模拟结果
                result = random.choice(["no_response", "no_response", "replied", "success"])
                self.outreach.learn_result(biz["email"], result)
                self.log(f"Outreach: {biz['name']} → {result}")
                return True
        
        self.log("Outreach: no targets available")
        return False
    
    def run_content_task(self):
        """生成内容灵感"""
        topic = self.generate_content_with_memory()
        content_memory.remember("content_idea", {
            "topic": topic,
            "timestamp": datetime.now().isoformat()
        })
        self.log(f"Content idea: {topic}")
        return True
    
    def run_cycle(self):
        """执行一个完整周期"""
        self.iteration += 1
        self.log(f"=== Cycle {self.iteration} ===")
        
        # Twitter发推
        self.run_twitter_task()
        time.sleep(random.randint(5, 15))
        
        # 外联
        if random.random() < 0.3:  # 30%概率执行外联
            self.run_outreach_task()
        
        time.sleep(random.randint(5, 15))
        
        # 内容策略
        self.run_content_task()
        
        self.log(f"Cycle {self.iteration} completed")
    
    def start(self):
        """启动24/7循环"""
        self.log("=" * 50)
        self.log("MoneyPrinterV2 + SuperMemory STARTED")
        self.log("=" * 50)
        
        while self.running:
            try:
                self.run_cycle()
                
                # 随机等待 30秒-2分钟
                wait = random.randint(30, 120)
                self.log(f"Sleeping {wait}s...")
                time.sleep(wait)
                
            except KeyboardInterrupt:
                self.log("Stopping...")
                self.running = False
            except Exception as e:
                self.log(f"Error: {e}")
                time.sleep(30)

if __name__ == "__main__":
    printer = MoneyPrinterV2()
    printer.start()
