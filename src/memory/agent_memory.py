"""
SuperMemory Layer for MoneyPrinterV2
让系统记住之前的行为，持续优化
"""
import json
import os
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path("~/.money-printer-memory").expanduser()
MEMORY_DIR.mkdir(exist_ok=True)

class AgentMemory:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.memory_file = MEMORY_DIR / f"{agent_name}.json"
        self.memory = self._load()
    
    def _load(self):
        if self.memory_file.exists():
            with open(self.memory_file) as f:
                return json.load(f)
        return {
            "agent": self.agent_name,
            "created": datetime.now().isoformat(),
            "history": [],
            "preferences": {},
            "performance": {},
            "learnings": []
        }
    
    def save(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def remember(self, key, value):
        """记忆存储"""
        self.memory["history"].append({
            "timestamp": datetime.now().isoformat(),
            "key": key,
            "value": value
        })
        self.save()
    
    def recall(self, key, limit=10):
        """回忆检索"""
        results = [h for h in self.memory["history"] if h["key"] == key]
        return results[-limit:]
    
    def learn(self, event, result):
        """从结果中学习"""
        self.memory["learnings"].append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "result": result
        })
        self.save()
    
    def get_preference(self, key, default=None):
        return self.memory["preferences"].get(key, default)
    
    def set_preference(self, key, value):
        self.memory["preferences"][key] = value
        self.save()
    
    def get_stats(self):
        return {
            "total_memories": len(self.memory["history"]),
            "total_learnings": len(self.memory["learnings"]),
            "preferences": self.memory["preferences"]
        }

# 全局实例
twitter_memory = AgentMemory("twitter")
content_memory = AgentMemory("content")
outreach_memory = AgentMemory("outreach")

if __name__ == "__main__":
    # 测试
    twitter_memory.remember("last_tweet", "Hello world")
    twitter_memory.remember("engagement", {"likes": 10, "replies": 2})
    twitter_memory.learn("morning_tweet", "high_engagement")
    print(twitter_memory.get_stats())
