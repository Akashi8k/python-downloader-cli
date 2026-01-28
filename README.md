Here’s a clean, well-structured **README.md** you can copy-paste directly. No file creation, just the text 👌
I kept it professional but friendly, and formatted nicely for GitHub.

---

# 🎥 YouTube Video Downloader (Python)

A simple, interactive **YouTube video downloader** built with **Python** and **yt-dlp**, supporting resolution selection, automatic audio merging, and bundled **FFmpeg** support (including PyInstaller compatibility).

---

## ✨ Features

* 📺 Download YouTube videos in multiple resolutions (up to **4K** if available)
* 🔊 Automatically merges **best video + best audio**
* 🧠 Detects and displays **available resolutions** before download
* 🧩 Automatically installs missing dependencies (`yt-dlp`)
* 🎞️ Uses **FFmpeg** for merging (bundled or local)
* 📁 Custom output folder with a sensible default
* 🔁 Supports **multiple downloads in one session**
* 📦 Works both as a Python script and a **PyInstaller executable**

---

## 📦 Requirements

* **Python 3.8+**
* Internet connection
* Supported OS:

  * ✅ Windows
  * ⚠️ Linux / macOS (FFmpeg path may need adjustment)

> **Note:**
> The script will automatically install `yt-dlp` if it’s not already installed.

---

## 🛠 Dependencies

* [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
* **FFmpeg**

  * Bundled with PyInstaller builds **or**
  * Placed in `ffmpeg/bin` next to the script

---

## 📂 FFmpeg Folder Structure

For script mode:

```
project-folder/
│── downloader.py
│── ffmpeg/
│   └── bin/
│       └── ffmpeg.exe
```

For PyInstaller mode:

```
_MEIPASS/
│── ffmpeg/
│   └── bin/
│       └── ffmpeg.exe
```

The script automatically adds FFmpeg to `PATH`.

---

## ▶️ How to Run

### Run as Python Script

```bash
python downloader.py
```

### Run as Executable

Just double-click the `.exe` file (if built using PyInstaller).

---

## 🧭 How It Works

1. Enter a **YouTube video URL**
2. Script fetches and shows **available resolutions**
3. Choose a resolution (e.g. `1080`, `720`, `4k`)
4. Choose an output folder (or press Enter for default)
5. Video downloads with **best audio merged**
6. Repeat or exit

---

## 📁 Default Download Location

If no folder is specified:

```
Desktop/yt downloads
```

---

## 🎞️ Output File Naming

Downloaded videos are saved as:

```
Video Title-1080.mp4
```

Resolution suffix adjusts automatically.

---

## ⚠️ Error Handling

* Invalid URLs or resolutions are handled gracefully
* FFmpeg-related issues are clearly reported
* Network or download errors display helpful messages

---

## 🧪 Example Resolutions Supported

* `4k` (2160p)
* `1440`
* `1080`
* `720`
* `480`
* `360`
* `240`

Availability depends on the video.

---

## 🚫 Limitations

* DRM-protected or private videos cannot be downloaded
* Some videos may not offer all resolutions
* YouTube rate limits may apply

---

## 🧰 Built With

* **Python**
* **yt-dlp**
* **FFmpeg**

---

## 📜 Disclaimer

This tool is intended for **educational and personal use only**.
Please respect YouTube’s Terms of Service and the rights of content creators.

---

## 🙌 Credits

* yt-dlp community
* FFmpeg project

---

If you want, I can also:

* ✨ Make this README **more minimal**
* 🧱 Add **PyInstaller build instructions**
* 🌐 Add **screenshots / badges**
* 🧪 Add **troubleshooting section**

Just say the word 😄
