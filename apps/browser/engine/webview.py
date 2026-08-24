# Deprecated - use chromium_engine.py instead
class BrowserWebView:
    def __init__(self, parent):
        self.frame = None
        print("[Browser] Use chromium_engine.py instead")
    
    def pack(self, **kwargs):
        pass
    
    def pack_forget(self):
        pass
    
    def load(self, url):
        print(f"[Browser] Use chromium_engine.py instead")
    
    def back(self):
        pass
    
    def forward(self):
        pass
    
    def reload(self):
        pass