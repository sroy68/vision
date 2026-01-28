import os, json, subprocess, requests, time
from core.tools import run_tool, rollback
from core.auto_feature import propose

PLUGIN_DIR = "plugins"
PLUGIN_LOG = "plugins_log.json"
TRUSTED_REPO = "https://raw.githubusercontent.com/yourusername/vision-plugins/main/"

class SelfPluginManager:
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

    # ------------------------
    # Install plugin (auto + owner approval)
    # ------------------------
    def install_plugin(self, name, owner=False):
        url = f"{TRUSTED_REPO}{name}.py"
        target = os.path.join(PLUGIN_DIR, f"{name}.py")
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            code = r.text

            # Auto-propose only if new
            if not os.path.exists(target) or propose(f"Install plugin {name}", f"From {url}"):
                with open(target, "w") as f:
                    f.write(code)
                self.log.append({"plugin": name, "action": "installed", "time": time.time()})
                self.save_log()
                return f"✅ Plugin {name} installed"
            return f"❌ Installation rejected by owner"
        except Exception as e:
            rollback(f"plugin {name}")
            return f"❌ Installation failed: {e}"

    # ------------------------
    # Remove plugin
    # ------------------------
    def remove_plugin(self, name, owner=False):
        path = os.path.join(PLUGIN_DIR, f"{name}.py")
        if os.path.exists(path):
            os.remove(path)
            self.log.append({"plugin": name, "action": "removed", "time": time.time()})
            self.save_log()
            return f"✅ Plugin {name} removed"
        return "❌ Plugin not found"

    # ------------------------
    # Run plugin
    # ------------------------
    def run_plugin(self, name, args=None, owner=False):
        path = os.path.join(PLUGIN_DIR, f"{name}.py")
        if not os.path.exists(path):
            # Auto-install if trusted
            return self.install_plugin(name, owner=True)
        try:
            result = subprocess.check_output(
                f"python {path} {args or ''}", shell=True, stderr=subprocess.STDOUT, timeout=15
            ).decode()
            self.log.append({"plugin": name, "action": "executed", "time": time.time()})
            self.save_log()
            return result
        except Exception as e:
            rollback(f"plugin {name}")
            return f"❌ Execution failed: {e}"

    def list_plugins(self):
        return [f.replace(".py","") for f in os.listdir(PLUGIN_DIR) if f.endswith(".py")]
