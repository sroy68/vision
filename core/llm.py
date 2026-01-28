import openai, time
from config_private import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# 🔹 Usage tracking (prevents abuse)
_usage_counter = 0
_USAGE_LIMIT = 50       # max 50 calls per session
_USAGE_RESET = 3600     # reset every 1 hour
_last_reset = time.time()

def think(prompt, online=True):
    global _usage_counter, _last_reset

    # reset counter hourly
    if time.time() - _last_reset > _USAGE_RESET:
        _usage_counter = 0
        _last_reset = time.time()

    if _usage_counter >= _USAGE_LIMIT:
        return "⚠️ OpenAI usage limit reached. Try later."

    if online and OPENAI_API_KEY:
        try:
            _usage_counter += 1
            res = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                timeout=10
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"❌ OpenAI error: {e}"

    # fallback offline
    return "আমি offline আছি। পরিষ্কার করে বলো।"
