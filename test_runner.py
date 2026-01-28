#!/usr/bin/env python3
from core.brain import VisionBrain
from core.memory import Memory
from core.voice import listen, speak
from core.plugin_manager_full import FullPluginManager
from core.auto_feature import AutoFeatureManager
from core.global_tools import GlobalExecutor
from config_private import VISION_PASSWORD, OPENAI_API_KEY

# Initialize memory & brain
mem = Memory(VISION_PASSWORD)
brain = VisionBrain(owner_password=VISION_PASSWORD, memory=mem, api_key=OPENAI_API_KEY)
pm = FullPluginManager()
afm = AutoFeatureManager(owner=True)
ge = GlobalExecutor(owner=True)

# Minimal test queries
test_queries = [
    "Hello",
    "Cricket score",
    "Install plugin x",
    "Activate feature y"
]

for q in test_queries:
    print("TEST QUERY:", q)
    resp = brain.reply(q)
    print("RESPONSE:", resp)
    mem.log_interaction(q, resp)
    pm.auto_install_trending(owner=True)
    afm.check_proposals(owner=True)
    ge.execute_if_approved(q)

print("✅ Minimal test finished")
