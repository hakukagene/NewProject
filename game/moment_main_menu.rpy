# Approved phone-on-desk artwork, with real focusable Ren'Py controls.
screen moment_desk_menu():
    default active_item = "Start"
    $ latest_save = renpy.newest_slot()
    $ continue_action = FileLoad(latest_save, confirm=False, slot=True) if latest_save else NullAction()
    $ menu_items = [("Start", Start()), ("Continue", continue_action), ("Load", ShowMenu("load")), ("Settings", ShowMenu("preferences")), ("Gallery", ShowMenu("story_character_gallery")), ("Quit", Quit(confirm=True))]

    add "gui/moment_menu/desk.webp" xysize (1920, 1080)

    vbox:
        xpos 96
        ypos 450
        spacing 0
        for caption, command in menu_items:
            button:
                style "moment_desk_button"
                action command
                sensitive caption != "Continue" or latest_save is not None
                hovered SetScreenVariable("active_item", caption)
                default_focus caption == "Start"
                selected active_item == caption
                # Include the label for screen readers even though the visible
                # text lives in a custom horizontal layout.
                alt caption
                fixed:
                    xysize (430, 64)
                    if active_item == caption:
                        add "gui/moment_menu/diamond.svg" xpos 16 ypos 22 xysize (17, 22)
                    hbox:
                        xpos 68
                        yalign 0.5
                        spacing 18
                        text caption style "moment_desk_label"
                        if active_item == caption:
                            add Solid("#c79850") xysize (205, 1) yalign 0.55

style moment_desk_button is button:
    xysize (430, 64)
    padding (0, 0)
    background None
    hover_background None
    selected_background None
    insensitive_background None

style moment_desk_label is button_text:
    font "fonts/DejaVuSerif.ttf"
    size 34
    kerning 2.0
    color "#c6c6c8"
    hover_color "#ffe3b4"
    selected_color "#ffe3b4"
    selected_hover_color "#ffe3b4"
    insensitive_color "#88868a"
    outlines []
