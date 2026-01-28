import socket
import os
import openai
from core.audit_log import log
from core.memory_manager import MemoryManager

class VisionBrain:
    def __init__(self, feature_manager):
        self.fm = feature_manager
        self.memory = MemoryManager()
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise Exception("OpenAI API key not found in environment variables!")
        openai.api_key = self.api_key

    def internet_available(self, host="8.8.8.8", port=53, timeout=2):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket().connect((host, port))
            return True
        except:
            return False

    def offline_reasoning(self, text):
        text_lower = text.lower()
        feature_keywords = ["analyze", "monitor", "track", "detect", "usage", "battery", "notes"]
        reply = "আমি আপনার কমান্ড বুঝতে পারলাম কিন্তু এখন আমি offline।"
        if any(k in text_lower for k in feature_keywords):
            feature_name = "Auto Generated Feature"
            summary = f"Required to perform: {text}"
            self.fm.propose(feature_name, summary)
            self.memory.add_feature(feature_name, summary)
            reply += f" Feature '{feature_name}' propose করা হলো।"
        return reply

    def online_reasoning(self, text):
        messages = [{"role": "system", "content": "You are VISION, an AI assistant. Respond in Bengali+English. Only propose features if command requires analysis, tracking, or monitoring, owner approval required."}]
        for m in self.memory.memory["chat"]:
            messages.append({"role": "user", "content": m["user"]})
            messages.append({"role": "assistant", "content": m["vision"]})
        messages.append({"role": "user", "content": text})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()

        # Auto feature proposal
        feature_keywords = ["analyze", "monitor", "track", "detect", "usage", "battery", "notes"]
        if any(k in text.lower() for k in feature_keywords):
            feature_name = "Auto Generated Feature"
            summary = f"Required to perform: {text}"
            self.fm.propose(feature_name, summary)
            self.memory.add_feature(feature_name, summary)
            reply += f"\n[Auto Feature Proposed: {feature_name}]"

        return reply

    def think(self, text):
        if self.internet_available():
            try:
                reply = self.online_reasoning(text)
            except:
                reply = self.offline_reasoning(text)
        else:
            reply = self.offline_reasoning(text)

        self.memory.add_chat(text, reply)
        log(f"[CHAT] User: {text}")
        log(f"[CHAT] Vision: {reply}")
        return reply

    def start(self):
        print("\nVISION SECURE PRODUCTION READY TO CHAT (type 'exit')")
        while True:
            cmd = input("VISION > ").strip()
            if cmd.lower() == "exit":
                print("VISION shutting down chat.")
                break
            response = self.think(cmd)
            print("VISION:", response)
