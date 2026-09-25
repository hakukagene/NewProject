# Moment social app.
#
# The app is intentionally data-driven so story replies, direct messages,
# relationship progress, close-friend content, notifications, and profiles
# can be connected to later chapters without rebuilding the UI.


default moment_theme = "midnight"
default moment_relationship = 28
default sara_mood = "neutral"
default sara_boundary_strikes = 0
default sara_blocked = False
default sara_cooldown_until = 0.0
default moment_story_replied = False
default moment_active_contact = "sara"
default moment_profile_handle = "tsogoo.player"
default moment_profile_name = "Цогтоо"
default moment_profile_bio = "Нууцлаг аялал, дурсамж, ойр хүмүүс."
default moment_feed_carousel_index = 0
default moment_feed_carousel_pending_index = None
default moment_story_index = 0
default moment_close_story_index = 0
default moment_contact_unread = {
    "sara": 2,
    "misheel": 0,
    "temuulen": 1,
    "class_chat": 0,
}
default moment_other_dm_messages = {
    "misheel": [
        {"sender": "contact", "text": "Маргаашийн хичээл хэдээс билээ?", "time": "14:32"},
    ],
    "temuulen": [
        {"sender": "contact", "text": "Шөнийн зургийг харсан уу?", "time": "13:18"},
    ],
    "class_chat": [
        {"sender": "contact", "text": "Аяллын зургуудыг энд оруулаарай.", "time": "12:04"},
    ],
}
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
]


init python:
    import time
    import unicodedata

    MOMENT_THEME_ORDER = ("midnight", "violet", "daylight")
    MOMENT_CLOSE_FRIEND_THRESHOLD = 60


    def moment_chat_draft_rows(value):
        """Reserve vertical space for a wrapped draft, capped at nine lines."""
        rows = 1
        columns = 0
        for character in value:
            if character == "\n":
                rows += 1
                columns = 0
                continue
            width = 2 if unicodedata.east_asian_width(character) in ("W", "F") else 1
            if columns + width > 18:
                rows += 1
                columns = 0
            columns += width
        return min(9, rows)
    MOMENT_FEED_CAROUSEL_WIDTH = 624
    MOMENT_FEED_CAROUSEL_SLIDE_COUNT = 3
    MOMENT_FEED_CAROUSEL_SWIPE_DISTANCE = 80
    MOMENT_REMOVED_NOTIFICATION_IDS = (
        "photo_hint",
        "hidden_post_unlock",
    )

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

    MOMENT_CONTACT_ORDER = (
        "sara",
        "misheel",
        "temuulen",
        "class_chat",
    )

    MOMENT_CONTACTS = {
        "sara": {
            "name": "Сара",
            "handle": "sara.light",
            "initial": "S",
            "color": "#ff3d71",
            "preview": "Маргааш дахиад очвол ямар вэ?",
            "status": "Идэвхтэй байна",
        },
        "misheel": {
            "name": "Мишээл",
            "handle": "misheel.qqq",
            "initial": "M",
            "color": "#8b5cf6",
            "preview": "Маргаашийн хичээл хэдээс билээ?",
            "status": "Seen 29m ago",
        },
        "temuulen": {
            "name": "Тэмүүжин",
            "handle": "temuulen.jpg",
            "initial": "T",
            "color": "#22d3ee",
            "preview": "Шөнийн зургийг харсан уу?",
            "status": "Sent 44m ago",
        },
        "class_chat": {
            "name": "Манай анги",
            "handle": "class.room",
            "initial": "A",
            "color": "#34d399",
            "preview": "Аяллын зургуудыг энд оруулаарай.",
            "status": "4 хүн идэвхтэй",
        },
    }

    # A photo can use a short display time, while a future video Story can set
    # duration_seconds to its real media duration. The timer and progress bar
    # read this value directly, so each Story advances at its own pace.
    MOMENT_SARA_STORIES = (
        {
            "duration_seconds": 7.0,
            "age": "2м",
            "wallpaper_y": 48,
            "tint": "#02061755",
            "title": "Энэ газар өмнө нь харж байсан юм шиг санагдахгүй байна уу?",
            "subtitle": "Story reply нь Сарагийн Relationship оноонд нөлөөлнө.",
        },
        {
            "duration_seconds": 5.5,
            "age": "1м",
            "wallpaper_y": -42,
            "tint": "#312e814d",
            "title": "Нуурын эрэг өнөө орой бүр ч нам гүм байна.",
            "subtitle": "Зүүн тал руу дарвал өмнөх Story, баруун тал руу дарвал дараагийн Story.",
        },
        {
            "duration_seconds": 8.0,
            "age": "одоо",
            "wallpaper_y": -128,
            "tint": "#0e74904d",
            "title": "Маргааш энд дахин ирэх үү?",
            "subtitle": "Энэ Story дуусахад дараагийн боломжтой Story автоматаар нээгдэнэ.",
        },
    )

    MOMENT_CLOSE_FRIEND_STORIES = (
        {
            "duration_seconds": 9.0,
            "age": "Close Friends",
            "wallpaper_y": 48,
            "tint": "#052e244d",
            "title": "Маргаашийн аяллын төлөвлөгөөг зөвхөн ойр хүмүүстээ хуваалцлаа.",
            "subtitle": "Чамайг ирнэ гэж найдаж байна.",
        },
    )


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


    def moment_feed_carousel_drag_position(x, y):
        """Keep the post gallery on its horizontal three-slide track."""
        min_x = -(
            (MOMENT_FEED_CAROUSEL_SLIDE_COUNT - 1)
            * MOMENT_FEED_CAROUSEL_WIDTH
        )
        return min(0, max(min_x, x)), 0


    def moment_feed_carousel_dragged(drags, drop):
        """Snap a completed swipe to the previous or next post image."""
        gallery = drags[0]
        current = max(
            0,
            min(
                MOMENT_FEED_CAROUSEL_SLIDE_COUNT - 1,
                renpy.store.moment_feed_carousel_index,
            ),
        )
        distance = gallery.x - gallery.start_x
        target = current

        if distance <= -MOMENT_FEED_CAROUSEL_SWIPE_DISTANCE:
            target = min(MOMENT_FEED_CAROUSEL_SLIDE_COUNT - 1, current + 1)
        elif distance >= MOMENT_FEED_CAROUSEL_SWIPE_DISTANCE:
            target = max(0, current - 1)

        renpy.store.moment_feed_carousel_pending_index = target
        gallery.snap(-target * MOMENT_FEED_CAROUSEL_WIDTH, 0, 0.22)


    def moment_feed_carousel_snapped(gallery, x, y, completed):
        """Commit the selected slide only after the snap animation ends."""
        pending = renpy.store.moment_feed_carousel_pending_index
        if not completed or pending is None:
            renpy.store.moment_feed_carousel_pending_index = None
            return

        renpy.store.moment_feed_carousel_index = pending
        renpy.store.moment_feed_carousel_pending_index = None
        renpy.restart_interaction()


    def moment_relationship_level():
        if renpy.store.sara_blocked:
            return "Харилцаа тасарсан"
        value = renpy.store.moment_relationship
        if value >= 80:
            return "Онцгой хүн"
        if value >= 60:
            return "Дотны хүн"
        if value >= 35:
            return "Дотносож байна"
        return "Танил"


    def moment_is_close_friend():
        return (
            renpy.store.moment_relationship
            >= MOMENT_CLOSE_FRIEND_THRESHOLD
            and not renpy.store.sara_blocked
        )


    def sara_mood_label():
        if renpy.store.sara_blocked:
            return "Харилцаагаа зогсоосон"
        if renpy.store.sara_cooldown_until > time.time():
            return "Түр завсарлага авсан"
        return {
            "neutral": "Тайван", "warm": "Дотно", "guarded": "Болгоомжтой",
            "upset": "Гомдсон",
        }.get(renpy.store.sara_mood, "Тайван")


    def moment_active_notifications():
        """Hide notifications from the removed clue/hidden-post systems."""
        visible = []
        for item in renpy.store.moment_notifications:
            notice_id = item.get("id", "")
            if notice_id in MOMENT_REMOVED_NOTIFICATION_IDS:
                continue
            if notice_id.startswith("clue_"):
                continue
            visible.append(item)
        return visible


    def moment_unread_count():
        return sum(
            1 for item in moment_active_notifications()
            if not item.get("read", False)
        )


    def moment_dm_unread_count():
        unread = dict(renpy.store.moment_contact_unread)
        unread["sara"] = max(
            unread.get("sara", 0),
            renpy.store.sara_unread_messages,
        )
        return sum(unread.values())


    def moment_active_contact_data():
        if story_active:
            return STORY_CONTACTS.get(renpy.store.moment_active_contact, STORY_CONTACTS["sara"])
        return MOMENT_CONTACTS.get(
            renpy.store.moment_active_contact,
            MOMENT_CONTACTS["sara"],
        )


    def moment_active_messages():
        if renpy.store.moment_active_contact == "sara":
            return renpy.store.sara_messages

        return renpy.store.moment_other_dm_messages.get(
            renpy.store.moment_active_contact,
            [],
        )


    def moment_open_dm_inbox():
        renpy.store.phone_view = "dm"
        renpy.restart_interaction()


    def moment_open_contact(contact_id):
        if contact_id not in (STORY_CONTACTS if story_active else MOMENT_CONTACTS):
            return

        renpy.store.moment_active_contact = contact_id
        unread = dict(renpy.store.moment_contact_unread)
        unread[contact_id] = 0
        renpy.store.moment_contact_unread = unread

        if contact_id == "sara":
            renpy.store.sara_unread_messages = 0

        renpy.store.phone_view = "chat"
        renpy.store.phone_chat_scroll_pending = True
        renpy.restart_interaction()


    def moment_story_safe_index(index, stories):
        if not stories:
            return 0
        return max(0, min(len(stories) - 1, int(index)))


    def moment_open_story(target="story"):
        if target == "close_story":
            if not moment_is_close_friend():
                renpy.notify("Close Friends Story одоогоор нээгдээгүй.")
                return
            renpy.store.moment_close_story_index = 0
        else:
            target = "story"
            renpy.store.moment_story_index = 0

        renpy.store.phone_view = target
        renpy.restart_interaction()


    def moment_advance_story():
        """Advance using the duration stored on the currently displayed Story."""
        if renpy.store.phone_view == "story":
            current = moment_story_safe_index(
                renpy.store.moment_story_index,
                MOMENT_SARA_STORIES,
            )
            if current + 1 < len(MOMENT_SARA_STORIES):
                renpy.store.moment_story_index = current + 1
            elif moment_is_close_friend():
                renpy.store.moment_close_story_index = 0
                renpy.store.phone_view = "close_story"
            else:
                renpy.store.phone_view = "social"
        elif renpy.store.phone_view == "close_story":
            current = moment_story_safe_index(
                renpy.store.moment_close_story_index,
                MOMENT_CLOSE_FRIEND_STORIES,
            )
            if current + 1 < len(MOMENT_CLOSE_FRIEND_STORIES):
                renpy.store.moment_close_story_index = current + 1
            else:
                renpy.store.phone_view = "social"
        else:
            return

        renpy.restart_interaction()


    def moment_previous_story():
        if renpy.store.phone_view == "story":
            current = moment_story_safe_index(
                renpy.store.moment_story_index,
                MOMENT_SARA_STORIES,
            )
            if current > 0:
                renpy.store.moment_story_index = current - 1
            else:
                renpy.store.phone_view = "social"
        elif renpy.store.phone_view == "close_story":
            current = moment_story_safe_index(
                renpy.store.moment_close_story_index,
                MOMENT_CLOSE_FRIEND_STORIES,
            )
            if current > 0:
                renpy.store.moment_close_story_index = current - 1
            elif MOMENT_SARA_STORIES:
                renpy.store.moment_story_index = len(MOMENT_SARA_STORIES) - 1
                renpy.store.phone_view = "story"
            else:
                renpy.store.phone_view = "social"
        else:
            return

        renpy.restart_interaction()


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

        crossed_close_friend = (
            old_value < MOMENT_CLOSE_FRIEND_THRESHOLD
            and new_value >= MOMENT_CLOSE_FRIEND_THRESHOLD
        )
        if crossed_close_friend and not story_active:
            moment_add_notification(
                "Сара таныг Close Friends-д нэмлээ",
                "Нэмэлт story болон post Moment feed-д нээгдлээ.",
                "social",
                "close_friends_unlocked",
            )


    def moment_reply_story(reply_text, relationship_points):
        if renpy.store.sara_blocked:
            renpy.notify("Сара харилцаагаа зогсоосон байна.")
            return
        if renpy.store.moment_story_replied:
            renpy.store.moment_active_contact = "sara"
            renpy.store.phone_view = "chat"
            renpy.store.sara_unread_messages = 0
            renpy.store.phone_chat_scroll_pending = True
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
        renpy.store.moment_active_contact = "sara"
        renpy.store.phone_view = "chat"
        renpy.store.phone_chat_scroll_pending = True
        renpy.restart_interaction()


    def moment_mark_all_notifications():
        updated = []
        for item in moment_active_notifications():
            copy = dict(item)
            copy["read"] = True
            updated.append(copy)

        renpy.store.moment_notifications = updated
        renpy.restart_interaction()


    def moment_open_notification(index):
        visible_notifications = moment_active_notifications()
        if index < 0 or index >= len(visible_notifications):
            return

        updated = []
        target = "social"
        for item_index, item in enumerate(visible_notifications):
            copy = dict(item)
            if item_index == index:
                copy["read"] = True
                target = copy.get("target", "social")
            updated.append(copy)

        renpy.store.moment_notifications = updated
        if target == "hidden_post":
            target = "social"
        if target == "chat":
            renpy.store.moment_active_contact = "sara"
            renpy.store.sara_unread_messages = 0
            renpy.store.phone_chat_scroll_pending = True
        elif target == "story":
            renpy.store.moment_story_index = 0
        elif target == "close_story":
            renpy.store.moment_close_story_index = 0
        renpy.store.phone_view = target
        renpy.restart_interaction()


    def moment_send_dm():
        message = renpy.store.phone_chat_input.strip()
        if not message or renpy.store.sara_is_typing:
            return

        phone_send_message()


    def moment_send_active_dm():
        if renpy.store.moment_active_contact == "sara":
            moment_send_dm()
            return

        if story_active:
            story_send_scripted_dm()
            return

        message = renpy.store.phone_chat_input.strip()
        if not message:
            return

        contact_id = renpy.store.moment_active_contact
        all_messages = dict(renpy.store.moment_other_dm_messages)
        thread = list(all_messages.get(contact_id, []))
        thread.append({
            "sender": "player",
            "text": message,
            "time": phone_current_time(),
        })
        thread.append({
            "sender": "contact",
            "text": "За, ойлголоо. Дараа дэлгэрэнгүй ярья.",
            "time": phone_current_time(),
        })
        all_messages[contact_id] = thread
        renpy.store.moment_other_dm_messages = all_messages
        renpy.store.phone_chat_input = ""
        renpy.store.phone_chat_scroll_pending = True
        renpy.restart_interaction()


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


screen moment_nav_button(icon_path, target, selected=False, badge=0):
    $ theme = moment_theme_colors()
    $ icon_color = theme["accent_alt"] if selected else theme["muted"]
    $ button_width = 144
    $ badge_x = button_width - 36

    button:
        xysize (button_width, 54)
        padding (0, 0)
        background None
        hover_background None
        action SetVariable("phone_view", target)

        fixed:
            xysize (button_width, 54)

            if selected:
                add Transform(
                    AlphaMask(
                        Solid(theme["accent"] + "24", xysize=(118, 54)),
                        "images/phoneUI/Momenticon/nav_pill_mask.svg",
                    ),
                    xysize=(button_width, 54),
                )

            add Transform(
                AlphaMask(
                    Solid(icon_color, xysize=(512, 512)),
                    icon_path,
                ),
                xysize=(42, 34),
                xalign=0.5,
                yalign=0.5,
            )

            if badge:
                frame:
                    xpos badge_x
                    ypos 5
                    xysize (24, 24)
                    padding (0, 0)
                    background Solid(theme["hot"])
                    text "[badge]" xalign 0.5 yalign 0.5 size 11 bold True color "#ffffff"


screen moment_bottom_nav(active="home"):
    $ theme = moment_theme_colors()

    frame:
        xpos 0
        ypos 912
        xysize (624, 72)
        padding (16, 9)
        background Solid(theme["surface"])

        hbox:
            spacing 5

            use moment_nav_button(
                "images/phoneUI/Momenticon/home.png",
                "social",
                selected=active == "home",
            )
            use moment_nav_button(
                "images/phoneUI/Momenticon/dm.png",
                "dm",
                selected=active == "dm",
                badge=moment_dm_unread_count(),
            )
            use moment_nav_button(
                "images/phoneUI/Momenticon/comment.png",
                "relationship",
                selected=active == "relationship",
            )
            use moment_nav_button(
                "images/phoneUI/Momenticon/profile.png",
                "profile",
                selected=active == "profile",
            )


screen moment_composer_icon(icon_path, button_action, button_x, accent=False, icon_crop=None, button_y=20):
    $ theme = moment_theme_colors()
    $ icon_color = "#ffffff" if accent else theme["text"]
    $ icon_source = Crop(icon_crop, icon_path) if icon_crop else icon_path

    button:
        xpos button_x
        ypos button_y
        xysize (54, 50)
        padding (0, 0)
        background None
        hover_background None
        action button_action

        fixed:
            xysize (54, 50)

            if accent:
                add Transform(
                    AlphaMask(
                        Solid(theme["accent"], xysize=(100, 100)),
                        "images/phoneUI/Momenticon/circle_mask.svg",
                    ),
                    xalign=0.5,
                    yalign=0.5,
                    xysize=(64, 47),
                )

            add Transform(
                AlphaMask(
                    Solid(icon_color, xysize=(64, 64)),
                    Transform(icon_source, xysize=(64, 64)),
                ),
                xalign=0.5,
                yalign=0.5,
                xysize=(36, 27),
            )


screen moment_avatar(initial, avatar_color, avatar_x=18, avatar_y=10, avatar_size=56, initial_size=20):
    fixed:
        xpos avatar_x
        ypos avatar_y
        xysize (avatar_size, avatar_size)

        add Transform(
            AlphaMask(
                Solid(avatar_color, xysize=(100, 100)),
                "images/phoneUI/Momenticon/circle_mask.svg",
            ),
            xysize=(avatar_size, avatar_size),
        )
        text initial:
            xalign 0.5
            yalign 0.5
            size initial_size
            bold True
            color "#ffffff"


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
                Function(moment_open_story, target)
                if target and not locked
                else Notify("Энэ story одоогоор түгжээтэй.")
            )

            fixed:
                xysize (82, 82)
                add Transform(
                    AlphaMask(
                        Solid(ring_color, xysize=(100, 100)),
                        "images/phoneUI/Momenticon/story_ring_mask.svg",
                    ),
                    xysize=(82, 82),
                )
                add Transform(
                    AlphaMask(
                        Solid(theme["surface_alt"], xysize=(100, 100)),
                        "images/phoneUI/Momenticon/circle_mask.svg",
                    ),
                    xpos=7,
                    ypos=7,
                    xysize=(68, 68),
                )
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
    $ close_friend = moment_is_close_friend()

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
        text "Close people. Real moments.":
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
            xpos 414
            ypos 22
            xysize (72, 50)
            text_size 12
            text_color theme["muted"]
            text_hover_color theme["accent"]
            background None
            action SetVariable("phone_view", "moment_settings")

        button:
            xpos 512
            ypos 15
            xysize (82, 64)
            padding (0, 0)
            background None
            hover_background Solid(theme["surface_alt"])
            action SetVariable("phone_view", "notifications")

            fixed:
                xysize (82, 64)

                add Transform(
                    AlphaMask(
                        Solid(theme["text"], xysize=(512, 512)),
                        "images/phoneUI/Momenticon/like.png",
                    ),
                    xpos=18,
                    ypos=17,
                    xysize=(42, 34),
                )

                if unread:
                    frame:
                        xpos 53
                        ypos 4
                        xysize (25, 25)
                        padding (0, 0)
                        background Solid(theme["hot"])
                        text "[unread]" xalign 0.5 yalign 0.5 size 12 bold True color "#ffffff"

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
            if close_friend:
                use moment_story_item(
                    "Close Friends",
                    "S",
                    theme["success"],
                    target="close_story",
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

            fixed:
                xysize (624, 78)
                add Solid(theme["surface"])

                use moment_avatar("S", theme["hot"], avatar_y=11)
                text "sara.light" xpos 78 ypos 13 size 21 bold True color theme["text"]
                text "Нуурын эрэг":
                    xpos 78
                    ypos 41
                    size 14
                    color theme["accent_alt"]
                text "•••" xpos 588 xanchor 1.0 ypos 16 size 20 color theme["muted"]

            fixed:
                xysize (624, 340)
                clipping True

                drag:
                    drag_name "moment_sara_feed_carousel"
                    xpos (-moment_feed_carousel_index * MOMENT_FEED_CAROUSEL_WIDTH)
                    ypos 0
                    draggable True
                    droppable False
                    drag_raise False
                    drag_handle (0, 0, 1872, 340)
                    drag_offscreen moment_feed_carousel_drag_position
                    dragged moment_feed_carousel_dragged
                    snapped moment_feed_carousel_snapped

                    hbox:
                        spacing 0

                        fixed:
                            xysize (624, 340)
                            add "pWallpaper" xysize (624, 936) ypos -250
                            add Solid("#02061742")

                        fixed:
                            xysize (624, 340)
                            add "pWallpaper" xysize (624, 936) ypos -360
                            add Solid("#312e8133")

                        fixed:
                            xysize (624, 340)
                            add "pWallpaper" xysize (624, 936) ypos -145
                            add Solid("#0e749033")

                text "[moment_feed_carousel_index + 1]/[MOMENT_FEED_CAROUSEL_SLIDE_COUNT]":
                    xpos 594
                    xanchor 1.0
                    ypos 16
                    size 15
                    bold True
                    color "#ffffff"

                hbox:
                    xalign 0.5
                    ypos 314
                    spacing 8

                    for slide_index in range(MOMENT_FEED_CAROUSEL_SLIDE_COUNT):
                        add Transform(
                            AlphaMask(
                                Solid(
                                    "#ffffff" if slide_index == moment_feed_carousel_index else "#ffffff66",
                                    xysize=(100, 100),
                                ),
                                "images/phoneUI/Momenticon/circle_mask.svg",
                            ),
                            xysize=(7, 7),
                        )

            fixed:
                xysize (624, 70)
                add Solid(theme["surface"])

                add Transform(
                    AlphaMask(
                        Solid(theme["hot"], xysize=(512, 512)),
                        "images/phoneUI/Momenticon/like.png",
                    ),
                    xpos=22,
                    ypos=19,
                    xysize=(38, 31),
                )
                text "2.4K" xpos 65 yalign 0.5 size 18 color theme["text"]
                add Transform(
                    AlphaMask(
                        Solid(theme["text"], xysize=(512, 512)),
                        "images/phoneUI/Momenticon/comment.png",
                    ),
                    xpos=145,
                    ypos=20,
                    xysize=(36, 29),
                )
                text "126" xpos 187 yalign 0.5 size 16 color theme["text"]
                button:
                    xpos 522
                    ypos 8
                    xysize (72, 54)
                    padding (0, 0)
                    background None
                    action Function(moment_open_contact, "sara")

                    add Transform(
                        AlphaMask(
                            Solid(theme["accent_alt"], xysize=(512, 512)),
                            "images/phoneUI/Momenticon/dm.png",
                        ),
                        xalign=0.5,
                        yalign=0.5,
                        xysize=(42, 34),
                    )

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

            fixed:
                xysize (624, 76)
                add Solid(theme["surface"])

                use moment_avatar("T", theme["accent_alt"], avatar_y=10, avatar_size=54)
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

            frame:
                xfill True
                ysize 92
                padding (22, 12)
                background Solid(theme["surface"])

                text "{b}temuulen.jpg{/b}  Хот унтсан ч зарим газар сэрүүн байдаг.":
                    size 17
                    color theme["text"]

            if close_friend:
                fixed:
                    xysize (624, 78)
                    add Solid(theme["surface"])

                    use moment_avatar("S", theme["hot"], avatar_y=11)
                    text "sara.light" xpos 78 ypos 13 size 21 bold True color theme["text"]
                    text "Close Friends" xpos 78 ypos 41 size 14 bold True color theme["success"]
                    text "•••" xpos 588 xanchor 1.0 ypos 16 size 20 color theme["muted"]

                fixed:
                    xysize (624, 340)
                    clipping True

                    add "pWallpaper" xysize (624, 936) ypos -340
                    add Solid("#052e2466")
                    text "CLOSE FRIENDS":
                        xpos 22
                        ypos 24
                        size 17
                        bold True
                        color "#a7f3d0"
                    text "Зөвхөн ойр хүмүүст":
                        xpos 22
                        ypos 52
                        size 14
                        color "#d1fae5"

                fixed:
                    xysize (624, 70)
                    add Solid(theme["surface"])

                    add Transform(
                        AlphaMask(
                            Solid(theme["hot"], xysize=(512, 512)),
                            "images/phoneUI/Momenticon/like.png",
                        ),
                        xpos=22,
                        ypos=19,
                        xysize=(38, 31),
                    )
                    text "128" xpos 65 yalign 0.5 size 18 color theme["text"]
                    add Transform(
                        AlphaMask(
                            Solid(theme["text"], xysize=(512, 512)),
                            "images/phoneUI/Momenticon/comment.png",
                        ),
                        xpos=145,
                        ypos=20,
                        xysize=(36, 29),
                    )
                    text "18" xpos 187 yalign 0.5 size 16 color theme["text"]
                    button:
                        xpos 522
                        ypos 8
                        xysize (72, 54)
                        padding (0, 0)
                        background None
                        action Function(moment_open_contact, "sara")

                        add Transform(
                            AlphaMask(
                                Solid(theme["accent_alt"], xysize=(512, 512)),
                                "images/phoneUI/Momenticon/dm.png",
                            ),
                            xalign=0.5,
                            yalign=0.5,
                            xysize=(42, 34),
                        )

                frame:
                    xfill True
                    ysize 126
                    padding (22, 10)
                    background Solid(theme["surface"])

                    vbox:
                        spacing 5
                        text "{b}sara.light{/b}  Чамд л харуулахыг хүссэн мөч.":
                            size 18
                            color theme["text"]
                        text "Маргаашийн аяллын жижиг төлөвлөгөөг энд үлдээлээ.":
                            size 17
                            color theme["text"]
                        text "Close Friends · саяхан":
                            size 14
                            color theme["success"]

            null height 24

    use moment_bottom_nav("home")


transform moment_story_progress_fill(duration, target_width):
    xsize 0
    linear duration xsize target_width


screen moment_story_progress_row(stories, current_index, story_duration):
    $ story_count = max(1, len(stories))
    $ segment_width = int((588 - ((story_count - 1) * 5)) / story_count)

    hbox:
        xpos 18
        ypos 51
        spacing 5

        for segment in range(story_count):
            fixed:
                xysize (segment_width, 4)

                add Solid("#ffffff55") xysize (segment_width, 4)

                if segment < current_index:
                    add Solid("#ffffff") xysize (segment_width, 4)
                elif segment == current_index:
                    add Solid("#ffffff"):
                        xysize (segment_width, 4)
                        at moment_story_progress_fill(story_duration, segment_width)


screen phone_moment_story():
    $ theme = moment_theme_colors()
    $ stories = MOMENT_SARA_STORIES
    $ story_index = moment_story_safe_index(moment_story_index, stories)
    $ story = stories[story_index]
    $ story_duration = max(0.1, float(story.get("duration_seconds", 7.0)))

    add Solid("#030407")

    fixed:
        xysize (624, 984)
        clipping True

        add "pWallpaper" xysize (624, 936) ypos story.get("wallpaper_y", 48)
        add Solid(story.get("tint", "#02061755"))
        add Solid("#000000b8") ypos 678 ysize 306

    use phone_status_bar(dark=True)

    use moment_story_progress_row(stories, story_index, story_duration)

    text "●" xpos 18 ypos 70 size 54 color theme["hot"]
    text "S" xpos 36 xanchor 0.5 ypos 84 size 18 bold True color "#ffffff"
    text "sara.light  ·  [story['age']]":
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

    button:
        xpos 0
        ypos 120
        xysize (312, 400)
        padding (0, 0)
        background None
        hover_background None
        action Function(moment_previous_story)

    button:
        xpos 312
        ypos 120
        xysize (312, 400)
        padding (0, 0)
        background None
        hover_background None
        action Function(moment_advance_story)

    frame:
        xpos 24
        ypos 532
        xysize (576, 126)
        padding (20, 16)
        background Solid("#0000009c")

        vbox:
            spacing 8
            text story["title"]:
                size 24
                bold True
                color "#ffffff"
            text story["subtitle"]:
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

    timer story_duration action Function(moment_advance_story)


screen phone_moment_close_story():
    $ theme = moment_theme_colors()
    $ stories = MOMENT_CLOSE_FRIEND_STORIES
    $ story_index = moment_story_safe_index(moment_close_story_index, stories)
    $ story = stories[story_index]
    $ story_duration = max(0.1, float(story.get("duration_seconds", 7.0)))

    add Solid("#030407")

    fixed:
        xysize (624, 984)
        clipping True

        add "pWallpaper" xysize (624, 936) ypos story.get("wallpaper_y", 48)
        add Solid(story.get("tint", "#052e244d"))
        add Solid("#000000c4") ypos 650 ysize 334

    use phone_status_bar(dark=True)

    use moment_story_progress_row(stories, story_index, story_duration)

    text "●" xpos 18 ypos 70 size 54 color theme["hot"]
    text "S" xpos 36 xanchor 0.5 ypos 84 size 18 bold True color "#ffffff"
    text "sara.light  ·  [story['age']]":
        xpos 72
        ypos 84
        size 17
        bold True
        color "#ffffff"

    textbutton "×":
        xpos 594
        xanchor 1.0
        ypos 67
        xysize (52, 52)
        text_size 30
        text_color "#ffffff"
        background None
        action SetVariable("phone_view", "social")

    button:
        xpos 0
        ypos 120
        xysize (312, 450)
        padding (0, 0)
        background None
        hover_background None
        action Function(moment_previous_story)

    button:
        xpos 312
        ypos 120
        xysize (312, 450)
        padding (0, 0)
        background None
        hover_background None
        action Function(moment_advance_story)

    frame:
        xpos 24
        ypos 590
        xysize (210, 44)
        padding (12, 8)
        background Solid("#059669e8")
        text "CLOSE FRIENDS":
            xalign 0.5
            yalign 0.5
            size 14
            bold True
            color "#ffffff"

    fixed:
        xpos 24
        ypos 680
        xysize (576, 174)

        text story["title"]:
            xmaximum 560
            size 24
            bold True
            color "#ffffff"
        text story["subtitle"]:
            ypos 78
            size 18
            color "#d1fae5"

    timer story_duration action Function(moment_advance_story)

    textbutton "DM-ЭЭР ХАРИУЛАХ":
        xpos 24
        ypos 878
        xysize (576, 62)
        text_size 17
        text_bold True
        text_color "#ffffff"
        background Solid(theme["accent"])
        hover_background Solid(theme["accent_alt"])
        action Function(moment_open_contact, "sara")


screen phone_moment_notifications():
    $ theme = moment_theme_colors()
    $ unread = moment_unread_count()
    $ visible_notifications = moment_active_notifications()

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
        ysize 736
        mousewheel True
        draggable True
        scrollbars None

        vbox:
            xsize 624
            spacing 2

            for index, notice in enumerate(visible_notifications):
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

    use moment_bottom_nav("notifications")


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
    $ close_friend = moment_is_close_friend()
    $ close_friend_remaining = max(0, MOMENT_CLOSE_FRIEND_THRESHOLD - moment_relationship)

    add Solid(theme["bg"])
    use moment_page_header("Relationship", back_target="social", right_label="DM", right_target="dm")

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

        text "Харилцах арга, story reply болон сонголтууд энэ оноонд нөлөөлнө.":
            xpos 18
            ypos 174
            xmaximum 540
            size 15
            color theme["muted"]

        text "Сара: [sara_mood_label()]" xpos 142 ypos 101 size 16 color theme["accent_alt"]

    frame:
        xpos 24
        ypos 388
        xysize (576, 154)
        padding (18, 15)
        background Solid(theme["surface_alt"])

        vbox:
            spacing 9
            text "CLOSE FRIEND":
                size 15
                bold True
                color (theme["success"] if close_friend else theme["accent_alt"])
            if sara_blocked:
                text "Сара харилцаагаа зогсоосон":
                    size 18
                    bold True
                    color theme["hot"]
                text "Close Friends контент одоогоор харагдахгүй.":
                    size 15
                    color theme["muted"]
            elif close_friend:
                text "Нэмэлт story болон post нээгдсэн":
                    size 18
                    bold True
                    color theme["success"]
                text "Сарагийн Close Friends контент feed дээр автоматаар харагдана.":
                    xmaximum 530
                    size 15
                    color theme["muted"]
            else:
                text "Relationship [MOMENT_CLOSE_FRIEND_THRESHOLD]+ хүрэхэд нээгдэнэ":
                    size 17
                    color theme["text"]
                text "Дахин [close_friend_remaining] оноо хэрэгтэй":
                    size 15
                    color theme["muted"]

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


screen phone_moment_dm():
    $ theme = moment_theme_colors()
    $ total_unread = moment_dm_unread_count()

    add Solid(theme["bg"])
    use phone_status_bar(dark=theme["status_light"])

    fixed:
        xpos 0
        ypos 42
        xysize (624, 82)

        add Solid(theme["surface"])
        text "[moment_profile_handle]":
            xalign 0.5
            yalign 0.5
            size 28
            bold True
            color theme["text"]
        text "⌄":
            xpos 430
            yalign 0.5
            size 25
            color theme["text"]
        textbutton "+":
            xpos 574
            xanchor 1.0
            yalign 0.5
            xysize (54, 54)
            text_size 34
            text_color theme["text"]
            text_hover_color theme["accent"]
            background None
            action Notify("Шинэ message дараагийн шатанд нэмэгдэнэ.")

    textbutton "Search messages...":
        xpos 24
        ypos 132
        xysize (576, 58)
        text_size 18
        text_color theme["muted"]
        text_hover_color theme["accent"]
        background Solid(theme["surface_alt"])
        hover_background Solid(theme["line"])
        action Notify("DM хайлт")

    frame:
        xpos 0
        ypos 204
        xysize (624, 128)
        padding (14, 5)
        background Solid(theme["surface"])

        hbox:
            spacing 42

            use moment_story_item(
                "Таны note",
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
                "Мишээл",
                "M",
                theme["accent"],
                target=None,
            )
            use moment_story_item(
                "Тэмүүжин",
                "T",
                theme["accent_alt"],
                target=None,
            )

    text "Messages":
        xpos 24
        ypos 350
        size 25
        bold True
        color theme["text"]
    text "Requests":
        xpos 596
        xanchor 1.0
        ypos 355
        size 17
        bold True
        color theme["muted"]

    if total_unread:
        text "[total_unread] unread":
            xpos 24
            ypos 382
            size 13
            color theme["hot"]

    viewport:
        xpos 0
        ypos 410
        xsize 624
        ysize 502
        mousewheel True
        draggable True
        scrollbars None

        vbox:
            xsize 624
            spacing 0

            for contact_id in MOMENT_CONTACT_ORDER:
                $ contact = MOMENT_CONTACTS[contact_id]
                $ contact_unread = (
                    max(moment_contact_unread.get("sara", 0), sara_unread_messages)
                    if contact_id == "sara"
                    else moment_contact_unread.get(contact_id, 0)
                )

                button:
                    xsize 624
                    ysize 106
                    padding (20, 10)
                    background None
                    hover_background Solid(theme["surface_alt"])
                    action Function(moment_open_contact, contact_id)

                    fixed:
                        xysize (584, 86)

                        add Transform(
                            AlphaMask(
                                Solid(contact["color"], xysize=(100, 100)),
                                "images/phoneUI/Momenticon/circle_mask.svg",
                            ),
                            xpos=0,
                            ypos=2,
                            xysize=(78, 78),
                        )
                        text contact["initial"]:
                            xpos 39
                            xanchor 0.5
                            ypos 25
                            size 25
                            bold True
                            color "#ffffff"

                        text contact["name"]:
                            xpos 98
                            ypos 7
                            size 21
                            bold (contact_unread > 0)
                            color theme["text"]
                        text contact["preview"]:
                            xpos 98
                            ypos 38
                            xmaximum 400
                            size 16
                            color (theme["text"] if contact_unread > 0 else theme["muted"])
                        text contact["status"]:
                            xpos 98
                            ypos 62
                            size 13
                            color theme["muted"]

                        if contact_unread:
                            frame:
                                xpos 552
                                ypos 28
                                xysize (26, 26)
                                padding (0, 0)
                                background Solid(theme["hot"])
                                text "[contact_unread]" xalign 0.5 yalign 0.5 size 12 bold True color "#ffffff"

    use moment_bottom_nav("dm")


screen phone_moment_chat():
    $ theme = moment_theme_colors()
    $ contact = moment_active_contact_data()
    $ active_messages = moment_active_messages()
    $ active_is_sara = moment_active_contact == "sara"
    $ active_typing = active_is_sara and sara_is_typing
    $ typing_text = "%s бичиж байна..." % contact["name"]
    $ sara_unavailable = active_is_sara and (sara_blocked or sara_cooldown_until > time.time())
    $ can_send = bool(phone_chat_input.strip()) and not active_typing and not sara_unavailable
    $ final_icon_path = "images/phoneUI/Momenticon/send.png" if can_send else "images/phoneUI/Momenticon/add.png"
    $ final_icon_crop = (398, 389, 403, 396) if can_send else None
    $ unavailable_message = contact["name"] + (" харилцаагаа зогсоосон байна." if sara_blocked else " түр завсарлага авч байна.")
    $ final_button_action = Function(moment_send_active_dm) if can_send else Notify(unavailable_message if sara_unavailable else "Attachment menu дараагийн шатанд нэмэгдэнэ.")
    $ composer_height = 92 + (moment_chat_draft_rows("" if sara_unavailable else phone_chat_input) - 1) * 24
    $ composer_top = 984 - composer_height
    $ composer_icon_y = composer_height - 72

    add Solid(theme["bg"])
    use phone_status_bar(dark=theme["status_light"])

    fixed:
        xpos 0
        ypos 42
        xysize (624, 92)

        add Solid(theme["surface"])
        add Solid(theme["line"]) ypos 90 ysize 2

        textbutton "<":
            xpos 10
            yalign 0.5
            xysize (55, 58)
            text_size 34
            text_color theme["text"]
            text_hover_color theme["accent"]
            background None
            action SetVariable("phone_view", "dm")

        add Transform(
            AlphaMask(
                Solid(contact["color"], xysize=(100, 100)),
                "images/phoneUI/Momenticon/circle_mask.svg",
            ),
            xpos=70,
            ypos=14,
            xysize=(62, 62),
        )
        text contact["initial"] xpos 101 xanchor 0.5 ypos 31 size 21 bold True color "#ffffff"
        text contact["handle"] xpos 148 ypos 14 size 23 bold True color theme["text"]
        text (sara_mood_label() if active_is_sara else contact["status"]) xpos 148 ypos 47 size 14 color theme["success"]

        textbutton ("BOND [moment_relationship]" if active_is_sara else "PROFILE"):
            xpos 594
            xanchor 1.0
            yalign 0.5
            text_size 14
            text_color theme["accent_alt"]
            text_hover_color theme["accent"]
            background None
            action SetVariable("phone_view", "relationship" if active_is_sara else "profile")

    viewport:
        id "moment_dm_viewport"
        xpos 18
        ypos 150
        xsize 588
        ysize composer_top - 162
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

            if not story_active:
                frame:
                    xalign 1.0
                    xysize (360, 330)
                    padding (0, 0)
                    background Solid(theme["surface_alt"])

                    fixed:
                        xysize (360, 330)
                        clipping True

                        add "pWallpaper" xysize (360, 540) ypos -80
                        add Solid("#00000055")
                        text "SHARED MOMENT":
                            xpos 18
                            ypos 17
                            size 15
                            bold True
                            color "#ffffff"
                        text "▶":
                            xalign 0.5
                            yalign 0.5
                            size 54
                            color "#ffffff"
                        text contact["handle"]:
                            xpos 18
                            ypos 286
                            size 18
                            bold True
                            color "#ffffff"

                text "15:15":
                    xalign 0.5
                    size 14
                    color theme["muted"]

            for msg in active_messages:
                if msg["sender"] == "player":
                    frame:
                        xalign 1.0
                        xmaximum 448
                        padding (17, 11)
                        background Frame(
                            AlphaMask(
                                Solid(theme["accent"], xysize=(86, 64)),
                                "images/phoneUI/Momenticon/message_bubble_mask.svg",
                            ),
                            29, 22, 29, 22,
                        )

                        vbox:
                            spacing 5
                            text phone_escape_chat_text(msg["text"]):
                                size 19
                                language "anywhere"
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
                            add Transform(
                                AlphaMask(
                                    Solid(contact["color"], xysize=(100, 100)),
                                    "images/phoneUI/Momenticon/circle_mask.svg",
                                ),
                                xysize=(36, 36),
                            )
                            text contact["initial"] xalign 0.5 yalign 0.5 size 14 bold True color "#ffffff"

                        frame:
                            xmaximum 430
                            padding (17, 11)
                            background Frame(
                                AlphaMask(
                                    Solid(theme["surface_alt"], xysize=(86, 64)),
                                    "images/phoneUI/Momenticon/message_bubble_mask.svg",
                                ),
                                29, 22, 29, 22,
                            )

                            vbox:
                                spacing 5
                                text phone_escape_chat_text(msg["text"]):
                                    size 19
                                    language "anywhere"
                                    color theme["text"]
                                text msg.get("time", ""):
                                    size 12
                                    color theme["muted"]

            if active_typing:
                hbox:
                    spacing 9
                    fixed:
                        yalign 1.0
                        xysize (36, 36)
                        add Transform(
                            AlphaMask(
                                Solid(contact["color"], xysize=(100, 100)),
                                "images/phoneUI/Momenticon/circle_mask.svg",
                            ),
                            xysize=(36, 36),
                        )
                        text contact["initial"] xalign 0.5 yalign 0.5 size 14 bold True color "#ffffff"
                    frame:
                        padding (17, 11)
                        background Frame(
                            AlphaMask(
                                Solid(theme["surface_alt"], xysize=(86, 64)),
                                "images/phoneUI/Momenticon/message_bubble_mask.svg",
                            ),
                            29, 22, 29, 22,
                        )
                        text typing_text size 16 color theme["muted"]

    if phone_chat_scroll_pending:
        timer 0.01 action [
            Scroll(
                "moment_dm_viewport",
                "vertical increase",
                amount=1000000,
            ),
            SetVariable("phone_chat_scroll_pending", False),
        ]

    if phone_chat_draft_scroll_pending and not sara_unavailable:
        timer 0.01 action [
            Scroll("moment_chat_draft_viewport", "vertical increase", amount=1000000),
            SetVariable("phone_chat_draft_scroll_pending", False),
        ]

    frame:
        xpos 0
        ypos composer_top
        xysize (624, composer_height)
        padding (0, 0)
        background Solid(theme["surface"])

        fixed:
            xysize (624, composer_height)

            add Frame(
                AlphaMask(
                    Solid(theme["surface_alt"], xysize=(600, 66)),
                    "images/phoneUI/Momenticon/composer_pill_mask.svg",
                ),
                32, 30, 32, 30,
            ) xpos 12 ypos 13 xysize (600, composer_height - 26)

            use moment_composer_icon(
                "images/phoneUI/CameraIcon.png",
                Notify("Camera дараагийн шатанд нэмэгдэнэ."),
                20,
                accent=True,
                icon_crop=(317, 357, 346, 266),
                button_y=composer_icon_y,
            )

            if not phone_chat_input or sara_unavailable:
                text (sara_mood_label() if sara_unavailable else "Message..."):
                    xpos 84
                    ypos 34
                    size 18
                    color theme["muted"]

            if not sara_unavailable:
                viewport:
                    id "moment_chat_draft_viewport"
                    xpos 84
                    ypos 31
                    xsize 238
                    ysize composer_height - 46
                    mousewheel True
                    draggable True
                    scrollbars None
                    yinitial 1.0

                    input:
                        value PhoneChatDraftInputValue()
                        length 180
                        xsize 238
                        multiline True
                        copypaste True
                        language "anywhere"
                        size 18
                        color theme["text"]
                        caret Solid(theme["accent_alt"], xsize=2)
                        default_focus True

            use moment_composer_icon(
                "images/phoneUI/Momenticon/mic.svg",
                Notify("Voice message дараагийн шатанд нэмэгдэнэ."),
                330,
                button_y=composer_icon_y,
            )
            use moment_composer_icon(
                "images/phoneUI/Momenticon/picture.png",
                Notify("Gallery дараагийн шатанд нэмэгдэнэ."),
                390,
                icon_crop=(446, 446, 308, 308),
                button_y=composer_icon_y,
            )
            use moment_composer_icon(
                "images/phoneUI/Momenticon/sticker.png",
                Notify("Sticker дараагийн шатанд нэмэгдэнэ."),
                450,
                button_y=composer_icon_y,
            )
            use moment_composer_icon(
                final_icon_path,
                final_button_action,
                510,
                accent=can_send,
                icon_crop=final_icon_crop,
                button_y=composer_icon_y,
            )


screen phone_moment_profile():
    $ theme = moment_theme_colors()

    add Solid(theme["bg"])
    use phone_status_bar(dark=theme["status_light"])

    fixed:
        xpos 0
        ypos 42
        xysize (624, 82)

        add Solid(theme["surface"])
        textbutton "+":
            xpos 18
            yalign 0.5
            xysize (58, 58)
            text_size 36
            text_color theme["text"]
            text_hover_color theme["accent"]
            background None
            action Notify("Шинэ post дараагийн шатанд нэмэгдэнэ.")
        text "▣ [moment_profile_handle]":
            xalign 0.5
            yalign 0.5
            size 24
            bold True
            color theme["text"]
        textbutton "STYLE":
            xpos 598
            xanchor 1.0
            yalign 0.5
            text_size 14
            text_color theme["text"]
            text_hover_color theme["accent"]
            background None
            action SetVariable("phone_view", "moment_settings")

    fixed:
        xpos 24
        ypos 142
        xysize (576, 254)

        add Transform(
            AlphaMask(
                Solid(theme["accent"], xysize=(100, 100)),
                "images/phoneUI/Momenticon/story_ring_mask.svg",
            ),
            xpos=0,
            ypos=0,
            xysize=(116, 116),
        )
        add Transform(
            AlphaMask(
                Solid(theme["surface_alt"], xysize=(100, 100)),
                "images/phoneUI/Momenticon/circle_mask.svg",
            ),
            xpos=10,
            ypos=10,
            xysize=(96, 96),
        )
        text "YOU":
            xpos 58
            xanchor 0.5
            ypos 40
            size 22
            bold True
            color theme["text"]

        text "[moment_profile_name]":
            xpos 142
            ypos 8
            size 27
            bold True
            color theme["text"]
        text "@[moment_profile_handle]":
            xpos 142
            ypos 47
            size 16
            color theme["muted"]
        text "[moment_profile_bio]":
            xpos 142
            ypos 78
            xmaximum 410
            size 16
            color theme["text"]

        hbox:
            xpos 0
            ypos 132
            spacing 12

            frame:
                xysize (184, 52)
                padding (8, 7)
                background Solid(theme["surface_alt"])
                text "12 POST" xalign 0.5 yalign 0.5 size 14 bold True color theme["text"]
            frame:
                xysize (184, 52)
                padding (8, 7)
                background Solid(theme["surface_alt"])
                text "4 FRIEND" xalign 0.5 yalign 0.5 size 14 bold True color theme["text"]
            frame:
                xysize (184, 52)
                padding (8, 7)
                background Solid(theme["accent"] + "28")
                text "[moment_relationship] BOND" xalign 0.5 yalign 0.5 size 14 bold True color theme["accent_alt"]

        hbox:
            xpos 0
            ypos 196
            spacing 12

            textbutton "EDIT PROFILE":
                xysize (282, 50)
                text_size 14
                text_bold True
                text_color theme["text"]
                background Solid(theme["surface_alt"])
                hover_background Solid(theme["line"])
                action Notify("Profile засах хэсэг дараагийн шатанд нэмэгдэнэ.")
            textbutton "SHARE PROFILE":
                xysize (282, 50)
                text_size 14
                text_bold True
                text_color "#ffffff"
                background Solid(theme["accent"])
                hover_background Solid(theme["accent_alt"])
                action Notify("@%s profile link хуулагдлаа." % moment_profile_handle)

    fixed:
        xpos 0
        ypos 414
        xysize (624, 58)

        add Solid(theme["surface"])
        text "▦":
            xpos 104
            yalign 0.5
            size 29
            color theme["text"]
        text "▶":
            xalign 0.5
            yalign 0.5
            size 24
            color theme["muted"]
        text "PROFILE":
            xpos 520
            xanchor 0.5
            yalign 0.5
            size 14
            bold True
            color theme["muted"]
        add Solid(theme["accent"]) xpos 24 ypos 55 xysize (184, 3)

    grid 3 2:
        xpos 24
        ypos 486
        xspacing 8
        yspacing 8

        button:
            xysize (184, 188)
            padding (0, 0)
            background Solid("#10233d")
            action Notify("Post 1")
            fixed:
                xysize (184, 188)
                add "pWallpaper" xysize (184, 276) ypos -45
                add Solid("#00000024")
                text "01" xpos 12 ypos 148 size 18 bold True color "#ffffff"

        button:
            xysize (184, 188)
            padding (0, 0)
            background Solid("#351249")
            action Notify("Post 2")
            fixed:
                xysize (184, 188)
                add Solid(theme["accent"] + "66")
                text "MOMENT" xalign 0.5 yalign 0.5 size 18 bold True color "#ffffff"

        button:
            xysize (184, 188)
            padding (0, 0)
            background Solid("#0f3a38")
            action Notify("Post 3")
            fixed:
                xysize (184, 188)
                add Solid(theme["success"] + "55")
                text "TRIP" xalign 0.5 yalign 0.5 size 20 bold True color "#ffffff"

        button:
            xysize (184, 188)
            padding (0, 0)
            background Solid("#402118")
            action Notify("Post 4")
            fixed:
                xysize (184, 188)
                add Solid("#f59e0b55")
                text "NIGHT" xalign 0.5 yalign 0.5 size 20 bold True color "#ffffff"

        button:
            xysize (184, 188)
            padding (0, 0)
            background Solid("#1e1b4b")
            action Notify("Post 5")
            fixed:
                xysize (184, 188)
                add Solid(theme["accent_alt"] + "50")
                text "TRAIN" xalign 0.5 yalign 0.5 size 20 bold True color "#ffffff"

        button:
            xysize (184, 188)
            padding (0, 0)
            background Solid("#311827")
            action Notify("Post 6")
            fixed:
                xysize (184, 188)
                add Solid(theme["hot"] + "48")
                text "SECRET" xalign 0.5 yalign 0.5 size 18 bold True color "#ffffff"

    use moment_bottom_nav("profile")
