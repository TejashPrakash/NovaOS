"""Weather Dashboard for NovaOS with animated weather display."""

import requests
import math
from datetime import datetime, timedelta

import customtkinter as ctk
from sdk.app import NovaApp
from core.config import CONFIG
from core.theme import ThemeManager


WEATHER_ICONS = {
    "clear": "☀️",
    "sunny": "☀️",
    "clouds": "☁️",
    "cloudy": "☁️",
    "partly cloudy": "⛅",
    "rain": "🌧️",
    "light rain": "🌦️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "fog": "🌫️",
    "haze": "🌫️",
    "wind": "💨",
    "default": "🌡️",
}


def _get_icon(description: str) -> str:
    desc = description.lower()
    for key, icon in WEATHER_ICONS.items():
        if key in desc:
            return icon
    return WEATHER_ICONS["default"]


class WeatherApp(NovaApp):
    """NovaOS Weather Dashboard with live weather data."""

    APP_NAME = "Weather"
    APP_ICON = "🌤"
    DEFAULT_WIDTH = 700
    DEFAULT_HEIGHT = 550

    def __init__(self, window):
        super().__init__(window)
        self.theme = ThemeManager()
        self.current_weather = None

    def build(self):
        # Search bar
        search_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(15, 10))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search city...",
            height=40,
            fg_color="#161B22",
            text_color="#FFFFFF",
            corner_radius=20,
            border_width=1,
            border_color="#00E5FF",
            font=("Segoe UI", 14)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.search_entry.bind("<Return>", lambda e: self._fetch_weather())

        self.search_btn = ctk.CTkButton(
            search_frame, text="🔍 Search", width=100, height=40,
            fg_color="#00E5FF", text_color="black",
            hover_color="#00C8E8", corner_radius=20,
            font=("Segoe UI", 13, "bold"),
            command=self._fetch_weather
        )
        self.search_btn.pack(side="right")

        # Main weather display
        self.weather_frame = ctk.CTkFrame(
            self.content, fg_color="#0D1117", corner_radius=16
        )
        self.weather_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self._build_placeholder()

    def _build_placeholder(self):
        """Show placeholder before weather is loaded."""
        for w in self.weather_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.weather_frame,
            text="🌤",
            font=("Segoe UI Emoji", 64)
        ).pack(pady=(60, 10))

        ctk.CTkLabel(
            self.weather_frame,
            text="Search for a city to see the weather",
            font=("Segoe UI", 16),
            text_color="#666666"
        ).pack()

        if not CONFIG.is_weather_available():
            ctk.CTkLabel(
                self.weather_frame,
                text="⚠ Set OPENWEATHER_API_KEY in .env for live data",
                font=("Segoe UI", 12),
                text_color="#FFC107"
            ).pack(pady=(10, 0))

    def _fetch_weather(self):
        city = self.search_entry.get().strip()
        if not city:
            return

        if not CONFIG.is_weather_available():
            self._show_demo_weather(city)
            return

        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f?q={city}&appid={CONFIG.openweather_api_key}&units=metric"
            )
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self._display_weather(data)
            else:
                self._show_error(f"City not found: {city}")
        except Exception as e:
            self._show_error(f"Could not fetch weather: {e}")

    def _display_weather(self, data):
        """Display live weather data from API."""
        for w in self.weather_frame.winfo_children():
            w.destroy()

        city = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        description = data["weather"][0]["description"].title()
        icon = _get_icon(description)
        pressure = data["main"].get("pressure", 0)
        visibility = data.get("visibility", 0) / 1000

        # City header
        header = ctk.CTkFrame(self.weather_frame, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(20, 0))

        ctk.CTkLabel(
            header, text=f"{icon}",
            font=("Segoe UI Emoji", 42)
        ).pack(side="left")

        city_frame = ctk.CTkFrame(header, fg_color="transparent")
        city_frame.pack(side="left", padx=10)

        ctk.CTkLabel(
            city_frame, text=f"{city}, {country}",
            font=("Segoe UI", 22, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w")

        ctk.CTkLabel(
            city_frame, text=f"{description}  •  {datetime.now().strftime('%I:%M %p')}",
            font=("Segoe UI", 12),
            text_color="#888888"
        ).pack(anchor="w")

        # Temperature
        temp_frame = ctk.CTkFrame(self.weather_frame, fg_color="transparent")
        temp_frame.pack(fill="x", padx=25, pady=(15, 0))

        ctk.CTkLabel(
            temp_frame, text=f"{temp:.0f}°C",
            font=("Segoe UI", 56, "bold"),
            text_color="#00E5FF"
        ).pack(side="left")

        detail_frame = ctk.CTkFrame(temp_frame, fg_color="transparent")
        detail_frame.pack(side="left", padx=20)

        ctk.CTkLabel(
            detail_frame, text=f"Feels like {feels_like:.0f}°C",
            font=("Segoe UI", 14),
            text_color="#BBBBBB"
        ).pack(anchor="w")

        ctk.CTkLabel(
            detail_frame, text=f"H: {data['main']['temp_max']:.0f}°  L: {data['main']['temp_min']:.0f}°",
            font=("Segoe UI", 13),
            text_color="#888888"
        ).pack(anchor="w")

        # Details cards
        cards_frame = ctk.CTkFrame(self.weather_frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=25, pady=(20, 0))

        details = [
            ("💧 Humidity", f"{humidity}%", "#00B8D4"),
            ("💨 Wind", f"{wind} m/s", "#7B61FF"),
            ("🌡 Pressure", f"{pressure} hPa", "#FF00E5"),
            ("👁 Visibility", f"{visibility:.1f} km", "#00E676"),
        ]

        for label_text, value, color in details:
            card = ctk.CTkFrame(
                cards_frame, fg_color="#161B22",
                corner_radius=12, height=80
            )
            card.pack(side="left", fill="x", expand=True, padx=4)
            card.pack_propagate(False)

            ctk.CTkLabel(
                card, text=label_text,
                font=("Segoe UI", 11),
                text_color="#888888"
            ).pack(pady=(12, 2))

            ctk.CTkLabel(
                card, text=value,
                font=("Segoe UI", 18, "bold"),
                text_color=color
            ).pack()

        # Temperature bar visualization
        bar_frame = ctk.CTkFrame(self.weather_frame, fg_color="transparent")
        bar_frame.pack(fill="x", padx=25, pady=(15, 0))

        ctk.CTkLabel(
            bar_frame, text="Temperature Range",
            font=("Segoe UI", 12, "bold"),
            text_color="#888888"
        ).pack(anchor="w")

        self._draw_temp_bar(bar_frame, temp)

    def _draw_temp_bar(self, parent, temp):
        """Draw an animated temperature visualization bar."""
        bar_bg = ctk.CTkFrame(
            parent, height=20, fg_color="#161B22", corner_radius=10
        )
        bar_bg.pack(fill="x", pady=(5, 0))
        bar_bg.pack_propagate(False)

        # Map temp (-10 to 45) to width percentage
        pct = max(0.05, min(1.0, (temp + 10) / 55))
        bar_width = int(600 * pct)

        # Color based on temp
        if temp < 0:
            color = "#00B8D4"
        elif temp < 15:
            color = "#00E5FF"
        elif temp < 25:
            color = "#00E676"
        elif temp < 35:
            color = "#FFC107"
        else:
            color = "#E53935"

        bar_fill = ctk.CTkFrame(
            bar_bg, width=bar_width, height=20,
            fg_color=color, corner_radius=10
        )
        bar_fill.place(x=0, y=0, relheight=1.0)

        ctk.CTkLabel(
            bar_bg, text=f"{temp:.0f}°C",
            font=("Segoe UI", 10, "bold"),
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _show_demo_weather(self, city):
        """Show demo weather when API key is not set."""
        for w in self.weather_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.weather_frame,
            text="☀️",
            font=("Segoe UI Emoji", 64)
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self.weather_frame,
            text=f"{city}",
            font=("Segoe UI", 28, "bold"),
            text_color="#FFFFFF"
        ).pack()

        ctk.CTkLabel(
            self.weather_frame,
            text="24°C  •  Clear Sky",
            font=("Segoe UI", 18),
            text_color="#00E5FF"
        ).pack(pady=(5, 15))

        cards_frame = ctk.CTkFrame(self.weather_frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=25)

        demo_details = [
            ("💧 Humidity", "45%", "#00B8D4"),
            ("💨 Wind", "3.2 m/s", "#7B61FF"),
            ("🌡 Pressure", "1013 hPa", "#FF00E5"),
            ("👁 Visibility", "10.0 km", "#00E676"),
        ]

        for label_text, value, color in demo_details:
            card = ctk.CTkFrame(
                cards_frame, fg_color="#161B22",
                corner_radius=12, height=80
            )
            card.pack(side="left", fill="x", expand=True, padx=4)
            card.pack_propagate(False)
            ctk.CTkLabel(
                card, text=label_text,
                font=("Segoe UI", 11), text_color="#888888"
            ).pack(pady=(12, 2))
            ctk.CTkLabel(
                card, text=value,
                font=("Segoe UI", 18, "bold"), text_color=color
            ).pack()

        ctk.CTkLabel(
            self.weather_frame,
            text="⚠ Demo mode — set OPENWEATHER_API_KEY for live data",
            font=("Segoe UI", 11),
            text_color="#FFC107"
        ).pack(pady=(20, 0))

    def _show_error(self, message):
        """Show error message."""
        for w in self.weather_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.weather_frame, text="⚠️",
            font=("Segoe UI Emoji", 48)
        ).pack(pady=(60, 10))

        ctk.CTkLabel(
            self.weather_frame, text=message,
            font=("Segoe UI", 16),
            text_color="#E53935"
        ).pack()