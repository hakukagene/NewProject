# Coordinates follow the 1920x1080 story backgrounds. The existing label
# still owns narration, visited state, and discoveries such as knows_piano.
init python:
    STORY_INSPECTION_REGIONS = {
        "classroom": {
            "class_window": (12, 30, 550, 520),
            "class_students": (1160, 488, 730, 365),
            "class_board": (700, 164, 794, 270),
        },
        "saruul_home": {
            "saruul_family": (24, 95, 208, 222),
            "saruul_study": (20, 364, 355, 430),
            "saruul_room": (910, 444, 910, 370),
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
                xpos (680 if room == "saruul_home" else 52) ypos 88
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
        # Future scenes without mapped artwork keep a functional list.
        use story_inspection_list(room)


transform story_inspection_open:
    alpha 0.0 zoom .96
    ease .18 alpha 1.0 zoom 1.0

screen story_inspection_closeup(room, item):
    modal True
    zorder 160
    key "game_menu" action Return()
    $ region = STORY_INSPECTION_REGIONS[room][item[0]]
    $ preview_scale = min(1000.0 / region[2], 570.0 / region[3])
    $ preview_size = (int(region[2] * preview_scale), int(region[3] * preview_scale))
    add Transform(story_background(room), blur=12)
    add Solid("#080d18a8")
    frame at story_inspection_open:
        xalign .5 yalign .5 xysize (1160, 950)
        padding (2, 2)
        background device_panel("#d6b875")
        frame:
            xfill True yfill True padding (64, 46)
            background device_panel("#162232f5")
            fixed:
                text item[1] xalign .5 ypos 4 size 36 color "#ffe0a5"
                textbutton "×":
                    id "inspection_close"
                    xalign 1.0 ypos 0 xysize (52, 52)
                    text_font "DejaVuSans.ttf" text_size 36 text_xalign .5 text_yalign .5
                    text_color "#ffe0a5"
                    background None hover_background device_panel("#ffffff18")
                    action Return()
                fixed:
                    xpos 14 ypos 78 xysize (1000, 570)
                    add Transform(Crop(region, story_background(room)), xysize=preview_size) xalign .5 yalign .5
                viewport:
                    xpos 14 ypos 673 xysize (1000, 100)
                    mousewheel True draggable True
                    text item[2] size 25 color "#e3e5e8" xminimum 980 xmaximum 980 textalign .5
                textbutton "Буцах":
                    id "inspection_back"
                    xalign .5 ypos 790 xysize (300, 64)
                    text_size 27 text_xalign .5 text_yalign .5 text_color "#ffe0a5"
                    background device_panel("#364457") hover_background device_panel("#4c5c70")
                    action Return()
