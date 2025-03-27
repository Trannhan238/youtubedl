class Translations:
    def __init__(self):
        self.languages = {
            "en": {
                "title": "Professional YouTube Downloader",
                "url_label": "YouTube URL:",
                # ... các translation khác ...
            },
            "vi": {
                "title": "Trình tải video YouTube",
                "url_label": "Đường dẫn YouTube:",
                # ... các translation khác ...
            }
        }
        self.current_lang = "vi"
        
    def set_language(self, lang_code: str):
        if lang_code in self.languages:
            self.current_lang = lang_code
            
    def get(self, key: str) -> str:
        return self.languages[self.current_lang].get(key, key)