import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
import pydirectinput
import keyboard  # for global hotkeys


# -----------------------
# Automation Engine
# -----------------------
class AutoClicker:
    def __init__(self):
        self.running = False
        self.thread = None
        self.interval = 0.1
        self.button = "left"

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            pyautogui.click(button=self.button)
            time.sleep(self.interval)


class AutoKeyboard:
    def __init__(self):
        self.running = False
        self.thread = None
        self.key = None
        self.mode = "Pressing"
        self.interval = 0.2

    def start(self):
        if not self.running and self.key:
            self.running = True
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False

    def _loop(self):
        if self.mode == "Pressing":
            pydirectinput.keyDown(self.key)
            while self.running:
                time.sleep(0.1)
            pydirectinput.keyUp(self.key)

        elif self.mode == "Clicking":
            while self.running:
                pydirectinput.press(self.key)
                time.sleep(self.interval)


# -----------------------
# GUI
# -----------------------
class AutoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automation Tool")
        self.root.geometry("450x400")

        # Engines
        self.mouse_engine = AutoClicker()
        self.keyboard_engine = AutoKeyboard()

        # Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Mouse Tab
        mouse_tab = ttk.Frame(self.notebook)
        self.notebook.add(mouse_tab, text="Mouse")
        self._build_mouse_tab(mouse_tab)

        # Keyboard Tab
        keyboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(keyboard_tab, text="Keyboard")
        self._build_keyboard_tab(keyboard_tab)

        # Global hotkeys
        keyboard.add_hotkey("f4",self.start_mouse)         # Start mouse
        keyboard.add_hotkey("f5", self.stop_mouse)         # Stop mouse
        keyboard.add_hotkey("f6", self.start_keyboard)     # Start keyboard
        keyboard.add_hotkey("f7", self.stop_keyboard)      # Stop keyboard
        keyboard.add_hotkey("esc", self.stop_all)          # Emergency stop

    # ---- Mouse Tab ----
    def _build_mouse_tab(self, frame):
        ttk.Label(frame, text="Interval (s):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.mouse_interval_var = tk.DoubleVar(value=0.1)
        ttk.Entry(frame, textvariable=self.mouse_interval_var).grid(row=0, column=1)

        ttk.Label(frame, text="Button:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.mouse_button_var = tk.StringVar(value="left")
        ttk.Combobox(frame, textvariable=self.mouse_button_var,
                     values=["left", "right", "middle"]).grid(row=1, column=1)

        ttk.Button(frame, text="Start Mouse(F4)", command=self.start_mouse).grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="Stop Mouse(F5)", command=self.stop_mouse).grid(row=2, column=1, pady=10)

        self.mouse_status = tk.StringVar(value="Stopped")
        ttk.Label(frame, textvariable=self.mouse_status).grid(row=3, column=0, columnspan=2, pady=5)

    # ---- Keyboard Tab ----
    def _build_keyboard_tab(self, frame):
        ttk.Label(frame, text="Key:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.key_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.key_var).grid(row=0, column=1)

        ttk.Label(frame, text="Mode:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.mode_var = tk.StringVar(value="Pressing")
        ttk.Combobox(frame, textvariable=self.mode_var,
                     values=["Pressing", "Clicking"]).grid(row=1, column=1)

        ttk.Label(frame, text="Click Interval (s):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.key_interval_var = tk.DoubleVar(value=0.2)
        ttk.Entry(frame, textvariable=self.key_interval_var).grid(row=2, column=1)

        ttk.Button(frame, text="Start Keyboard(F6)", command=self.start_keyboard).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Stop Keyboard(F7)", command=self.stop_keyboard).grid(row=3, column=1, pady=10)

        self.keyboard_status = tk.StringVar(value="Stopped")
        ttk.Label(frame, textvariable=self.keyboard_status).grid(row=4, column=0, columnspan=2, pady=5)

    # ---- Mouse control ----
    def start_mouse(self):
        self.mouse_engine.interval = self.mouse_interval_var.get()
        self.mouse_engine.button = self.mouse_button_var.get()
        self.mouse_engine.start()
        self.mouse_status.set("Running")

    def stop_mouse(self):
        self.mouse_engine.stop()
        self.mouse_status.set("Stopped")

    # ---- Keyboard control ----
    def start_keyboard(self):
        self.keyboard_engine.key = self.key_var.get()
        self.keyboard_engine.mode = self.mode_var.get()
        self.keyboard_engine.interval = self.key_interval_var.get()
        self.keyboard_engine.start()
        self.keyboard_status.set(f"Running ({self.keyboard_engine.mode})")

    def stop_keyboard(self):
        self.keyboard_engine.stop()
        self.keyboard_status.set("Stopped")

    # ---- Context-aware hotkey ----
    def start_current_tab(self):
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        if current_tab == "Mouse":
            self.start_mouse()
        elif current_tab == "Keyboard":
            self.start_keyboard()

    # ---- Global stop ----
    def stop_all(self):
        self.stop_mouse()
        self.stop_keyboard()


# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoGUI(root)
    root.mainloop()
