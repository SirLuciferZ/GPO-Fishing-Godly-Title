# GPO Fishing Godly Title

This Python script monitors a specific region of your screen for a target color. When the color appears, it automatically presses the **W** key, waits one second, and then left‑clicks. The cycle repeats indefinitely, and a counter shows how many successful cycles have been completed. You can toggle the automation on and off with the **F1** key. If the target color does not appear within a configurable timeout, the process restarts from the initial left click.

Perfect for automating repetitive tasks in games or applications where you need to react to a visual cue.

---

## Features

- 🎯 Monitor a custom screen region for an exact RGB color.
- ⌨️ Simulates **W** key press and left mouse click when color is detected.
- 🔁 Loops automatically – after clicking, it waits for the same color again.
- ⏱️ Timeout protection: if the color isn’t seen within a set time, the cycle restarts.
- 📊 On‑screen counter in the console showing total successful cycles.
- ⏯️ Toggle on/off anytime with the **F1** hotkey.
- 🛡️ Uses `pydirectinput` for game‑friendly key presses (bypasses many input blockers).

---

## Requirements

- Python 3.6 or higher
- Windows (for the hotkey and Win32 API – the script can be adapted for macOS/Linux with minor changes)

---

## Installation

1. **Clone or download** this repository.

2. **Install the required Python packages**:

   ```bash
   pip install -r requirements.txt
   ```

- `pyautogui` – screen capture and mouse control.
- `pydirectinput` – simulates keyboard input in a way that works with most games.
- `keyboard` – global hotkey (F1) handling.
- `pillow` & `numpy` – fast pixel scanning.
- `pygetwindow` – optional, for bringing the game window to focus.

---

## Configuration

Open the script in a text editor and adjust the constants at the top:

```python
# ===== CONFIGURATION =====
TARGET_COLOR = (255, 0, 0)          # RGB of the color to look for
REGION = (100, 100, 200, 200)       # (left, top, width, height) 
TIMEOUT = 10                        # seconds to wait for color before restart
CLICK_DELAY = 1                      # seconds between W press and left click
# =========================
```

- **TARGET_COLOR**: The exact RGB value you want to detect. You can find it using a tool like the one described below.
- **REGION**: The screen area to search. See [Finding the Region](#finding-the-region).
- **TIMEOUT**: How long (in seconds) to wait for the color before giving up and restarting the cycle.
- **CLICK_DELAY**: The pause between pressing **W** and performing the left click.

---

## Finding the Region

You need to know the pixel coordinates of the top‑left corner of the area you want to monitor, and its width and height. Use this helper script to get them easily.

Run it, follow the prompts, and copy the resulting tuple into your main script.

> **Tip**: Keep the region as small as possible for faster scanning. If the color always appears at the exact same pixel, you can set `width=1, height=1` and use the pixel’s coordinates.

---

## Usage

1. **Place your mouse** where you want the initial left click to happen. (The script always clicks at the current mouse position when starting a cycle.)

2. **Run the script** from your terminal:

   ```bash
   python Main.py
   ```

3. **Press F1** to start the automation. The console will show:

   ```bash
   [INFO] Process started. Press F1 to stop.
   [ACTION] Left click (initial)
   ```

4. When the target color appears in the defined region, the script will:
   - Press **W**
   - Wait 1 second (or your configured `CLICK_DELAY`)
   - Left‑click
   - Increase the counter and print:

     ```bash
     [DETECTED] Target color appears!
     [ACTION] W pressed
     [ACTION] Left click
     [COUNTER] Successful cycles: 1
     ```

5. The script will then wait for the color to appear again. If the color does **not** appear within `TIMEOUT` seconds, it restarts from the initial left click:

   ```bash
   [TIMEOUT] Color not seen. Restarting...
   [ACTION] Left click (initial)
   ```

6. Press **F1** again at any time to pause. Press F1 once more to resume (the script will start again with a left click).

7. To exit completely, press **Ctrl+C** in the terminal.

---

## Troubleshooting

### ❌ The W key is not working in my game

- The script now uses `pydirectinput` by default, which works with most games. Make sure you have it installed (`pip install pydirectinput`).
- **Run the script as Administrator** – right‑click your terminal and select “Run as administrator”.
- Add window focusing before pressing W. In the script, uncomment and adjust the `pygetwindow` section:

  ```python
  import pygetwindow as gw
  game = gw.getWindowsWithTitle('Your Game Title')[0]
  game.activate()
  time.sleep(0.2)
  ```

### ❌ The color is never detected

- Double‑check your `REGION` and `TARGET_COLOR` values.
- Use the pixel‑color tool from the [Finding the Region](#finding-the-region) section to verify the exact RGB at the target spot.
- If the color varies slightly (due to anti‑aliasing or lighting), you may need to modify the script to accept a range (e.g., check if each RGB component is within a tolerance). Let me know if you need help with that.

### ❌ `ValueError: Coordinate 'right' is less than 'left'`

- This happens when you selected the corners in the wrong order. The improved helper script above automatically handles this by always using `min`/`max`. Rerun the helper to get a valid region.

### ❌ The script stops responding or the hotkey doesn't work

- Make sure you’re running the script with the console in focus (the hotkey listener works globally, but some terminal emulators may interfere).
- Try running in a simple Command Prompt or PowerShell window.

---

## Notes for Game Automation

- Some games with advanced anti‑cheat systems may still block simulated input. In that case, consider using a hardware device (e.g., Arduino) or a different approach.
- The left click is performed with `pyautogui.click()`, which is usually fine. If you need a “hardware” click, you can replace it with a `pydirectinput.click()` (though that may not be supported on all systems).

---

## License

This script is provided as‑is under the MIT License. Feel free to modify and distribute it.

---

## Support

If you encounter any issues or have questions, please open an issue on the repository or contact the author.

Happy automating!
