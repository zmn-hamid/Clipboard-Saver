import tkinter as tk
import time
import threading
import pyperclip

TIME_BETWEEN_UPDATES = 1
try:
    FONT_DATA = ("Corbel", 14)
except tk.TclError:
    FONT_DATA = ("Arial", 14)

root = tk.Tk()
root.title("add album")

app_label = tk.Label(root, text="- your clipboard here -", font=FONT_DATA)
app_label.pack(pady=10)

clipboard_text_area = tk.Text(root, font=FONT_DATA, width=50, height=10)
clipboard_text_area.pack(pady=10)

clip_watcher = None


def enable_or_disable_callback():
    global clip_watcher
    if enable_or_disable.config("text")[-1] == "Start Logging":
        enable_or_disable.config(text="Stop Logging", bg="red")
        clip_watcher = ClipboardWatcher(add_to_text_area, 1.0)
        clip_watcher.start()
    else:
        enable_or_disable.config(text="Start Logging", bg="green")
        if clip_watcher is not None:
            clip_watcher.stop()
            clip_watcher = None


enable_or_disable = tk.Button(
    root,
    text="Start Logging",
    font=FONT_DATA,
    command=enable_or_disable_callback,
    bg="green",
    fg="white",
)
enable_or_disable.pack(pady=10)


def add_to_text_area(clipboard):
    clipboard_text_area.insert("end", str(clipboard) + "\n")


class ClipboardWatcher(threading.Thread):
    def __init__(self, callback, pause=5.0):
        super(ClipboardWatcher, self).__init__()
        self._callback = callback
        self._pause = pause
        self._stopping = False
        self._recent_value = pyperclip.paste()  # Ignore the current clipboard content

    def run(self):
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != self._recent_value:
                self._recent_value = tmp_value
                self._callback(clipboard=tmp_value)
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True


root.mainloop()
clip_watcher.stop()
