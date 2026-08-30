# 🖥️ NovaOS — AI-Powered Desktop Operating System

**An intelligent desktop operating system built with Python, featuring a fully integrated AI assistant, 11 built-in applications, and a premium glassmorphism UI.**

NovaOS is a unique AI-first desktop environment that goes beyond traditional operating systems by embedding artificial intelligence into every aspect of the user experience — from natural language commands to intelligent suggestions, voice interaction, and AI-powered applications.

---

## 🌟 Features

### 🤖 AI-Powered Core
- **34 AI Skills** — Control the entire OS through natural language
- **Smart Hub** — Context-aware suggestions based on time and usage patterns
- **AI Desktop Search** (`Ctrl+K`) — Natural language search across apps, files, and notes
- **AI Context Menu** — Right-click any file for AI analysis
- **Voice Interaction** — Speak to your OS (via pyttsx3)
- **AI Panel** — Full chat interface with close button and conversation history
- **Smart Notifications** — AI-generated contextual tips and reminders
- **Dual AI Providers** — Gemini (cloud) + Ollama (local) with automatic fallback

### 🖥️ Desktop Environment
- **Glassmorphism UI** — Premium glass-effect windows and widgets
- **7 Themes** — Cyberpunk, Midnight, Ocean, Forest, Sunset, Arctic, Neon
- **Neural Background** — Animated canvas background with floating particles
- **Ambient Lighting** — Dynamic glow effects on the desktop
- **AI Wallpaper** — Auto-generated gradient wallpapers
- **Desktop Clock** — Large floating clock with date and day
- **Weather Widget** — Live weather data on the desktop
- **Desktop Icons** — Responsive grid, all 11 apps visible
- **Virtual Desktops** — 4 switchable workspaces (Ctrl+1/2/3/4)

### 🪟 Window Management
- **Drag & Resize** — Full window manipulation with smooth animations
- **Minimize / Maximize / Close** — Standard window controls
- **Window Snapping** — Snap to left, right, top, bottom edges
- **Auto-Tiling** — Automatic 2-column grid layout for multiple windows
- **State Persistence** — Window positions saved between sessions
- **Tab Support** — Multi-tab window titles

### 🔒 Security
- **Lock Screen** — Password-protected lock screen with clock display
- **3-Attempt Lockout** — Prevents brute-force attempts
- **Keyboard Shortcut** — `Ctrl+Shift+L` to lock instantly

### 🎮 Demo Mode
- **Interactive Walkthrough** — Press `Ctrl+D` or click the Demo button (▶) in the dock
- **15-Step Tour** — Showcases every major feature with guided transitions
- **Perfect for presentations** — Auto-opens apps, demonstrates AI, and highlights capabilities

### 🎵 12 Built-In Applications

| App | Description |
|-----|-------------|
| 🌐 **Browser** | Full Chromium browser via Playwright — YouTube, Google, any website |
| 📝 **Notes** | Create, edit, save, delete notes with AI assist |
| 🧮 **Calculator** | Full calculator with themed buttons and safe evaluation |
| 📁 **Files** | File manager with copy, paste, delete, rename, context menu |
| >_ **Terminal** | 30+ built-in commands, history, tab completion, aliases |
| 🌤 **Weather** | Live weather data via OpenWeather API with visual display |
| 📅 **Calendar** | Monthly calendar with event management and persistence |
| 📊 **System Monitor** | Real-time CPU, RAM, disk, and network monitoring |
| 🎵 **Music Player** | Full playback with playlist, volume, progress, and file picker |
| 👁 **Viewer** | Image and text file viewer with zoom and pan |
| 📋 **Task Manager** | Process list, CPU/RAM monitoring, kill/suspend/resume |
| ⚙️ **Settings** | Theme, AI provider, wallpaper, effects, and system info |

### ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Space` | Toggle AI Launcher |
| `Ctrl+K` | AI Desktop Search |
| `Ctrl+Shift+L` | Lock Screen |
| `Ctrl+1/2/3/4` | Switch Virtual Desktop |
| `Ctrl+Q` | Close Active Window |
| `Ctrl+D` | Start Demo Mode |
| `Ctrl+/` | Show Keyboard Shortcuts |

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Windows 10/11 (primary target)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/NovaOS.git
cd NovaOS

# Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser engine (for the built-in browser)
python -m playwright install chromium

# Set up API keys (optional — for AI features)
copy .env.example .env
# Edit .env and add your API keys

# Run NovaOS
python main.py
```

### Default Lock Screen Password
```
nova
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# AI Provider (gemini or ollama)
NOVA_PROVIDER=gemini

# Google Gemini API Key (get from https://aistudio.google.com/apikey)
GEMINI_API_KEY=your_api_key_here

# OpenWeatherMap API Key (get from https://openweathermap.org/api)
OPENWEATHER_API_KEY=your_api_key_here
```

### Without API Keys
NovaOS works without API keys — AI features will show "not configured" messages, but all apps, themes, and desktop features work fully.

---

## 🏗️ Architecture

```
NovaOS/
├── main.py                 # Entry point: splash → lock screen → desktop
├── core/                   # OS kernel and core systems
│   ├── kernel.py           # Central coordinator
│   ├── app.py              # Main NovaOS orchestrator
│   ├── desktop.py          # Desktop with wallpaper and widgets
│   ├── window_manager.py   # Window creation, tiling, snapping
│   ├── dock.py             # Bottom dock with running apps
│   ├── launcher.py         # Ctrl+Space spotlight launcher
│   ├── start_menu.py       # Start menu with app grid
│   ├── lock_screen.py      # Password-protected lock screen
│   ├── splash.py           # Animated boot sequence
│   ├── system_tray.py      # CPU, RAM, network indicators
│   ├── theme.py            # 7 theme engine
│   ├── virtual_desktops.py # 4 workspace switcher
│   └── ...
├── ai/                     # AI system
│   ├── assistant.py        # Main AI assistant
│   ├── router.py           # Routes queries to skills
│   ├── skills/             # 34 AI skills
│   ├── providers/          # Gemini, Ollama, Voice
│   └── ui/                 # Smart Hub, AI Panel, Search, Notifications
├── apps/                   # 11 built-in applications
│   ├── browser/            # Chromium browser (Playwright)
│   ├── notes/              # Note-taking app
│   ├── calculator/         # Calculator
│   ├── file_manager/       # File operations
│   ├── terminal/           # Terminal emulator
│   ├── weather/            # Weather dashboard
│   ├── music_player/       # Music player
│   ├── system_monitor/     # System monitor
│   ├── calendar_app/       # Calendar
│   ├── viewer/             # File viewer
│   └── settings.py         # Settings app
├── widgets/                # Reusable UI widgets
├── services/               # AI, audio, wallpaper services
├── commands/               # Shell-like command system
└── sdk/                    # App framework and event bus
```

---

## 🎮 Demo Mode

NovaOS includes a built-in interactive demo that showcases all features — perfect for college admission presentations.

### How to Use
1. Launch NovaOS: `python main.py`
2. Unlock the lock screen (password: `nova`)
3. Press **Ctrl+D** or click the **▶ Demo** button in the dock
4. Watch as NovaOS walks through all 12 apps, AI features, themes, and desktop capabilities

### Demo Walkthrough (15 Steps)
| Step | Feature Demonstrated |
|------|---------------------|
| 1 | Smart Hub — AI-powered suggestions |
| 2 | AI Desktop Search (Ctrl+K) |
| 3 | Browser — opens Google, performs search |
| 4 | Notes — create and save a note |
| 5 | Calculator — perform calculations |
| 6 | Weather — live weather data |
| 7 | System Monitor — live CPU/RAM graphs |
| 8 | Terminal — run commands |
| 9 | Calendar — create an event |
| 10 | Music Player — play/pause controls |
| 11 | Settings — theme switching demo |
| 12 | Virtual Desktops — switch workspaces |
| 13 | AI Assistant — ask a question |
| 14 | Theme showcase — cycle through all 7 themes |
| 15 | Task Manager — view running processes |

Each step includes a timed transition with explanatory notifications. The demo runs autonomously — no interaction required.

### For Presentations
- The demo takes approximately **3-4 minutes** to complete
- All apps open and close with smooth animations
- AI features demonstrate real-time responses
- Themes cycle to show visual variety

## 🎨 Screenshots

> *Screenshots coming soon — run `python main.py` to see NovaOS in action!*

---

## 🛠️ Built With

- **Python 3.10+**
- **CustomTkinter** — Modern tkinter UI framework
- **Pillow** — Image processing for wallpapers
- **psutil** — System monitoring
- **Playwright** — Chromium browser engine
- **pygame** — Audio playback
- **pyttsx3** — Text-to-speech
- **Google Gemini** — Cloud AI
- **python-dotenv** — Environment configuration

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built as a college admission project showcasing AI integration, operating system design, and software engineering skills.

**NovaOS** — *Where AI meets the Desktop* ✨
