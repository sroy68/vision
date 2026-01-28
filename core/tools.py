import subprocess

OWNER_ONLY = True

def run_tool(command, owner=False):
    if OWNER_ONLY and not owner:
        return "❌ Permission denied (Owner only)"

    try:
        out = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, timeout=5
        )
        return out.decode()
    except subprocess.TimeoutExpired:
        return "⚠️ Command timeout"
    except Exception as e:
        return f"❌ Error: {e}"
