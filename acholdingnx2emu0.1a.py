"""AC's nx2emu 0.1 - clean-room blue Tkinter shell.

Run with:
    python3.14 nx2emu_fixed_py314.py

This is only a clean-room GUI/homebrew boot-shell mockup. It does not load keys,
firmware, proprietary boot code, or commercial game content.
"""

import math
from collections.abc import Callable
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

TITLE = "AC NX2EMU 0.1"

BLUE = "#2388ff"
BLUE2 = "#66b7ff"
BG = "#0b0f18"
PANEL = "#121827"
BLACK = "#000000"
TEXT = "#eaf2ff"
TOP = "#182033"
STATUS_BG = "#090d15"
SCREEN_BG = "#02040a"
FPS = 60
FRAME_DELAY_MS = round(1000 / FPS)


class NX2Engine:
    """Small clean-room state machine for the GUI animation."""

    def __init__(self) -> None:
        self.running = False
        self.frame = 0
        self.loaded: Path | None = None
        self.mode = "Clean-room homebrew shell"

    def load_homebrew(self, path: str | Path) -> None:
        self.loaded = Path(path)
        self.frame = 0
        self.running = False

    def boot(self) -> None:
        self.running = True
        self.frame = 0

    def pause(self) -> None:
        self.running = False

    def reset(self) -> None:
        self.running = False
        self.frame = 0

    def tick(self) -> None:
        if self.running:
            self.frame += 1


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(TITLE)
        self.root.geometry("1000x620")
        self.root.minsize(760, 480)
        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.engine = NX2Engine()
        self.after_id: str | None = None
        self.build_ui()
        self.loop()

    def btn(self, parent: tk.Widget, text: str, cmd: Callable[[], None]) -> tk.Button:
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
            cursor="hand2",
            takefocus=True,
        )

    def build_ui(self) -> None:
        side = tk.Frame(self.root, bg=PANEL, width=230)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

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
            bg=STATUS_BG,
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

        top = tk.Frame(main, bg=TOP, height=54)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(
            top,
            text="Game / Homebrew List",
            bg=TOP,
            fg=TEXT,
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left", padx=18, pady=11)

        self.listbox = tk.Listbox(
            main,
            bg="#080c14",
            fg=TEXT,
            selectbackground=BLUE,
            selectforeground="white",
            font=("Consolas", 11),
            relief="flat",
            activestyle="none",
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
            bg=TOP,
            fg=BLUE2,
            anchor="w",
            font=("Consolas", 10),
            padx=8,
        )
        self.bottom.pack(fill="x")

    def load(self) -> None:
        path = filedialog.askopenfilename(
            title="Open clean-room homebrew/test file",
            filetypes=[
                ("Homebrew/Test", "*.elf *.nro *.bin *.nx2"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        selected = Path(path)
        self.engine.load_homebrew(selected)
        self.listbox.insert("end", selected.name)
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set("end")
        self.listbox.see("end")
        self.bottom.config(text=f"Loaded: {selected}")

    def boot(self) -> None:
        self.engine.boot()
        self.bottom.config(text="Simple NX2 boot animation started.")

    def pause(self) -> None:
        self.engine.pause()
        self.bottom.config(text="Paused.")

    def reset(self) -> None:
        self.engine.reset()
        self.bottom.config(text="Reset.")
        self.draw_idle()

    def about(self) -> None:
        messagebox.showinfo(
            "About",
            "AC NX2EMU 0.1\n"
            "Blue Tkinter Ryujinx-style shell\n"
            "No keys, firmware, leaks, or proprietary boot code.",
        )

    def draw_boot(self) -> None:
        self.screen.delete("all")
        w = max(self.screen.winfo_width(), 1)
        h = max(self.screen.winfo_height(), 1)

        f = self.engine.frame
        pulse = int((math.sin(f / 12) + 1) * 30)

        self.screen.create_rectangle(0, 0, w, h, fill=SCREEN_BG, outline="")

        if f < 60:
            text = "AC HOLDINGS"
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

        left = w // 2 - 120
        top = h // 2 + 20
        right = w // 2 + 120
        bottom = h // 2 + 36
        self.screen.create_rectangle(left, top, right, bottom, outline=BLUE)

        bar = min(240, (f * 3) % 260)
        self.screen.create_rectangle(
            left,
            top,
            left + bar,
            bottom,
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

    def draw_idle(self) -> None:
        self.screen.delete("all")
        w = max(self.screen.winfo_width(), 1)
        h = max(self.screen.winfo_height(), 1)

        self.screen.create_rectangle(0, 0, w, h, fill="black", outline="")

        self.screen.create_text(
            w // 2,
            h // 2 - 20,
            text="AC NX2EMU 0.1",
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

    def update_status(self) -> None:
        loaded = self.engine.loaded.name if self.engine.loaded else "None"
        self.status.config(
            text=(
                f"Status: {'Booting' if self.engine.running else 'Idle'}\n"
                f"Core: nx2 clean-room\n"
                f"Frame: {self.engine.frame}\n"
                f"FPS: {FPS}\n"
                f"Loaded: {loaded}\n"
                f"Blue: enabled"
            )
        )

    def loop(self) -> None:
        self.engine.tick()

        if self.engine.running:
            self.draw_boot()
        else:
            self.draw_idle()

        self.update_status()
        self.after_id = self.root.after(FRAME_DELAY_MS, self.loop)

    def close(self) -> None:
        if self.after_id is not None:
            try:
                self.root.after_cancel(self.after_id)
            except tk.TclError:
                pass
            self.after_id = None
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
