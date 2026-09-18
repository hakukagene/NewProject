# Moment social app.
#
# The app is intentionally data-driven so story replies, direct messages,
# relationship progress, clues, hidden posts, notifications, and locations
# can be connected to later chapters without rebuilding the UI.


default moment_theme = "midnight"
default moment_relationship = 28
default moment_story_replied = False
default moment_found_clues = []
default moment_hidden_post_unlocked = False
default moment_hidden_post_viewed = False
default moment_selected_location = "lake"
default moment_relationship_events = [
    "Сара таныг дагасан · +3",
    "Нуурын аяллын дурсамж · +5",
]
default moment_notifications = [
    {
        "id": "sara_story",
        "title": "Сара шинэ story орууллаа",
        "body": "Story-д хариулбал харилцаа нэмэгдэнэ.",
        "target": "story",
        "read": False,
    },
    {
        "id": "photo_hint",
        "title": "Зурагт нэг зүйл нуугдсан байна",
        "body": "Сарагийн хамгийн сүүлийн post-ыг сайн ажиглаарай.",
        "target": "social",
        "read": False,
    },
]


init python:
    MOMENT_THEME_ORDER = ("midnight", "violet", "daylight")

    MOMENT_THEMES = {
        "midnight": {
            "name": "Midnight",
            "bg": "#07080b",
            "surface": "#101217",
            "surface_alt": "#181b22",
            "line": "#272b35",
            "text": "#f8fafc",
            "muted": "#9ca3af",
            "accent": "#8b5cf6",
            "accent_alt": "#22d3ee",
            "hot": "#ff3d71",
            "success": "#34d399",
            "status_light": True,
        },
        "violet": {
            "name": "Violet",
            "bg": "#10091b",
            "surface": "#1b102b",
            "surface_alt": "#28153d",
            "line": "#43225f",
            "text": "#fff7ff",
            "muted": "#c4b5d4",
            "accent": "#d946ef",
            "accent_alt": "#7c3aed",
            "hot": "#fb7185",
            "success": "#2dd4bf",
            "status_light": True,
        },
        "daylight": {
            "name": "Daylight",
            "bg": "#f8fafc",
            "surface": "#ffffff",
            "surface_alt": "#eef2ff",
            "line": "#d8deea",
            "text": "#111827",
            "muted": "#64748b",
            "accent": "#7c3aed",
            "accent_alt": "#0284c7",
            "hot": "#e11d48",
            "success": "#059669",
            "status_light": False,
        },
    }

    MOMENT_CLUES = {
        "blade_reflection": {
            "title": "Илдний тусгал",
            "description": "Сарагийн post-ын арын тусгалд хуучин буудлын цаг харагдсан.",
            "location": "Нуурын эрэг",
        },
        "blue_pin": {
            "title": "Цэнхэр байршлын тэмдэг",
            "description": "Зургийн буланд 23:10 гэсэн цагтай нууц location pin байна.",
            "location": "Хотын төв",
        },
        "station_ticket": {
            "title": "Урагдсан тасалбар",
            "description": "Нууц post доторх тасалбар дээр 04-р тавцан гэж бичжээ.",
            "location": "Хуучин буудал",
        },
    }


    def moment_theme_colors():
        return MOMENT_THEMES.get(
            renpy.store.moment_theme,
            MOMENT_THEMES["midnight"],
        )


    def moment_set_theme(theme_name):
        if theme_name not in MOMENT_THEMES:
            return

        renpy.store.moment_theme = theme_name
        renpy.notify("Moment theme: %s" % MOMENT_THEMES[theme_name]["name"])
        renpy.restart_interaction()


    def moment_cycle_theme():
        current = renpy.store.moment_theme
        try:
            index = MOMENT_THEME_ORDER.index(current)
        except ValueError:
            index = 0

        moment_set_theme(
            MOMENT_THEME_ORDER[(index + 1) % len(MOMENT_THEME_ORDER)]
        )


    def moment_relationship_level():
        value = renpy.store.moment_relationship
        if value >= 80:
            return "Онцгой хүн"
        if value >= 60:
            return "Дотны хүн"
        if value >= 35:
            return "Дотносож байна"
        return "Танил"


    def moment_unread_count():
        return sum(
            1 for item in renpy.store.moment_notifications
            if not item.get("read", False)
        )


    def moment_add_notification(title, body, target="social", notice_id=None):
        if notice_id:
            for item in renpy.store.moment_notifications:
                if item.get("id") == notice_id:
                    return

        new_item = {
            "id": notice_id or ("notice_%d" % len(renpy.store.moment_notifications)),
            "title": title,
            "body": body,
            "target": target,
            "read": False,
        }
        renpy.store.moment_notifications = (
            [new_item] + list(renpy.store.moment_notifications)
        )


    def moment_refresh_hidden_post():
        can_unlock = (
            renpy.store.moment_story_replied
            and renpy.store.moment_relationship >= 35
            and "blade_reflection" in renpy.store.moment_found_clues
        )

        if can_unlock and not renpy.store.moment_hidden_post_unlocked:
            renpy.store.moment_hidden_post_unlocked = True
            moment_add_notification(
                "Нууц post нээгдлээ",
                "Story reply болон photo clue хоёр шинэ post-ын түгжээг тайллаа.",
                "hidden_post",
                "hidden_post_unlock",
            )


    def moment_adjust_relationship(amount, reason):
        old_value = renpy.store.moment_relationship
        new_value = max(0, min(100, old_value + amount))
        renpy.store.moment_relationship = new_value

        if new_value != old_value:
            sign = "+" if amount > 0 else ""
            entry = "%s · %s%d" % (reason, sign, amount)
            renpy.store.moment_relationship_events = (
                [entry] + list(renpy.store.moment_relationship_events)
            )[:6]

        moment_refresh_hidden_post()


    def moment_reply_story(reply_text, relationship_points):
        if renpy.store.moment_story_replied:
            renpy.store.phone_view = "chat"
            renpy.store.sara_unread_messages = 0
            renpy.restart_interaction()
            return

        renpy.store.moment_story_replied = True
        moment_adjust_relationship(
            relationship_points,
            "Сарагийн story-д хариулсан",
        )
        renpy.store.sara_messages = list(renpy.store.sara_messages) + [
            {
                "sender": "player",
                "text": "Story reply: %s" % reply_text,
                "time": phone_current_time(),
            },
            {
                "sender": "sara",
                "text": "Хариулсанд баярлалаа. Чи тэр жижиг деталыг анзаарсан уу?",
                "time": phone_current_time(),
            },
        ]
        moment_add_notification(
            "Relationship нэмэгдлээ",
            "Сара таны story reply-д хариуллаа.",
            "chat",
            "story_reply_result",
        )
        renpy.store.sara_unread_messages = 0
        renpy.store.phone_view = "chat"
        renpy.restart_interaction()


    def moment_collect_clue(clue_id):
        if clue_id not in MOMENT_CLUES:
            return

        if clue_id in renpy.store.moment_found_clues:
            renpy.notify("Энэ clue аль хэдийн олдсон.")
            return

        renpy.store.moment_found_clues = (
            list(renpy.store.moment_found_clues) + [clue_id]
        )
        clue = MOMENT_CLUES[clue_id]
        moment_adjust_relationship(2, "Photo clue олсон")
        moment_add_notification(
            "Шинэ photo clue",
            clue["title"] + " clue цуглуулгад нэмэгдлээ.",
            "clues",
            "clue_%s" % clue_id,
        )
        moment_refresh_hidden_post()
        renpy.notify("Photo clue оллоо: %s" % clue["title"])
        renpy.restart_interaction()


    def moment_mark_all_notifications():
        updated = []
        for item in renpy.store.moment_notifications:
            copy = dict(item)
            copy["read"] = True
            updated.append(copy)

        renpy.store.moment_notifications = updated
        renpy.restart_interaction()


    def moment_open_notification(index):
        if index < 0 or index >= len(renpy.store.moment_notifications):
            return

        updated = []
        target = "social"
        for item_index, item in enumerate(renpy.store.moment_notifications):
            copy = dict(item)
            if item_index == index:
                copy["read"] = True
                target = copy.get("target", "social")
            updated.append(copy)

        renpy.store.moment_notifications = updated
        renpy.store.phone_view = target
        renpy.restart_interaction()


    def moment_open_location(location_id):
        renpy.store.moment_selected_location = location_id
        renpy.restart_interaction()


    def moment_open_hidden_post():
        if not renpy.store.moment_hidden_post_unlocked:
            renpy.notify("Story reply болон эхний photo clue хэрэгтэй.")
            return

        renpy.store.moment_hidden_post_viewed = True
        renpy.store.phone_view = "hidden_post"
        renpy.restart_interaction()


    def moment_send_dm():
        message = renpy.store.phone_chat_input.strip()
        if not message or renpy.store.sara_is_typing:
            return

        phone_send_message()
        moment_adjust_relationship(1, "Саратай DM бичсэн")


screen moment_page_header(title, back_target="social", right_label=None, right_target=None):
    $ theme = moment_theme_colors()

    use phone_status_bar(dark=theme["status_light"])

    fixed:
        ypos 42
        xysize (624, 76)

        add Solid(theme["surface"])
        add Solid(theme["line"]) ypos 74 ysize 2

        textbutton "<":
            xpos 12
            yalign 0.5
            xysize (58, 58)
            text_size 34
            text_color theme["text"]
            text_hover_color theme["accent"]
            background None
            action SetVariable("phone_view", back_target)

        text title:
            xpos 76
            yalign 0.5
            size 27
            bold True
            color theme["text"]

        if right_label and right_target:
            textbutton right_label:
                xpos 596
                xanchor 1.0
                yalign 0.5
                text_size 15
                text_color theme["accent_alt"]
                text_hover_color theme["accent"]
                background None
                action SetVariable("phone_view", right_target)


screen moment_bottom_nav(active="home"):
    $ theme = moment_theme_colors()

    frame:
        xpos 0
        ypos 912
        xysize (624, 72)
        padding (10, 8)
        background Solid(theme["surface"])

        hbox:
            spacing 2

            textbutton "HOME":
                xysize (118, 54)
                text_size 14
                text_bold active == "home"
                text_color (theme["accent_alt"] if active == "home" else theme["muted"])
                text_hover_color theme["accent"]
                background None
                action SetVariable("phone_view", "social")

            textbutton "DM":
                xysize (118, 54)
                text_size 14
                text_bold active == "dm"
                text_color (theme["accent_alt"] if active == "dm" else theme["muted"])
                text_hover_color theme["accent"]
                background None
                action Function(phone_open_chat)

            textbutton "CLUES":
                xysize (118, 54)
                text_size 14
                text_bold active == "clues"
                text_color (theme["accent_alt"] if active == "clues" else theme["muted"])
                text_hover_color theme["accent"]
                background None
                action SetVariable("phone_view", "clues")

            textbutton "MAP":
                xysize (118, 54)
                text_size 14
                text_bold active == "location"
                text_color (theme["accent_alt"] if active == "location" else theme["muted"])
                text_hover_color theme["accent"]
                background None
                action SetVariable("phone_view", "location")

            textbutton "BOND":
                xysize (118, 54)
                text_size 14
                text_bold active == "relationship"
                text_color (theme["accent_alt"] if active == "relationship" else theme["muted"])
                text_hover_color theme["accent"]
                background None
                action SetVariable("phone_view", "relationship")


screen moment_story_item(label, initial, ring_color, target=None, locked=False):
    $ theme = moment_theme_colors()

    vbox:
        xysize (104, 112)
        spacing 0

        button:
            xalign 0.5
            xysize (82, 82)
            padding (0, 0)
            background None
            hover_background None
            action (
                SetVariable("phone_view", target)
                if target and not locked
                else Notify("Энэ story одоогоор түгжээтэй.")
            )

            fixed:
                xysize (82, 82)
                text "●" xalign 0.5 yalign 0.5 size 82 color ring_color
                text "●" xalign 0.5 yalign 0.5 size 70 color theme["surface_alt"]
                text initial xalign 0.5 yalign 0.5 size 24 bold True color theme["text"]

                if locked:
                    text "LOCK" xalign 0.5 yalign 0.82 size 10 bold True color theme["hot"]

        text label:
            xalign 0.5
            xmaximum 100
            text_align 0.5
            size 13
            color (theme["text"] if not locked else theme["muted"])


screen phone_moment_feed():
    $ theme = moment_theme_colors()
    $ unread = moment_unread_count()
    $ hidden_summary = "Сарагийн зөвхөн дотны хүмүүст зориулсан post нээгдсэн." if moment_hidden_post_unlocked else "Story reply + Relationship 35 + Photo clue шаардлагатай."
    $ hidden_action = "НЭЭХ" if moment_hidden_post_unlocked else "Одоогоор түгжээтэй"

    add Solid(theme["bg"])
    use phone_status_bar(dark=theme["status_light"])

    # Brand header inspired by the supplied dark social-feed reference.
    fixed:
        xpos 0
        ypos 42
        xysize (624, 100)

        add Solid(theme["surface"])
        text "moment":
            xpos 24
            ypos 8
            size 42
            bold True
            color theme["text"]
        text "Close people. Hidden moments.":
            xpos 27
            ypos 59
            size 14
            color theme["muted"]
        text "•":
            xpos 141
            ypos 0
            size 30
            color theme["hot"]

        textbutton "STYLE":
            xpos 342
            ypos 22
            xysize (72, 50)
            text_size 12
            text_color theme["muted"]
            text_hover_color theme["accent"]
            background None
            action SetVariable("phone_view", "moment_settings")

        textbutton "ALERT":
            xpos 418
            ypos 22
            xysize (82, 50)
            text_size 12
            text_color theme["text"]
            text_hover_color theme["accent"]
            background None
            action SetVariable("phone_view", "notifications")

        if unread:
            frame:
                xpos 480
                ypos 14
                xysize (25, 25)
                padding (0, 0)
                background Solid(theme["hot"])
                text "[unread]" xalign 0.5 yalign 0.5 size 12 bold True color "#ffffff"

        textbutton "DM":
            xpos 515
            ypos 22
            xysize (80, 50)
            text_size 15
            text_bold True
            text_color theme["text"]
            text_hover_color theme["accent_alt"]
            background None
            action Function(phone_open_chat)

        add Solid(theme["line"]) ypos 98 ysize 2

    frame:
        xpos 0
        ypos 142
        xysize (624, 118)
        padding (12, 4)
        background Solid(theme["surface"])

        hbox:
            spacing 15

            use moment_story_item(
                "Таны story",
                "+",
                theme["accent_alt"],
                target=None,
            )
            use moment_story_item(
                "Сара",
                "S",
                theme["hot"],
                target="story",
            )
            use moment_story_item(
                "Тэмүүжин",
                "T",
                theme["accent_alt"],
                target=None,
            )
            use moment_story_item(
                "Анги",
                "A",
                theme["success"],
                target=None,
            )
            use moment_story_item(
                "Нууц",
                "?",
                theme["accent"],
                target="hidden_post",
                locked=not moment_hidden_post_unlocked,
            )

    viewport:
        xpos 0
        ypos 260
        xsize 624
        ysize 652
        mousewheel True
        draggable True
        scrollbars None

        vbox:
            xsize 624
            spacing 2

            # Sara's post contains the first interactive photo clue.
            fixed:
                xysize (624, 78)
                add Solid(theme["surface"])

                text "●" xpos 17 yalign 0.5 size 58 color theme["hot"]
                text "S" xpos 38 xanchor 0.5 yalign 0.5 size 20 bold True color "#ffffff"
                text "sara.light" xpos 78 ypos 13 size 21 bold True color theme["text"]
                textbutton "PIN · Нуурын эрэг":
                    xpos 70
                    ypos 39
                    text_size 14
                    text_color theme["accent_alt"]
                    text_hover_color theme["accent"]
                    background None
                    action [
                        SetVariable("moment_selected_location", "lake"),
                        SetVariable("phone_view", "location"),
                    ]
                text "•••" xpos 588 xanchor 1.0 ypos 16 size 20 color theme["muted"]

            fixed:
                xysize (624, 340)
                clipping True

                add "pWallpaper" xysize (624, 936) ypos -250
                add Solid("#02061742")
                add Solid(theme["accent"] + "24") ypos 276 ysize 64

                text "1/3":
                    xpos 594
                    xanchor 1.0
                    ypos 16
                    size 15
                    bold True
                    color "#ffffff"

                if "blade_reflection" in moment_found_clues:
                    frame:
                        xpos 411
                        ypos 278
                        xysize (190, 46)
                        padding (10, 8)
                        background Solid("#064e3bde")
                        text "CLUE FOUND":
                            xalign 0.5
                            yalign 0.5
                            size 14
                            bold True
                            color "#a7f3d0"
                else:
                    textbutton "PHOTO CLUE":
                        xpos 411
                        ypos 278
                        xysize (190, 46)
                        text_size 14
                        text_bold True
                        text_color "#ffffff"
                        text_hover_color "#ffffff"
                        background Solid(theme["accent"] + "e8")
                        hover_background Solid(theme["accent_alt"] + "e8")
                        action Function(moment_collect_clue, "blade_reflection")

            fixed:
                xysize (624, 70)
                add Solid(theme["surface"])

                text "♥" xpos 22 yalign 0.5 size 35 color theme["hot"]
                text "2.4K" xpos 65 yalign 0.5 size 18 color theme["text"]
                text "COMMENT 126" xpos 145 yalign 0.5 size 15 color theme["text"]
                textbutton "DM":
                    xpos 538
                    yalign 0.5
                    text_size 16
                    text_bold True
                    text_color theme["accent_alt"]
                    background None
                    action Function(phone_open_chat)

            frame:
                xfill True
                ysize 126
                padding (22, 10)
                background Solid(theme["surface"])

                vbox:
                    spacing 5
                    text "{b}sara.light{/b}  Зарим зураг дурсамжаас илүү зүйл хадгалдаг.":
                        size 18
                        color theme["text"]
                    text "Зургийн жижиг деталыг анзаарч чадна гэж бодож байна.":
                        size 17
                        color theme["text"]
                    text "3 минутын өмнө":
                        size 14
                        color theme["muted"]

            # A second post connects the feed to the location system.
            fixed:
                xysize (624, 76)
                add Solid(theme["surface"])

                text "●" xpos 17 yalign 0.5 size 56 color theme["accent_alt"]
                text "T" xpos 38 xanchor 0.5 yalign 0.5 size 20 bold True color "#ffffff"
                text "temuulen.jpg" xpos 78 ypos 13 size 20 bold True color theme["text"]
                text "Хотын төв · 23:10" xpos 78 ypos 41 size 14 color theme["muted"]

            fixed:
                xysize (624, 238)
                add Solid("#071a32")
                add Solid(theme["accent_alt"] + "45") xpos 0 ypos 128 xysize (624, 110)
                add Solid("#f59e0b55") xpos 46 ypos 38 xysize (90, 160)
                add Solid("#ef444455") xpos 160 ypos 72 xysize (108, 126)
                add Solid("#8b5cf655") xpos 304 ypos 52 xysize (118, 146)
                text "ШӨНИЙН ГУДАМЖ":
                    xalign 0.5
                    ypos 84
                    size 27
                    bold True
                    color "#ffffff"

                if "blue_pin" in moment_found_clues:
                    text "LOCATION CLUE FOUND":
                        xpos 594
                        xanchor 1.0
                        ypos 199
                        size 13
                        bold True
                        color "#a7f3d0"
                else:
                    textbutton "CHECK PIN":
                        xpos 456
                        ypos 184
                        xysize (145, 42)
                        text_size 13
                        text_bold True
                        text_color "#ffffff"
                        background Solid(theme["accent_alt"] + "e8")
                        action Function(moment_collect_clue, "blue_pin")

            frame:
                xfill True
                ysize 92
                padding (22, 12)
                background Solid(theme["surface"])

                text "{b}temuulen.jpg{/b}  Хот унтсан ч зарим газар сэрүүн байдаг.":
                    size 17
                    color theme["text"]

            # Hidden post status is always visible so the player understands
            # how story replies, relationship, and clues connect.
            button:
                xsize 624
                ysize 180
                padding (22, 18)
                background Solid(theme["surface_alt"])
                hover_background Solid(theme["accent"] + "35")
                action Function(moment_open_hidden_post)

                vbox:
                    spacing 9
                    text "HIDDEN POST":
                        size 16
                        bold True
                        color (theme["hot"] if moment_hidden_post_unlocked else theme["muted"])
                    text hidden_summary:
                        size 20
                        bold True
                        color theme["text"]
                    text "Relationship: [moment_relationship]/100":
                        size 15
                        color theme["accent_alt"]
                    text hidden_action:
                        size 14
                        bold True
                        color (theme["success"] if moment_hidden_post_unlocked else theme["muted"])

            null height 24

    use moment_bottom_nav("home")


screen phone_moment_story():
    $ theme = moment_theme_colors()

    add Solid("#030407")

    fixed:
        xysize (624, 984)
        clipping True

        add "pWallpaper" xysize (624, 936) ypos 48
        add Solid("#02061755")
        add Solid("#000000b8") ypos 678 ysize 306

    use phone_status_bar(dark=True)

    hbox:
        xpos 18
        ypos 51
        spacing 5

        for segment in range(3):
            add Solid("#ffffff" if segment == 0 else "#ffffff55") xysize (192, 4)

    text "●" xpos 18 ypos 70 size 54 color theme["hot"]
    text "S" xpos 36 xanchor 0.5 ypos 84 size 18 bold True color "#ffffff"
    text "sara.light  ·  2м":
        xpos 72
        ypos 84
        size 18
        bold True
        color "#ffffff"

    textbutton "×":
        xpos 586
        xanchor 1.0
        ypos 68
        text_size 35
        text_color "#ffffff"
        background None
        action SetVariable("phone_view", "social")

    frame:
        xpos 24
        ypos 532
        xysize (576, 126)
        padding (20, 16)
        background Solid("#0000009c")

        vbox:
            spacing 8
            text "Энэ газар өмнө нь харж байсан юм шиг санагдахгүй байна уу?":
                size 24
                bold True
                color "#ffffff"
            text "Story reply нь Сарагийн Relationship оноонд нөлөөлнө.":
                size 15
                color "#d1d5db"

    frame:
        xpos 0
        ypos 678
        xysize (624, 306)
        padding (24, 17)
        background Solid(theme["surface"] + "f2")

        vbox:
            spacing 10

            text "STORY REPLY":
                size 15
                bold True
                color theme["accent_alt"]

            if moment_story_replied:
                text "Та энэ story-д аль хэдийн хариулсан.":
                    size 20
                    color theme["text"]
                textbutton "DM РҮҮ ОРОХ":
                    xsize 576
                    ysize 62
                    text_size 18
                    text_bold True
                    text_color "#ffffff"
                    background Solid(theme["accent"])
                    action Function(phone_open_chat)
            else:
                textbutton "“Тийм ээ, арын тусгал их сонин байна.”  +12":
                    xsize 576
                    ysize 55
                    text_size 16
                    text_color theme["text"]
                    text_hover_color "#ffffff"
                    background Solid(theme["surface_alt"])
                    hover_background Solid(theme["accent"])
                    action Function(
                        moment_reply_story,
                        "Тийм ээ, арын тусгал их сонин байна.",
                        12,
                    )
                textbutton "“Дахиад хамт очъё.”  +10":
                    xsize 576
                    ysize 55
                    text_size 16
                    text_color theme["text"]
                    text_hover_color "#ffffff"
                    background Solid(theme["surface_alt"])
                    hover_background Solid(theme["accent"])
                    action Function(
                        moment_reply_story,
                        "Дахиад хамт очъё.",
                        10,
                    )
                textbutton "“Гоё зураг болжээ.”  +8":
                    xsize 576
                    ysize 55
                    text_size 16
                    text_color theme["text"]
                    text_hover_color "#ffffff"
                    background Solid(theme["surface_alt"])
                    hover_background Solid(theme["accent"])
                    action Function(
                        moment_reply_story,
                        "Гоё зураг болжээ.",
                        8,
                    )


screen phone_moment_notifications():
    $ theme = moment_theme_colors()
    $ unread = moment_unread_count()

    add Solid(theme["bg"])
    use moment_page_header(
        "Notifications",
        back_target="social",
        right_label="БҮГДИЙГ УНШИХ",
        right_target="notifications",
    )

    textbutton "БҮГДИЙГ УНШСАН БОЛГОХ":
        xpos 334
        ypos 122
        xysize (270, 46)
        text_size 13
        text_color theme["accent_alt"]
        text_hover_color theme["accent"]
        background None
        action Function(moment_mark_all_notifications)

    text "[unread] шинэ мэдэгдэл":
        xpos 22
        ypos 136
        size 16
        color theme["muted"]

    viewport:
        xpos 0
        ypos 176
        xsize 624
        ysize 808
        mousewheel True
        draggable True
        scrollbars None

        vbox:
            xsize 624
            spacing 2

            for index, notice in enumerate(moment_notifications):
                button:
                    xsize 624
                    ysize 112
                    padding (20, 14)
                    background Solid(
                        theme["accent"] + "24"
                        if not notice.get("read", False)
                        else theme["surface"]
                    )
                    hover_background Solid(theme["surface_alt"])
                    action Function(moment_open_notification, index)

                    hbox:
                        spacing 15

                        fixed:
                            xysize (56, 56)
                            text "●":
                                xalign 0.5
                                yalign 0.5
                                size 56
                                color (
                                    theme["hot"]
                                    if not notice.get("read", False)
                                    else theme["muted"]
                                )
                            text "!":
                                xalign 0.5
                                yalign 0.5
                                size 21
                                bold True
                                color "#ffffff"

                        vbox:
                            xsize 495
                            spacing 5
                            text notice["title"]:
                                size 19
                                bold True
                                color theme["text"]
                            text notice["body"]:
                                xmaximum 490
                                size 15
                                color theme["muted"]


screen phone_moment_settings():
    $ theme = moment_theme_colors()

    add Solid(theme["bg"])
    use moment_page_header("Moment style", back_target="social")

    text "Өнгөний загвар":
        xpos 24
        ypos 142
        size 22
        bold True
        color theme["text"]
    text "Тоглоомын явцад хүссэн үедээ сольж болно.":
        xpos 24
        ypos 176
        size 15
        color theme["muted"]

    vbox:
        xpos 24
        ypos 224
        spacing 18

        for theme_name in MOMENT_THEME_ORDER:
            $ option = MOMENT_THEMES[theme_name]
            $ option_state = "ИДЭВХТЭЙ" if moment_theme == theme_name else "Сонгох"

            button:
                xysize (576, 150)
                padding (18, 16)
                background Solid(
                    option["accent"] + "32"
                    if moment_theme == theme_name
                    else theme["surface"]
                )
                hover_background Solid(option["accent"] + "45")
                action Function(moment_set_theme, theme_name)

                vbox:
                    spacing 12

                    hbox:
                        spacing 12
                        add Solid(option["bg"]) xysize (66, 42)
                        add Solid(option["surface_alt"]) xysize (66, 42)
                        add Solid(option["accent"]) xysize (66, 42)
                        add Solid(option["accent_alt"]) xysize (66, 42)
                        add Solid(option["hot"]) xysize (66, 42)

                    text option["name"]:
                        size 22
                        bold True
                        color theme["text"]
                    text option_state:
                        size 13
                        bold True
                        color (
                            option["success"]
                            if moment_theme == theme_name
                            else theme["muted"]
                        )

    textbutton "THEME-Г ШУУД СОЛИХ":
        xpos 24
        ypos 770
        xysize (576, 62)
        text_size 17
        text_bold True
        text_color "#ffffff"
        background Solid(theme["accent"])
        hover_background Solid(theme["accent_alt"])
        action Function(moment_cycle_theme)


screen phone_moment_relationship():
    $ theme = moment_theme_colors()
    $ relationship_width = int(540 * moment_relationship / 100.0)

    add Solid(theme["bg"])
    use moment_page_header("Relationship", back_target="social", right_label="DM", right_target="chat")

    fixed:
        xpos 24
        ypos 142
        xysize (576, 222)

        add Solid(theme["surface"])
        text "●" xpos 28 ypos 22 size 98 color theme["hot"]
        text "S" xpos 77 xanchor 0.5 ypos 52 size 34 bold True color "#ffffff"
        text "Сара" xpos 142 ypos 26 size 30 bold True color theme["text"]
        text "[moment_relationship_level()]" xpos 142 ypos 70 size 18 color theme["accent_alt"]
        text "[moment_relationship]/100" xpos 546 xanchor 1.0 ypos 38 size 25 bold True color theme["text"]

        add Solid(theme["line"]) xpos 18 ypos 138 xysize (540, 18)
        if relationship_width > 0:
            add Solid(theme["accent"]) xpos 18 ypos 138 xysize (relationship_width, 18)

        text "Story reply, DM, clue болон сонголтууд энэ оноонд нөлөөлнө.":
            xpos 18
            ypos 174
            xmaximum 540
            size 15
            color theme["muted"]

    frame:
        xpos 24
        ypos 388
        xysize (576, 154)
        padding (18, 15)
        background Solid(theme["surface_alt"])

        vbox:
            spacing 9
            text "HIDDEN POST НӨХЦӨЛ":
                size 15
                bold True
                color theme["hot"]
            text "Story reply":
                size 17
                color (theme["success"] if moment_story_replied else theme["muted"])
            text "Relationship 35+":
                size 17
                color (theme["success"] if moment_relationship >= 35 else theme["muted"])
            text "Илдний тусгал photo clue":
                size 17
                color (
                    theme["success"]
                    if "blade_reflection" in moment_found_clues
                    else theme["muted"]
                )

    text "Сүүлийн өөрчлөлтүүд":
        xpos 24
        ypos 570
        size 20
        bold True
        color theme["text"]

    vbox:
        xpos 24
        ypos 610
        spacing 8

        for event in moment_relationship_events[:5]:
            frame:
                xysize (576, 48)
                padding (15, 10)
                background Solid(theme["surface"])
                text event size 15 color theme["text"]

    use moment_bottom_nav("relationship")


screen phone_moment_clues():
    $ theme = moment_theme_colors()
    $ clue_count = len(moment_found_clues)

    add Solid(theme["bg"])
    use moment_page_header("Photo clues", back_target="social", right_label="MAP", right_target="location")

    fixed:
        xpos 24
        ypos 140
        xysize (576, 108)

        add Solid(theme["surface_alt"])
        text "ЦУГЛУУЛГА":
            xpos 18
            ypos 17
            size 15
            bold True
            color theme["accent_alt"]
        text "[clue_count]/3":
            xpos 550
            xanchor 1.0
            ypos 12
            size 32
            bold True
            color theme["text"]
        add Solid(theme["line"]) xpos 18 ypos 72 xysize (540, 14)
        if clue_count:
            add Solid(theme["accent"]) xpos 18 ypos 72 xysize (int(540 * clue_count / 3.0), 14)

    vbox:
        xpos 24
        ypos 272
        spacing 14

        for clue_id in ("blade_reflection", "blue_pin", "station_ticket"):
            $ clue = MOMENT_CLUES[clue_id]
            $ found = clue_id in moment_found_clues

            frame:
                xysize (576, 154)
                padding (18, 16)
                background Solid(theme["surface"] if found else theme["surface_alt"])

                hbox:
                    spacing 16

                    fixed:
                        xysize (76, 76)
                        add Solid(theme["accent"] if found else theme["line"])
                        text ("✓" if found else "?"):
                            xalign 0.5
                            yalign 0.5
                            size 31
                            bold True
                            color "#ffffff"

                    vbox:
                        xsize 440
                        spacing 5
                        text (clue["title"] if found else "Нээгдээгүй clue"):
                            size 20
                            bold True
                            color theme["text"]
                        text (clue["description"] if found else "Moment feed-ийн зураг дотроос хайна уу."):
                            xmaximum 430
                            size 15
                            color theme["muted"]
                        text (clue["location"] if found else "Байршил нууц"):
                            size 14
                            color (theme["accent_alt"] if found else theme["muted"])

    use moment_bottom_nav("clues")


screen phone_moment_location():
    $ theme = moment_theme_colors()
    $ station_known = (
        "blue_pin" in moment_found_clues
        or "station_ticket" in moment_found_clues
    )

    add Solid(theme["bg"])
    use moment_page_header("Locations", back_target="social", right_label="CLUES", right_target="clues")

    fixed:
        xpos 24
        ypos 140
        xysize (576, 348)
        clipping True

        add Solid("#071a2c")
        add Solid(theme["accent_alt"] + "28") xpos 0 ypos 190 xysize (576, 158)
        add Solid(theme["line"]) xpos 60 ypos 54 xysize (450, 4)
        add Solid(theme["line"]) xpos 92 ypos 154 xysize (380, 4)
        add Solid(theme["line"]) xpos 46 ypos 256 xysize (466, 4)
        text "●" xpos 86 ypos 89 size 44 color theme["accent_alt"]
        text "●" xpos 420 ypos 196 size 44 color (theme["hot"] if station_known else theme["muted"])
        text "НУУР" xpos 70 ypos 133 size 14 bold True color "#ffffff"
        text "БУУДАЛ" xpos 393 ypos 241 size 14 bold True color "#ffffff"
        text "INTERACTIVE LOCATION MAP":
            xpos 18
            ypos 18
            size 14
            bold True
            color "#ffffffaa"

    hbox:
        xpos 24
        ypos 508
        spacing 12

        textbutton "НУУРЫН ЭРЭГ":
            xysize (282, 62)
            text_size 15
            text_bold True
            text_color "#ffffff"
            background Solid(
                theme["accent_alt"]
                if moment_selected_location == "lake"
                else theme["surface_alt"]
            )
            action Function(moment_open_location, "lake")

        textbutton "ХУУЧИН БУУДАЛ":
            xysize (282, 62)
            text_size 15
            text_bold True
            text_color ("#ffffff" if station_known else theme["muted"])
            background Solid(
                theme["hot"]
                if moment_selected_location == "station" and station_known
                else theme["surface_alt"]
            )
            sensitive station_known
            action Function(moment_open_location, "station")

    frame:
        xpos 24
        ypos 592
        xysize (576, 238)
        padding (20, 18)
        background Solid(theme["surface"])

        if moment_selected_location == "station" and station_known:
            vbox:
                spacing 10
                text "Хуучин буудал · 04-р тавцан":
                    size 24
                    bold True
                    color theme["text"]
                text "Сарагийн зураг болон нууц post хоёр энэ байршилтай холбоотой.":
                    size 17
                    color theme["muted"]
                text "Олдсон мэдээлэл: 23:10 · хаалттай тавцан":
                    size 15
                    color theme["accent_alt"]
                textbutton "HIDDEN POST ШАЛГАХ":
                    xsize 520
                    ysize 54
                    text_size 15
                    text_color "#ffffff"
                    background Solid(theme["accent"])
                    sensitive moment_hidden_post_unlocked
                    action Function(moment_open_hidden_post)
        else:
            vbox:
                spacing 10
                text "Нуурын эрэг":
                    size 24
                    bold True
                    color theme["text"]
                text "Сарагийн хамгийн сүүлийн post нийтлэгдсэн газар.":
                    size 17
                    color theme["muted"]
                text "Clue: арын тусгалыг шалгах":
                    size 15
                    color theme["accent_alt"]
                textbutton "POST РУУ БУЦАХ":
                    xsize 520
                    ysize 54
                    text_size 15
                    text_color "#ffffff"
                    background Solid(theme["accent"])
                    action SetVariable("phone_view", "social")

    use moment_bottom_nav("location")


screen phone_moment_hidden_post():
    $ theme = moment_theme_colors()

    add Solid(theme["bg"])
    use moment_page_header("Hidden post", back_target="social", right_label="BOND", right_target="relationship")

    if not moment_hidden_post_unlocked:
        fixed:
            xpos 24
            ypos 180
            xysize (576, 520)

            add Solid(theme["surface"])
            text "LOCKED":
                xalign 0.5
                ypos 80
                size 38
                bold True
                color theme["muted"]
            text "Story reply, Relationship 35 болон Илдний тусгал clue хэрэгтэй.":
                xalign 0.5
                ypos 160
                xmaximum 500
                text_align 0.5
                size 21
                color theme["text"]
            textbutton "RELATIONSHIP ШАЛГАХ":
                xalign 0.5
                ypos 270
                xysize (430, 62)
                text_size 17
                text_color "#ffffff"
                background Solid(theme["accent"])
                action SetVariable("phone_view", "relationship")
    else:
        viewport:
            xpos 0
            ypos 118
            xsize 624
            ysize 866
            mousewheel True
            draggable True
            scrollbars None

            vbox:
                xsize 624
                spacing 0

                fixed:
                    xysize (624, 80)
                    add Solid(theme["surface"])
                    text "●" xpos 18 yalign 0.5 size 58 color theme["hot"]
                    text "S" xpos 39 xanchor 0.5 yalign 0.5 size 20 bold True color "#ffffff"
                    text "sara.light" xpos 78 ypos 16 size 21 bold True color theme["text"]
                    text "Close Friends · зөвхөн танд" xpos 78 ypos 44 size 14 color theme["success"]

                fixed:
                    xysize (624, 410)
                    add Solid("#111827")
                    add "pWallpaper" xysize (420, 630) xpos 204 ypos -80 alpha 0.52
                    add Solid(theme["accent"] + "35") xpos 0 ypos 0 xysize (230, 410)
                    add Solid("#00000055")
                    text "04":
                        xpos 52
                        ypos 88
                        size 112
                        bold True
                        color "#ffffff"
                    text "ТАВЦАН":
                        xpos 58
                        ypos 208
                        size 25
                        bold True
                        color theme["accent_alt"]
                    text "23:10":
                        xpos 58
                        ypos 251
                        size 19
                        color "#d1d5db"

                    if "station_ticket" in moment_found_clues:
                        text "TICKET CLUE FOUND":
                            xpos 596
                            xanchor 1.0
                            ypos 362
                            size 14
                            bold True
                            color "#a7f3d0"
                    else:
                        textbutton "CHECK TICKET":
                            xpos 420
                            ypos 348
                            xysize (180, 48)
                            text_size 14
                            text_bold True
                            text_color "#ffffff"
                            background Solid(theme["hot"])
                            action Function(moment_collect_clue, "station_ticket")

                frame:
                    xfill True
                    ysize 210
                    padding (24, 18)
                    background Solid(theme["surface"])

                    vbox:
                        spacing 10
                        text "{b}sara.light{/b}  Энэ зургийг нийтэд харуулахыг хүссэнгүй.":
                            size 20
                            color theme["text"]
                        text "Маргааш 23:10-д 04-р тавцанд очих хэрэгтэй юм шиг байна. Гэхдээ ганцаараа биш.":
                            size 18
                            color theme["text"]
                        text "Hidden post · Relationship [moment_relationship]/100":
                            size 14
                            color theme["muted"]

                textbutton "САРАД DM БИЧИХ":
                    xalign 0.5
                    xysize (576, 64)
                    text_size 18
                    text_bold True
                    text_color "#ffffff"
                    background Solid(theme["accent"])
                    action Function(phone_open_chat)

                null height 30


screen phone_moment_dm():
    $ theme = moment_theme_colors()

    add Solid(theme["bg"])
    use phone_status_bar(dark=theme["status_light"])

    fixed:
        xpos 0
        ypos 42
        xysize (624, 82)

        add Solid(theme["surface"])
        add Solid(theme["line"]) ypos 80 ysize 2

        textbutton "<":
            xpos 10
            yalign 0.5
            xysize (55, 58)
            text_size 34
            text_color theme["text"]
            text_hover_color theme["accent"]
            background None
            action SetVariable("phone_view", "social")

        text "●" xpos 66 yalign 0.5 size 58 color theme["hot"]
        text "S" xpos 87 xanchor 0.5 yalign 0.5 size 20 bold True color "#ffffff"
        text "Сара" xpos 124 ypos 13 size 23 bold True color theme["text"]
        text "идэвхтэй байна" xpos 124 ypos 45 size 14 color theme["success"]

        textbutton "BOND [moment_relationship]":
            xpos 594
            xanchor 1.0
            yalign 0.5
            text_size 14
            text_color theme["accent_alt"]
            text_hover_color theme["accent"]
            background None
            action SetVariable("phone_view", "relationship")

    fixed:
        xpos 0
        ypos 124
        xysize (624, 38)

        add Solid(theme["surface_alt"])
        text "[moment_relationship_level()] · Story reply болон clue нь харилцаанд нөлөөлнө":
            xalign 0.5
            yalign 0.5
            size 13
            color theme["muted"]

    viewport:
        id "moment_dm_viewport"
        xpos 18
        ypos 174
        xsize 588
        ysize 656
        mousewheel True
        draggable True
        scrollbars None
        yinitial 1.0

        vbox:
            xsize 588
            spacing 12

            text "ӨНӨӨДӨР":
                xalign 0.5
                size 13
                bold True
                color theme["muted"]

            for msg in sara_messages:
                if msg["sender"] == "player":
                    frame:
                        xalign 1.0
                        xmaximum 448
                        padding (17, 11)
                        background Solid(theme["accent"])

                        vbox:
                            spacing 5
                            text msg["text"]:
                                size 19
                                color "#ffffff"
                            text msg.get("time", ""):
                                xalign 1.0
                                size 12
                                color "#e9d5ff"
                else:
                    hbox:
                        xalign 0.0
                        spacing 9

                        fixed:
                            yalign 1.0
                            xysize (36, 36)
                            text "●" xalign 0.5 yalign 0.5 size 36 color theme["hot"]
                            text "S" xalign 0.5 yalign 0.5 size 14 bold True color "#ffffff"

                        frame:
                            xmaximum 430
                            padding (17, 11)
                            background Solid(theme["surface_alt"])

                            vbox:
                                spacing 5
                                text msg["text"]:
                                    size 19
                                    color theme["text"]
                                text msg.get("time", ""):
                                    size 12
                                    color theme["muted"]

            if sara_is_typing:
                hbox:
                    spacing 9
                    fixed:
                        yalign 1.0
                        xysize (36, 36)
                        text "●" xalign 0.5 yalign 0.5 size 36 color theme["hot"]
                        text "S" xalign 0.5 yalign 0.5 size 14 bold True color "#ffffff"
                    frame:
                        padding (17, 11)
                        background Solid(theme["surface_alt"])
                        text "Сара бичиж байна..." size 16 color theme["muted"]

    if sara_is_typing:
        timer 1.25 action Function(phone_finish_mock_reply)

    frame:
        xpos 0
        ypos 840
        xysize (624, 72)
        padding (12, 9)
        background Solid(theme["surface"])

        hbox:
            spacing 8

            frame:
                xysize (478, 54)
                padding (15, 8)
                background Solid(theme["surface_alt"])

                input:
                    value VariableInputValue("phone_chat_input")
                    length 180
                    xsize 445
                    yalign 0.5
                    size 18
                    color theme["text"]
                    caret Solid(theme["accent_alt"])
                    default_focus True

            textbutton "ИЛГЭЭХ":
                xysize (112, 54)
                text_size 14
                text_bold True
                text_color "#ffffff"
                background Solid(theme["accent"])
                hover_background Solid(theme["accent_alt"])
                sensitive bool(phone_chat_input.strip()) and not sara_is_typing
                action Function(moment_send_dm)

    use moment_bottom_nav("dm")
