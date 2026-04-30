"""Custom Tkinter widgets: lightweight markdown renderer, code editor with line numbers."""
from __future__ import annotations

import re
import tkinter as tk
from tkinter import ttk

from . import theme


def render_markdown(text_widget: tk.Text, markdown: str) -> None:
    """Render a small subset of markdown into a tk.Text widget.

    Supported:
      # H1, ## H2, ### H3
      ```code blocks```
      `inline code`
      **bold**, *italic*
      - bullet lists
      | tables (rendered as plain text, but with monospace styling)
    """
    text_widget.configure(state="normal")
    text_widget.delete("1.0", "end")

    # tags
    text_widget.tag_configure("h1", font=theme.FONT_H1, foreground=theme.ACCENT, spacing3=10, spacing1=10)
    text_widget.tag_configure("h2", font=theme.FONT_H2, foreground=theme.ACCENT, spacing3=8, spacing1=10)
    text_widget.tag_configure("h3", font=theme.FONT_H3, foreground=theme.FG, spacing3=6, spacing1=6)
    text_widget.tag_configure("code_block", font=theme.FONT_CODE_SMALL, background=theme.BG_INSET,
                              foreground="#d6e4ff", lmargin1=20, lmargin2=20, rmargin=20,
                              spacing1=4, spacing3=4)
    text_widget.tag_configure("inline_code", font=theme.FONT_CODE_SMALL, background=theme.BG_INSET,
                              foreground="#fbbf24")
    text_widget.tag_configure("bold", font=theme.FONT_BODY_BOLD)
    text_widget.tag_configure("italic", font=("Segoe UI", 11, "italic"))
    text_widget.tag_configure("bullet", lmargin1=20, lmargin2=40)
    text_widget.tag_configure("body", font=theme.FONT_BODY, spacing3=4)
    text_widget.tag_configure("table", font=theme.FONT_CODE_SMALL, foreground="#cbd5e1")

    lines = markdown.splitlines()
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            text_widget.insert("end", "\n")
            continue
        if in_code:
            text_widget.insert("end", line + "\n", "code_block")
            continue

        # tables (rough): treat any line starting with | as table-styled
        if line.strip().startswith("|"):
            text_widget.insert("end", line + "\n", "table")
            continue

        # headers
        if line.startswith("### "):
            text_widget.insert("end", line[4:] + "\n", "h3"); continue
        if line.startswith("## "):
            text_widget.insert("end", line[3:] + "\n", "h2"); continue
        if line.startswith("# "):
            text_widget.insert("end", line[2:] + "\n", "h1"); continue

        # bullets
        if line.lstrip().startswith("- "):
            indent = len(line) - len(line.lstrip())
            inner = line.lstrip()[2:]
            text_widget.insert("end", "  " * (indent // 2) + "•  ", "bullet")
            _insert_inline(text_widget, inner, base_tag="bullet")
            text_widget.insert("end", "\n")
            continue

        # plain paragraph (with inline tokens)
        _insert_inline(text_widget, line, base_tag="body")
        text_widget.insert("end", "\n", "body")

    text_widget.configure(state="disabled")


_INLINE_RE = re.compile(
    r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)"
)


def _insert_inline(widget: tk.Text, line: str, base_tag: str) -> None:
    pos = 0
    for m in _INLINE_RE.finditer(line):
        if m.start() > pos:
            widget.insert("end", line[pos:m.start()], base_tag)
        token = m.group(0)
        if token.startswith("`"):
            widget.insert("end", token[1:-1], "inline_code")
        elif token.startswith("**"):
            widget.insert("end", token[2:-2], ("bold", base_tag))
        else:
            widget.insert("end", token[1:-1], ("italic", base_tag))
        pos = m.end()
    if pos < len(line):
        widget.insert("end", line[pos:], base_tag)


class CodeEditor(ttk.Frame):
    """Code editor with line numbers and tab-to-4-spaces."""

    def __init__(self, parent: tk.Misc, *, height: int = 14, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.line_numbers = tk.Text(
            self, width=4, padx=6, takefocus=0, border=0,
            background=theme.BG_INSET, foreground=theme.FG_MUTED,
            font=theme.FONT_CODE, highlightthickness=0,
            state="disabled",
        )
        self.line_numbers.grid(row=0, column=0, sticky="nsew")

        self.text = tk.Text(
            self, height=height, undo=True, wrap="none",
            background=theme.BG_INSET, foreground=theme.FG, insertbackground=theme.FG,
            font=theme.FONT_CODE, border=0, highlightthickness=1,
            highlightbackground=theme.GRID, highlightcolor=theme.ACCENT_DIM,
            tabs=("1c",),
        )
        self.text.grid(row=0, column=1, sticky="nsew")

        scroll = ttk.Scrollbar(self, command=self._on_scroll)
        scroll.grid(row=0, column=2, sticky="ns")
        self.text.configure(yscrollcommand=scroll.set)
        self.line_numbers.configure(yscrollcommand=scroll.set)
        self._scroll = scroll

        self.text.bind("<Tab>", self._tab_indent)
        self.text.bind("<KeyRelease>", lambda e: self._refresh_line_numbers())
        self.text.bind("<MouseWheel>", lambda e: self.after(1, self._refresh_line_numbers))
        self.text.bind("<Button-4>", lambda e: self.after(1, self._refresh_line_numbers))
        self.text.bind("<Button-5>", lambda e: self.after(1, self._refresh_line_numbers))

    def _on_scroll(self, *args) -> None:
        self.text.yview(*args)
        self.line_numbers.yview(*args)

    def _tab_indent(self, _event) -> str:
        self.text.insert("insert", "    ")
        return "break"

    def _refresh_line_numbers(self) -> None:
        try:
            self.line_numbers.configure(state="normal")
            self.line_numbers.delete("1.0", "end")
            count = int(self.text.index("end-1c").split(".")[0])
            self.line_numbers.insert("1.0", "\n".join(str(i) for i in range(1, count + 1)))
            self.line_numbers.configure(state="disabled")
        except (tk.TclError, ValueError):
            pass

    # public API ---------------------------------------------------------
    def get_code(self) -> str:
        return self.text.get("1.0", "end-1c")

    def set_code(self, code: str) -> None:
        self.text.delete("1.0", "end")
        self.text.insert("1.0", code)
        self._refresh_line_numbers()


class Toast:
    """Tiny achievement / XP popup overlay (auto-dismiss)."""

    def __init__(self, parent: tk.Misc):
        self.parent = parent
        self._win: tk.Toplevel | None = None

    def show(self, title: str, message: str, color: str = theme.GOLD, duration_ms: int = 3500) -> None:
        if self._win is not None:
            try:
                self._win.destroy()
            except tk.TclError:
                pass
        win = tk.Toplevel(self.parent)
        win.overrideredirect(True)
        win.configure(bg=theme.BG_PANEL)
        win.attributes("-topmost", True)
        try:
            win.attributes("-alpha", 0.95)
        except tk.TclError:
            pass

        frame = tk.Frame(win, bg=theme.BG_PANEL,
                         highlightbackground=color, highlightthickness=2, padx=14, pady=10)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text=title, bg=theme.BG_PANEL, fg=color, font=theme.FONT_H3).pack(anchor="w")
        tk.Label(frame, text=message, bg=theme.BG_PANEL, fg=theme.FG,
                 font=theme.FONT_BODY, wraplength=320, justify="left").pack(anchor="w", pady=(4, 0))

        # position: bottom-right of parent
        self.parent.update_idletasks()
        try:
            px = self.parent.winfo_rootx()
            py = self.parent.winfo_rooty()
            pw = self.parent.winfo_width()
            ph = self.parent.winfo_height()
            win.update_idletasks()
            ww = win.winfo_width()
            wh = win.winfo_height()
            x = px + pw - ww - 30
            y = py + ph - wh - 30
            win.geometry(f"+{x}+{y}")
        except tk.TclError:
            pass

        self._win = win
        win.after(duration_ms, lambda: self._dismiss(win))

    def _dismiss(self, win: tk.Toplevel) -> None:
        try:
            win.destroy()
        except tk.TclError:
            pass
        if self._win is win:
            self._win = None
