"""Engine-independent state checks; Ren'Py lint still needed for display code."""
import ast
import re
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
    def test_each_label_is_defined_once_across_game(self):
        labels = {}
        for path in (ROOT / "game").rglob("*.rpy"):
            source = path.read_text(encoding="utf-8-sig")
            for name in re.findall(r"(?m)^label\s+([A-Za-z_][A-Za-z_0-9.]*)", source):
                self.assertNotIn(name, labels, "%s duplicated in %s and %s" % (name, labels.get(name), path))
                labels[name] = path
        self.assertEqual(labels["chapter_one"].name, "chapter_one.rpy")
        self.assertEqual(labels["listen_anu_cover"].name, "chapter_one.rpy")

    def setUp(self):
        self.store = SimpleNamespace(
            story_relationships={"khulan": 20},
            moment_other_dm_messages={}, story_dm_replied=[], story_post_likes=[],
        )
        fake = SimpleNamespace(store=self.store, restart_interaction=lambda: None, loadable=lambda _: False)
        self.ns = {"renpy": fake, "phone_current_time": lambda: "23:00", "Solid": lambda color: color}
        for block in init_blocks(ROOT / "game/story_system.rpy"):
            exec(compile(block, "story_system.rpy", "exec"), self.ns)

    def test_changed_python_blocks_parse(self):
        for filename in ("story_system.rpy", "story_devices.rpy", "phone_ui.rpy", "moment_app.rpy"):
            for block in init_blocks(ROOT / "game" / filename):
                ast.parse(block, filename=filename)

    def test_relationships_are_independent_and_bounded(self):
        self.ns["change_story_relationship"]("khulan", 200)
        self.ns["change_story_relationship"]("anu", -200)
        self.assertEqual(self.store.story_relationships, {"khulan": 100, "anu": 0})

    def test_phone_initialization_and_bolor_history(self):
        self.ns["start_chapter_one"]()
        self.ns["story_prepare_bolor"]()
        self.assertEqual(self.store.moment_profile_name, "Билгүүн")
        self.assertEqual(self.store.moment_relationship, 55)
        self.assertFalse(self.store.sara_blocked)
        self.assertEqual(len(self.store.sara_messages), 8)
        self.assertIn("khulan", self.store.moment_other_dm_messages)
        self.assertEqual(self.ns["STORY_CONTACTS"]["sara"]["name"], "Болор")

    def test_scripted_contacts_do_not_spam_replies_or_change_bolor(self):
        self.store.moment_active_contact = "anu"
        for text in ("Сайн уу", "Баярлалаа"):
            self.store.phone_chat_input = text
            self.ns["story_send_scripted_dm"]()
        thread = self.store.moment_other_dm_messages["anu"]
        self.assertEqual([m["sender"] for m in thread], ["player", "contact", "player"])
        self.assertEqual(self.store.phone_chat_input, "")

    def test_optional_assets_have_fallback(self):
        self.assertEqual(self.ns["story_background"]("bilguun_room"), "#152132")
        self.assertEqual(self.ns["story_background"]("classroom"), "#34424b")

    def test_likes_toggle_without_relationship_farming(self):
        self.ns["story_toggle_like"]("khulan")
        self.assertEqual(self.store.story_post_likes, ["khulan"])
        self.ns["story_toggle_like"]("khulan")
        self.assertEqual(self.store.story_post_likes, [])
        self.assertEqual(self.store.story_relationships["khulan"], 20)

    def test_day_one_contains_all_major_scenes_and_native_choices(self):
        text = (ROOT / "game/chapter_one.rpy").read_text()
        for scene in ("family_future", "cafeteria", "corridor", "classroom", "gazebo", "street_escape", "khulan_gate", "khulan_room", "dinner", "police_car", "bilguun_home", "bilguun_room", "dream", "day_two"):
            self.assertIn('story_background("%s")' % scene, text)
        self.assertGreaterEqual(text.count("    menu:\n"), 20)
        self.assertIn("call screen story_timed_choice", text)
        self.assertIn('call story_inspect("khulan_room")', text)
        self.assertIn("call screen story_computer", text)
        self.assertIn("$ story_day_one_complete = True", text)


if __name__ == "__main__":
    unittest.main()
