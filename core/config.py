import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    """Runtime configuration for NovaOS, sourced from the environment."""

    # ==========================================
    # AI Provider Configuration
    # ==========================================
    provider: str
    gemini_api_key: str
    gemini_model: str
    ollama_host: str
    ollama_model: str
    
    # ==========================================
    # External API Keys
    # ==========================================
    openweather_api_key: str
    
    # ==========================================
    # System Configuration
    # ==========================================
    debug_mode: bool = False
    log_level: str = "INFO"
    
    # ==========================================
    # AI Configuration
    # ==========================================
    ai_max_context_turns: int = 20
    ai_response_timeout: int = 30
    ai_temperature: float = 0.7
    
    # ==========================================
    # Voice Configuration
    # ==========================================
    voice_enabled: bool = True
    voice_rate: int = 150
    voice_volume: float = 0.9
    
    # ==========================================
    # UI Configuration
    # ==========================================
    theme: str = "dark"
    glassmorphism_enabled: bool = True
    animations_enabled: bool = True

    @classmethod
    def load(cls):
        return cls(
            # AI Provider Configuration
            provider=os.getenv("NOVA_PROVIDER", "gemini"),
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            gemini_model=os.getenv("NOVA_GEMINI_MODEL", "gemini-3.6-flash"),
            ollama_host=os.getenv("NOVA_OLLAMA_HOST", "http://localhost:11434"),
            ollama_model=os.getenv("NOVA_OLLAMA_MODEL", "llama3.1"),
            
            # External API Keys
            openweather_api_key=os.getenv("OPENWEATHER_API_KEY", ""),
            
            # System Configuration
            debug_mode=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            
            # AI Configuration
            ai_max_context_turns=int(os.getenv("AI_MAX_CONTEXT_TURNS", "20")),
            ai_response_timeout=int(os.getenv("AI_RESPONSE_TIMEOUT", "30")),
            ai_temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
            
            # Voice Configuration
            voice_enabled=os.getenv("VOICE_ENABLED", "true").lower() == "true",
            voice_rate=int(os.getenv("VOICE_RATE", "150")),
            voice_volume=float(os.getenv("VOICE_VOLUME", "0.9")),
            
            # UI Configuration
            theme=os.getenv("THEME", "dark"),
            glassmorphism_enabled=os.getenv("GLASSMORPHISM_ENABLED", "true").lower() == "true",
            animations_enabled=os.getenv("ANIMATIONS_ENABLED", "true").lower() == "true",
        )
    
    def is_weather_available(self) -> bool:
        """Check if weather API is properly configured."""
        return bool(self.openweather_api_key)
    
    def is_ai_available(self) -> bool:
        """Check if AI provider is properly configured."""
        return bool(self.gemini_api_key) or self.provider == "ollama"


CONFIG = Config.load()