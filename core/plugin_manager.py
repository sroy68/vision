import os, json, subprocess, requests
from core.tools import run_tool, rollback
from core.auto_feature import propose

PLUGIN_DIR = "plugins"
PLUGIN_LOG = "plugins_log.json"

class PluginManager:
    def __init__(self):
        if not os.path.exists(PLUGIN_DIR):
            os.makedirs(PLUGIN_DIR)
        self.load_log()

    def load_log(self):
        if os.path.exists(PLUGIN_LOG):
            with open(PLUGIN_LOG) as f:
                self.log = json.load(f)
        else:
            self.log = []

    def save_log(self):
        with open(PLUGIN_LOG, "w") as f:
            json.dump(self.log, f, indent=2)

    def install_plugin(self, url, owner=False):
        """
        Downloads and installs a plugin from URL (GitHub/raw)
        Owner approval required
        """
        if not owner:
            return "❌ Owner approval required"

        name = url.split("/")[-1].replace(".py","")
        target = os.path.join(PLUGIN_DIR, name+".py")

        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            code = r.text

            # Owner approval for first-time install
            if propose(f"Install plugin {name}", f"Install plugin from {url}"):
                with open(target, "w") as f:
                    f.write(code)
                self.log.append({"plugin": name, "action": "installed"})
                self.save_log()
                return f"✅ Plugin {name} installed"
            else:
                return f"❌ Installation rejected by owner"
        except Exception as e:
            rollback(f"plugin {name}")
            return f"❌ Installation failed: {e}"

    def remove_plugin(self, name, owner=False):
        if not owner:
            return "❌ Owner approval required"
        path = os.path.join(PLUGIN_DIR, name+".py")
        if os.path.exists(path):
            os.remove(path)
            self.log.append({"plugin": name, "action": "removed"})
            self.save_log()
            return f"✅ Plugin {name} removed"
        return "❌ Plugin not found"

    def list_plugins(self):
        return [f.replace(".py","") for f in os.listdir(PLUGIN_DIR) if f.endswith(".py")]

    def run_plugin(self, name, args=None, owner=False):
        if not owner:
            return "❌ Owner approval required"
        path = os.path.join(PLUGIN_DIR, name+".py")
        if not os.path.exists(path):
            return "❌ Plugin not found"
        try:
            result = subprocess.check_output(
                f"python {path} {args or ''}",
                shell=True,
                stderr=subprocess.STDOUT,
                timeout=10
            ).decode()
            self.log.append({"plugin": name, "action": "executed"})
            self.save_log()
            return result
        except Exception as e:
            rollback(f"plugin {name}")
            return f"❌ Execution failed: {e}"
