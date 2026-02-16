import time
import threading
import numpy as np
import pyautogui
import keyboard
import ctypes
import pydirectinput

# ===== CONFIGURATION =====
TARGET_COLOR = (170, 255, 127)
REGION = (1161, 465, 246, 475)  # (left, top, width, height)
TIMEOUT = 25  # seconds to wait for color before restart
CLICK_DELAY = 1  # seconds between W press and left click
# =========================

# Global state
running = False  # Toggle state: True = process active
counter = 0  # Number of successful cycles
stop_event = threading.Event()  # Used to abort waits when toggling off


# Virtual key codes
KEY_W = 0x57


def send_w():
    """Send W key using Win32 API (keybd_event)"""
    ctypes.windll.user32.keybd_event(KEY_W, 0, 0, 0)  # down
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(KEY_W, 0, 2, 0)  # up


def toggle_running():
    """Callback for F1 hotkey."""
    global running, stop_event
    running = not running
    if running:
        stop_event.clear()
        print("\n[INFO] Process started. Press F1 to stop.")
    else:
        stop_event.set()  # Interrupt any ongoing wait/sleep
        print("\n[INFO] Process stopped. Press F1 to start again.")


def color_in_region(region, target_color):
    """
    Take a screenshot of the given region and return True if any pixel
    matches the target color exactly.
    """
    screenshot = pyautogui.screenshot(region=region)
    # Convert to numpy array
    pixels = np.array(screenshot)
    # Check if any pixel equals target color
    matches = np.all(pixels == target_color, axis=-1)
    return np.any(matches)


def wait_for_color_with_abort(region, target_color, timeout, abort_event):
    """
    Wait up to `timeout` seconds for the target color to appear in the region.
    Returns True if color found, False on timeout.
    Checks `abort_event` periodically to exit early when the user toggles off.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if abort_event.is_set():
            # Aborted by F1
            return False
        if color_in_region(region, target_color):
            return True
        time.sleep(0.1)
    return False


def main_loop():
    global counter
    print("Script ready. Press F1 to start.")
    while True:
        if not running:
            time.sleep(0.1)
            continue

        # ----- Process -----
        # 1. left click
        if not stop_event.is_set():
            pyautogui.click()
            print("[ACTION] Left click (initial)")

        # 2. wait for color -> W -> left click -> repeat
        while running and not stop_event.is_set():
            # Wait for color with timeout
            found = wait_for_color_with_abort(REGION, TARGET_COLOR, TIMEOUT, stop_event)
            if not found:
                if stop_event.is_set():
                    break 
                # Timeout = restart
                print("[TIMEOUT] Color not seen. Restarting...")
                break 
            
            # Color found
            print("[DETECTED] Target color appears!")

            # Press W
            pydirectinput.press('w')
            print("[ACTION] W pressed")

            # wait time before the next click
            wait_end = time.time() + CLICK_DELAY
            while time.time() < wait_end and running and not stop_event.is_set():
                time.sleep(0.1)

            if stop_event.is_set() or not running:
                break

            # next left click
            pyautogui.click()
            print("[ACTION] Left click")

            # number of cycles
            counter += 1
            print(f"[COUNTER] Successful cycles: {counter}")



if __name__ == "__main__":
    # Register hotkey
    keyboard.add_hotkey("f1", toggle_running)

    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n[EXIT] Script terminated by user.")
