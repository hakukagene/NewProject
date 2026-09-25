"""Engine-independent state checks; Ren'Py lint still needed for display code."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]


def init_blocks(path):
    lines = path.read_text(encoding="utf-8-sig").splitlines(True)
    for i, line in enumerate(lines):
        if line == "init python:\n":
            body = []
            for child in lines[i + 1:]:
                if child.strip() and not child.startswith((" ", "\t")):
                    break
                body.append(child[4:] if child.startswith("    ") else child)
            yield "".join(body)


class StoryTests(unittest.TestCase):
    def setUp(self):
        self.store = SimpleNamespace(
            kh_relationships={"khulan": 20},
            moment_other_dm_messages={}, kh_dm_replied=[], kh_post_likes=[],
        )
        fake = SimpleNamespace(store=self.store, restart_interaction=lambda: None, loadable=lambda _: False)
        self.ns = {"renpy": fake, "phone_current_time": lambda: "23:00", "Solid": lambda color: color}
        for block in init_blocks(ROOT / "game/khulan_system.rpy"):
            exec(compile(block, "khulan_system.rpy", "exec"), self.ns)

    def test_changed_python_blocks_parse(self):
        for filename in ("khulan_system.rpy", "phone_ui.rpy", "moment_app.rpy"):
            for block in init_blocks(ROOT / "game" / filename):
                ast.parse(block, filename=filename)

    def test_relationships_are_independent_and_bounded(self):
        self.ns["kh_change"]("khulan", 200)
        self.ns["kh_change"]("anu", -200)
        self.assertEqual(self.store.kh_relationships, {"khulan": 100, "anu": 0})

    def test_phone_initialization_and_bolor_history(self):
        self.ns["kh_start_story"]()
        self.ns["kh_prepare_bolor"]()
        self.assertEqual(self.store.moment_profile_name, "Билгүүн")
        self.assertEqual(self.store.moment_relationship, 55)
        self.assertFalse(self.store.sara_blocked)
        self.assertEqual(len(self.store.sara_messages), 8)
        self.assertIn("khulan", self.store.moment_other_dm_messages)
        self.assertEqual(self.ns["KH_CONTACTS"]["sara"]["name"], "Болор")

    def test_scripted_contacts_do_not_spam_replies_or_change_bolor(self):
        self.store.moment_active_contact = "anu"
        for text in ("Сайн уу", "Баярлалаа"):
            self.store.phone_chat_input = text
            self.ns["kh_send_scripted_dm"]()
        thread = self.store.moment_other_dm_messages["anu"]
        self.assertEqual([m["sender"] for m in thread], ["player", "contact", "player"])
        self.assertEqual(self.store.phone_chat_input, "")

    def test_optional_assets_have_fallback(self):
        self.assertEqual(self.ns["kh_background"]("bilguun_room"), "#152132")
        self.assertEqual(self.ns["kh_background"]("classroom"), "#34424b")

    def test_likes_toggle_without_relationship_farming(self):
        self.ns["kh_toggle_like"]("khulan")
        self.assertEqual(self.store.kh_post_likes, ["khulan"])
        self.ns["kh_toggle_like"]("khulan")
        self.assertEqual(self.store.kh_post_likes, [])
        self.assertEqual(self.store.kh_relationships["khulan"], 20)

    def test_day_one_contains_all_major_scenes_and_native_choices(self):
        text = (ROOT / "game/khulan_day_one.rpy").read_text()
        for scene in ("family_future", "cafeteria", "corridor", "classroom", "gazebo", "street_escape", "khulan_gate", "khulan_room", "dinner", "police_car", "bilguun_home", "bilguun_room", "dream", "day_two"):
            self.assertIn('kh_background("%s")' % scene, text)
        self.assertGreaterEqual(text.count("    menu:\n"), 20)
        self.assertIn("call screen kh_timed_choice", text)
        self.assertIn('call kh_inspect("khulan_room")', text)
        self.assertIn("call screen kh_computer", text)
        self.assertIn("$ kh_day_one_complete = True", text)


if __name__ == "__main__":
    unittest.main()
