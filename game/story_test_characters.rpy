# Temporary still-image stand-ins. Disable before switching to final video scenes.
default persistent.story_test_art = True
default story_test_scene = ""
default story_test_actors = ()

init python:
    STORY_TEST_CHARACTERS = {
        "khulan": "Хулан",
        "bilguun": "Билгүүн",
        "chingun": "Чингүн",
        "anu": "Ану",
        "saruul": "Саруул",
        "bolor": "Болор",
        "teacher": "Багш",
        "khulan_mother": "Хулангийн ээж",
        "khulan_father": "Хулангийн аав",
        "bilguun_father": "Билгүүний аав",
        "badral": "Бадрал",
        "older_students": "Ахлах курсын залуус",
    }
    STORY_TEST_CAST = {
        "family_future": ("bilguun", "bilguun_father"),
        "cafeteria": ("bilguun", "chingun"),
        "corridor": ("bilguun", "chingun", "saruul"),
        "classroom": ("teacher", "bilguun", "khulan", "chingun"),
        "school_gate": ("bilguun", "chingun"),
        "gazebo": ("bilguun", "khulan"),
        "street_escape": ("bilguun", "khulan", "chingun"),
        "khulan_gate": ("bilguun", "khulan"),
        "khulan_room": ("bilguun", "khulan"),
        "dinner": ("khulan_mother", "khulan_father", "khulan", "badral"),
        "departure": ("bilguun", "khulan", "badral"),
        "police_car": ("bilguun", "badral"),
        "bilguun_home": ("bilguun", "bilguun_father"),
        "bilguun_room": ("bilguun",),
        "dream": ("khulan",),
        "day_two": ("bilguun",),
    }

    def story_test_asset(actor):
        return "images/characters/test/%s.webp" % actor

    def story_refresh_test_cast():
        # Only our own master-layer tags are touched. Dialogue and device screens
        # remain above them; an ordinary scene statement clears all previous art.
        for actor in STORY_TEST_CHARACTERS:
            renpy.hide("test_actor_" + actor)
        actors = [a for a in renpy.store.story_test_actors
                  if a in STORY_TEST_CHARACTERS and renpy.loadable(story_test_asset(a))]
        positions = {1: (.68,), 2: (.28, .72), 3: (.18, .5, .82), 4: (.12, .37, .63, .88)}
        actors = actors[:4]
        for actor, position in zip(actors, positions.get(len(actors), ())):
            height = 930 if len(actors) < 4 else 880
            # A live condition also updates the underlying game after leaving
            # the gallery's separate menu context, without waiting for a scene.
            visible_art = ConditionSwitch("persistent.story_test_art", story_test_asset(actor), "True", Null(), predict_all=True)
            renpy.show("test_actor_" + actor, what=Transform(
                visible_art, xysize=(int(height * 2 / 3), height),
                xpos=position, xanchor=.5, ypos=1080, yanchor=1.0), zorder=1)

    def story_set_test_cast(scene_id):
        renpy.store.story_test_scene = scene_id
        renpy.store.story_test_actors = STORY_TEST_CAST.get(scene_id, ())
        story_refresh_test_cast()

    def story_set_test_actors(actors):
        renpy.store.story_test_actors = tuple(actors)
        story_refresh_test_cast()

    def story_toggle_test_art():
        persistent.story_test_art = not persistent.story_test_art
        renpy.save_persistent()
        story_refresh_test_cast()
        renpy.restart_interaction()

screen story_character_gallery():
    tag menu
    modal True
    default selected_actor = "khulan"
    default selected_background = "gazebo"
    use gold_shell("Gallery"):
        fixed:
            viewport:
                style_prefix "gold"
                xpos 0 ypos 0 xysize (360, 472)
                scrollbars "vertical"
                mousewheel True
                draggable True
                vbox:
                    spacing 5
                    for actor, name in STORY_TEST_CHARACTERS.items():
                        textbutton name:
                            style "gold_actor"
                            selected selected_actor == actor
                            action SetScreenVariable("selected_actor", actor)
            fixed:
                xpos 392 ypos 0 xysize (1276, 472) clipping True
                add story_background(selected_background) xysize (1276, 472)
                add story_test_asset(selected_actor) xysize (315, 472) xalign .5
                frame:
                    xpos 18 ypos 16 padding (15, 8) background gold_panel()
                    text STORY_TEST_CHARACTERS[selected_actor] style "gold_text"
            hbox:
                xpos 392 ypos 488 spacing 8
                for scene_id, caption in [("gazebo", "Саравч"), ("classroom", "Анги"), ("khulan_room", "Өрөө"), ("bilguun_home", "Шөнө")]:
                    textbutton caption:
                        style "gold_action"
                        selected selected_background == scene_id
                        action SetScreenVariable("selected_background", scene_id)
            textbutton ("Түр дүр: Асаалттай" if persistent.story_test_art else "Түр дүр: Унтраалттай"):
                style "gold_actor"
                xpos 0 ypos 492
                action Function(story_toggle_test_art)
