# Coordinates follow the 1920x1080 story backgrounds. The existing label
# still owns narration, visited state, and discoveries such as knows_piano.
init python:
    STORY_INSPECTION_REGIONS = {
        "classroom": {
            "class_window": (12, 30, 550, 520),
            "class_students": (1160, 488, 730, 365),
            "class_board": (700, 164, 794, 270),
        },
        "khulan_room": {
            "room_drawing": (4, 28, 390, 355),
            "room_awards": (1016, 175, 224, 177),
            "piano_award": (1040, 60, 188, 115),
        },
    }

    def story_has_inspection_regions(room):
        regions = STORY_INSPECTION_REGIONS.get(room, {})
        return (renpy.loadable("images/story/%s.webp" % room)
                and all(item[0] in regions for item in STORY_INSPECTIONS[room]))

screen story_inspection(room):
    modal True
    if story_has_inspection_regions(room):
        $ items = STORY_INSPECTIONS[room]
        $ visited = sum(item[0] in story_inspected for item in items)
        fixed:
            xysize (1920, 1080)
            for index, item in enumerate(items):
                $ x, y, w, h = STORY_INSPECTION_REGIONS[room][item[0]]
                $ seen = item[0] in story_inspected
                button:
                    id item[0]
                    xpos x ypos y xysize (w, h)
                    padding (0, 0)
                    background None
                    hover_background device_panel("#ffe0a52b")
                    action Return(index)
                    tooltip item[1]
                    frame:
                        xalign .5 yalign .5
                        padding (16, 10)
                        background device_panel("#162232dd")
                        hbox:
                            spacing 10
                            text ("✓" if seen else "◎") size 24 color ("#94d9bb" if seen else "#ffe0a5") font "DejaVuSans.ttf"
                            text item[1] size (20 if item[0] == "piano_award" else 23) xsize (280 if item[0] == "piano_award" else None) color "#fff5df"

            frame:
                xpos 52 ypos 88
                padding (20, 14)
                background device_panel("#162232dd")
                vbox:
                    spacing 4
                    text "Орчноо ажиглах" size 25 color "#fff5df"
                    text "Зураг дээрх зүйлсийг дарж үзээрэй." size 19 color "#cfdae5"

            frame:
                xalign 1.0 yalign 1.0
                xoffset -48 yoffset -45
                padding (18, 14)
                background device_panel("#162232ee")
                hbox:
                    spacing 22
                    yalign .5
                    text "[visited] / [len(items)]" size 22 color "#cfdae5" yalign .5
                    textbutton "Үргэлжлүүлэх →":
                        id "inspection_continue"
                        padding (20, 10)
                        background device_panel("#ffe0a5")
                        hover_background device_panel("#fff0ca")
                        insensitive_background device_panel("#455160")
                        text_size 23
                        text_font "DejaVuSans.ttf"
                        text_color "#1c2735"
                        text_hover_color "#1c2735"
                        text_insensitive_color "#a8b4c1"
                        sensitive visited == len(items)
                        action Return("done")
    else:
        # A later scene currently has no background artwork. Keep its working
        # inspection list until matching art and object coordinates are added.
        use story_inspection_list(room)
