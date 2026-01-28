import os, json, subprocess, requests, time
from core.tools import run_tool, rollback
from core.auto_feature import propose

PLUGIN_DIR = "plugins"
PLUGIN_LOG = "plugins_log.json"
TRUSTED_REPO = "https://raw.githubusercontent.com/yourusername/vision-plugins/main/"

class AdvancedPluginManager:
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

    # --------------------------
    # Install or Update plugin
    # --------------------------
    def install_plugin(self, name, owner=False, auto_update=True):
        url = f"{TRUSTED_REPO}{name}.py"
        target = os.path.join(PLUGIN_DIR, f"{name}.py")

        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            code = r.text

            # Owner approval for first time or major update
            if not os.path.exists(target) or (auto_update and propose(f"Update plugin {name}", f"From {url}")):
                with open(target, "w") as f:
                    f.write(code)
                self.log.append({"plugin": name, "action": "installed/updated", "time": time.time()})
                self.save_log()
                self.resolve_dependencies(target)
                return f"✅ Plugin {name} installed/updated"
            return f"❌ Installation/update rejected by owner"
        except Exception as e:
            rollback(f"plugin {name}")
            return f"❌ Installation/update failed: {e}"

    # --------------------------
    # Remove plugin
    # --------------------------
    def remove_plugin(self, name, owner=False):
        path = os.path.join(PLUGIN_DIR, f"{name}.py")
        if os.path.exists(path):
            os.remove(path)
            self.log.append({"plugin": name, "action": "removed", "time": time.time()})
            self.save_log()
            return f"✅ Plugin {name} removed"
        return "❌ Plugin not found"

    # --------------------------
    # Run plugin
    # --------------------------
    def run_plugin(self, name, args=None, owner=False):
        path = os.path.join(PLUGIN_DIR, f"{name}.py")
        if not os.path.exists(path):
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

    # --------------------------
    # Resolve Python dependencies inside plugin
    # --------------------------
    def resolve_dependencies(self, path):
        with open(path) as f:
            code = f.read()
        lines = [l for l in code.splitlines() if l.startswith("## REQUIRE:")]
        for dep_line in lines:
            pkg = dep_line.replace("## REQUIRE:","").strip()
            subprocess.run(f"pip install {pkg}", shell=True)

    def list_plugins(self):
        return [f.replace(".py","") for f in os.listdir(PLUGIN_DIR) if f.endswith(".py")]
