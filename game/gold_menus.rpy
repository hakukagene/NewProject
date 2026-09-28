# Shared, live Ren'Py interface matching approved concept 04 / GOLD TABS.
init -1 python:
    def gold_panel(hover=False):
        return Frame("gui/gold/panel_hover.svg" if hover else "gui/gold/panel.svg", 18, 18)

screen gold_shell(title, panel=True):
    add "gui/gold/desk.webp" xysize (1920, 1080)
    add Solid("#10090636")
    add Solid("#100b09c7") xysize (1920, 134)
    add Solid("#c99c5866") ypos 133 xysize (1920, 1)
    text "MOMENT" xpos 88 ypos 35 size 59 font "fonts/DejaVuSerif.ttf" color "#fff4df"
    add "gui/gold/flourish.svg" xpos 86 ypos 104 xysize (285, 22)
    add Solid("#bb965a") xpos 435 ypos 51 xysize (1, 51)
    hbox:
        xpos 474 ypos 48 spacing 9
        for caption, target in [("History", "history"), ("Save", "save"), ("Load", "load"), ("Settings", "preferences"), ("Gallery", "story_character_gallery"), ("About", "about"), ("Help", "help")]:
            $ current = title == caption
            button:
                style "gold_tab"
                action ShowMenu(target)
                sensitive not (main_menu and target in ("save", "history"))
                selected current
                vbox:
                    spacing 10
                    text caption style "gold_tab_text" xalign .5
                    if current:
                        fixed:
                            xysize (130, 18)
                            add Solid("#d7aa63") ypos 8 xysize (130, 1)
                            add "gui/moment_menu/diamond.svg" xpos 59 xysize (12, 17)
    text title xpos 90 ypos 196 style "gold_title"
    add "gui/gold/flourish.svg" xpos 90 ypos 293 xysize (470, 30)
    if panel:
        frame:
            style "gold_body"
            transclude
    else:
        transclude
    if title != "Welcome":
        textbutton "‹  Return" style "gold_footer" xpos 80 ypos 982 action (ShowMenu("main_menu") if main_menu else Return())
    if not main_menu:
        if _in_replay:
            textbutton "End Replay" style "gold_footer" xpos 1410 ypos 982 action EndReplay(confirm=True)
        else:
            textbutton "Main Menu" style "gold_footer" xpos 1410 ypos 982 action MainMenu()
    if renpy.variant("pc"):
        textbutton "Quit" style "gold_footer" xpos 1760 ypos 982 action Quit(confirm=True)
    key "game_menu" action (ShowMenu("main_menu") if main_menu else Return())

screen gold_heading(caption):
    vbox:
        spacing 18
        hbox:
            spacing 20
            add "gui/moment_menu/diamond.svg" xysize (23, 30) yalign .5
            text caption style "gold_heading"
        add Solid("#d0a35f") xysize (486, 1)


screen gold_toggle(caption, command):
    button:
        style "gold_toggle"
        action command
        fixed:
            xysize (486, 42)
            text caption style "gold_text" xmaximum 390 yalign .5
            add ("gui/gold/switch_on.svg" if command.get_selected() else "gui/gold/switch_off.svg") xpos 410 xysize (76, 42)

screen gold_radio(caption, command):
    button:
        style "gold_toggle"
        action command
        hbox:
            spacing 16
            add ("gui/gold/radio_on.svg" if command.get_selected() else "gui/gold/radio_off.svg") xysize (34, 34)
            text caption style "gold_text" yalign .5

screen gold_slider(caption, preference):
    vbox:
        spacing 8
        text caption style "gold_text"
        bar style "gold_slider" value Preference(preference)


screen gold_settings():
    use gold_shell("Settings", panel=False):
        hbox:
            xpos 80 ypos 358 spacing 24
            frame:
                style "gold_card"
                vbox:
                    spacing 14
                    use gold_heading("Display")
                    text "Window Mode" style "gold_text"
                    if renpy.variant("pc") or renpy.variant("web"):
                        use gold_radio("Window", Preference("display", "window"))
                        use gold_radio("Fullscreen", Preference("display", "fullscreen"))
                    else:
                        text "Fullscreen" style "gold_text"
                    null height 29
                    add Solid("#a8855266") xysize (486, 1)
                    null height 8
                    use gold_toggle("Transitions", Preference("transitions", "toggle"))
                    text "Enable scene transitions and effects." style "gold_hint"
            frame:
                style "gold_card"
                vbox:
                    spacing 14
                    use gold_heading("Reading")
                    use gold_slider("Text Speed", "text speed")
                    null height 8
                    use gold_slider("Auto-Forward Time", "auto-forward time")
                    null height 12
                    use gold_toggle("Skip unseen text", Preference("skip", "toggle"))
                    use gold_toggle("After choices", Preference("after choices", "toggle"))
            frame:
                style "gold_card"
                vbox:
                    spacing 14
                    use gold_heading("Audio")
                    if config.has_music:
                        use gold_slider("Music", "music volume")
                    if config.has_sound:
                        use gold_slider("Sound", "sound volume")
                    if config.has_voice:
                        use gold_slider("Voice", "voice volume")
                    add Solid("#a8855266") xysize (486, 1)
                    use gold_toggle("Mute all", Preference("all mute", "toggle"))
                    if config.sample_sound:
                        textbutton "Test sound" style "gold_action" action Play("sound", config.sample_sound)
                    if config.sample_voice:
                        textbutton "Test voice" style "gold_action" action Play("voice", config.sample_voice)

screen gold_main_menu():
    $ latest_save = renpy.newest_slot()
    use gold_shell("Welcome", panel=False):
        hbox:
            xpos 80 ypos 358 spacing 24
            for heading, description, caption, command in [("New Story", "Start a new story.", "Start  ›", Start()), ("Continue", "Return to your latest save." if latest_save else "Your story begins here.", "Continue  ›", FileLoad(latest_save, confirm=False, slot=True) if latest_save else NullAction()), ("Explore", "Meet the characters.", "Gallery  ›", ShowMenu("story_character_gallery"))]:
                frame:
                    style "gold_card"
                    fixed:
                        xysize (490, 462)
                        vbox:
                            spacing 30
                            use gold_heading(heading)
                            text description style "gold_text" xmaximum 480
                        textbutton caption:
                            style "gold_primary"
                            ypos 270
                            action command
                            sensitive heading != "Continue" or latest_save is not None
                            default_focus heading == "New Story"
                        if heading == "Continue":
                            textbutton "Load a save" style "gold_action" ypos 350 action ShowMenu("load")
                        elif heading == "Explore":
                            textbutton "Settings" style "gold_action" ypos 350 action ShowMenu("preferences")


style gold_text is default:
    font "fonts/DejaVuSerif.ttf"
    size 28
    color "#f1e5d5"
    outlines []
style gold_hint is gold_text:
    size 21
    color "#c9baa6"
style gold_title is gold_text:
    size 86
    color "#fff3df"
style gold_heading is gold_text:
    size 38
    kerning 1.3
style gold_body is empty:
    xpos 80
    ypos 346
    xysize (1760, 606)
    padding (30, 24)
    background gold_panel()
style gold_content is empty:
    xfill True
    yfill True
    padding (0, 0)
style gold_card is empty:
    xysize (570, 522)
    padding (40, 30)
    background gold_panel()
style gold_tab is button:
    xysize (177, 76)
    padding (0, 0)
    background None
    hover_background None
style gold_tab_text is gold_text:
    size 28
    hover_color "#ffe1a0"
    selected_color "#e9b66b"
    insensitive_color "#b7a78b80"
style gold_footer is button:
    padding (10, 8)
    background None
style gold_footer_text is gold_tab_text:
    size 29
style gold_toggle is button:
    padding (0, 4)
    background None
    hover_background Solid("#d9a85f18")
style gold_action is button:
    padding (14, 12)
    background None
    hover_background gold_panel(True)
style gold_action_text is gold_tab_text:
    size 27
style gold_primary is gold_action:
    xsize 480
    background gold_panel()
    hover_background gold_panel(True)
style gold_primary_text is gold_action_text:
    color "#ffe1a0"
style gold_slider is slider:
    xsize 486
    ysize 30
    left_bar Frame("gui/gold/track_on.svg", 5, 0)
    right_bar Frame("gui/gold/track_off.svg", 5, 0)
    thumb "gui/gold/thumb.svg"
    thumb_shadow None
    thumb_offset 14
    left_gutter 14
    right_gutter 14
    bar_vertical False

# Shared menu styles are applied after the stock screen styles.
init 10:
    style slot_button:
        background gold_panel()
        hover_background gold_panel(True)
        padding (12, 10)
        xsize 470
        ysize 248
    style slot_time_text:
        size 19
        color "#e4c58c"
    style slot_name_text:
        size 19
        color "#f1e5d5"
    style page_button_text:
        color "#e0cfb4"
        hover_color "#ffe1a0"
        selected_color "#e9b66b"
    style page_label_text:
        size 25
        color "#f1e5d5"
    style history_text:
        color "#f1e5d5"
        size 28
        xsize 1250
        min_width 0
    style help_text:
        color "#f1e5d5"
        size 27
    style about_text:
        color "#f1e5d5"
        size 27
    style confirm_frame:
        background gold_panel()
        padding (60, 48)
    style confirm_button:
        background gold_panel()
        hover_background gold_panel(True)
        padding (26, 14)
    style notify_frame:
        background gold_panel()
    style skip_frame:
        background gold_panel()

style gold_save_slot is button:
    xysize (500, 225)
    padding (10, 9)
    background gold_panel()
    hover_background gold_panel(True)
style gold_slot_text is gold_text:
    size 18
    xalign .5
    textalign .5
    xmaximum 475
    layout "nobreak"
style gold_page is gold_action:
    padding (10, 4)
style gold_page_text is gold_tab_text:
    size 24
style gold_actor is gold_action:
    xsize 335
    padding (12, 10)
style gold_actor_text is gold_tab_text:
    size 24

init 10:
    style choice_button:
        background gold_panel()
        hover_background gold_panel(True)
    style choice_button_text:
        idle_color "#f1e5d5"
        hover_color "#ffe1a0"
    style quick_button_text:
        idle_color "#d1b78d"
        hover_color "#ffe1a0"
        selected_color "#e9b66b"

style gold_viewport is viewport
style gold_side is side:
    spacing 16
style gold_vscrollbar is vscrollbar:
    xsize 9
    base_bar Solid("#74604b55")
    thumb Solid("#d5a65c")
    hover_thumb Solid("#ffe1a0")
    unscrollable "hide"
style gold_primary_text:
    insensitive_color "#88785f"
