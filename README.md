# ◈ NovaOS

### AI-Powered Desktop Operating System

> A fully functional desktop environment built from scratch in Python, featuring a custom window manager, AI assistant with 15+ skills, and 11 built-in applications.

---

## 🎯 Overview

NovaOS is a from-scratch desktop operating system that demonstrates advanced software engineering concepts including:

- **Custom window manager** with drag, resize, minimize, maximize, and tiling
- **AI assistant** powered by Google Gemini / Ollama with natural language tool execution
- **Modular app architecture** — each app is an isolated process with its own lifecycle
- **Premium glassmorphism UI** with animated backgrounds and ambient lighting
- **Full boot sequence** — animated splash → lock screen → desktop

---

## ✨ Features

### 🖥️ Desktop Environment
| Feature | Description |
|---------|-------------|
| Window Manager | Drag, resize, minimize, restore, maximize, tiling for 2+ windows |
| Dock | Floating glassmorphism dock with running app indicators |
| Launcher | Searchable app launcher with AI-enhanced queries (Ctrl+Space) |
| Start Menu | Grid-based start menu with theme integration |
| Desktop Icons | Double-click to launch any app |
| System Tray | Live clock, CPU%, RAM%, network status, quick settings |
| Context Menu | Right-click desktop for actions |
| Notifications | Auto-dismissing toast notifications |
| Lock Screen | Clock, password auth, shake animation (Ctrl+Shift+L) |
| Boot Splash | Animated particle effect with progress bar |

### 🤖 AI Assistant
| Feature | Description |
|---------|-------------|
| Gemini / Ollama | Cloud or local AI provider with automatic fallback |
| 15+ Skills | Open/close apps, weather, calendar, notes, browser, calculator, terminal, music, files, settings, time, system |
| Voice Input | Speech-to-text and text-to-speech via speech_recognition + pyttsx3 |
| Desktop Widget | Always-visible AI chat on the desktop |
| AI Panel | Full chat panel accessible from the desktop |
| Context-Aware | AI can read browser pages, notes, and system state |

### 📱 Built-in Applications

| App | Description |
|-----|-------------|
| 🌐 Browser | Embedded web browser with tabs, bookmarks, AI page summarization |
| 📝 Notes | Rich note editor with SQLite persistence and AI assist |
| 🧮 Calculator | Theme-aware calculator with safe expression evaluation |
| 📁 Files | File explorer with navigation, icons, and directory history |
| 🖥️ Terminal | 30+ built-in commands, aliases, tab completion, history |
| 🌤 Weather | Live weather dashboard with OpenWeatherMap API |
| 📅 Calendar | Month view with event creation, deletion, and persistence |
| 📊 System Monitor | Real-time CPU, RAM, disk, network with live charts |
| 🎵 Music Player | Playlist management, playback controls, volume, progress |
| 👁 Viewer | Image zoom/pan and text file viewer with syntax support |
| ⚙️ Settings | Theme switching, AI provider, effects toggle |

### 🎨 Visual Design
- **4 Premium Themes**: Cyberpunk, Neon, Sunset, Ocean
- **Animated Neural Network** background with particle connections
- **Ambient Lighting** effects with floating light orbs
- **Glassmorphism** UI components throughout
- **Smooth Animations** on window open, close, and rearrange

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/NovaOS.git
cd NovaOS

# Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys:
#   GEMINI_API_KEY=your_key_here       (for AI features)
#   OPENWEATHER_API_KEY=your_key_here   (for weather app)

# Run NovaOS
python main.py
```

### Lock Screen
- **Password**: `nova`
- **Lock shortcut**: `Ctrl+Shift+L`

### Terminal
- 30+ built-in commands (grep, ps, df, tree, curl, ping, etc.)
- Tab completion for commands and file paths
- Command history with Up/Down arrows
- Aliases: `ll` → `ls`, `cls` → `clear`, `..` → `cd ..`

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_router.py -v
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.12** | Core language |
| **CustomTkinter** | Modern Tkinter widgets |
| **Pillow** | Image processing |
| **psutil** | System monitoring |
| **SQLite** | Notes database |
| **pygame** | Audio playback |
| **speech_recognition** | Voice input |
| **pyttsx3** | Text-to-speech |
| **google-genai** | Gemini AI provider |
| **requests** | HTTP/API calls |
| **python-dotenv** | Environment config |

---

## 📊 Project Stats

- **11 built-in applications**
- **15+ AI skills** (natural language tools)
- **30+ terminal commands**
- **4 premium themes**
- **3 AI providers** (Gemini, Ollama, Voice)
- **100% Python** — no compiled extensions

---

## 📄 License

This project was created for educational purposes.

---

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- AI powered by [Google Gemini](https://ai.google.dev/) and [Ollama](https://ollama.ai/)
- System monitoring via [psutil](https://github.com/giampaolo/psutil)
