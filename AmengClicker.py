from __future__ import annotations

import json
import os
import sys
import threading
import time
from pathlib import Path
from tkinter import messagebox
import tkinter as tk

import customtkinter as ctk
from pynput import keyboard, mouse

APP_NAME = "阿孟萬能連點器 2.0"
VERSION = "2.0.0"

# Every pair is (light appearance, dark appearance); all values are neutral gray.
COLORS = {
    "window": ("#FFFFFF", "#000000"),
    "card": ("#F7F7F7", "#141414"),
    "panel": ("#EFEFEF", "#222222"),
    "input": ("#FFFFFF", "#090909"),
    "border": ("#D0D0D0", "#484848"),
    "text": ("#111111", "#F4F4F4"),
    "muted": ("#666666", "#A8A8A8"),
    "button": ("#000000", "#F4F4F4"),
    "button_text": ("#FFFFFF", "#000000"),
    "button_hover": ("#303030", "#D8D8D8"),
    "segment_bg": ("#E7E7E7", "#242424"),
    "segment_selected": ("#CFCFCF", "#4A4A4A"),
    "segment_hover": ("#D6D6D6", "#383838"),
    "radio": ("#111111", "#EEEEEE"),
    "radio_hover": ("#555555", "#BBBBBB"),
}

TEXT = {
    "zh-TW": {
        "title": APP_NAME,
        "subtitle": "簡單、俐落，專注於操作",
        "mode_mouse": "滑鼠",
        "mode_keyboard": "鍵盤",
        "target": "連點目標",
        "left": "左鍵",
        "right": "右鍵",
        "middle": "中鍵",
        "keyboard_target": "鍵盤按鍵",
        "capture_key": "按一下此處，再按要連點的按鍵",
        "press_key": "請按一個按鍵…（Esc 取消）",
        "interval": "點擊間隔",
        "seconds": "秒",
        "count": "次數上限",
        "unlimited": "0 代表不限",
        "start": "開始連點",
        "stop": "停止連點",
        "stopping": "正在停止…",
        "ready": "準備就緒",
        "running": "連點中",
        "completed": "已完成",
        "settings": "設定",
        "settings_title": "設定",
        "tab_customize": "自訂",
        "tab_theme": "外觀",
        "tab_shortcuts": "快捷鍵",
        "click_type": "點擊方式",
        "single": "單擊",
        "double": "雙擊",
        "double_gap": "雙擊間隔（毫秒）",
        "mouse_button": "滑鼠按鍵",
        "appearance": "應用程式外觀",
        "system": "跟隨系統",
        "dark": "深色",
        "light": "淺色",
        "language": "語言",
        "zh": "繁體中文",
        "en": "English",
        "hotkey_toggle": "開始／暫停",
        "hotkey_stop": "立即停止",
        "capture": "設定按鍵",
        "save": "儲存設定",
        "cancel": "取消",
        "appearance_hint": "淺色為白底黑字；深色為黑底白字，介面只使用黑白灰。",
        "shortcut_hint": "按「設定按鍵」後按下想使用的按鍵；按 Esc 可取消。",
        "hotkey_conflict": "開始／暫停、立即停止及連點目標不可使用相同按鍵。",
        "invalid_interval": "請輸入大於 0 的間隔秒數（最多 3600 秒）。",
        "invalid_count": "次數上限請輸入 0 或正整數。",
        "invalid_gap": "雙擊間隔請輸入 0 到 2000 毫秒。",
        "stop_before_settings": "請先停止連點，再開啟設定。",
        "input_error": "輸入有誤",
        "input_error_title": "連點器錯誤",
        "listener_error": "全域鍵盤監聽無法啟動：",
        "rate": "估算速度",
        "per_second": "次／秒",
        "shortcut_line": "快捷鍵：",
        "footer": "可用全域快捷鍵操作；F6 開始／暫停 · F7 立即停止",
    },
    "en": {
        "title": "Ameng Auto Clicker 2.0",
        "subtitle": "Clean, precise, ready when you are",
        "mode_mouse": "Mouse",
        "mode_keyboard": "Keyboard",
        "target": "Click target",
        "left": "Left",
        "right": "Right",
        "middle": "Middle",
        "keyboard_target": "Keyboard key",
        "capture_key": "Click here, then press a key",
        "press_key": "Press a key… (Esc to cancel)",
        "interval": "Click interval",
        "seconds": "sec",
        "count": "Click limit",
        "unlimited": "0 = unlimited",
        "start": "Start clicking",
        "stop": "Stop clicking",
        "stopping": "Stopping…",
        "ready": "Ready",
        "running": "Clicking",
        "completed": "Completed",
        "settings": "Settings",
        "settings_title": "Settings",
        "tab_customize": "Customize",
        "tab_theme": "Appearance",
        "tab_shortcuts": "Shortcuts",
        "click_type": "Click type",
        "single": "Single",
        "double": "Double",
        "double_gap": "Double-click gap (ms)",
        "mouse_button": "Mouse button",
        "appearance": "App appearance",
        "system": "System",
        "dark": "Dark",
        "light": "Light",
        "language": "Language",
        "zh": "繁體中文",
        "en": "English",
        "hotkey_toggle": "Start / Pause",
        "hotkey_stop": "Stop now",
        "capture": "Set key",
        "save": "Save settings",
        "cancel": "Cancel",
        "appearance_hint": "Light uses white and black; dark uses black and white. The UI is grayscale only.",
        "shortcut_hint": "Click Set key, then press a key. Press Esc to cancel.",
        "hotkey_conflict": "Start/Pause, Stop, and the click target must use different keys.",
        "invalid_interval": "Enter an interval greater than 0 and no more than 3600 seconds.",
        "invalid_count": "Click limit must be 0 or a positive whole number.",
        "invalid_gap": "Double-click gap must be from 0 to 2000 milliseconds.",
        "stop_before_settings": "Stop clicking before opening Settings.",
        "input_error": "Invalid input",
        "input_error_title": "Auto Clicker error",
        "listener_error": "Could not start the global keyboard listener: ",
        "rate": "Estimated rate",
        "per_second": "clicks/sec",
        "shortcut_line": "Hotkeys: ",
        "footer": "Global hotkeys · F6 Start/Pause · F7 Stop now",
    },
}

DEFAULTS = {
    "mode": "Mouse",
    "mouse_button": "left",
    "target_key": "a",
    "interval": 0.1,
    "click_limit": 0,
    "click_type": "single",
    "double_gap_ms": 60,
    "theme": "system",
    "language": "zh-TW",
    "hotkey_toggle": "f6",
    "hotkey_stop": "f7",
}


def resource_path(name: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


def apply_app_icon(window, icon_path: str | None = None) -> None:
    """Apply the genuine ICO to both CTk windows; harmless if a platform rejects it."""
    path = icon_path or resource_path("67.ico")
    try:
        if os.path.isfile(path):
            window.iconbitmap(path)
    except Exception:
        pass


def appearance_value(theme: str) -> str:
    return {"system": "System", "dark": "Dark", "light": "Light"}.get(theme, "System")


def key_name(key) -> str:
    char = getattr(key, "char", None)
    if isinstance(char, str) and len(char) == 1 and char.isprintable():
        return char.lower()
    name = getattr(key, "name", None)
    if name:
        return str(name).lower()
    vk = getattr(key, "vk", None)
    if vk is not None:
        return f"vk:{int(vk)}"
    return ""


def key_from_name(name: str):
    value = str(name or "").strip().lower()
    if not value:
        return None
    if value.startswith("vk:"):
        try:
            return keyboard.KeyCode.from_vk(int(value.split(":", 1)[1]))
        except (TypeError, ValueError):
            return None
    if len(value) == 1:
        try:
            return keyboard.KeyCode.from_char(value)
        except (TypeError, ValueError):
            return None
    return getattr(keyboard.Key, value, None)


def display_key(name: str) -> str:
    value = str(name or "").strip()
    if value.lower().startswith("vk:"):
        return f"VK {value.split(':', 1)[1]}"
    return value.upper() if len(value) == 1 or value.lower().startswith("f") else value.replace("_", " ").title()


def style_button(parent, text, command, *, width=120, height=38, primary=False, font=None):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=height,
        corner_radius=12,
        border_width=0,
        fg_color=COLORS["button"] if primary else COLORS["panel"],
        hover_color=COLORS["button_hover"] if primary else COLORS["segment_hover"],
        text_color=COLORS["button_text"] if primary else COLORS["text"],
        font=font or ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
    )


def style_frame(parent, *, card=False, **kwargs):
    return ctk.CTkFrame(
        parent,
        corner_radius=18 if card else 12,
        border_width=1 if card else 0,
        border_color=COLORS["border"],
        fg_color=COLORS["card"] if card else COLORS["panel"],
        **kwargs,
    )


class AutoClickerApp:
    """Main window, settings state, pynput input and click worker."""

    def __init__(self, start_listener: bool = True):
        theme_file = resource_path("monochrome.json")
        ctk.set_default_color_theme(theme_file)
        self.settings = dict(DEFAULTS)
        self.config_path = os.path.join(
            os.environ.get("APPDATA", os.path.expanduser("~")),
            "AmengClicker2",
            "settings.json",
        )
        self._load_config()
        ctk.set_appearance_mode(appearance_value(self.settings["theme"]))

        self.root = ctk.CTk()
        self.root.title(APP_NAME)
        self.root.geometry("520x560")
        self.root.resizable(False, False)
        self.root.configure(fg_color=COLORS["window"])
        apply_app_icon(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self._stop_event = threading.Event()
        self._key_lock = threading.Lock()
        self._pressed_keys: set[str] = set()
        self._capture_callback = None
        self._injecting = threading.Event()
        self._click_thread: threading.Thread | None = None
        self._listener = None
        self._closing = False
        self.is_running = False
        self.click_count = 0
        self.click_limit = 0
        self.settings_window: SettingsWindow | None = None
        self._build_ui()
        self.update_language()
        self._update_status()

        if start_listener:
            self._start_global_listener()

    def t(self, key: str) -> str:
        lang = self.settings.get("language", "zh-TW")
        return TEXT.get(lang, TEXT["zh-TW"]).get(key, key)

    def _load_config(self) -> None:
        try:
            with open(self.config_path, "r", encoding="utf-8") as stream:
                saved = json.load(stream)
            if isinstance(saved, dict):
                self.settings.update({k: v for k, v in saved.items() if k in DEFAULTS})
        except (OSError, json.JSONDecodeError, TypeError):
            pass
        if self.settings.get("mode") not in ("Mouse", "Keyboard"):
            self.settings["mode"] = DEFAULTS["mode"]
        if self.settings.get("mouse_button") not in ("left", "right", "middle"):
            self.settings["mouse_button"] = DEFAULTS["mouse_button"]
        if self.settings.get("click_type") not in ("single", "double"):
            self.settings["click_type"] = DEFAULTS["click_type"]
        if self.settings.get("theme") not in ("system", "dark", "light"):
            self.settings["theme"] = DEFAULTS["theme"]
        if self.settings.get("language") not in TEXT:
            self.settings["language"] = DEFAULTS["language"]
        for name in ("hotkey_toggle", "hotkey_stop", "target_key"):
            if not key_from_name(str(self.settings.get(name, ""))):
                self.settings[name] = DEFAULTS[name]
        if len({self.settings["hotkey_toggle"], self.settings["hotkey_stop"], self.settings["target_key"]}) < 3:
            for name in ("hotkey_toggle", "hotkey_stop", "target_key"):
                self.settings[name] = DEFAULTS[name]
        try:
            self.settings["interval"] = min(3600.0, max(0.001, float(self.settings["interval"])))
        except (ValueError, TypeError):
            self.settings["interval"] = DEFAULTS["interval"]
        try:
            self.settings["click_limit"] = max(0, int(self.settings["click_limit"]))
        except (ValueError, TypeError):
            self.settings["click_limit"] = DEFAULTS["click_limit"]
        try:
            self.settings["double_gap_ms"] = min(2000, max(0, int(self.settings["double_gap_ms"])))
        except (ValueError, TypeError):
            self.settings["double_gap_ms"] = DEFAULTS["double_gap_ms"]

    def save_config(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as stream:
                json.dump(self.settings, stream, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def _build_ui(self) -> None:
        outer = ctk.CTkFrame(self.root, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=22, pady=(20, 16))

        header = ctk.CTkFrame(outer, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))
        self.title_label = ctk.CTkLabel(
            header, text=self.t("title"), text_color=COLORS["text"],
            font=ctk.CTkFont(family="Segoe UI", size=23, weight="bold"), anchor="w",
        )
        self.title_label.pack(anchor="w")
        self.subtitle_label = ctk.CTkLabel(
            header, text=self.t("subtitle"), text_color=COLORS["muted"],
            font=ctk.CTkFont(family="Segoe UI", size=12), anchor="w",
        )
        self.subtitle_label.pack(anchor="w", pady=(2, 0))

        self.mode_widget = ctk.CTkSegmentedButton(
            outer,
            values=[self.t("mode_mouse"), self.t("mode_keyboard")],
            command=self._on_mode_changed,
            height=42,
            corner_radius=14,
            border_width=3,
            fg_color=COLORS["segment_bg"],
            selected_color=COLORS["segment_selected"],
            selected_hover_color=COLORS["segment_hover"],
            unselected_color=COLORS["segment_bg"],
            unselected_hover_color=COLORS["segment_hover"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        )
        self.mode_widget.pack(fill="x", pady=(0, 14))

        target_card = style_frame(outer, card=True)
        target_card.pack(fill="x", pady=(0, 12))
        self.target_label = ctk.CTkLabel(
            target_card, text=self.t("target"), text_color=COLORS["muted"],
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), anchor="w",
        )
        self.target_label.pack(fill="x", padx=16, pady=(12, 8))
        self.mouse_target_widget = ctk.CTkSegmentedButton(
            target_card,
            values=[self.t("left"), self.t("right"), self.t("middle")],
            command=self._on_mouse_target,
            height=42,
            corner_radius=12,
            border_width=3,
            fg_color=COLORS["segment_bg"],
            selected_color=COLORS["segment_selected"],
            selected_hover_color=COLORS["segment_hover"],
            unselected_color=COLORS["segment_bg"],
            unselected_hover_color=COLORS["segment_hover"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        )
        self.mouse_target_widget.pack(fill="x", padx=12, pady=(0, 12))
        self.keyboard_target_widget = style_button(
            target_card, self.t("capture_key"), self.capture_keyboard_target,
            width=430, height=42,
        )
        self.keyboard_target_widget.pack(fill="x", padx=12, pady=(0, 12))

        values = style_frame(outer, card=True)
        values.pack(fill="x", pady=(0, 14))
        row = ctk.CTkFrame(values, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(12, 5))
        self.interval_label = ctk.CTkLabel(row, text=self.t("interval"), text_color=COLORS["muted"], anchor="w", font=ctk.CTkFont(size=12, weight="bold"))
        self.interval_label.grid(row=0, column=0, sticky="w")
        self.count_label = ctk.CTkLabel(row, text=self.t("count"), text_color=COLORS["muted"], anchor="w", font=ctk.CTkFont(size=12, weight="bold"))
        self.count_label.grid(row=0, column=1, sticky="w", padx=(18, 0))
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)

        entry_row = ctk.CTkFrame(values, fg_color="transparent")
        entry_row.pack(fill="x", padx=15, pady=(0, 13))
        self.interval_var = tk.StringVar(value=f"{self.settings['interval']:g}")
        self.limit_var = tk.StringVar(value=str(self.settings["click_limit"]))
        entry_style = dict(
            height=42, corner_radius=10, border_width=1,
            fg_color=COLORS["input"], border_color=COLORS["border"],
            text_color=COLORS["text"], placeholder_text_color=COLORS["muted"],
            font=ctk.CTkFont(family="Segoe UI", size=15),
        )
        self.interval_entry = ctk.CTkEntry(entry_row, textvariable=self.interval_var, **entry_style)
        self.interval_entry.grid(row=0, column=0, sticky="ew")
        self.seconds_label = ctk.CTkLabel(entry_row, text=self.t("seconds"), text_color=COLORS["muted"], width=38)
        self.seconds_label.grid(row=0, column=1, padx=(5, 3))
        self.limit_entry = ctk.CTkEntry(entry_row, textvariable=self.limit_var, **entry_style)
        self.limit_entry.grid(row=0, column=2, sticky="ew", padx=(12, 0))
        self.unlimited_label = ctk.CTkLabel(entry_row, text=self.t("unlimited"), text_color=COLORS["muted"], width=75, font=ctk.CTkFont(size=11))
        self.unlimited_label.grid(row=0, column=3, padx=(5, 0))
        entry_row.grid_columnconfigure(0, weight=1)
        entry_row.grid_columnconfigure(2, weight=1)
        self.rate_label = ctk.CTkLabel(values, text="", text_color=COLORS["muted"], anchor="w", font=ctk.CTkFont(size=11))
        self.rate_label.pack(fill="x", padx=16, pady=(0, 11))

        self.start_button = style_button(outer, self.t("start"), self.toggle_clicking, width=470, height=56, primary=True, font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"))
        self.start_button.pack(fill="x", pady=(1, 10))

        bottom = ctk.CTkFrame(outer, fg_color="transparent")
        bottom.pack(fill="x", side="bottom")
        self.status_dot = ctk.CTkLabel(bottom, text="●", text_color=COLORS["radio"], font=ctk.CTkFont(family="Segoe UI Symbol", size=14), width=18)
        self.status_dot.pack(side="left")
        self.status_label = ctk.CTkLabel(bottom, text=self.t("ready"), text_color=COLORS["muted"], anchor="w", font=ctk.CTkFont(size=12))
        self.status_label.pack(side="left", padx=(4, 0))
        self.hotkey_label = ctk.CTkLabel(bottom, text="", text_color=COLORS["muted"], font=ctk.CTkFont(size=11))
        self.hotkey_label.pack(side="left", padx=(18, 0))
        self.settings_button = ctk.CTkButton(
            bottom, text="⚙", command=self.open_settings, width=40, height=38,
            corner_radius=12, border_width=0, fg_color=COLORS["panel"],
            hover_color=COLORS["segment_hover"], text_color=COLORS["text"],
            font=ctk.CTkFont(family="Segoe UI Symbol", size=18),
        )
        self.settings_button.pack(side="right")
        self._sync_main_mode()
        self._update_rate()

    def update_language(self) -> None:
        if not hasattr(self, "title_label"):
            return
        self.root.title(self.t("title"))
        self.title_label.configure(text=self.t("title"))
        self.subtitle_label.configure(text=self.t("subtitle"))
        self.target_label.configure(text=self.t("target"))
        self.interval_label.configure(text=self.t("interval"))
        self.count_label.configure(text=self.t("count"))
        self.seconds_label.configure(text=self.t("seconds"))
        self.unlimited_label.configure(text=self.t("unlimited"))
        self.start_button.configure(text=self.t("stop") if self.is_running else self.t("start"))
        self.settings_button.configure(text="⚙", state="normal")
        self.mode_widget.configure(values=[self.t("mode_mouse"), self.t("mode_keyboard")])
        self.mouse_target_widget.configure(values=[self.t("left"), self.t("right"), self.t("middle")])
        self._sync_main_mode()
        self._update_rate()
        self._update_status()
        self.hotkey_label.configure(text=f"{display_key(self.settings['hotkey_toggle'])} · {display_key(self.settings['hotkey_stop'])}")

    def _sync_main_mode(self) -> None:
        if not hasattr(self, "mode_widget"):
            return
        if self.settings["mode"] == "Mouse":
            self.mode_widget.set(self.t("mode_mouse"))
            self.mouse_target_widget.pack(fill="x", padx=12, pady=(0, 12))
            self.keyboard_target_widget.pack_forget()
            self.mouse_target_widget.set(self._mouse_display(self.settings["mouse_button"]))
        else:
            self.mode_widget.set(self.t("mode_keyboard"))
            self.mouse_target_widget.pack_forget()
            self.keyboard_target_widget.pack(fill="x", padx=12, pady=(0, 12))
            target = display_key(self.settings.get("target_key", "a"))
            self.keyboard_target_widget.configure(text=f"{self.t('keyboard_target')}:  {target}  ·  {self.t('capture_key')}")

    def _mouse_display(self, button: str) -> str:
        key = {"left": "left", "right": "right", "middle": "middle"}.get(button, "left")
        return self.t(key)

    def _on_mode_changed(self, value: str) -> None:
        self.settings["mode"] = "Mouse" if value == self.t("mode_mouse") else "Keyboard"
        self.save_config()
        self._sync_main_mode()

    def _on_mouse_target(self, value: str) -> None:
        lookup = {self.t("left"): "left", self.t("right"): "right", self.t("middle"): "middle"}
        self.settings["mouse_button"] = lookup.get(value, "left")
        self.save_config()

    def _update_rate(self) -> None:
        try:
            interval = max(0.001, float(self.interval_var.get()))
        except (ValueError, TypeError):
            interval = float(self.settings["interval"])
        per_cycle = 2 if self.settings.get("click_type") == "double" else 1
        rate = per_cycle / interval
        self.rate_label.configure(text=f"{self.t('rate')}:  {rate:.1f} {self.t('per_second')}")

    def _validate_main_values(self) -> tuple[float, int] | None:
        try:
            interval = float(self.interval_var.get().strip())
            if not (0 < interval <= 3600):
                raise ValueError
        except (ValueError, TypeError):
            messagebox.showerror(self.t("input_error_title"), self.t("invalid_interval"), parent=self.root)
            return None
        try:
            limit = int(self.limit_var.get().strip())
            if limit < 0:
                raise ValueError
        except (ValueError, TypeError):
            messagebox.showerror(self.t("input_error_title"), self.t("invalid_count"), parent=self.root)
            return None
        self.settings["interval"] = interval
        self.settings["click_limit"] = limit
        self.save_config()
        self._update_rate()
        return interval, limit

    def _start_global_listener(self) -> None:
        try:
            self._listener = keyboard.Listener(on_press=self._on_global_press, on_release=self._on_global_release)
            self._listener.daemon = True
            self._listener.start()
        except Exception as exc:
            messagebox.showwarning(self.t("input_error_title"), self.t("listener_error") + str(exc), parent=self.root)

    def _on_global_press(self, key):
        if self._closing or self._injecting.is_set():
            return
        name = key_name(key)
        if not name:
            return
        with self._key_lock:
            if name in self._pressed_keys:
                return
            self._pressed_keys.add(name)
            callback = self._capture_callback
            if callback is not None:
                self._capture_callback = None
        if callback is not None:
            try:
                self.root.after(0, callback, None if name == "esc" else name)
            except RuntimeError:
                pass
            return
        if name == self.settings.get("hotkey_toggle"):
            try:
                self.root.after(0, self.toggle_clicking)
            except RuntimeError:
                pass
        elif name == self.settings.get("hotkey_stop"):
            try:
                self.root.after(0, self.stop_clicking)
            except RuntimeError:
                pass

    def _on_global_release(self, key):
        name = key_name(key)
        with self._key_lock:
            self._pressed_keys.discard(name)

    def begin_key_capture(self, callback) -> None:
        with self._key_lock:
            self._capture_callback = callback

    def cancel_key_capture(self) -> None:
        with self._key_lock:
            self._capture_callback = None

    def capture_keyboard_target(self) -> None:
        if self.is_running:
            messagebox.showinfo(self.t("settings"), self.t("stop_before_settings"), parent=self.root)
            return
        self.keyboard_target_widget.configure(text=self.t("press_key"))
        self.begin_key_capture(self._finish_main_key_capture)

    def _finish_main_key_capture(self, name: str | None) -> None:
        if name is None:
            self._sync_main_mode()
            return
        if name in (self.settings["hotkey_toggle"], self.settings["hotkey_stop"]):
            messagebox.showerror(self.t("input_error_title"), self.t("hotkey_conflict"), parent=self.root)
            self._sync_main_mode()
            return
        self.settings["target_key"] = name
        self.save_config()
        self._sync_main_mode()

    def toggle_clicking(self) -> None:
        if self.is_running:
            self.stop_clicking()
            return
        if self._click_thread and self._click_thread.is_alive():
            return
        values = self._validate_main_values()
        if values is None:
            return
        if self.settings["mode"] == "Keyboard":
            target = key_from_name(self.settings.get("target_key", ""))
            if target is None:
                messagebox.showerror(self.t("input_error_title"), self.t("capture_key"), parent=self.root)
                return
        self.click_count = 0
        self.click_limit = values[1]
        self._stop_event.clear()
        self.is_running = True
        self.start_button.configure(text=self.t("stop"))
        self._update_status()
        self._click_thread = threading.Thread(target=self._click_loop, args=(values[0],), daemon=True, name="AmengClickerWorker")
        self._click_thread.start()

    def stop_clicking(self) -> None:
        if not self.is_running:
            return
        self._stop_event.set()
        self.status_label.configure(text=self.t("stopping"))

    def _perform_action(self) -> None:
        if self.settings["mode"] == "Mouse":
            button = {"left": mouse.Button.left, "right": mouse.Button.right, "middle": mouse.Button.middle}[self.settings["mouse_button"]]
            mouse.Controller().click(button)
        else:
            target = key_from_name(self.settings.get("target_key", ""))
            if target is None:
                raise RuntimeError(self.t("capture_key"))
            controller = keyboard.Controller()
            self._injecting.set()
            try:
                controller.press(target)
                controller.release(target)
            finally:
                self._injecting.clear()

    def _click_loop(self, interval: float) -> None:
        error_text = None
        try:
            double = self.settings.get("click_type") == "double"
            gap = max(0, int(self.settings.get("double_gap_ms", 60))) / 1000.0
            while not self._stop_event.is_set():
                cycle_size = 2 if double else 1
                for index in range(cycle_size):
                    if self._stop_event.is_set() or (self.click_limit and self.click_count >= self.click_limit):
                        break
                    self._perform_action()
                    self.click_count += 1
                    try:
                        self.root.after(0, self._update_status)
                    except RuntimeError:
                        return
                    if index + 1 < cycle_size and not (self.click_limit and self.click_count >= self.click_limit):
                        if self._stop_event.wait(gap):
                            break
                if self.click_limit and self.click_count >= self.click_limit:
                    break
                if self._stop_event.wait(interval):
                    break
        except Exception as exc:
            error_text = str(exc)
        finally:
            self._stop_event.set()
            try:
                self.root.after(0, self._worker_finished, error_text)
            except RuntimeError:
                pass

    def _worker_finished(self, error_text: str | None = None) -> None:
        self.is_running = False
        self.start_button.configure(text=self.t("start"))
        self._update_status()
        if error_text and not self._closing:
            messagebox.showerror(self.t("input_error_title"), error_text, parent=self.root)

    def _update_status(self) -> None:
        if self._closing or not hasattr(self, "status_label"):
            return
        if self.is_running:
            label = self.t("running")
        elif self.click_limit > 0 and self.click_count >= self.click_limit and self.click_count > 0:
            label = self.t("completed")
        else:
            label = self.t("ready")
        if self.click_count:
            label += f"  ·  {self.click_count}"
        self.status_label.configure(text=label)
        self.status_dot.configure(text_color=COLORS["radio"] if self.is_running else COLORS["muted"])

    def open_settings(self) -> None:
        if self.is_running:
            messagebox.showinfo(self.t("settings"), self.t("stop_before_settings"), parent=self.root)
            return
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.focus()
            return
        self.settings_window = SettingsWindow(self)

    def apply_theme(self, theme: str | None = None) -> None:
        selected = theme or self.settings.get("theme", "system")
        ctk.set_appearance_mode(appearance_value(selected))

    def close(self) -> None:
        if self._closing:
            return
        self._closing = True
        self._stop_event.set()
        self.save_config()
        if self._listener is not None:
            try:
                self._listener.stop()
            except Exception:
                pass
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


class SettingsWindow(ctk.CTkToplevel):
    """Three-tab settings window, matching the 1.0 customtkinter structure."""

    def __init__(self, app: AutoClickerApp):
        super().__init__(app.root)
        self.app = app
        self.draft = dict(app.settings)
        self.saved = False
        self.title(app.t("settings_title"))
        self.geometry("500x570")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["window"])
        self.transient(app.root)
        apply_app_icon(self)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        header = ctk.CTkLabel(self, text=app.t("settings_title"), text_color=COLORS["text"], anchor="w", font=ctk.CTkFont(family="Segoe UI", size=21, weight="bold"))
        header.pack(fill="x", padx=22, pady=(20, 6))
        self.tabs = ctk.CTkTabview(
            self,
            width=456,
            height=430,
            corner_radius=16,
            border_width=1,
            bg_color="transparent",
            fg_color=COLORS["card"],
            border_color=COLORS["border"],
            segmented_button_fg_color=COLORS["segment_bg"],
            segmented_button_selected_color=COLORS["segment_selected"],
            segmented_button_selected_hover_color=COLORS["segment_hover"],
            segmented_button_unselected_color=COLORS["segment_bg"],
            segmented_button_unselected_hover_color=COLORS["segment_hover"],
            text_color=COLORS["text"],
            segmented_button_font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        )
        self.tabs.pack(fill="both", expand=True, padx=18, pady=(4, 8))
        self.custom_tab = self.tabs.add(app.t("tab_customize"))
        self.theme_tab = self.tabs.add(app.t("tab_theme"))
        self.shortcuts_tab = self.tabs.add(app.t("tab_shortcuts"))
        self._build_customize()
        self._build_theme()
        self._build_shortcuts()

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=22, pady=(0, 18))
        style_button(footer, app.t("cancel"), self.cancel, width=120).pack(side="right", padx=(8, 0))
        style_button(footer, app.t("save"), self.save, width=160, primary=True).pack(side="right")
        self.grab_set()

    def _label(self, parent, text, *, size=12, bold=False):
        return ctk.CTkLabel(parent, text=text, text_color=COLORS["text"], anchor="w", font=ctk.CTkFont(family="Segoe UI", size=size, weight="bold" if bold else "normal"))

    def _entry(self, parent, variable: tk.StringVar, width=180):
        return ctk.CTkEntry(
            parent, width=width, height=38, corner_radius=10, border_width=1,
            fg_color=COLORS["input"], border_color=COLORS["border"],
            text_color=COLORS["text"], placeholder_text_color=COLORS["muted"],
            textvariable=variable, font=ctk.CTkFont(size=13),
        )

    def _build_customize(self) -> None:
        tab = self.custom_tab
        self._label(tab, self.app.t("interval"), bold=True).pack(anchor="w", padx=14, pady=(14, 5))
        self.interval_var = tk.StringVar(value=f"{self.draft['interval']:g}")
        self.interval_entry = self._entry(tab, self.interval_var, width=320)
        self.interval_entry.pack(fill="x", padx=14)
        self._label(tab, self.app.t("seconds"), size=10).pack(anchor="w", padx=16, pady=(3, 10))

        self._label(tab, self.app.t("mouse_button"), bold=True).pack(anchor="w", padx=14, pady=(3, 5))
        self.mouse_var = tk.StringVar(value=self.draft["mouse_button"])
        self.mouse_radios = ctk.CTkFrame(tab, fg_color="transparent")
        self.mouse_radios.pack(fill="x", padx=12, pady=(0, 10))
        mouse_labels = [("left", self.app.t("left")), ("right", self.app.t("right")), ("middle", self.app.t("middle"))]
        for value, label in mouse_labels:
            ctk.CTkRadioButton(
                self.mouse_radios, text=label, value=value, variable=self.mouse_var,
                fg_color=COLORS["radio"], hover_color=COLORS["radio_hover"],
                border_color=COLORS["border"], text_color=COLORS["text"],
                font=ctk.CTkFont(size=12),
            ).pack(side="left", padx=(4, 18), pady=4)

        self._label(tab, self.app.t("click_type"), bold=True).pack(anchor="w", padx=14, pady=(3, 5))
        self.click_type_var = tk.StringVar(value=self.draft["click_type"])
        self.click_radios = ctk.CTkFrame(tab, fg_color="transparent")
        self.click_radios.pack(fill="x", padx=12, pady=(0, 8))
        for value, label in (("single", self.app.t("single")), ("double", self.app.t("double"))):
            ctk.CTkRadioButton(
                self.click_radios, text=label, value=value, variable=self.click_type_var,
                fg_color=COLORS["radio"], hover_color=COLORS["radio_hover"],
                border_color=COLORS["border"], text_color=COLORS["text"],
                font=ctk.CTkFont(size=12),
            ).pack(side="left", padx=(4, 22), pady=4)

        self._label(tab, self.app.t("double_gap"), bold=True).pack(anchor="w", padx=14, pady=(4, 5))
        self.double_gap_var = tk.StringVar(value=str(self.draft["double_gap_ms"]))
        self.double_gap_entry = self._entry(tab, self.double_gap_var, width=180)
        self.double_gap_entry.pack(anchor="w", padx=14)

    def _build_theme(self) -> None:
        tab = self.theme_tab
        self._label(tab, self.app.t("appearance"), bold=True).pack(anchor="w", padx=14, pady=(20, 10))
        self.theme_labels = {
            self.app.t("system"): "system",
            self.app.t("dark"): "dark",
            self.app.t("light"): "light",
        }
        current_label = next((label for label, value in self.theme_labels.items() if value == self.draft["theme"]), self.app.t("system"))
        self.theme_var = tk.StringVar(value=current_label)
        self.theme_segment = ctk.CTkSegmentedButton(
            tab,
            values=list(self.theme_labels),
            variable=self.theme_var,
            command=self._preview_theme,
            height=38,
            corner_radius=11,
            border_width=2,
            fg_color=COLORS["segment_bg"],
            selected_color=COLORS["segment_selected"],
            selected_hover_color=COLORS["segment_hover"],
            unselected_color=COLORS["segment_bg"],
            unselected_hover_color=COLORS["segment_hover"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.theme_segment.pack(fill="x", padx=14)
        ctk.CTkLabel(tab, text=self.app.t("appearance_hint"), text_color=COLORS["muted"], wraplength=390, justify="left", anchor="w", font=ctk.CTkFont(size=11)).pack(fill="x", padx=16, pady=(10, 24))

        self._label(tab, self.app.t("language"), bold=True).pack(anchor="w", padx=14, pady=(6, 10))
        self.language_labels = {self.app.t("zh"): "zh-TW", self.app.t("en"): "en"}
        current_language = next((label for label, value in self.language_labels.items() if value == self.draft["language"]), self.app.t("zh"))
        self.language_var = tk.StringVar(value=current_language)
        self.language_segment = ctk.CTkSegmentedButton(
            tab,
            values=list(self.language_labels),
            variable=self.language_var,
            height=38,
            corner_radius=11,
            border_width=2,
            fg_color=COLORS["segment_bg"],
            selected_color=COLORS["segment_selected"],
            selected_hover_color=COLORS["segment_hover"],
            unselected_color=COLORS["segment_bg"],
            unselected_hover_color=COLORS["segment_hover"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.language_segment.pack(fill="x", padx=14)

    def _build_shortcuts(self) -> None:
        tab = self.shortcuts_tab
        ctk.CTkLabel(tab, text=self.app.t("shortcut_hint"), text_color=COLORS["muted"], wraplength=390, justify="left", anchor="w", font=ctk.CTkFont(size=11)).pack(fill="x", padx=14, pady=(15, 12))
        self.shortcut_vars = {
            "hotkey_toggle": tk.StringVar(value=self.draft["hotkey_toggle"]),
            "hotkey_stop": tk.StringVar(value=self.draft["hotkey_stop"]),
        }
        self.capture_buttons = {}
        for slot, label_key in (("hotkey_toggle", "hotkey_toggle"), ("hotkey_stop", "hotkey_stop")):
            row = ctk.CTkFrame(tab, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=7)
            ctk.CTkLabel(row, text=self.app.t(label_key), text_color=COLORS["text"], anchor="w", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 5))
            button = style_button(row, display_key(self.draft[slot]), lambda s=slot: self._begin_capture(s), width=410, height=40)
            button.pack(fill="x")
            self.capture_buttons[slot] = button
        ctk.CTkLabel(tab, text=self.app.t("shortcut_line") + f"{display_key(self.draft['hotkey_toggle'])}  ·  {display_key(self.draft['hotkey_stop'])}", text_color=COLORS["muted"], anchor="w", font=ctk.CTkFont(size=11)).pack(fill="x", padx=14, pady=(14, 0))

    def _begin_capture(self, slot: str) -> None:
        self.capture_buttons[slot].configure(text=self.app.t("press_key"))
        self.app.begin_key_capture(lambda name, s=slot: self._finish_capture(s, name))

    def _finish_capture(self, slot: str, name: str | None) -> None:
        if not self.winfo_exists():
            return
        if name is None:
            self.capture_buttons[slot].configure(text=display_key(self.draft[slot]))
            return
        other = "hotkey_stop" if slot == "hotkey_toggle" else "hotkey_toggle"
        if name in (self.draft[other], self.draft.get("target_key")):
            self.capture_buttons[slot].configure(text=display_key(self.draft[slot]))
            messagebox.showerror(self.app.t("input_error_title"), self.app.t("hotkey_conflict"), parent=self)
            return
        self.draft[slot] = name
        self.capture_buttons[slot].configure(text=display_key(name))

    def _preview_theme(self, label: str) -> None:
        theme = self.theme_labels.get(label, "system")
        self.app.apply_theme(theme)

    def save(self) -> None:
        try:
            interval = float(self.interval_var.get().strip())
            if not (0 < interval <= 3600):
                raise ValueError
        except (ValueError, TypeError):
            messagebox.showerror(self.app.t("input_error_title"), self.app.t("invalid_interval"), parent=self)
            return
        try:
            gap = int(self.double_gap_var.get().strip())
            if not 0 <= gap <= 2000:
                raise ValueError
        except (ValueError, TypeError):
            messagebox.showerror(self.app.t("input_error_title"), self.app.t("invalid_gap"), parent=self)
            return
        toggle = self.draft["hotkey_toggle"]
        stop = self.draft["hotkey_stop"]
        target_key = str(self.draft.get("target_key", ""))
        if toggle == stop or toggle == target_key or stop == target_key:
            messagebox.showerror(self.app.t("input_error_title"), self.app.t("hotkey_conflict"), parent=self)
            return
        self.draft["interval"] = interval
        self.draft["double_gap_ms"] = gap
        self.draft["mouse_button"] = self.mouse_var.get()
        self.draft["click_type"] = self.click_type_var.get()
        self.draft["theme"] = self.theme_labels.get(self.theme_var.get(), "system")
        self.draft["language"] = self.language_labels.get(self.language_var.get(), "zh-TW")
        self.app.settings.update(self.draft)
        self.app.apply_theme()
        self.app.save_config()
        self.saved = True
        self.app.settings_window = None
        self.app.update_language()
        self.destroy()

    def cancel(self) -> None:
        if self.saved:
            return
        self.app.cancel_key_capture()
        self.app.apply_theme(self.app.settings.get("theme", "system"))
        self.app.settings_window = None
        self.destroy()


def smoke_test() -> None:
    app = AutoClickerApp(start_listener=False)
    app.root.withdraw()
    settings = SettingsWindow(app)
    settings.withdraw()
    app.root.update()
    if len(settings.tabs._name_list) != 3:
        raise RuntimeError("Settings tabs failed to initialize")
    settings.cancel()
    app.close()


def main() -> None:
    if "--smoke" in sys.argv:
        smoke_test()
        return
    app = AutoClickerApp()
    app.run()


if __name__ == "__main__":
    main()
