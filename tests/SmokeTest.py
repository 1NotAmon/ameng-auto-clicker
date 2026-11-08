import json
import re
import unittest
from pathlib import Path

from pynput import keyboard

import AmengClicker


ROOT = Path(__file__).resolve().parents[1]


class ProjectSmokeTest(unittest.TestCase):
    def test_version_and_default_hotkeys(self):
        self.assertEqual(AmengClicker.VERSION, "2.0.0")
        self.assertEqual(AmengClicker.DEFAULTS["hotkey_toggle"], "f6")
        self.assertEqual(AmengClicker.DEFAULTS["hotkey_stop"], "f7")

    def test_special_and_character_key_mapping(self):
        self.assertEqual(AmengClicker.key_name(keyboard.Key.f6), "f6")
        self.assertEqual(AmengClicker.key_from_name("f6"), keyboard.Key.f6)
        self.assertEqual(AmengClicker.key_name(keyboard.KeyCode.from_char("A")), "a")
        self.assertEqual(AmengClicker.key_from_name("b").char, "b")

    def test_mouse_and_click_defaults(self):
        self.assertEqual(AmengClicker.DEFAULTS["mouse_button"], "left")
        self.assertEqual(AmengClicker.DEFAULTS["click_type"], "single")
        self.assertEqual(AmengClicker.DEFAULTS["interval"], 0.1)

    def test_theme_file_contains_only_grayscale_hex_colors(self):
        theme_path = ROOT / "monochrome.json"
        theme = json.loads(theme_path.read_text(encoding="utf-8"))
        for color in re.findall(r"#[0-9A-Fa-f]{6}", json.dumps(theme)):
            red, green, blue = (int(color[index:index + 2], 16) for index in (1, 3, 5))
            self.assertEqual(red, green, color)
            self.assertEqual(green, blue, color)

    def test_application_palette_is_grayscale(self):
        for pair in AmengClicker.COLORS.values():
            for color in pair:
                red, green, blue = (int(color[index:index + 2], 16) for index in (1, 3, 5))
                self.assertEqual(red, green, color)
                self.assertEqual(green, blue, color)


if __name__ == "__main__":
    unittest.main()
