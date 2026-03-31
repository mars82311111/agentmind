"""
Content Generator with SuperMemory
基于记忆生成内容策略
"""
import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.agent_memory import content_memory
from datetime import datetime

class ContentGenerator:
    def __init__(self):
        self.themes = {
            "ai_agent": [
                "AI Agent正在改变做生意的方式",
                "24/7无人值守的AI团队",
                "一个人如何用AI运营跨国公司",
                "SuperMemory让AI记住一切",
                "AI Agent团队协作实战"
            ],
            "productivity": [
                "自动化提升效率的10个方法",
                "AI时代的生产力工具",
                "让AI为你工作的艺术",
                "从忙碌到高效的转变"
            ],
            "创业": [
                "一个人创业的真实故事",
                "AI时代的创业机会",
                "低成本创业的可行性",
                "用AI实现财务自由"
            ]
        }
    
    def get_preferred_theme(self):
        """从记忆中找出表现最好的主题"""
        learnings = content_memory.memory.get("learnings", [])
        good_results = [l for l in learnings if "good" in str(l["result"]).lower()]
        
        if good_results:
            last_theme = good_results[-1].get("event", "")
            for theme, topics in self.themes.items():
                for topic in topics:
                    if last_theme.lower() in topic.lower():
                        return theme
        return random.choice(list(self.themes.keys()))
    
    def generate_content_idea(self):
        """生成内容创意"""
        theme = self.get_preferred_theme()
        topics = self.themes.get(theme, self.themes["ai_agent"])
        
        idea = random.choice(topics)
        
        # 记忆这个创意
        content_memory.remember("content_idea", {
            "theme": theme,
            "topic": idea,
            "timestamp": datetime.now().isoformat()
        })
        
        return idea, theme
    
    def generate_tweet(self):
        """生成推文"""
        idea, theme = self.generate_content_idea()
        
        templates = [
            f"🚀 {idea}",
            f"💡 {idea}...",
            f"你以为{idea}很难？",
            f"关于{idea}的几个真相",
        ]
        
        tweet = random.choice(templates)
        tweet += f"\n\n#AI #{theme} #创业"
        
        # 记忆
        content_memory.remember("tweet_generated", {
            "content": tweet,
            "theme": theme,
            "timestamp": datetime.now().isoformat()
        })
        
        return tweet
    
    def mark_as_good(self, content):
        """标记为成功内容"""
        content_memory.learn(f"content_{content[:30]}", "good")
    
    def mark_as_bad(self, content):
        """标记为失败内容"""
        content_memory.learn(f"content_{content[:30]}", "bad")

if __name__ == "__main__":
    gen = ContentGenerator()
    tweet = gen.generate_tweet()
    print(f"Generated tweet:\n{tweet}")
