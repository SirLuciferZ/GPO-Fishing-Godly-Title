import pyautogui
import time


def get_region():
    print("Move your mouse to the TOP‑LEFT corner of the region.")
    time.sleep(3)
    x1, y1 = pyautogui.position()
    print(f"Point 1: ({x1}, {y1})")

    print("Now move your mouse to the BOTTOM‑RIGHT corner of the region.")
    time.sleep(3)
    x2, y2 = pyautogui.position()
    print(f"Point 2: ({x2}, {y2})")

    # Compute the bounding box (always positive width/height)
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    width = right - left
    height = bottom - top

    print(f"\n✅ Region = ({left}, {top}, {width}, {height})")
    return left, top, width, height


if __name__ == "__main__":
    get_region()
