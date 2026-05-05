import math
import tkinter as tk
from tkinter import filedialog, messagebox

TITLE = "ac's nx2emu 0.1"

BLUE = "#2388ff"
BLUE2 = "#66b7ff"
BG = "#0b0f18"
PANEL = "#121827"
BLACK = "#000000"
TEXT = "#eaf2ff"


class NX2Engine:
    def __init__(self):
        self.running = False
        self.frame = 0
        self.loaded = None
        self.mode = "Clean-room homebrew shell"

    def load_homebrew(self, path):
        self.loaded = path
        self.frame = 0

    def boot(self):
        self.running = True
        self.frame = 0

    def pause(self):
        self.running = False

    def reset(self):
        self.frame = 0

    def tick(self):
        if self.running:
            self.frame += 1


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(TITLE)
        self.root.geometry("1000x620")
        self.root.configure(bg=BG)

        self.engine = NX2Engine()
        self.build_ui()
        self.loop()

    def btn(self, parent, text, cmd):
        return tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=BLACK,
            fg=BLUE,
            activebackground="#050505",
            activeforeground=BLUE2,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=8,
        )

    def build_ui(self):
        side = tk.Frame(self.root, bg=PANEL, width=230)
        side.pack(side="left", fill="y")

        tk.Label(
            side,
            text="nx2emu",
            bg=PANEL,
            fg=BLUE,
            font=("Segoe UI", 28, "bold"),
        ).pack(pady=(28, 4))

        tk.Label(
            side,
            text="Ryujinx-style blue UI",
            bg=PANEL,
            fg=BLUE2,
            font=("Segoe UI", 10),
        ).pack(pady=(0, 22))

        self.btn(side, "Load Homebrew", self.load).pack(fill="x", padx=18, pady=5)
        self.btn(side, "Simple Boot", self.boot).pack(fill="x", padx=18, pady=5)
        self.btn(side, "Pause", self.pause).pack(fill="x", padx=18, pady=5)
        self.btn(side, "Reset", self.reset).pack(fill="x", padx=18, pady=5)
        self.btn(side, "About", self.about).pack(fill="x", padx=18, pady=5)

        self.status = tk.Label(
            side,
            text="Status: Idle\nCore: nx2 clean-room\nFPS: 60",
            bg="#090d15",
            fg=TEXT,
            justify="left",
            anchor="nw",
            font=("Consolas", 10),
            padx=10,
            pady=10,
        )
        self.status.pack(fill="x", padx=18, pady=26)

        main = tk.Frame(self.root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        top = tk.Frame(main, bg="#182033", height=54)
        top.pack(fill="x")

        tk.Label(
            top,
            text="Game / Homebrew List",
            bg="#182033",
            fg=TEXT,
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left", padx=18)

        self.listbox = tk.Listbox(
            main,
            bg="#080c14",
            fg=TEXT,
            selectbackground=BLUE,
            selectforeground="white",
            font=("Consolas", 11),
            relief="flat",
        )
        self.listbox.pack(fill="x", padx=14, pady=(14, 8), ipady=8)

        self.listbox.insert("end", "Blue Boot Test App")
        self.listbox.insert("end", "Input Tester Homebrew")
        self.listbox.insert("end", "Clean-room NX2 Demo")

        self.screen = tk.Canvas(
            main,
            bg="black",
            highlightthickness=2,
            highlightbackground=BLUE,
        )
        self.screen.pack(fill="both", expand=True, padx=14, pady=14)

        self.bottom = tk.Label(
            main,
            text="Ready. Clean-room mode only.",
            bg="#182033",
            fg=BLUE2,
            anchor="w",
            font=("Consolas", 10),
        )
        self.bottom.pack(fill="x")

    def load(self):
        path = filedialog.askopenfilename(
            title="Open clean-room homebrew/test file",
            filetypes=[
                ("Homebrew/Test", "*.elf *.nro *.bin *.nx2"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self.engine.load_homebrew(path)
            self.listbox.insert("end", path.split("/")[-1])
            self.bottom.config(text=f"Loaded: {path}")

    def boot(self):
        self.engine.boot()
        self.bottom.config(text="Simple NX2 boot animation started.")

    def pause(self):
        self.engine.pause()
        self.bottom.config(text="Paused.")

    def reset(self):
        self.engine.reset()
        self.bottom.config(text="Reset.")

    def about(self):
        messagebox.showinfo(
            "About",
            "Chatgpt's nx2emu 0.1\n"
            "Blue Tkinter Ryujinx-style shell\n"
            "No keys, firmware, leaks, or proprietary boot code.",
        )

    def draw_boot(self):
        self.screen.delete("all")
        w = self.screen.winfo_width()
        h = self.screen.winfo_height()

        f = self.engine.frame
        pulse = int((math.sin(f / 12) + 1) * 30)

        self.screen.create_rectangle(0, 0, w, h, fill="#02040a", outline="")

        if f < 60:
            text = "CHATGPT"
        elif f < 120:
            text = "NX2EMU"
        else:
            text = "SWITCH TWO STYLE BOOT"

        self.screen.create_text(
            w // 2,
            h // 2 - 50,
            text=text,
            fill=BLUE,
            font=("Segoe UI", 36, "bold"),
        )

        self.screen.create_rectangle(
            w // 2 - 120,
            h // 2 + 20,
            w // 2 + 120,
            h // 2 + 36,
            outline=BLUE,
        )

        bar = min(240, (f * 3) % 260)
        self.screen.create_rectangle(
            w // 2 - 120,
            h // 2 + 20,
            w // 2 - 120 + bar,
            h // 2 + 36,
            fill=BLUE,
            outline="",
        )

        self.screen.create_text(
            w // 2,
            h // 2 + 80,
            text="clean-room homebrew boot shell",
            fill=BLUE2,
            font=("Consolas", 12),
        )

        r = 26 + pulse // 3
        self.screen.create_oval(
            w // 2 - r,
            h // 2 - 145 - r,
            w // 2 + r,
            h // 2 - 145 + r,
            outline=BLUE2,
            width=3,
        )

    def draw_idle(self):
        self.screen.delete("all")
        w = self.screen.winfo_width()
        h = self.screen.winfo_height()

        self.screen.create_text(
            w // 2,
            h // 2 - 20,
            text="Chatgpt's nx2emu 0.1",
            fill=BLUE,
            font=("Segoe UI", 34, "bold"),
        )

        self.screen.create_text(
            w // 2,
            h // 2 + 30,
            text="Load homebrew or press Simple Boot",
            fill=TEXT,
            font=("Segoe UI", 13),
        )

    def loop(self):
        self.engine.tick()

        if self.engine.running:
            self.draw_boot()
        else:
            self.draw_idle()

        self.status.config(
            text=(
                f"Status: {'Booting' if self.engine.running else 'Idle'}\n"
                f"Core: nx2 clean-room\n"
                f"Frame: {self.engine.frame}\n"
                f"FPS: 60\n"
                f"Blue: enabled"
            )
        )

        self.root.after(16, self.loop)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
