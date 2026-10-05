# Story devices share messages, music, photographs and notes with the phone.
# The browser is an in-world interface; its address bar does not navigate the web.
default story_desktop_app = "moment"
default story_desktop_page = "messages"
default story_desktop_minimized = False
default story_desktop_maximized = False
default story_device_drafts = {}
default story_latest_contact = "anu"

init python:
    def device_panel(color):
        return Frame(AlphaMask(Solid(color, xysize=(86, 64)),
            "images/phoneUI/Momenticon/message_bubble_mask.svg"), 29, 22, 29, 22)

    def story_desktop_open(app):
        if renpy.store.story_desktop_app == "notes" and renpy.store.phone_notes_page == "editor":
            phone_notes_save(silent=True)
        renpy.store.story_desktop_app = app
        renpy.store.story_desktop_minimized = False
        renpy.restart_interaction()

    def story_desktop_contact(contact):
        moment_open_contact(contact)
        renpy.store.story_desktop_page = "messages"

    def story_desktop_leave():
        if renpy.store.story_desktop_app == "notes" and renpy.store.phone_notes_page == "editor":
            phone_notes_save(silent=True)

    def story_desktop_edit_note(index=-1):
        count = len(persistent.phone_notes or [])
        story_desktop_leave()
        # Saving an unsaved note inserts it at index 0. Preserve the clicked note.
        if index >= 0:
            index += len(persistent.phone_notes or []) - count
        phone_notes_open(index)

    def story_message_preview(contact):
        messages = renpy.store.sara_messages if contact == "sara" else renpy.store.moment_other_dm_messages.get(contact, [])
        return phone_escape_chat_text((messages[-1]["text"] if messages else STORY_CONTACTS[contact]["preview"]).replace("\n", " ")[:42])

    def story_desktop_rows(value):
        return min(5, sum(max(1, (len(line) + 55) // 56) for line in value.split("\n")))

style device_button is button:
    padding (18, 12)
    background None
    hover_background Solid("#ffffff12")
    selected_background Solid("#7360e533")
style device_button_text is default:
    font "DejaVuSans.ttf"
    size 20
    color "#dce3ef"
    hover_color "#ffffff"
    selected_color "#b6a8ff"
style device_text is default:
    font "DejaVuSans.ttf"
    size 20
    color "#edf1f8"

screen device_avatar(cid, diameter=48):
    style_prefix "device"
    $ person = STORY_CONTACTS[cid]
    fixed:
        xysize (diameter, diameter)
        add AlphaMask(Solid(person["color"], xysize=(100, 100)), "images/phoneUI/Momenticon/circle_mask.svg") xysize (diameter, diameter)
        text person["initial"] xalign 0.5 yalign 0.5 size int(diameter * .38) color "#ffffff" bold True

screen story_desktop_shell():
    style_prefix "device"
    timer 20 repeat True action Function(renpy.restart_interaction)
    key "game_menu" action If(story_desktop_app and not story_desktop_minimized, SetVariable("story_desktop_minimized", True), [Function(story_desktop_leave), Return()])
    add device_wallpaper() xysize (1920, 1080) fit "cover"
    add Solid("#07101c28")
    text "BILGUUN" xpos 40 ypos 25 size 17 color "#ffffff" kerning 4
    vbox:
        xpos 22 ypos 100 spacing 22
        for app, title in [("moment", "Moment"), ("music", "Music"), ("notes", "Тэмдэглэл"), ("photos", "Зураг"), ("settings", "Тохиргоо")]:
            button:
                xysize (120, 110) padding (0, 0) background None hover_background device_panel("#ffffff26")
                action Function(story_desktop_open, app)
                vbox:
                    xalign .5 spacing 9
                    add device_icon(app) xalign .5 xysize (66, 66)
                    text title size 17 color "#ffffff" xalign .5 outlines [(1, "#00000060", 0, 1)]

    if story_desktop_app and not story_desktop_minimized:
        fixed:
            xalign .5 yalign .4 xysize (1640, 850)
            at Transform(zoom=1.13 if story_desktop_maximized else 1.0)
            add device_panel("#060b1499") xpos -8 ypos 12 xysize (1656, 850)
            frame:
                xysize (1640, 850) padding (0, 0) background device_panel(device_palette()["surface"])
                fixed:
                    xysize (1640, 850) clipping True
                    if story_desktop_app == "moment":
                        frame:
                            xpos 10 ypos 6 xysize (290, 40) padding (14, 6) background device_panel(device_palette()["surface_alt"])
                            add device_icon("moment") xysize (25, 25)
                            text "MOMENT" xpos 38 ypos 2 size 17 color device_palette()["text"]
                    else:
                        text {"music": "Music Player", "notes": "Тэмдэглэл", "photos": "Зураг", "settings": "Тохиргоо"}.get(story_desktop_app, "Desktop") xpos 24 ypos 15 size 17 color device_palette()["text"]
                    hbox:
                        xpos 1470 ypos 0 spacing 0
                        textbutton "−" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] xysize (54, 46) action SetVariable("story_desktop_minimized", True)
                        textbutton "□" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] xysize (54, 46) action ToggleVariable("story_desktop_maximized")
                        textbutton "×" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] xysize (54, 46) hover_background Solid("#be465d") action Function(story_desktop_open, "")
                    if story_desktop_app == "moment":
                        use story_desktop_browser
                    elif story_desktop_app == "music":
                        use story_desktop_music
                    elif story_desktop_app == "notes":
                        use story_desktop_notes
                    elif story_desktop_app == "photos":
                        use story_desktop_photos
                    elif story_desktop_app == "settings":
                        use device_desktop_settings

    frame:
        ypos 1004 xysize (1920, 76) padding (28, 8) background Solid(device_palette()["glass"])
        hbox:
            xalign .5 spacing 20 yalign .5
            for app in ("moment", "music", "notes", "photos", "settings"):
                button:
                    xysize (64, 58) padding (6, 4) background None hover_background device_panel(device_palette()["surface_alt"])
                    action Function(story_desktop_open, app)
                    add device_icon(app) xysize (48, 48)
                    if story_desktop_app == app:
                        add Solid(device_palette()["accent"]) xpos 14 ypos 48 xysize (22, 3)
        vbox:
            xpos 1390 yalign .5 spacing 3
            text phone_current_time() size 20 color device_palette()["text"] xalign 1.0
            text phone_current_date() size 13 color device_palette()["muted"] xalign 1.0
        textbutton "Компьютероос босох" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] xalign 1.0 yalign .5 text_size 18 action [Function(story_desktop_leave), Return()]

screen story_desktop_browser():
    style_prefix "device"
    frame:
        xpos 0 ypos 48 xysize (1640, 58) padding (20, 8) background Solid(device_palette()["surface_alt"])
        textbutton "‹" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] xysize (44, 42) padding (8, 0) text_size 30 action SetVariable("story_desktop_page", "feed")
        frame:
            xpos 64 xysize (1450, 40) padding (18, 9) background device_panel(device_palette()["bg"])
            text ("moment.local/" + {"messages": "messages/" + STORY_CONTACTS[moment_active_contact]["handle"], "feed": "home", "profile": "bilguun"}.get(story_desktop_page, "home")) size 16 color device_palette()["muted"]
    fixed:
        ypos 106 xysize (1640, 744)
        add Solid(device_palette()["bg"])
        frame:
            xysize (220, 744) padding (22, 30) background Solid(device_palette()["surface"])
            vbox:
                spacing 22
                text "moment" size 34 bold True color device_palette()["text"]
                text "Close people. Real moments." size 11 color device_palette()["muted"]
                null height 20
                for page, title in [("feed", "⌂  Нүүр"), ("messages", "✉  Мессеж"), ("profile", "○  Профайл")]:
                    textbutton title style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] xsize 178 selected story_desktop_page == page action SetVariable("story_desktop_page", page)
            vbox:
                ypos 584 spacing 8
                text "Билгүүн" size 20 color device_palette()["text"] bold True
                text "@bilguun" size 16 color device_palette()["muted"]
                text "52 дагагч · 52 дагасан" size 13 color device_palette()["muted"]
        fixed:
            xpos 220 xysize (1420, 744) clipping True
            if story_desktop_page == "messages":
                use story_desktop_messages
            elif story_desktop_page == "profile":
                use story_desktop_profile
            else:
                use story_desktop_feed

screen story_desktop_messages():
    style_prefix "device"
    $ person = STORY_CONTACTS[moment_active_contact]
    $ active_typing = moment_active_contact == "sara" and sara_is_typing
    $ unavailable = moment_active_contact == "sara" and (sara_blocked or sara_cooldown_until > time.time())
    $ composer_h = 106 + 27 * (story_desktop_rows(phone_chat_input) - 1)
    $ can_send = bool(phone_chat_input.strip()) and not active_typing and not unavailable
    if unavailable and not sara_blocked:
        timer 1.0 repeat True action Function(renpy.restart_interaction)
    frame:
        xysize (304, 744) padding (16, 26) background Solid(device_palette()["surface"])
        vbox:
            spacing 14
            text "Мессежүүд" size 24 color device_palette()["text"] bold True
            text "Өнөөдрийн ярианууд" size 14 color device_palette()["muted"]
            null height 8
            for cid, contact in STORY_CONTACTS.items():
                button:
                    style "device_button" selected_background device_panel(device_palette()["accent"] + "22") xysize (272, 95) padding (12, 14)
                    selected moment_active_contact == cid
                    action Function(story_desktop_contact, cid)
                    hbox:
                        spacing 12
                        use device_avatar(cid, 42)
                        vbox:
                            spacing 8 xsize 190
                            text contact["name"] size 18 color device_palette()["text"] bold True
                            text story_message_preview(cid) size 13 color device_palette()["muted"] xmaximum 185
    fixed:
        xpos 304 xysize (1116, 744) clipping True
        add Solid(device_palette()["line"]) xysize (1, 744)
        fixed:
            xysize (1116, 83)
            fixed:
                xpos 30 ypos 18 xysize (48, 48)
                use device_avatar(moment_active_contact, 48)
            text person["name"] xpos 92 ypos 18 size 23 bold True color device_palette()["text"]
            text (sara_mood_label() if moment_active_contact == "sara" else person["status"]) xpos 92 ypos 51 size 14 color device_palette()["success"]
            text ("Харилцаа · %d" % moment_relationship if moment_active_contact == "sara" else person["handle"]) xalign .96 ypos 32 size 15 color device_palette()["accent_alt"]
            add Solid(device_palette()["line"]) ypos 82 xysize (1116, 1)
        viewport:
            id "desktop_messages" xpos 28 ypos 102 xsize 1060 ysize 744 - composer_h - 118
            mousewheel True draggable True yinitial 1.0
            vbox:
                xsize 1042 spacing 18
                text "ӨНӨӨДӨР" xalign .5 size 12 color device_palette()["muted"]
                for msg in moment_active_messages():
                    frame:
                        xalign (1.0 if msg["sender"] == "player" else 0.0)
                        xmaximum 760 padding (22, 14)
                        background device_panel(device_palette()["accent"] if msg["sender"] == "player" else device_palette()["surface_alt"])
                        vbox:
                            spacing 8
                            text phone_escape_chat_text(msg["text"]) size 21 color (device_palette()["on_accent"] if msg["sender"] == "player" else device_palette()["text"]) language "anywhere" xmaximum 716
                            text msg.get("time", "") size 12 color (device_palette()["on_accent"] if msg["sender"] == "player" else device_palette()["muted"]) xalign 1.0
                if active_typing:
                    text "Болор бичиж байна…" size 17 color device_palette()["success"]
        frame:
            ypos 744 - composer_h xysize (1116, composer_h) padding (26, 16) background Solid(device_palette()["surface"])
            if unavailable:
                text ("Болор харилцаагаа зогсоосон." if sara_blocked else "Болор түр завсарлага авч байна.") yalign .5 size 19 color device_palette()["hot"]
            else:
                frame:
                    xysize (908, composer_h - 49) padding (18, 12) background device_panel(device_palette()["surface_alt"])
                    if not phone_chat_input:
                        text "Мессеж бичих…" size 20 color device_palette()["muted"]
                    viewport:
                        id "desktop_draft" xsize 872 ysize composer_h - 73 mousewheel True yinitial 1.0
                        input:
                            value PhoneChatDraftInputValue()
                            length 600 multiline True copypaste True
                            xsize 850 size 21 color device_palette()["text"] language "anywhere"
                            default_focus True
                textbutton "Илгээх" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["on_accent"] text_hover_color device_palette()["on_accent"] text_selected_color device_palette()["on_accent"] xpos 924 ypos 0 xysize (136, 55) background device_panel(device_palette()["accent"] if can_send else device_palette()["line"]) text_insensitive_color device_palette()["muted"] sensitive can_send action Function(moment_send_active_dm)
                text "Ctrl + Enter · Илгээх" ypos composer_h - 43 size 12 color device_palette()["muted"]
                key "ctrl_K_RETURN" action If(can_send, Function(moment_send_active_dm), NullAction())
                if phone_chatbot_last_error and moment_active_contact == "sara":
                    text "Холболт тасарсан · Түр хариу харуулж байна" xpos 360 ypos composer_h - 43 size 12 color "#edbc91"
        if phone_chat_scroll_pending:
            timer .01 action [Scroll("desktop_messages", "vertical increase", amount=1000000), SetVariable("phone_chat_scroll_pending", False)]
        if phone_chat_draft_scroll_pending and not unavailable:
            timer .01 action [Scroll("desktop_draft", "vertical increase", amount=1000000), SetVariable("phone_chat_draft_scroll_pending", False)]

screen story_desktop_feed():
    style_prefix "device"
    text "Таны хүрээлэл" xpos 42 ypos 28 size 30 bold True color device_palette()["text"]
    text "Өдрийн жижигхэн мөчүүд" xpos 42 ypos 72 size 16 color device_palette()["muted"]
    viewport:
        xpos 42 ypos 120 xsize 940 ysize 598 mousewheel True draggable True
        vbox:
            spacing 24 xsize 900
            for cid, caption, title in story_current_posts():
                frame:
                    xsize 900 padding (26, 24) background device_panel(device_palette()["surface"])
                    vbox:
                        spacing 20
                        hbox:
                            spacing 16
                            use device_avatar(cid, 46)
                            vbox:
                                spacing 6
                                text STORY_CONTACTS[cid]["handle"] size 22 color device_palette()["text"] bold True
                                text "Өнөөдөр" size 13 color device_palette()["muted"]
                        text title size 27 color STORY_CONTACTS[cid]["color"]
                        text caption size 23 color device_palette()["text"] xmaximum 835
                        if cid == "anu" and story_flags.get("oct02_night_feed"):
                            use story_farewell_media
                        hbox:
                            spacing 24
                            textbutton ("♥ Таалагдсан" if cid in story_post_likes else "♡ Таалагдлаа") style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] action Function(story_toggle_like, cid)
                            textbutton "Мессеж" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] action Function(story_desktop_contact, cid)
    frame:
        xpos 1030 ypos 120 xysize (346, 360) padding (26, 26) background device_panel(device_palette()["surface"])
        vbox:
            spacing 24
            text "Танилууд" size 22 color device_palette()["text"] bold True
            for cid in ("khulan", "anu", "saruul", "chingun"):
                textbutton STORY_CONTACTS[cid]["name"] style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] action Function(story_desktop_contact, cid)

screen story_desktop_profile():
    style_prefix "device"
    frame:
        xpos 60 ypos 48 xsize 1260 padding (40, 40) background device_panel(device_palette()["surface"])
        vbox:
            spacing 24
            text "Билгүүн" size 44 color device_palette()["text"] bold True
            text "@bilguun  ·  Оюутан" size 21 color device_palette()["muted"]
            text "52 дагагч      52 дагасан" size 23 color device_palette()["accent_alt"]
            text "Миний хүрээлэл" size 26 color device_palette()["text"]
            for cid in ("khulan", "anu", "chingun"):
                text ("%s    %d / 100" % (STORY_CONTACTS[cid]["name"], story_relationships[cid])) size 22 color device_palette()["text"]
            text ("Болор    %d / 100" % moment_relationship) size 22 color device_palette()["text"]

screen story_desktop_music():
    style_prefix "device"
    $ tracks = phone_music_catalog()
    $ current = phone_music_selected_track()
    timer .5 repeat True action Function(phone_music_sync)
    text "Таны хөгжмийн сан" xpos 55 ypos 95 size 36 bold True color device_palette()["text"]
    text ("%d дуу · Утасны Music Player-тэй ижил сан" % len(tracks)) xpos 58 ypos 150 size 18 color device_palette()["muted"]
    viewport:
        xpos 52 ypos 210 xsize 1050 ysize 470 mousewheel True draggable True
        vbox:
            spacing 12
            for track in tracks:
                button:
                    style "device_button" selected_background device_panel(device_palette()["accent"] + "22") xysize (1020, 85)
                    selected phone_music_current == track["path"]
                    action Function(phone_music_play, track["path"], [t["path"] for t in tracks])
                    hbox:
                        spacing 24
                        text "♫" size 32 color device_palette()["accent_alt"]
                        vbox:
                            spacing 6
                            text phone_music_safe(track["title"]) size 24 color device_palette()["text"]
                            text phone_music_safe(track["artist"]) size 16 color device_palette()["muted"]
    add "pMusicCover" xpos 1190 ypos 215 xysize (340, 340)
    frame:
        xpos 32 ypos 712 xysize (1576, 106) padding (28, 20) background device_panel(device_palette()["surface_alt"])
        vbox:
            spacing 8
            text (phone_music_safe(current["title"]) if current else "Дуу сонгоно уу") size 25 color device_palette()["text"]
            text (phone_music_safe(current["artist"]) if current else "Music Player") size 16 color device_palette()["muted"]
        hbox:
            xpos 1150 spacing 18 yalign .5
            textbutton "|‹" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] action Function(phone_music_skip, -1) sensitive bool(current)
            textbutton ("Ⅱ" if phone_music_is_active() and not renpy.music.get_pause(channel="phone_music") else "▶") style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] action Function(phone_music_toggle) sensitive bool(current)
            textbutton "›|" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] action Function(phone_music_skip, 1) sensitive bool(current)

screen story_desktop_notes():
    style_prefix "device"
    text "Тэмдэглэл" xpos 45 ypos 84 size 34 color device_palette()["accent_alt"] bold True
    textbutton "+ Шинэ" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] xpos 1390 ypos 78 action Function(story_desktop_edit_note)
    viewport:
        xpos 32 ypos 160 xsize 366 ysize 650 mousewheel True draggable True
        vbox:
            spacing 12
            for index, note in enumerate(persistent.phone_notes or []):
                button:
                    style "device_button" selected_background device_panel(device_palette()["accent"] + "22") xsize 348 padding (18, 22) selected phone_note_selected == index
                    action Function(story_desktop_edit_note, index)
                    vbox:
                        spacing 10
                        text phone_escape_chat_text(note["title"]) size 21 color device_palette()["text"] xmaximum 312
                        text phone_note_preview(note) size 16 color device_palette()["muted"] xmaximum 312
    frame:
        xpos 420 ypos 157 xysize (1180, 655) padding (30, 26) background device_panel(device_palette()["surface_alt"])
        if phone_notes_page == "editor":
            vbox:
                spacing 24
                fixed:
                    xysize (1110, 48)
                    if not phone_note_draft_title:
                        text "Гарчиг" size 30 color device_palette()["muted"]
                    input value VariableInputValue("phone_note_draft_title") length 80 size 30 color device_palette()["text"] xsize 1080 default_focus True
                viewport:
                    xsize 1110 ysize 450 mousewheel True
                    fixed:
                        xsize 1110 yfit True
                        if not phone_note_draft_body:
                            text "Энд тэмдэглэлээ бичнэ үү…" size 23 color device_palette()["muted"]
                        input value VariableInputValue("phone_note_draft_body") length 5000 multiline True copypaste True size 23 color device_palette()["text"] xsize 1080 language "anywhere"
                textbutton "Хадгалах" action Function(phone_notes_save) text_size 22 text_color device_palette()["accent"] background None
        else:
            text "Тэмдэглэл сонгох эсвэл шинээр үүсгэнэ үү." xalign .5 yalign .5 size 25 color device_palette()["muted"]

screen story_desktop_photos():
    style_prefix "device"
    $ photos = phone_gallery_items()
    text "Зураг" xpos 48 ypos 82 size 34 bold True color device_palette()["text"]
    text ("%d / 10 · Утасны зургийн сан" % len(photos)) xpos 50 ypos 133 size 18 color device_palette()["muted"]
    if 0 <= phone_gallery_selected < len(photos):
        add im.Data(photos[phone_gallery_selected]["data"], "camera.jpg") xpos 250 ypos 180 xysize (1150, 580) fit "contain"
        textbutton "‹ Бүх зураг" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] xpos 45 ypos 180 action SetVariable("phone_gallery_selected", -1)
    elif photos:
        viewport:
            xpos 50 ypos 200 xsize 1540 ysize 600 mousewheel True draggable True
            vpgrid:
                cols 4 spacing 20
                for index, photo in enumerate(photos):
                    button:
                        xysize (360, 260) padding (0, 0) background None
                        action SetVariable("phone_gallery_selected", index)
                        add im.Data(photo["data"], "camera.jpg") xysize (360, 260) fit "cover"
    else:
        text "Зураг хараахан алга" xalign .5 ypos 370 size 30 color device_palette()["text"]
        text "Утасны камераар авсан зураг энд харагдана." xalign .5 ypos 425 size 20 color device_palette()["muted"]

screen story_device_launcher():
    style_prefix "device"
    use device_phone_home

screen story_device_moment():
    style_prefix "device"
    add Solid(device_palette()["bg"])
    use phone_status_bar(dark=device_palette()["status_light"])
    textbutton "‹" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] xpos 8 ypos 48 xysize (54, 70) text_size 40 padding (12, 5) action Function(phone_go_home)
    text "moment" xpos 74 ypos 58 size 40 bold True color device_palette()["text"]
    textbutton "⚙" xpos 470 ypos 61 text_size 26 text_color device_palette()["muted"] background None action SetVariable("phone_view", "device_settings")
    textbutton "✉" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] xpos 523 ypos 56 text_size 27 action SetVariable("phone_view", "dm")
    add Solid(device_palette()["line"]) ypos 130 xysize (624, 1)
    viewport:
        xpos 24 ypos 156 xsize 576 ysize 700 mousewheel True draggable True
        vbox:
            spacing 22 xsize 576
            if phone_view == "dm":
                text "Мессежүүд" size 32 bold True color device_palette()["text"]
                for cid, person in STORY_CONTACTS.items():
                    button:
                        xsize 576 padding (16, 22) background device_panel(device_palette()["surface"]) hover_background device_panel(device_palette()["surface_alt"])
                        action Function(moment_open_contact, cid)
                        hbox:
                            spacing 18
                            use device_avatar(cid, 60)
                            vbox:
                                spacing 10 xsize 443
                                text person["name"] size 24 color device_palette()["text"] bold True
                                text story_message_preview(cid) size 18 color device_palette()["muted"] xmaximum 423
            elif phone_view in ("profile", "relationship"):
                frame:
                    xsize 576 padding (28, 32) background device_panel(device_palette()["surface_alt"])
                    vbox:
                        spacing 22
                        text "Билгүүн" size 38 color device_palette()["text"] bold True
                        text "@bilguun · Оюутан" size 21 color device_palette()["muted"]
                        text "52 дагагч     52 дагасан" size 23 color device_palette()["accent_alt"]
                text "Миний хүрээлэл" size 27 color device_palette()["text"]
                for cid in ("khulan", "anu", "chingun"):
                    text ("%s · %d / 100" % (STORY_CONTACTS[cid]["name"], story_relationships[cid])) size 25 color device_palette()["muted"]
                text ("Болор · %d / 100" % moment_relationship) size 25 color device_palette()["muted"]
            elif story_phone_tab == "story":
                $ person = STORY_CONTACTS[story_story_contact]
                $ post = next(item for item in story_current_posts() if item[0] == story_story_contact)
                frame:
                    xsize 576 padding (28, 38) background device_panel(device_palette()["surface_alt"])
                    vbox:
                        spacing 36
                        use device_avatar(story_story_contact, 76)
                        text (person["name"] + " · Story") size 30 color person["color"]
                        text post[1] size 32 color device_palette()["text"] xmaximum 510
                        textbutton "Мессеж бичих" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] action Function(moment_open_contact, story_story_contact)
                        textbutton "‹ Буцах" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] action SetVariable("story_phone_tab", "feed")
            else:
                if story_notice:
                    frame:
                        xsize 576 padding (20, 18) background device_panel(device_palette()["surface_alt"])
                        text story_notice size 20 color device_palette()["success"] xmaximum 528
                hbox:
                    spacing 12
                    for cid in ("khulan", "anu", "saruul", "chingun"):
                        button:
                            xysize (135, 114) padding (0, 0) background None
                            action [SetVariable("story_story_contact", cid), SetVariable("story_phone_tab", "story")]
                            vbox:
                                xalign .5 spacing 10
                                fixed:
                                    xysize (68, 68) xalign .5
                                    use device_avatar(cid, 68)
                                text STORY_CONTACTS[cid]["name"] size 17 color device_palette()["text"] xalign .5
                for cid, caption, title in story_current_posts():
                    frame:
                        xsize 576 padding (24, 24) background device_panel(device_palette()["surface"])
                        vbox:
                            spacing 22
                            hbox:
                                spacing 14
                                use device_avatar(cid, 45)
                                vbox:
                                    spacing 4
                                    text STORY_CONTACTS[cid]["handle"] size 22 bold True color device_palette()["text"]
                                    text "Өнөөдөр" size 13 color device_palette()["muted"]
                            if renpy.loadable("images/story/post_%s.webp" % cid):
                                add ("images/story/post_%s.webp" % cid) xysize (528, 290) fit "cover"
                            else:
                                frame:
                                    xsize 528 padding (24, 36) background device_panel(device_palette()["surface_alt"])
                                    text title size 32 color STORY_CONTACTS[cid]["color"] xmaximum 475
                            text caption size 24 color device_palette()["text"] xmaximum 518
                            if cid == "anu" and story_flags.get("oct02_night_feed"):
                                use story_farewell_media
                            hbox:
                                spacing 16
                                textbutton ("♥" if cid in story_post_likes else "♡") style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] text_size 30 text_color device_palette()["hot"] action Function(story_toggle_like, cid)
                                textbutton "Мессеж" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] text_size 21 action Function(moment_open_contact, cid)
    frame:
        ypos 876 xysize (624, 78) padding (22, 8) background Solid(device_palette()["surface"])
        hbox:
            spacing 8
            for page, title in [("social", "⌂ Нүүр"), ("dm", "✉ Чат"), ("profile", "○ Би")]:
                textbutton title style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] xysize (185, 60) text_size 22 selected phone_view == page action [SetVariable("phone_view", page), SetVariable("story_phone_tab", "feed")]


screen story_farewell_media():
    style_prefix "device"
    if renpy.loadable("audio/story/anu_farewell.ogg"):
        textbutton "▶ Cover сонсох" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] action Play("music", "audio/story/anu_farewell.ogg")
        textbutton "■ Зогсоох" style "device_button" selected_background device_panel(device_palette()["accent"] + "22") text_color device_palette()["text"] text_hover_color device_palette()["accent_alt"] text_selected_color device_palette()["accent_alt"] action Stop("music", fadeout=.5)
    else:
        text "Cover · Бичлэг хараахан нэмэгдээгүй" size 18 color device_palette()["muted"]
