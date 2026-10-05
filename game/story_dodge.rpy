# Six direction-based dodges preserve the existing parking-fight score.
init python:
    import pygame_sdl2 as dodge_pygame
    STORY_DODGE_ATTACKS = ("left", "right", "right", "left", "right", "left")
    STORY_DODGE_SECONDS = 2.5
    STORY_DODGE_WINDUP = .55

    def story_dodge_attack(value):
        # Older saves may resume the original WASD prompt parameters.
        return {"a": "left", "d": "right", "w": "left", "s": "right"}.get(value, value)

    def story_dodge_target(attack):
        return "right" if story_dodge_attack(attack) == "left" else "left"

    class StoryDodgeSwipe(renpy.Displayable):
        def __init__(self, attack, **kwargs):
            super(StoryDodgeSwipe, self).__init__(**kwargs)
            self.attack = attack
            self.start = None

        def render(self, width, height, st, at):
            return renpy.Render(width, height)

        def event(self, ev, x, y, st):
            if st < STORY_DODGE_WINDUP:
                self.start = None
                return None
            if ev.type == dodge_pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.start = (x, y)
            elif ev.type == dodge_pygame.MOUSEBUTTONUP and ev.button == 1:
                start, self.start = self.start, None
                if start is not None:
                    dx, dy = x - start[0], y - start[1]
                    if abs(dx) >= 90 and abs(dx) > abs(dy) * 1.4:
                        return ("right" if dx > 0 else "left") == story_dodge_target(self.attack)
            return None

transform story_dodge_windup(side):
    xoffset (35 if side == "right" else -35)
    ease .55 xoffset 0
    ease .15 xoffset (70 if side == "right" else -70)

screen story_fight_prompt(expected, round_index, score):
    modal True
    zorder 150
    default remaining = STORY_DODGE_SECONDS
    default swipe = StoryDodgeSwipe(story_dodge_attack(expected))
    $ attack = story_dodge_attack(expected)
    $ target = story_dodge_target(attack)
    $ ready = remaining <= STORY_DODGE_SECONDS - STORY_DODGE_WINDUP
    timer .05 repeat True action If(remaining > .05, SetScreenVariable("remaining", remaining - .05), Return(False))
    for binding in ("a", "K_LEFT"):
        key binding action If(ready, Return(target == "left"), NullAction())
    for binding in ("d", "K_RIGHT"):
        key binding action If(ready, Return(target == "right"), NullAction())

    add swipe
    frame:
        xalign .5 ypos 110
        padding (28, 14) background gold_panel()
        vbox:
            spacing 5
            text "ӨӨРИЙГӨӨ ХАМГААЛ" size 28 color "#f4d89a" xalign .5
            text ("Хөдөлгөөн %d / 6  ·  Зөв %d" % (round_index + 1, score)) size 22 color "#fff5df" xalign .5

    fixed:
        xpos 700 ypos 268 xysize (520, 430)
        add "images/story/dodge/attacker.svg" xpos 60 ypos 0 xysize (400, 400) xzoom (-1 if attack == "right" else 1) at story_dodge_windup(attack)
        text ("←" if attack == "left" else "→") xpos (0 if attack == "left" else 425) ypos 92 size 92 color "#ef7064" font "DejaVuSans.ttf"

    frame:
        xalign .5 ypos 713 xsize 920
        padding (30, 22) background gold_panel()
        vbox:
            spacing 16 xalign .5
            text ("Зүүн талаас цохилт — баруун тийш булт!" if attack == "left" else "Баруун талаас цохилт — зүүн тийш булт!") size 26 color "#fff5df" xalign .5
            bar value remaining range STORY_DODGE_SECONDS xsize 820 ysize 10 left_bar Solid("#dab76c") right_bar Solid("#514534")
            hbox:
                spacing 30 xalign .5
                for direction, caption in (("left", "← Зүүн · A"), ("right", "Баруун · D →")):
                    textbutton caption:
                        id "dodge_" + direction
                        xysize (360, 76) padding (10, 8)
                        text_font "DejaVuSans.ttf" text_size 26 text_xalign .5 text_yalign .5
                        text_color "#f5e8ca" text_hover_color "#ffffff" text_insensitive_color "#827970"
                        background device_panel("#51412f") hover_background device_panel("#80623b")
                        sensitive ready
                        action Return(direction == target)
            text ("A / D · ← / → · Swipe" if ready else "Хөдөлгөөнийг ажигла…") size 20 color "#cfbd9d" xalign .5

screen story_dodge_feedback(success, attack):
    modal True
    zorder 150
    if not success:
        add Solid("#b328282b")
    frame:
        xalign .5 yalign .5 xsize 650 padding (35, 30)
        background gold_panel()
        vbox:
            spacing 12 xalign .5
            text ("Бултаж чадлаа" if success else "Цохилт авлаа") size 38 color ("#94d9bb" if success else "#ef938b") xalign .5
            text ("Баруун тийш" if story_dodge_target(attack) == "right" else "Зүүн тийш") size 24 color "#fff5df" xalign .5
    timer .5 action Return()
