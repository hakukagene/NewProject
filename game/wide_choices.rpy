# Concept 04: wide, bottom-aligned answers. Captions and actions pass through unchanged.
screen moment_wide_answers(answers, remaining=None, seconds=None):
    $ answer_width = 1560 if renpy.variant("small") else 1380
    $ answer_bottom = int((config.screen_height - gui.textbox_height) * gui.textbox_yalign) - 24
    $ answer_height = max(240, answer_bottom - 110)
    viewport:
        id "moment_answer_scroll"
        xalign .5
        ypos 110
        xsize answer_width
        ysize answer_height
        mousewheel True
        draggable True
        arrowkeys True
        vbox:
            xsize answer_width
            yminimum answer_height
            box_align 1.0
            spacing 12
            if remaining is not None:
                text "Юу асуух вэ?" size 30 color "#f1e5d5"
                bar:
                    value remaining range seconds
                    xsize answer_width ysize 8
                    left_bar Solid("#dfba70")
                    right_bar Solid("#382b21")
            for caption, answer_action in answers:
                textbutton caption:
                    style "moment_wide_answer"
                    xsize answer_width
                    action answer_action

style moment_wide_answer is button:
    background Frame("gui/gold/answer_idle.svg", 16, 16)
    hover_background Frame("gui/gold/answer_hover.svg", 16, 16)
    selected_background Frame("gui/gold/answer_hover.svg", 16, 16)
    insensitive_background Frame("gui/gold/answer_idle.svg", 16, 16)
    padding (34, 13)
    yminimum 64
    xfill True

style moment_wide_answer_text is button_text:
    font gui.text_font
    size 28
    color "#f1e5d5"
    hover_color "#28190e"
    selected_color "#28190e"
    insensitive_color "#a59a88"
    xalign 0.0
    textalign 0.0
    layout "greedy"
    outlines []

style moment_wide_answer variant "small":
    padding (30, 14)
    yminimum 76

style moment_wide_answer_text variant "small":
    size 32
