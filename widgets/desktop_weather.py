"""Weather widget for the NovaOS desktop — auto-detects location via IP."""

import customtkinter as ctk
import requests
from core.config import CONFIG


class DesktopWeather(ctk.CTkFrame):
    """Compact weather widget floating on the desktop."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#0D1117",
            corner_radius=16,
            border_width=1,
            border_color="#1A2332",
            **kwargs
        )
        self.configure(width=220, height=140)
        self.pack_propagate(False)

        # Icon + temp row
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=15, pady=(12, 0))

        self.icon_label = ctk.CTkLabel(
            top, text="🌤", font=("Segoe UI Emoji", 32),
            text_color="#FFFFFF"
        )
        self.icon_label.pack(side="left")

        self.temp_label = ctk.CTkLabel(
            top, text="--°",
            font=("Segoe UI", 28, "bold"),
            text_color="#00E5FF"
        )
        self.temp_label.pack(side="left", padx=(8, 0))

        # City
        self.city_label = ctk.CTkLabel(
            self, text="Detecting...",
            font=("Segoe UI", 11),
            text_color="#888888"
        )
        self.city_label.pack(anchor="w", padx=15, pady=(2, 0))

        # Description
        self.desc_label = ctk.CTkLabel(
            self, text="",
            font=("Segoe UI", 10),
            text_color="#666666"
        )
        self.desc_label.pack(anchor="w", padx=15)

        # Details row
        details = ctk.CTkFrame(self, fg_color="transparent")
        details.pack(fill="x", padx=15, pady=(4, 0))

        self.humidity_label = ctk.CTkLabel(
            details, text="💧 --",
            font=("Segoe UI", 10), text_color="#555555"
        )
        self.humidity_label.pack(side="left")

        self.wind_label = ctk.CTkLabel(
            details, text="💨 --",
            font=("Segoe UI", 10), text_color="#555555"
        )
        self.wind_label.pack(side="left", padx=(12, 0))

        self._detected_city = None
        self._fetch_weather()

    def _detect_city(self):
        """Detect city from IP geolocation."""
        try:
            resp = requests.get("https://ipapi.co/json/", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                city = data.get("city")
                if city:
                    self._detected_city = city
                    return city
        except Exception:
            pass
        # Fallback: try another service
        try:
            resp = requests.get("http://ip-api.com/json/", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                city = data.get("city")
                if city:
                    self._detected_city = city
                    return city
        except Exception:
            pass
        return None

    def _fetch_weather(self):
        """Fetch weather data for detected city."""
        if not CONFIG.is_weather_available():
            self.temp_label.configure(text="--°")
            self.city_label.configure(text="No API key")
            self.desc_label.configure(text="Set OPENWEATHER_API_KEY in .env")
            self.after(60000, self._fetch_weather)
            return

        # Detect city if not yet detected
        if not self._detected_city:
            city = self._detect_city()
            if not city:
                self.city_label.configure(text="Location unavailable")
                self.desc_label.configure(text="Check internet connection")
                self.after(120000, self._fetch_weather)
                return
        else:
            city = self._detected_city

        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={CONFIG.openweather_api_key}&units=metric"
            )
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                self._display(data)
            else:
                self._show_error()
        except Exception:
            self._show_error()

        # Refresh every 10 minutes
        self.after(600000, self._fetch_weather)

    def _display(self, data):
        """Display weather data."""
        city = data.get("name", "")
        country = data.get("sys", {}).get("country", "")
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        desc_lower = desc.lower()
        if "cloud" in desc_lower:
            icon = "☁️"
        elif "rain" in desc_lower:
            icon = "🌧️"
        elif "snow" in desc_lower:
            icon = "❄️"
        elif "clear" in desc_lower:
            icon = "☀️"
        elif "thunder" in desc_lower:
            icon = "⛈️"
        elif "mist" in desc_lower or "fog" in desc_lower:
            icon = "🌫️"
        else:
            icon = "🌡️"

        self.icon_label.configure(text=icon)
        self.temp_label.configure(text=f"{temp:.0f}°C")
        self.city_label.configure(text=f"{city}, {country}")
        self.desc_label.configure(text=desc)
        self.humidity_label.configure(text=f"💧 {humidity}%")
        self.wind_label.configure(text=f"💨 {wind}m/s")

    def _show_error(self):
        self.temp_label.configure(text="--°")
        self.city_label.configure(text="Weather unavailable")
        self.desc_label.configure(text="Check internet / API key")
