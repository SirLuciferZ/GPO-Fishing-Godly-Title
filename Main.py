import time
import threading
import numpy as np
import pyautogui
import keyboard
import ctypes
import pydirectinput

# ===== CONFIGURATION =====
TARGET_COLOR = (170, 255, 127)  # RGB of the color to look for
REGION = (1161, 465, 246, 475)  # (left, top, width, height) – screen area to monitor
TIMEOUT = 25  # seconds to wait for color before restart
CLICK_DELAY = 1  # seconds between W press and left click
# =========================

# Global state
running = False  # Toggle state: True = process active
counter = 0  # Number of successful cycles
stop_event = threading.Event()  # Used to abort waits when toggling off


# Virtual key codes (for Win32 API)
KEY_W = 0x57


def send_w():
    """Send W key using Win32 API (keybd_event)"""
    ctypes.windll.user32.keybd_event(KEY_W, 0, 0, 0)  # down
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(KEY_W, 0, 2, 0)  # up


def toggle_running():
    """Callback for F1 hotkey – toggles the process on/off."""
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
    # Convert to numpy array for fast pixel access
    pixels = np.array(screenshot)
    # Check if any pixel equals target_color
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
        # Small sleep to avoid high CPU usage
        time.sleep(0.1)
    return False


def main_loop():
    global counter
    print("Script ready. Press F1 to start.")
    while True:
        if not running:
            time.sleep(0.1)
            continue

        # ----- Process is active -----
        # 1. Initial left click
        if not stop_event.is_set():
            pyautogui.click()
            print("[ACTION] Left click (initial)")

        # 2. Inner cycle: wait for color -> W -> left click -> repeat
        while running and not stop_event.is_set():
            # Wait for color with timeout
            found = wait_for_color_with_abort(REGION, TARGET_COLOR, TIMEOUT, stop_event)
            if not found:
                if stop_event.is_set():
                    break  # Stopped by user
                # Timeout – restart from initial left click
                print("[TIMEOUT] Color not seen. Restarting...")
                break  # Break inner loop to go back to initial left click

            # Color found
            print("[DETECTED] Target color appears!")
            
            # # Color found
            # print("[DETECTED] Target color appears!")

            # # Optional: activate the game window
            # try:
            #     import pygetwindow as gw
            #     game = gw.getWindowsWithTitle('Your Game Title')[0]  # change this
            #     game.activate()
            #     time.sleep(0.1)
            # except:
            #     pass

            # # Send W using Win32 API
            # send_w()
            # print("[ACTION] W pressed")

            # Press W
            pydirectinput.press('w')
            print("[ACTION] W pressed")

            # Wait 1 second (check abort every 0.1s)
            wait_end = time.time() + CLICK_DELAY
            while time.time() < wait_end and running and not stop_event.is_set():
                time.sleep(0.1)

            if stop_event.is_set() or not running:
                break  # User stopped during delay

            # Left click
            pyautogui.click()
            print("[ACTION] Left click")

            # Increment counter and print
            counter += 1
            print(f"[COUNTER] Successful cycles: {counter}")

        # End of inner loop – either timeout or user stop
        # If user stopped, outer loop will see running == False and sleep.
        # Otherwise (timeout), outer loop will continue and trigger another initial left click.


if __name__ == "__main__":
    # Register hotkey (F1)
    keyboard.add_hotkey("f1", toggle_running)

    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n[EXIT] Script terminated by user.")
