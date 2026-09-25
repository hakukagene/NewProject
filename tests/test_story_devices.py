"""State transitions that must stay consistent across desktop and phone."""
import unittest
from types import SimpleNamespace
from test_chapter_story import ROOT, init_blocks


class DeviceTests(unittest.TestCase):
    def setUp(self):
        self.store = SimpleNamespace(
            story_desktop_app="moment", story_desktop_minimized=True,
            phone_notes_page="list", moment_active_contact="anu",
            phone_chat_input="Анугийн ноорог", story_device_drafts={},
            moment_contact_unread={"sara": 2, "anu": 1},
            sara_unread_messages=2, moment_other_dm_messages={},
            sara_messages=[{"text": "Сайн уу {b}[name]", "sender": "sara"}],
        )
        self.saved = []
        self.ns = {
            "renpy": SimpleNamespace(store=self.store, restart_interaction=lambda: None),
            "story_active": True,
            "phone_notes_save": lambda silent=False: self.saved.append(silent),
            "phone_escape_chat_text": lambda v: v.replace("[", "[[").replace("{", "{{"),
        }
        for name in ("story_system.rpy", "story_devices.rpy", "moment_app.rpy"):
            for block in init_blocks(ROOT / "game" / name):
                exec(compile(block, name, "exec"), self.ns)

    def test_contact_switch_keeps_drafts_separate_and_marks_read(self):
        self.ns["story_desktop_contact"]("sara")
        self.assertEqual(self.store.phone_chat_input, "")
        self.assertEqual(self.store.sara_unread_messages, 0)
        self.assertEqual(self.store.story_desktop_page, "messages")
        self.store.phone_chat_input = "Болорын ноорог"
        self.ns["moment_open_contact"]("anu")
        self.assertEqual(self.store.phone_chat_input, "Анугийн ноорог")
        self.assertEqual(self.store.story_device_drafts["sara"], "Болорын ноорог")
        self.assertEqual(self.store.moment_contact_unread["anu"], 0)

    def test_switching_apps_and_leaving_saves_notes(self):
        self.store.story_desktop_app = "notes"
        self.store.phone_notes_page = "editor"
        self.ns["story_desktop_leave"]()
        self.ns["story_desktop_open"]("music")
        self.assertEqual(self.saved, [True, True])
        self.assertEqual(self.store.story_desktop_app, "music")
        self.assertFalse(self.store.story_desktop_minimized)

    def test_story_notification_updates_shared_inbox(self):
        self.ns["story_receive"]("anu", "Маргааш уулзъя.")
        self.assertEqual(self.store.story_latest_contact, "anu")
        self.assertEqual(self.store.moment_contact_unread["anu"], 2)
        self.assertEqual(self.store.moment_other_dm_messages["anu"][-1]["text"], "Маргааш уулзъя.")

    def test_long_draft_height_is_bounded(self):
        self.assertEqual(self.ns["story_desktop_rows"](""), 1)
        self.assertEqual(self.ns["story_desktop_rows"]("a\nb\nc"), 3)
        self.assertEqual(self.ns["story_desktop_rows"]("x" * 600), 5)
        self.assertEqual(self.ns["moment_chat_draft_rows"]("x" * 600, 32, 5), 5)
        self.assertEqual(self.ns["moment_chat_draft_rows"]("x" * 18), 1)

    def test_preview_escapes_renpy_markup(self):
        self.assertEqual(self.ns["story_message_preview"]("sara"), "Сайн уу {{b}[[name]")


if __name__ == "__main__":
    unittest.main()
