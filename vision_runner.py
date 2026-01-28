#!/usr/bin/env python3
from core.memory import Memory
from core.voice import speak, listen
from core.brain import VisionBrain
from core.plugin_manager_full import FullPluginManager, AutoFeatureManager

mem = Memory("CHANGE_ME")
brain = VisionBrain(owner_password="CHANGE_ME", memory=mem)
pm = FullPluginManager()
afm = AutoFeatureManager(owner=True)

print("VISION World No.1 AI ACTIVE (Type 'exit' to quit)")
while True:
    query = listen()
    if query.lower() in ["exit","quit"]:
        mem.save()
        break
    resp = brain.reply(query)
    print("VISION:", resp)
    speak(resp)
    mem.log_interaction(query, resp)
    pm.auto_install_trending(owner=True)
    afm.activate_all(owner=True)
