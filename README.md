# 🖥️ NovaOS — AI-Powered Desktop Operating System

**An intelligent desktop operating system built with Python, featuring a fully integrated AI assistant, 12 built-in applications, and a premium glassmorphism UI.**

NovaOS is a unique AI-first desktop environment that goes beyond traditional operating systems by embedding artificial intelligence into every aspect of the user experience — from natural language control to context-aware suggestions.

---

## 🎬 Live Interactive Demo

### 👉 **Try the Interactive Demo Now (No Installation Required!)**

[![🎮 Play Interactive Demo](https://img.shields.io/badge/🎮%20Play%20Interactive%20Demo-Click%20Here-blueviolet?style=for-the-badge&logo=github)](https://raw.githack.com/TejashPrakash/NovaOS/main/docs/demo.html)

**Features:**
- 🖱️ Click through 12 interactive steps
- ⌨️ Use arrow keys to navigate (← → arrows, ESC to skip)
- 📊 View project stats, themes, shortcuts, and more
- 🚀 Direct link to clone and run locally

---

## 🚀 Quick Start - Run Locally in 30 Seconds

```bash
# Clone and run
git clone https://github.com/TejashPrakash/NovaOS.git
cd NovaOS
pip install -r requirements.txt
python -m playwright install chromium
python main.py
```

**Then:** Unlock with password `nova` → Press **Ctrl+D** for the 15-step in-app demo! 🎮

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
- **Desktop Icons** — Responsive grid, all 12 apps visible
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

## 📊 Project Statistics

```
┌─────────────────────────────────────┐
│      NovaOS by the Numbers           │
├─────────────────────────────────────┤
│ 📝 Total Lines of Code    ~15,000+   │
│ 🤖 AI Skills              34         │
│ 🎨 Built-in Apps          12         │
│ 🎨 Themes                 7          │
│ 🖥️  Virtual Desktops      4          │
│ ⌨️  Keyboard Shortcuts    20+         │
│ 📚 Dependencies            14         │
│ 🔨 Development Time       6+ weeks    │
│ 💼 Purpose                College Admission Project
│ 🏆 Showcases              AI, OS Design, Software Engineering
└─────────────────────────────────────┘
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
├── apps/                   # 12 built-in applications
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
│   ├── task_manager/       # Process manager
│   └── settings.py         # Settings app
├── widgets/                # Reusable UI widgets
├── services/               # AI, audio, wallpaper services
├── commands/               # Shell-like command system
├── sdk/                    # App framework and event bus
└── docs/demo.html          # Interactive demo webpage
```

---

## 🎮 Demo Mode — Interactive Feature Showcase

NovaOS includes a built-in interactive demo that showcases all features — **perfect for college admission presentations**.

### In-App Demo (Ctrl+D)
```bash
# After running the application
python main.py
```
Then unlock (password: `nova`) and press **Ctrl+D** for the demo.

### How to Launch the Demo
| Method | How |
|--------|-----|
| **Keyboard** | Press `Ctrl+D` anywhere in NovaOS |
| **Dock** | Click the **▶** purple button in the dock |
| **Start Menu** | The demo is accessible from the dock controls |

### What the Demo Shows (15 Steps)
| Step | Feature | What Happens |
|------|---------|-------------|
| 1 | 🖥️ Welcome | Introduction to NovaOS |
| 2 | 🤖 AI Assistant | AI panel opens, shows 34 skills |
| 3 | 🌐 Browser | Chromium browser opens, loads a page |
| 4 | 📝 Notes | Note-taking app with AI assist |
| 5 | 📁 Files | File manager with operations |
| 6 | >_ Terminal | 30+ commands demonstrated |
| 7 | 🎵 Music Player | Playback controls shown |
| 8 | 🌤 Weather | Live weather data displayed |
| 9 | 📊 System Monitor | Real-time CPU/RAM graphs |
| 10 | 📋 Task Manager | Process management |
| 11 | 📅 Calendar & 🧮 Calculator | Event management and calculations |
| 12 | 🎨 7 Themes | All themes cycled through |
| 13 | 🖥️ Virtual Desktops | 4 workspaces demonstrated |
| 14 | 🤖 AI-Powered Desktop | Smart Hub, Search, Notifications |
| 15 | ✨ Thank You | Summary and project stats |

### Navigation
- **Next**: Click `Next →` or press `→` arrow key
- **Previous**: Click `← Previous` or press `←` arrow key
- **Skip**: Click `Skip Demo ✕` or press `Escape`

### For Presentations
- The demo takes approximately **3-4 minutes** to complete
- All apps open and close with smooth animations
- AI features demonstrate real-time responses
- Themes cycle to show visual variety
- **No interaction required** — runs fully autonomously
- Press `Escape` at any time to stop the demo

---

## 🎨 Screenshots & Visual Guide

> **Run `python main.py` to see NovaOS in action!** The demo mode (`Ctrl+D`) showcases all features automatically.

### What You'll Experience

- **Lock Screen** — Glassmorphism design with clock, glowing logo, and password field
- **Boot Animation** — Smooth splash screen transition
- **Desktop** — AI-generated wallpaper with floating widgets and responsive icon grid
- **Apps** — 12 fully functional applications with premium UI and smooth animations
- **AI Features** — Smart Hub suggestions, AI Search, voice interaction, notifications
- **7 Themes** — Cyberpunk (neon glow), Midnight (dark blue), Ocean (aqua), Forest (green), Sunset (warm), Arctic (cool white), Neon (vibrant)
- **Window Management** — Drag, resize, snap, tile with visual feedback
- **System Integration** — Real-time CPU/RAM/Network monitoring in system tray

---

## 💻 System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10/11 |
| **Python** | 3.10 or higher |
| **RAM** | 4GB minimum (8GB recommended) |
| **Storage** | 500MB for installation + dependencies |
| **Display** | 1920x1080 or higher |
| **Browser Engine** | Chromium (auto-installed with Playwright) |

---

## 🛠️ Built With

- **Python 3.10+**
- **CustomTkinter** — Modern tkinter UI framework with glassmorphism effects
- **Pillow** — Image processing for wallpapers and effects
- **psutil** — System monitoring and process management
- **Playwright** — Chromium browser engine for built-in browser
- **pygame** — Audio playback for music player
- **pyttsx3** — Text-to-speech for voice interaction
- **Google Gemini API** — Cloud AI for smart features
- **Ollama** — Local AI fallback option
- **python-dotenv** — Environment configuration management

---

## 🔧 Development & Contributing

This project was built as a comprehensive college admission portfolio piece demonstrating:

- **Operating System Design** — Kernel, window management, process handling
- **AI Integration** — Natural language processing, skill routing, multi-provider support
- **UI/UX Design** — Glassmorphism effects, theme system, responsive layouts
- **Software Architecture** — Service registry, event bus, modular app framework
- **System Programming** — Process monitoring, file management, device interaction

### Project Structure Overview

```
Core Systems (25% of code)
├── Kernel & Service Registry
├── Window Manager & Layout Engine
├── Theme Engine & UI Effects
├── Desktop & Widget System
└── Dock & Navigation

AI System (30% of code)
├── 34 Skills (router, voice, notifications)
├── Dual AI Providers (Gemini, Ollama)
├── Memory & Context Management
└── UI Components (Smart Hub, Search, Panels)

Applications (25% of code)
├── 12 Full-Featured Apps
├── Shared SDK & Event Bus
├── Command System (Terminal)
└── File/Process Management

Polish & Effects (20% of code)
├── Animations & Transitions
├── Themes & Customization
├── Demo Mode Orchestration
└── Boot Sequence & Splash
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built as a college admission project showcasing:
- Advanced AI integration techniques
- Modern operating system design principles
- Professional Python software engineering
- UI/UX design with glassmorphism effects
- Full-stack application development

**Special Thanks To:**
- CustomTkinter community for UI framework
- Playwright for browser automation
- Google Gemini for cloud AI
- Ollama for local AI capabilities

---

## 📞 Questions or Feedback?

For admission officers or anyone interested in the project:
- 📧 Review the code and architecture
- 🎮 Try the interactive demo above (no installation needed!)
- 🎮 Try the in-app demo mode (`Ctrl+D`) for a complete feature walkthrough
- 🐛 Check the GitHub issues for known features and improvements
- 💬 Feel free to reach out with questions about the design decisions

---

**NovaOS** — *Where AI meets the Desktop* ✨

*Built with passion for innovation and demonstrating professional-grade software engineering skills.*
