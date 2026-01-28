import requests

def online_query(text):
    q = text.lower()

    # Weather (free)
    if "weather" in q:
        city = text.split()[-1]
        try:
            r = requests.get(
                f"https://wttr.in/{city}?format=3",
                timeout=10
            )
            return r.text
        except:
            return "Weather service unavailable"

    # Cricket / Live score (browser-based hint)
    if "cricket" in q or "score" in q:
        return (
            "Live cricket score দেখতে:\n"
            "👉 https://www.espncricinfo.com/\n"
            "👉 https://www.cricbuzz.com/"
        )

    # General search
    try:
        r = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": text, "format": "json"},
            timeout=10
        )
        data = r.json()
        return data.get("AbstractText") or "Clear answer পাইনি।"
    except Exception as e:
        return f"Online error: {e}"
