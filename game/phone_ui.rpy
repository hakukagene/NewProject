# In-game phone UI prototype.
#
# This file intentionally uses only Ren'Py displayables so the prototype runs
# without any extra image assets. The future AI client can replace
# phone_finish_mock_reply() while keeping these screens unchanged.


default phone_view = "lock"
default phone_unlocked = False
default phone_unlock_pending = False
default phone_flashlight_on = False
default phone_chat_input = ""
default sara_unread_messages = 2
default sara_is_typing = False
default sara_messages = [
    {
        "sender": "sara",
        "text": "Сайн уу? Өнөөдрийн аялал үнэхээр гоё байлаа.",
        "time": "21:46",
    },
    {
        "sender": "player",
        "text": "Тийм ээ. Ялангуяа нуурын эрэг хамгийн гоё байсан.",
        "time": "21:47",
    },
    {
        "sender": "sara",
        "text": "Маргааш дахиад очвол ямар вэ? Энэ удаа камераа авч явна аа.",
        "time": "21:48",
    },
]


init python:
    import datetime


    PHONE_MOCK_REPLIES = (
        "Хаха, ойлголоо. Чамтай чатлах хөгжилтэй юм аа.",
        "Тэгж бодож байгааг чинь мэдсэнгүй. Дараа илүү дэлгэрэнгүй ярья.",
        "За тэгье. Маргааш уулзаад үргэлжлүүлж ярилцъя.",
    )


    def phone_current_time():
        return datetime.datetime.now().strftime("%H:%M")


    def phone_current_date():
        weekdays = (
            "Даваа", "Мягмар", "Лхагва", "Пүрэв",
            "Баасан", "Бямба", "Ням",
        )
        now = datetime.datetime.now()
        return "%d-р сарын %d · %s" % (
            now.month,
            now.day,
            weekdays[now.weekday()],
        )


    PHONE_UNLOCK_DISTANCE = 300
    PHONE_LOCK_EXIT_Y = -1199


    def phone_lock_drag_position(x, y):
        """Move the complete lock panel vertically and keep it on its track."""
        return 0, min(0, max(PHONE_LOCK_EXIT_Y, y))


    def phone_lock_dragged(drags, drop):
        """Finish the unlock animation or return the panel to the bottom."""
        panel = drags[0]
        distance = panel.start_y - panel.y

        if distance >= PHONE_UNLOCK_DISTANCE:
            renpy.store.phone_unlock_pending = True
            panel.snap(0, PHONE_LOCK_EXIT_Y, 0.28)
        else:
            renpy.store.phone_unlock_pending = False
            panel.snap(0, 0, 0.22)


    def phone_lock_snapped(panel, x, y, completed):
        """Switch screens only after the upward snap animation completes."""
        if not completed:
            renpy.store.phone_unlock_pending = False
            return

        if renpy.store.phone_unlock_pending and y <= PHONE_LOCK_EXIT_Y:
            renpy.store.phone_unlock_pending = False
            renpy.store.phone_unlocked = True
            renpy.store.phone_view = "home"
            renpy.restart_interaction()


    def phone_toggle_flashlight():
        renpy.store.phone_flashlight_on = not renpy.store.phone_flashlight_on
        if renpy.store.phone_flashlight_on:
            renpy.notify("Гэрэл асаалаа")
        else:
            renpy.notify("Гэрэл унтраалаа")
        renpy.restart_interaction()


    def phone_open_chat():
        renpy.store.phone_view = "chat"
        renpy.store.sara_unread_messages = 0
        renpy.restart_interaction()


    def phone_send_message():
        """Add the player's message without blocking the Ren'Py UI."""
        message = renpy.store.phone_chat_input.strip()
        if not message or renpy.store.sara_is_typing:
            return

        renpy.store.sara_messages.append({
            "sender": "player",
            "text": message,
            "time": phone_current_time(),
        })
        renpy.store.phone_chat_input = ""
        renpy.store.sara_is_typing = True
        renpy.restart_interaction()


    def phone_finish_mock_reply():
        """Temporary local reply; the AI endpoint will replace this later."""
        if not renpy.store.sara_is_typing:
            return

        reply_index = len(renpy.store.sara_messages) % len(PHONE_MOCK_REPLIES)
        renpy.store.sara_messages.append({
            "sender": "sara",
            "text": PHONE_MOCK_REPLIES[reply_index],
            "time": phone_current_time(),
        })
        renpy.store.sara_is_typing = False
        renpy.restart_interaction()


transform phone_appear:
    alpha 0.0
    zoom 0.85
    ease 0.18 alpha 1.0 zoom 0.9


transform phone_content_fit:
    # Unlocked pages stay inside the phone's safe rectangular area.
    xzoom 0.7692308
    yzoom 0.9756098


transform phone_lock_content_fit:
    # The lock screen can use the whole wallpaper. The gray layer is masked
    # to the same rounded shape, including the transparent notch.
    xzoom 0.7884615
    yzoom 1.0650407




style phone_text is default:
    font gui.interface_text_font
    color "#172033"
    size 24

style phone_small_text is phone_text:
    color "#758096"
    size 18

style phone_light_text is phone_text:
    color "#ffffff"

style phone_heading_text is phone_text:
    color "#111827"
    size 32
    bold True

style phone_icon_text is phone_light_text:
    size 28
    bold True
    text_align 0.5

style phone_button is button:
    background Solid("#ffffff00")
    hover_background Solid("#ffffff12")
    padding (8, 8)

style phone_button_text is phone_text:
    hover_color "#7c3aed"


screen phone_status_bar(dark=False):
    $ status_color = "#ffffff" if dark else "#111827"

    fixed:
        xpos 18
        ysize 42

        text "Mobicom":
            xpos 24
            yalign 0.5
            size 17
            bold True
            color status_color

        hbox:
            xalign 0.9
            yalign 0.5
            spacing 8

            text "5G" size 15 bold True color status_color
            text "|||" size 14 bold True color status_color
            frame:
                xysize (31, 15)
                padding (2, 2)
                background Solid(status_color)
                add Solid("#34d399") xysize (23, 11)


screen phone_ui():
    modal True
    zorder 200

    key "game_menu" action Return()
    timer 30.0 repeat True action Function(renpy.restart_interaction)
    $ phone_is_locked = phone_view == "lock" or not phone_unlocked
    
    add Solid("#07111bd9")

    fixed at phone_appear:
        xalign 0.5
        yalign 0.5
        xysize (800, 1199)
        clipping True

        # These two images were added in the LockScreen commit. The border is
        # intentionally below the wallpaper because its centre is opaque.
        add "pBorder"
        add "pWallpaper"

        if phone_is_locked:
            # The unlocked home page is already below the lock panel, so it
            # is revealed continuously while the player swipes upward.
            fixed at phone_content_fit:
                xpos 160
                ypos 120
                xysize (624, 984)

                use phone_main

            # Clip the moving page to the wallpaper's 492x1048 inner bounds.
            # This prevents it from escaping above or below the phone while
            # preserving the live swipe and snap-back animation.
            fixed:
                xpos 152
                ypos 78
                xysize (492, 1048)
                clipping True

                draggroup:
                    xpos -152
                    ypos -78
                    xysize (800, 1199)

                    drag:
                        xpos 0
                        ypos 0
                        draggable True
                        droppable False
                        drag_raise False
                        drag_handle (300, 1040, 200, 100)
                        drag_offscreen phone_lock_drag_position
                        dragged phone_lock_dragged
                        snapped phone_lock_snapped

                        fixed:
                            xysize (800, 1199)

                            # A second wallpaper travels with the lock layer.
                            # The stationary clipping area and border overlay
                            # keep it inside the physical screen opening.
                            add "pWallpaper"
                            add "lockScreenGray"

                            fixed at phone_lock_content_fit:
                                xpos 152
                                ypos 78
                                xysize (624, 984)

                                use phone_lockscreen
        else:
            # Scale only once. The old nested 480px container compressed and
            # shifted every child before this transform was applied.
            fixed at phone_content_fit:
                xpos 160
                ypos 120
                xysize (624, 984)

                if phone_view == "home":
                    use phone_main
                elif phone_view == "social":
                    use phone_social
                else:
                    use phone_sara_chat

        # Keep the bezel, rounded corners, and notch stationary above every
        # moving page. Transparent screen pixels remain fully interactive.
        add "pBorderOverlay"


screen phone_lockscreen():
    add Null(width=624, height=984)
    $ flashlight_color = "#fef08a" if phone_flashlight_on else "#ffffff"

    use phone_status_bar(dark=True)

    vbox:
        xalign 0.5
        ypos 96
        spacing 2

        text "[phone_current_time()]":
            xalign 0.5
            size 88
            bold True
            color "#ffffff"
        text "[phone_current_date()]":
            xalign 0.5
            size 21
            color "#e0e7ff"

    # Wide glass notification, proportioned like the phone reference.
    # Every label is positioned independently so a long message cannot move
    # the title or timestamp.
    fixed:
        xalign 0.5
        ypos 748
        xysize (592, 78)

        add "pNotificationGlass"

        fixed:
            xpos 22
            ypos 16
            xysize (64, 47)

            add "pMomentNotificationIcon"
            text "M":
                xalign 0.5
                yalign 0.5
                size 27
                bold True
                color "#ffffff"

        text "Moment · Сара":
            xpos 104
            ypos 12
            size 18
            bold True
            color "#ffffff"

        text "одоо":
            xpos 562
            xanchor 1.0
            ypos 12
            size 17
            color "#e2e8f0"

        text "Маргааш дахиад очвол ямар вэ?":
            xpos 104
            ypos 38
            xmaximum 454
            size 20
            color "#ffffff"

    button:
        xpos 70
        ypos 850
        xysize (96, 96)
        padding (0, 0)
        background None
        hover_background None
        action Function(phone_toggle_flashlight)
        fixed:
            add "pQuickActionBackground"

        fixed:
            xpos 35
            ypos 15
            xysize (96, 96)
            add "pLightOff"
    button:
        xpos 474
        ypos 850
        xysize (96, 96)
        padding (0, 0)
        background None
        hover_background None
        action Notify("Камер дараагийн шатанд нэмэгдэнэ.")
        fixed:
            add "pQuickActionBackground"
        fixed:
            xpos 25
            ypos 20
            xysize (96, 96)
            add "pCameraIcon"

    fixed:
        xpos 222
        ypos 930
        xysize (180, 36)

        text "━━━━━━━━":
            xalign 0.5
            yalign 0.5
            size 20
            color "#ffffff"



screen phone_main():
    add Solid("#172554")
    add Solid("#4c1d9588") ypos 360 ysize 624

    use phone_status_bar(dark=True)

    vbox:
        xpos 38
        ypos 92
        spacing 6

        text "Өдрийн мэнд":
            style "phone_light_text"
            size 22
        text "22°  ·  Улаанбаатар":
            style "phone_light_text"
            size 38
            bold True

    frame:
        xpos 32
        ypos 190
        xysize (560, 112)
        padding (24, 18)
        background Solid("#ffffff22")

        hbox:
            spacing 20
            yalign 0.5

            frame:
                xysize (68, 68)
                background Solid("#f59e0b")
                text "S" style "phone_icon_text" xalign 0.5 yalign 0.5

            vbox:
                yalign 0.5
                spacing 4
                text "Сара шинэ story орууллаа" style "phone_light_text" size 21 bold True
                text "5 минутын өмнө" style "phone_light_text" size 17 color "#ddd6fe"

    grid 3 2:
        xpos 37
        ypos 355
        xspacing 42
        yspacing 38

        button:
            style "phone_button"
            xysize (150, 150)
            action SetVariable("phone_view", "social")
            vbox:
                xalign 0.5
                spacing 10
                frame:
                    xalign 0.5
                    xysize (84, 84)
                    background Solid("#7c3aed")
                    text "M" style "phone_icon_text" xalign 0.5 yalign 0.5
                text "Moment" style "phone_light_text" size 18 xalign 0.5

        button:
            style "phone_button"
            xysize (150, 150)
            action Function(phone_open_chat)
            vbox:
                xalign 0.5
                spacing 10
                fixed:
                    xysize (84, 84)
                    frame:
                        xysize (84, 84)
                        background Solid("#10b981")
                        text "C" style "phone_icon_text" xalign 0.5 yalign 0.5
                    if sara_unread_messages:
                        frame:
                            xalign 1.0
                            yalign 0.0
                            xysize (30, 30)
                            padding (0, 0)
                            background Solid("#ef4444")
                            text "[sara_unread_messages]" size 15 color "#ffffff" bold True xalign 0.5 yalign 0.5
                text "Chat" style "phone_light_text" size 18 xalign 0.5

        button:
            style "phone_button"
            xysize (150, 150)
            action Notify("Камер дараагийн шатанд нэмэгдэнэ.")
            vbox:
                xalign 0.5
                spacing 10
                frame:
                    xalign 0.5
                    xysize (84, 84)
                    background Solid("#0ea5e9")
                    text "CAM" style "phone_icon_text" size 20 xalign 0.5 yalign 0.5
                text "Камер" style "phone_light_text" size 18 xalign 0.5

        button:
            style "phone_button"
            xysize (150, 150)
            action Notify("Зураг дараагийн шатанд нэмэгдэнэ.")
            vbox:
                xalign 0.5
                spacing 10
                frame:
                    xalign 0.5
                    xysize (84, 84)
                    background Solid("#ec4899")
                    text "PIC" style "phone_icon_text" size 20 xalign 0.5 yalign 0.5
                text "Зураг" style "phone_light_text" size 18 xalign 0.5

        button:
            style "phone_button"
            xysize (150, 150)
            action Notify("Тэмдэглэл дараагийн шатанд нэмэгдэнэ.")
            vbox:
                xalign 0.5
                spacing 10
                frame:
                    xalign 0.5
                    xysize (84, 84)
                    background Solid("#f59e0b")
                    text "N" style "phone_icon_text" xalign 0.5 yalign 0.5
                text "Тэмдэглэл" style "phone_light_text" size 18 xalign 0.5

        button:
            style "phone_button"
            xysize (150, 150)
            action Notify("Тохиргоо дараагийн шатанд нэмэгдэнэ.")
            vbox:
                xalign 0.5
                spacing 10
                frame:
                    xalign 0.5
                    xysize (84, 84)
                    background Solid("#64748b")
                    text "SET" style "phone_icon_text" size 18 xalign 0.5 yalign 0.5
                text "Тохиргоо" style "phone_light_text" size 18 xalign 0.5

    textbutton "УТСАА ХААХ":
        xalign 0.5
        ypos 900
        text_size 17
        text_color "#ddd6fe"
        text_hover_color "#ffffff"
        background Solid("#ffffff12")
        hover_background Solid("#ffffff24")
        padding (24, 12)
        action Return()

    add Solid("#ffffff") xysize (190, 5) xalign 0.5 ypos 966


screen phone_social():
    add Solid("#f8fafc")

    use phone_status_bar()

    fixed:
        ypos 42
        ysize 78

        textbutton "<":
            xpos 14
            yalign 0.5
            text_size 34
            text_color "#111827"
            text_hover_color "#7c3aed"
            background None
            action SetVariable("phone_view", "home")

        text "Moment":
            xalign 0.5
            yalign 0.5
            size 34
            bold True
            color "#111827"

        textbutton "CHAT":
            xpos 516
            yalign 0.5
            text_size 16
            text_color "#7c3aed"
            text_hover_color "#5b21b6"
            background None
            action Function(phone_open_chat)

    add Solid("#e5e7eb") ypos 119 ysize 2

    viewport:
        xpos 0
        ypos 122
        xsize 624
        ysize 790
        mousewheel True
        draggable True
        scrollbars None

        vbox:
            xsize 624
            spacing 0

            frame:
                xfill True
                ysize 142
                padding (24, 16)
                background Solid("#ffffff")

                hbox:
                    spacing 22

                    vbox:
                        spacing 6
                        frame:
                            xysize (78, 78)
                            padding (4, 4)
                            background Solid("#a855f7")
                            frame:
                                xfill True
                                yfill True
                                background Solid("#f59e0b")
                                text "S" style "phone_icon_text" xalign 0.5 yalign 0.5
                        text "Сара" style "phone_small_text" color "#111827" xalign 0.5

                    vbox:
                        spacing 6
                        frame:
                            xysize (78, 78)
                            padding (4, 4)
                            background Solid("#d1d5db")
                            frame:
                                xfill True
                                yfill True
                                background Solid("#0ea5e9")
                                text "T" style "phone_icon_text" xalign 0.5 yalign 0.5
                        text "Тэмүүжин" style "phone_small_text" color "#111827" xalign 0.5

                    vbox:
                        spacing 6
                        frame:
                            xysize (78, 78)
                            padding (4, 4)
                            background Solid("#d1d5db")
                            frame:
                                xfill True
                                yfill True
                                background Solid("#10b981")
                                text "A" style "phone_icon_text" xalign 0.5 yalign 0.5
                        text "Анги" style "phone_small_text" color "#111827" xalign 0.5

            frame:
                xfill True
                padding (0, 0)
                background Solid("#ffffff")

                vbox:
                    xfill True

                    hbox:
                        xsize 624
                        ysize 82
                        spacing 14

                        frame:
                            xpos 20
                            yalign 0.5
                            xysize (54, 54)
                            background Solid("#f59e0b")
                            text "S" style "phone_icon_text" size 22 xalign 0.5 yalign 0.5

                        vbox:
                            yalign 0.5
                            spacing 2
                            text "sara.light" style "phone_text" size 20 bold True
                            text "Найрамдал · Нуурын эрэг" style "phone_small_text" size 16

                    fixed:
                        xsize 624
                        ysize 430
                        add Solid("#312e81")
                        add Solid("#0ea5e966") ypos 246 ysize 184
                        text "ӨНӨӨДРИЙН ДУРСАМЖ":
                            xalign 0.5
                            ypos 164
                            size 30
                            bold True
                            color "#ffffff"
                        text "нуурын эрэг · 21:32":
                            xalign 0.5
                            ypos 207
                            size 18
                            color "#bfdbfe"

                    hbox:
                        xfill True
                        ysize 62
                        spacing 24
                        xpos 22
                        yalign 0.5
                        text "LIKE" style "phone_text" size 18 bold True color "#7c3aed"
                        textbutton "MESSAGE":
                            text_size 18
                            text_color "#111827"
                            text_hover_color "#7c3aed"
                            background None
                            action Function(phone_open_chat)

                    vbox:
                        xpos 22
                        xsize 580
                        spacing 8
                        text "128 хүнд таалагдсан" style "phone_text" size 19 bold True
                        text "sara.light  Зарим өдрийг зурагнаас илүү сэтгэлдээ хадгалмаар байдаг." style "phone_text" size 19
                        text "Бүх 12 сэтгэгдлийг харах" style "phone_small_text" size 17
                        null height 22

    frame:
        xpos 0
        ypos 912
        xsize 624
        ysize 72
        padding (18, 10)
        background Solid("#ffffff")

        hbox:
            xfill True
            yalign 0.5
            spacing 65
            textbutton "HOME" action NullAction() text_size 16 text_color "#7c3aed" background None
            textbutton "SEARCH" action Notify("Хайлт дараагийн шатанд нэмэгдэнэ.") text_size 16 text_color "#64748b" background None
            textbutton "+ POST" action Notify("Post оруулах хэсэг дараагийн шатанд нэмэгдэнэ.") text_size 16 text_color "#64748b" background None
            textbutton "CHAT" action Function(phone_open_chat) text_size 16 text_color "#64748b" text_hover_color "#7c3aed" background None


screen phone_sara_chat():
    add Solid("#f1f5f9")

    use phone_status_bar()

    frame:
        ypos 42
        xfill True
        ysize 86
        padding (12, 10)
        background Solid("#ffffff")

        hbox:
            spacing 14
            yalign 0.5

            textbutton "<":
                yalign 0.5
                text_size 34
                text_color "#111827"
                text_hover_color "#7c3aed"
                background None
                action SetVariable("phone_view", "social")

            frame:
                xysize (58, 58)
                background Solid("#f59e0b")
                text "S" style "phone_icon_text" size 23 xalign 0.5 yalign 0.5

            vbox:
                yalign 0.5
                spacing 1
                text "Сара" style "phone_text" size 23 bold True
                text "идэвхтэй байна" style "phone_small_text" size 16 color "#10b981"

            null width 180

            textbutton "PROFILE":
                yalign 0.5
                text_size 15
                text_color "#7c3aed"
                background None
                action Notify("Сарагийн profile дараагийн шатанд нэмэгдэнэ.")

    viewport:
        id "sara_chat_viewport"
        xpos 18
        ypos 142
        xsize 588
        ysize 715
        mousewheel True
        draggable True
        scrollbars None
        yinitial 1.0

        vbox:
            xsize 588
            spacing 12

            text "ӨНӨӨДӨР":
                xalign 0.5
                style "phone_small_text"
                size 15

            for msg in sara_messages:
                if msg["sender"] == "player":
                    frame:
                        xalign 1.0
                        xmaximum 430
                        padding (18, 12)
                        background Solid("#7c3aed")

                        vbox:
                            spacing 5
                            text msg["text"] style "phone_light_text" size 21
                            text msg.get("time", "") style "phone_light_text" size 13 color "#ddd6fe" xalign 1.0
                else:
                    hbox:
                        xalign 0.0
                        spacing 10

                        frame:
                            yalign 1.0
                            xysize (38, 38)
                            background Solid("#f59e0b")
                            text "S" style "phone_icon_text" size 17 xalign 0.5 yalign 0.5

                        frame:
                            xmaximum 420
                            padding (18, 12)
                            background Solid("#ffffff")

                            vbox:
                                spacing 5
                                text msg["text"] style "phone_text" size 21
                                text msg.get("time", "") style "phone_small_text" size 13

            if sara_is_typing:
                hbox:
                    spacing 10
                    frame:
                        yalign 1.0
                        xysize (38, 38)
                        background Solid("#f59e0b")
                        text "S" style "phone_icon_text" size 17 xalign 0.5 yalign 0.5
                    frame:
                        padding (18, 12)
                        background Solid("#ffffff")
                        text "Сара бичиж байна..." style "phone_small_text" size 18

    if sara_is_typing:
        timer 1.25 action Function(phone_finish_mock_reply)

    frame:
        xpos 0
        ypos 872
        xsize 624
        ysize 112
        padding (16, 18)
        background Solid("#ffffff")

        hbox:
            spacing 10
            yalign 0.5

            frame:
                xysize (475, 62)
                padding (18, 9)
                background Solid("#f1f5f9")

                input:
                    value VariableInputValue("phone_chat_input")
                    length 180
                    xsize 435
                    yalign 0.5
                    size 20
                    color "#111827"
                    caret Solid("#7c3aed")
                    default_focus True

            textbutton "ИЛГЭЭХ":
                xysize (105, 62)
                text_size 15
                text_color "#ffffff"
                text_hover_color "#ffffff"
                background Solid("#7c3aed")
                hover_background Solid("#6d28d9")
                sensitive bool(phone_chat_input.strip()) and not sara_is_typing
                action Function(phone_send_message)
