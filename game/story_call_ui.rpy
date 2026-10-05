# Concept 03: warm ivory call card. State belongs to saves and rollback.
default story_call_phase = "idle"
default story_call_seconds = 0

init python:
    def story_call_reset():
        renpy.store.story_call_phase = "ringing"
        renpy.store.story_call_seconds = 0
        renpy.store.story_call_declines = 0

    def story_call_answer():
        renpy.store.story_call_phase = "connected"
        renpy.store.story_call_seconds = 0

    def story_call_decline():
        renpy.store.story_call_declines += 1
        renpy.store.story_call_phase = "declined"

    def story_call_finish():
        renpy.store.story_call_phase = "ended"

    def story_call_time():
        seconds = int(renpy.store.story_call_seconds)
        return "%02d:%02d" % (seconds // 60, seconds % 60)

    def story_call_panel():
        return Frame("images/devices/call/panel.svg", 25, 25, 25, 25)

transform story_call_arrive:
    on show:
        alpha 0.0 xoffset -18
        ease .22 alpha 1.0 xoffset 0

transform story_call_pulse:
    alpha .7
    ease 1.0 alpha 1.0
    ease 1.0 alpha .7
    repeat

screen story_call_card(phase, compact=False):
    frame at story_call_arrive:
        xpos (54 if compact else 422)
        ypos (156 if compact else 286)
        xysize ((362, 216) if compact else (460, 600))
        padding (0, 0)
        background story_call_panel()
        fixed:
            if compact:
                add "images/devices/call/avatar.svg" xpos 22 ypos 22 xysize (92, 92)
                text "Э" xpos 68 ypos 68 xanchor .5 yanchor .5 size 39 color "#ffffff" font "DejaVuSans.ttf"
                text "Эгч" xpos 136 ypos 30 size 32 color "#263653" bold True
                text "Ярьж байна" xpos 136 ypos 74 size 21 color "#24835c"
                text story_call_time() xpos 136 ypos 109 size 27 color "#263653" font "DejaVuSans.ttf"
                text "●  Дуудлага холбогдсон" xpos 28 ypos 166 size 19 color "#24835c"
            else:
                if phase == "ringing":
                    add "images/devices/call/avatar.svg" xalign .5 ypos 40 xysize (200, 200) at story_call_pulse
                else:
                    add "images/devices/call/avatar.svg" xalign .5 ypos 40 xysize (200, 200)
                text "Э" xalign .5 ypos 140 yanchor .5 size 76 color "#ffffff" font "DejaVuSans.ttf"
                text "Эгч" xalign .5 ypos 252 size 46 color "#263653" bold True
                text ("Залгаж байна…" if phase == "ringing" else "Дуудлага дууслаа") xalign .5 ypos 316 size 27 color "#687991"
                if phase == "ringing":
                    hbox:
                        xalign .5 ypos 406 spacing 42
                        vbox:
                            spacing 10
                            button:
                                id "call_decline"
                                xysize (144, 110) padding (0, 0)
                                background None
                                hover_background Solid("#ffffff44")
                                sensitive story_call_declines < 2
                                action Function(story_call_decline)
                                alt "Дуудлагыг таслах"
                                add "images/devices/call/decline.svg" xalign .5 yalign .5 xysize (96, 96) alpha (1.0 if story_call_declines < 2 else .35)
                            text "Таслах" xalign .5 size 23 color ("#263653" if story_call_declines < 2 else "#9b9da6")
                        vbox:
                            spacing 10
                            button:
                                id "call_answer"
                                xysize (144, 110) padding (0, 0)
                                background None
                                hover_background Solid("#ffffff44")
                                action [Function(story_call_answer), Return()]
                                alt "Дуудлагыг авах"
                                add "images/devices/call/answer.svg" xalign .5 yalign .5 xysize (96, 96)
                            text "Авах" xalign .5 size 23 color "#263653"
                    if story_call_declines >= 2:
                        text "Авахгүй бол цаашаа явахгүй юм байна." xalign .5 ypos 562 xsize 422 text_align .5 size 18 color "#687991"
                else:
                    add "images/devices/call/decline.svg" xalign .5 ypos 392 xysize (88, 88)
                    if phase == "declined":
                        text "Дахин залгаж байна…" xalign .5 ypos 502 size 23 color "#687991"
                    else:
                        text story_call_time() xalign .5 ypos 502 size 27 color "#687991" font "DejaVuSans.ttf"

screen story_sister_call():
    modal True
    zorder 130
    on "show" action If(story_call_phase == "idle", SetVariable("story_call_phase", "ringing"), NullAction())
    use story_call_card(story_call_phase)
    if story_call_phase == "declined":
        timer 1.6 action SetVariable("story_call_phase", "ringing")

screen story_call_active():
    zorder 115
    if story_call_phase == "connected" and not main_menu and not renpy.get_screen("phone_ui") and not renpy.get_screen("story_computer") and not renpy.get_screen("menu"):
        use story_call_card("connected", compact=True)
        timer 1.0 repeat True action SetVariable("story_call_seconds", story_call_seconds + 1)

screen story_call_ended():
    modal True
    zorder 130
    use story_call_card("ended")
    timer 1.6 action [SetVariable("story_call_phase", "idle"), Return()]
