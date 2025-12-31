import json
import os

class Config:
    def __init__(self):
        self.config_file = "crosshair_config.json"
        self.default_config = {
            "dot_size": 4,
            "line_color": "#90EE90"
        }
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.default_config.update(json.load(f))
            except Exception as e:
                print(f"加载失败: {e}")
        
        for key, value in self.default_config.items():
            setattr(self, key, value)
    
    def save_config(self):
        config_dict = {key: getattr(self, key) for key in self.default_config.keys()}
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=4)
        except Exception as e:
            print(f"保存失败: {e}")

    def update_config(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save_config()