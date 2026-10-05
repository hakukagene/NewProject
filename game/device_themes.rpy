# Device appearance is a player preference, shared by the phone and desktop.
# It is deliberately persistent rather than part of story/save progression.
default persistent.device_theme = "clean"

init -10 python:
    DEVICE_THEME_ORDER = ("clean", "midnight", "everyday", "warm", "gold")
    DEVICE_THEMES = {
        "clean": dict(name="Clean Light", subtitle="Цайвар · Цэвэрхэн · Мөнгөлөг", bg="#f4f6fa", surface="#ffffff", surface_alt="#e9eef5", line="#d9e1eb", text="#1b2739", muted="#65768a", accent="#2675e8", accent_alt="#185dbd", hot="#dd4267", success="#21855f", status_light=False, on_accent="#ffffff", glass="#ffffffe6"),
        "midnight": dict(name="Midnight Glass", subtitle="Бараан · Шилэн · Нил ягаан", bg="#101320", surface="#191e2f", surface_alt="#262c41", line="#363d55", text="#f1f3fc", muted="#a4aec7", accent="#7764c5", accent_alt="#b7a8f2", hot="#ed7398", success="#61c9a7", status_light=True, on_accent="#ffffff", glass="#1b2030df"),
        "everyday": dict(name="Everyday Desktop", subtitle="Танил · Цэнхэр · Өдөр тутмын", bg="#f2f6fc", surface="#ffffff", surface_alt="#e3edfa", line="#cddcf0", text="#192a40", muted="#5d718d", accent="#1469d5", accent_alt="#0756b8", hot="#d94068", success="#258563", status_light=False, on_accent="#ffffff", glass="#f3f8ffdf"),
        "warm": dict(name="Warm Personal", subtitle="Дулаан · Байгаль · Тайван", bg="#f4f1e8", surface="#fffcf5", surface_alt="#e9e8db", line="#dad9c9", text="#313c33", muted="#727968", accent="#526b52", accent_alt="#39543e", hot="#b85055", success="#487451", status_light=False, on_accent="#ffffff", glass="#fffaf0e8"),
        "gold": dict(name="Moment Gold", subtitle="Хар · Алтлаг · MOMENT", bg="#121412", surface="#1d201d", surface_alt="#2c302b", line="#42483d", text="#f3efdf", muted="#b5b5a4", accent="#cfb475", accent_alt="#edcf8d", hot="#e28787", success="#a4c28e", status_light=True, on_accent="#24251e", glass="#20241fdf"),
    }

    def device_theme_key():
        key = persistent.device_theme
        return key if key in DEVICE_THEMES else "clean"

    def device_palette():
        return DEVICE_THEMES[device_theme_key()]

    def device_wallpaper(key=None):
        return "images/devices/wallpapers/%s.webp" % (key or device_theme_key())

    def device_icon(name, key=None):
        return "images/devices/icons/%s_%s.svg" % (key or device_theme_key(), name)

    def device_set_theme(key):
        if key not in DEVICE_THEMES:
            return
        persistent.device_theme = key
        renpy.store.moment_theme = key  # Compatibility with older saves/screens.
        renpy.save_persistent()
        renpy.restart_interaction()

    def device_notice_contact():
        return renpy.store.story_latest_contact if renpy.store.story_active else "sara"

    def device_notice_name():
        cid = device_notice_contact()
        return (STORY_CONTACTS if renpy.store.story_active else MOMENT_CONTACTS)[cid]["name"]

    def device_notice_preview():
        cid = device_notice_contact()
        if renpy.store.story_active:
            return story_message_preview(cid)
        messages = renpy.store.sara_messages
        return phone_escape_chat_text(messages[-1]["text"][:65]) if messages else "Moment"

    def device_unread():
        return sum(v for k, v in renpy.store.moment_contact_unread.items() if k != "sara") + renpy.store.sara_unread_messages

    def device_tint_icon(name, color, size=32):
        return Transform(AlphaMask(Solid(color, xysize=(100, 100)), "images/devices/icons/%s.svg" % name), xysize=(size, size))

screen device_wallpaper_layer():
    style_prefix "device"
    fixed:
        xysize (624, 984) clipping True
        add device_wallpaper() xysize (624, 984) fit "cover" xalign .5
        add Solid("#08101b25") xysize (624, 984)

screen device_app_shortcut(icon, caption, launch, badge=0):
    style_prefix "device"
    button:
        xysize (164, 132) padding (0, 0) background None
        hover_background device_panel("#ffffff20") action launch
        fixed:
            xysize (164, 132)
            add device_icon(icon) xpos 35 ypos 4 xysize (94, 74)
            text caption xalign .5 ypos 91 size 19 color "#ffffff" font "DejaVuSans.ttf" outlines [(1, "#00000060", 0, 1)]
            if badge:
                frame:
                    xpos 111 ypos 0 xysize (30, 25) padding (0, 0) background device_panel("#d94566")
                    text str(min(99, badge)) xalign .5 yalign .5 size 14 color "#ffffff"

screen device_phone_home():
    style_prefix "device"
    $ p = device_palette()
    $ key = device_theme_key()
    add Null(width=624, height=984)
    if key in ("warm", "everyday"):
        frame:
            xpos 30 ypos 58 xysize (564, 172) padding (26, 18) background device_panel(p["glass"])
            text phone_current_time() size 72 color p["text"] font "DejaVuSans.ttf"
            text phone_current_date() ypos 91 size 19 color p["muted"]
            add device_tint_icon("moment", p["accent"], 66) xpos 410 ypos 14
            text "MOMENT" xpos 399 ypos 98 size 15 color p["muted"]
    else:
        text phone_current_time() xalign .5 ypos 61 size 82 color "#ffffff" font "DejaVuSans.ttf"
        text phone_current_date() xalign .5 ypos 165 size 21 color "#ffffff"
    button:
        xpos 30 ypos 267 xysize (564, 128) padding (20, 18)
        background device_panel(p["glass"]) hover_background device_panel(p["surface"])
        action Function(moment_open_contact, device_notice_contact())
        fixed:
            add device_icon("moment") xpos 0 ypos 6 xysize (60, 48)
            text ("Moment · " + device_notice_name()) xpos 77 ypos 0 size 21 bold True color p["text"]
            text device_notice_preview() xpos 77 ypos 32 xsize 425 size 18 color p["muted"] line_spacing 2
    grid 3 2:
        xpos 30 ypos 436 xspacing 36 yspacing 18
        use device_app_shortcut("moment", "Moment", SetVariable("phone_view", "social"), device_unread())
        use device_app_shortcut("music", "Music", [Function(phone_music_open, "library"), SetVariable("phone_view", "music")])
        use device_app_shortcut("camera", "Камер", Function(phone_camera_open))
        use device_app_shortcut("photos", "Зураг", [SetVariable("phone_gallery_selected", -1), SetVariable("phone_view", "gallery")])
        use device_app_shortcut("notes", "Тэмдэглэл", [SetVariable("phone_notes_page", "list"), SetVariable("phone_view", "notes")])
        use device_app_shortcut("settings", "Тохиргоо", SetVariable("phone_view", "device_settings"))
    frame:
        xpos 44 ypos 780 xysize (536, 96) padding (40, 10) background device_panel(p["glass"])
        hbox:
            spacing 55
            for icon, target in [("chat", "dm"), ("moment", "social"), ("settings", "device_settings")]:
                button:
                    xysize (112, 74) padding (0, 0) background None hover_background device_panel(p["surface_alt"])
                    action SetVariable("phone_view", target)
                    add device_icon(icon) xalign .5 xysize (84, 68)
    textbutton "Утсаа тавих" xalign .5 ypos 906 text_size 19 text_color "#ffffff" background None action Return()

screen device_phone_settings():
    style_prefix "device"
    $ p = device_palette()
    add Solid(p["bg"])
    use phone_status_bar(dark=p["status_light"])
    textbutton "‹" xpos 18 ypos 52 text_size 36 text_color p["accent"] background None action Function(phone_go_home)
    text "Утасны загвар" xpos 82 ypos 65 size 30 bold True color p["text"]
    text "Wallpaper, icon, хүрээ ба аппын өнгө" xpos 28 ypos 125 size 19 color p["muted"]
    vbox:
        xpos 24 ypos 175 spacing 12
        for i, key in enumerate(DEVICE_THEME_ORDER):
            $ opt = DEVICE_THEMES[key]
            button:
                xysize (576, 134) padding (12, 12)
                background device_panel(p["surface_alt"] if device_theme_key() == key else p["surface"])
                hover_background device_panel(p["line"])
                action Function(device_set_theme, key)
                fixed:
                    fixed:
                        xysize (100, 110) clipping True
                        add device_wallpaper(key) xysize (100, 110) fit "cover" xalign .5
                    text ("%02d  %s" % (i + 1, opt["name"])) xpos 118 ypos 9 size 24 bold True color p["text"]
                    text opt["subtitle"] xpos 118 ypos 45 size 17 color p["muted"]
                    hbox:
                        xpos 118 ypos 82 spacing 7
                        for role in ("bg", "surface_alt", "accent", "hot"):
                            add Solid(opt[role]) xysize (28, 12)
                    if device_theme_key() == key:
                        text "✓" xpos 515 ypos 76 size 24 color p["accent"]
    text "Сонголт автоматаар хадгалагдана." xalign .5 ypos 921 size 17 color p["muted"]

screen device_desktop_settings():
    style_prefix "device"
    $ p = device_palette()
    text "Төхөөрөмжийн загвар" xpos 52 ypos 90 size 34 bold True color p["text"]
    text "Утас болон компьютерийн өнгө, wallpaper, icon хамт солигдоно." xpos 52 ypos 146 size 20 color p["muted"]
    hbox:
        xpos 52 ypos 238 spacing 18
        for i, key in enumerate(DEVICE_THEME_ORDER):
            $ opt = DEVICE_THEMES[key]
            button:
                xysize (292, 440) padding (14, 14)
                background device_panel(p["surface_alt"] if device_theme_key() == key else p["bg"])
                hover_background device_panel(p["line"]) action Function(device_set_theme, key)
                vbox:
                    spacing 20
                    fixed:
                        xysize (264, 232) clipping True
                        add device_wallpaper(key) xysize (264, 232) fit "cover" xalign .5
                    text ("%02d  %s" % (i + 1, opt["name"])) size 21 bold True color p["text"]
                    text opt["subtitle"] size 17 color p["muted"] xmaximum 264
                    text ("✓ Сонгосон" if device_theme_key() == key else "Сонгох") size 20 color p["accent"]

style device_input is input:
    font "DejaVuSans.ttf"
style device_button_text:
    font "DejaVuSans.ttf"
