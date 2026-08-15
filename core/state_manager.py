import json
import os
from typing import Dict, Any


class StateManager:
    """Application state persistence manager."""
    
    def __init__(self, state_file="data/state.json"):
        self.state_file = state_file
        self.state = {}
        self._ensure_data_dir()
        self._load_state()
        
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        
    def _load_state(self):
        """Load state from file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    self.state = json.load(f)
            except Exception as e:
                print(f"[StateManager] Error loading state: {e}")
                self.state = {}
        else:
            self.state = {}
            
    def _save_state(self):
        """Save state to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"[StateManager] Error saving state: {e}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get state value."""
        return self.state.get(key, default)
        
    def set(self, key: str, value: Any):
        """Set state value."""
        self.state[key] = value
        self._save_state()
        
    def delete(self, key: str):
        """Delete state value."""
        if key in self.state:
            del self.state[key]
            self._save_state()