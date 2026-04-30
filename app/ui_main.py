"""Main window: sidebar nav + content area + dashboard."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from . import theme, progress as progress_mod, achievements as ach
from .curriculum import ALL_MODULES, get_module
from .curriculum.modules import total_xp_available
from .ui_widgets import Toast


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mission: Python")
        self.geometry("1280x820")
        self.minsize(1024, 720)
        self.configure(bg=theme.BG)

        self.progress = progress_mod.load()
        self.progress.touch_streak()
        progress_mod.save(self.progress)
        self.toast = Toast(self)

        self._configure_styles()
        self._build_layout()
        self._build_sidebar()
        self.show_dashboard()

        # check for any achievements that should already be unlocked
        self.check_achievements()

    # ------------------------------------------------------------------
    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(".", background=theme.BG, foreground=theme.FG, fieldbackground=theme.BG_INSET)
        style.configure("TFrame", background=theme.BG)
        style.configure("Sidebar.TFrame", background=theme.BG_PANEL)
        style.configure("Content.TFrame", background=theme.BG)
        style.configure("Card.TFrame", background=theme.BG_PANEL)
        style.configure("TLabel", background=theme.BG, foreground=theme.FG, font=theme.FONT_BODY)
        style.configure("Sidebar.TLabel", background=theme.BG_PANEL, foreground=theme.FG, font=theme.FONT_BODY)
        style.configure("SidebarMuted.TLabel", background=theme.BG_PANEL, foreground=theme.FG_MUTED, font=theme.FONT_SMALL)
        style.configure("H1.TLabel", background=theme.BG, foreground=theme.ACCENT, font=theme.FONT_H1)
        style.configure("H2.TLabel", background=theme.BG, foreground=theme.FG, font=theme.FONT_H2)
        style.configure("H3.TLabel", background=theme.BG, foreground=theme.FG, font=theme.FONT_H3)
        style.configure("Card.TLabel", background=theme.BG_PANEL, foreground=theme.FG, font=theme.FONT_BODY)
        style.configure("CardH.TLabel", background=theme.BG_PANEL, foreground=theme.ACCENT, font=theme.FONT_H3)
        style.configure("Muted.TLabel", background=theme.BG, foreground=theme.FG_MUTED, font=theme.FONT_SMALL)
        style.configure("Gold.TLabel", background=theme.BG_PANEL, foreground=theme.GOLD, font=theme.FONT_H3)
        style.configure("Success.TLabel", background=theme.BG, foreground=theme.SUCCESS, font=theme.FONT_BODY_BOLD)

        style.configure("TButton", background=theme.ACCENT_DIM, foreground=theme.FG, font=theme.FONT_BODY,
                        padding=(12, 6), borderwidth=0)
        style.map("TButton",
                  background=[("active", theme.ACCENT)],
                  foreground=[("active", "white")])
        style.configure("Primary.TButton", background=theme.ACCENT, foreground="white",
                        font=theme.FONT_BODY_BOLD, padding=(14, 8))
        style.map("Primary.TButton", background=[("active", "#7ec9ff")])

        style.configure("Nav.TButton", background=theme.BG_PANEL, foreground=theme.FG,
                        font=theme.FONT_BODY, anchor="w", padding=(12, 8), borderwidth=0)
        style.map("Nav.TButton",
                  background=[("active", "#1a2440"), ("selected", theme.ACCENT_DIM)])
        style.configure("NavActive.TButton", background=theme.ACCENT_DIM, foreground="white",
                        font=theme.FONT_BODY_BOLD, anchor="w", padding=(12, 8), borderwidth=0)

        style.configure("Horizontal.TProgressbar", troughcolor=theme.BG_INSET,
                        background=theme.PURPLE, bordercolor=theme.BG_INSET, lightcolor=theme.PURPLE,
                        darkcolor=theme.PURPLE)

        style.configure("Treeview", background=theme.BG_INSET, fieldbackground=theme.BG_INSET,
                        foreground=theme.FG, font=theme.FONT_BODY, rowheight=26, borderwidth=0)
        style.configure("Treeview.Heading", background=theme.BG_PANEL, foreground=theme.ACCENT,
                        font=theme.FONT_H3)
        style.map("Treeview", background=[("selected", theme.ACCENT_DIM)])

    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = ttk.Frame(self, style="Content.TFrame")
        self.content.pack(side="right", fill="both", expand=True)

    def _build_sidebar(self) -> None:
        # header
        header = tk.Frame(self.sidebar, bg=theme.BG_PANEL)
        header.pack(fill="x", pady=(16, 6), padx=14)
        tk.Label(header, text="MISSION:", bg=theme.BG_PANEL, fg=theme.FG_MUTED,
                 font=theme.FONT_SMALL).pack(anchor="w")
        tk.Label(header, text="PYTHON", bg=theme.BG_PANEL, fg=theme.ACCENT,
                 font=theme.FONT_H1).pack(anchor="w")

        # XP / level card
        self.xp_card = tk.Frame(self.sidebar, bg=theme.BG_PANEL, padx=14, pady=10)
        self.xp_card.pack(fill="x")
        self.level_label = tk.Label(self.xp_card, bg=theme.BG_PANEL, fg=theme.FG, font=theme.FONT_H3,
                                    anchor="w", justify="left")
        self.level_label.pack(anchor="w", fill="x")
        self.xp_label = tk.Label(self.xp_card, bg=theme.BG_PANEL, fg=theme.FG_MUTED,
                                 font=theme.FONT_SMALL, anchor="w")
        self.xp_label.pack(anchor="w", fill="x")
        self.xp_bar = ttk.Progressbar(self.xp_card, mode="determinate", length=220)
        self.xp_bar.pack(fill="x", pady=(4, 0))
        self.streak_label = tk.Label(self.xp_card, bg=theme.BG_PANEL, fg=theme.GOLD,
                                     font=theme.FONT_SMALL, anchor="w")
        self.streak_label.pack(anchor="w", fill="x", pady=(4, 0))

        # nav buttons
        nav = tk.Frame(self.sidebar, bg=theme.BG_PANEL)
        nav.pack(fill="both", expand=True, pady=10)

        self._nav_buttons: dict[str, ttk.Button] = {}
        self._add_nav(nav, "dashboard", "  Mission Control", self.show_dashboard)

        tk.Label(nav, text="CURRICULUM", bg=theme.BG_PANEL, fg=theme.FG_MUTED,
                 font=theme.FONT_SMALL).pack(anchor="w", padx=14, pady=(14, 2))

        last_phase = None
        for m in ALL_MODULES:
            if m.phase != last_phase:
                tk.Label(nav, text=f"  · {m.phase}", bg=theme.BG_PANEL, fg=theme.FG_MUTED,
                         font=theme.FONT_SMALL).pack(anchor="w", padx=14, pady=(8, 0))
                last_phase = m.phase
            short = m.title.replace("Module ", "M").split(" — ")
            label = f"  {short[0]}  {short[1] if len(short) > 1 else ''}"
            self._add_nav(nav, f"module:{m.id}", label, lambda mid=m.id: self.show_module(mid))

        bottom = tk.Frame(self.sidebar, bg=theme.BG_PANEL)
        bottom.pack(fill="x", side="bottom", pady=10)
        self._add_nav(bottom, "achievements", "  Mission Patches", self.show_achievements)
        self._add_nav(bottom, "settings", "  Settings", self.show_settings)

        self.refresh_progress_card()

    def _add_nav(self, parent: tk.Misc, key: str, label: str, command) -> None:
        btn = ttk.Button(parent, text=label, style="Nav.TButton", command=command)
        btn.pack(fill="x", padx=8, pady=1)
        self._nav_buttons[key] = btn

    def _set_active_nav(self, key: str) -> None:
        for k, btn in self._nav_buttons.items():
            btn.configure(style="NavActive.TButton" if k == key else "Nav.TButton")

    # ------------------------------------------------------------------
    def refresh_progress_card(self) -> None:
        idx, title, badge, into, span = theme.level_for_xp(self.progress.xp)
        self.level_label.configure(text=f"{badge}  {title}")
        if span is None:
            self.xp_label.configure(text=f"{self.progress.xp} XP — max level")
            self.xp_bar.configure(value=100)
        else:
            self.xp_label.configure(text=f"{self.progress.xp} XP   ({into}/{span} to next)")
            try:
                self.xp_bar.configure(value=int(into / span * 100))
            except ZeroDivisionError:
                self.xp_bar.configure(value=0)
        days = self.progress.streak_days
        self.streak_label.configure(text=f"Streak: {days} day{'s' if days != 1 else ''}")

    # ------------------------------------------------------------------
    def _clear_content(self) -> None:
        for w in self.content.winfo_children():
            w.destroy()

    def show_dashboard(self) -> None:
        from .ui_dashboard import build_dashboard
        self._clear_content()
        self._set_active_nav("dashboard")
        build_dashboard(self.content, self)

    def show_module(self, module_id: str) -> None:
        from .ui_lesson import build_module_view
        m = get_module(module_id)
        if m is None:
            return
        self._clear_content()
        self._set_active_nav(f"module:{module_id}")
        build_module_view(self.content, self, m)

    def show_lesson(self, lesson_id: str, module_id: str) -> None:
        from .ui_lesson import build_lesson_view
        self._clear_content()
        self._set_active_nav(f"module:{module_id}")
        build_lesson_view(self.content, self, lesson_id, module_id)

    def show_project(self, project_id: str, module_id: str = "m_capstones") -> None:
        from .ui_lesson import build_project_view
        self._clear_content()
        self._set_active_nav(f"module:{module_id}")
        build_project_view(self.content, self, project_id, module_id)

    def show_achievements(self) -> None:
        from .ui_panels import build_achievements
        self._clear_content()
        self._set_active_nav("achievements")
        build_achievements(self.content, self)

    def show_settings(self) -> None:
        from .ui_panels import build_settings
        self._clear_content()
        self._set_active_nav("settings")
        build_settings(self.content, self)

    # ------------------------------------------------------------------
    def award_xp(self, amount: int, label: str = "") -> None:
        if amount <= 0:
            return
        self.progress.add_xp(amount)
        self.toast.show("+%d XP" % amount, label or "Nice work, cadet.", color=theme.PURPLE)
        progress_mod.save(self.progress)
        self.refresh_progress_card()

    def check_achievements(self) -> None:
        unlocked = ach.check_unlocks(self.progress)
        if unlocked:
            progress_mod.save(self.progress)
            self.refresh_progress_card()
            for a in unlocked:
                self.toast.show(
                    f"Patch unlocked: {a.title}",
                    f"{a.description}  (+{a.xp_bonus} XP)",
                    color=theme.GOLD,
                    duration_ms=4500,
                )

    @property
    def total_xp_available(self) -> int:
        return total_xp_available()
