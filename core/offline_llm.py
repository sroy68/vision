def offline_think(text):
    text = text.lower()
    if "google" in text:
        return "Google একটি search engine, তথ্য খোঁজার জন্য ব্যবহার হয়।"
    if "facebook" in text:
        return "Facebook social networking, মানুষ connect থাকে।"
    return "আমি ভাবছি। আরেকটু পরিষ্কার করে বলো।"
