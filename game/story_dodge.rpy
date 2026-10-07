# Six timed dodges preserve the existing parking-fight score and save arguments.
init python:
    import math
    import time
    import pygame_sdl2 as dodge_pygame
    STORY_DODGE_ATTACKS = ("left", "right", "right", "left", "right", "left")
    STORY_DODGE_SEGMENTS = 16
    STORY_DODGE_SECONDS = 6.0
    STORY_DODGE_PERIOD = 2.8
    STORY_DODGE_WINDUP = .55

    def story_dodge_angle(elapsed):
        return (max(0.0, elapsed - STORY_DODGE_WINDUP) / STORY_DODGE_PERIOD * 360.0) % 360.0

    def story_dodge_hit(elapsed, target):
        # Half-open sectors: exactly one 22.5-degree success window.
        return (STORY_DODGE_WINDUP <= elapsed < STORY_DODGE_SECONDS
                and int(story_dodge_angle(elapsed) / (360.0 / STORY_DODGE_SEGMENTS)) == target)

    class StoryDodgeDial(renpy.Displayable):
        def __init__(self, target, **kwargs):
            super(StoryDodgeDial, self).__init__(**kwargs)
            self.target = target
            self.started = None
            self.finished = False

        def elapsed(self):
            return 0.0 if self.started is None else time.monotonic() - self.started

        def submit(self):
            if self.started is not None and not self.finished:
                self.finished = True
                renpy.end_interaction(story_dodge_hit(self.elapsed(), self.target))

        def render(self, width, height, st, at):
            if self.started is None:
                self.started = time.monotonic()
            result = renpy.Render(520, 520)
            canvas = result.canvas()
            center = (260, 260)
            def point(radius, degrees):
                angle = math.radians(degrees - 90)
                return (int(260 + radius * math.cos(angle)), int(260 + radius * math.sin(angle)))
            canvas.circle("#121820e8", center, 248)
            for segment in range(STORY_DODGE_SEGMENTS):
                start = segment * 22.5
                outer = [point(242, start + step * 22.5 / 12) for step in range(13)]
                inner = [point(190, start + step * 22.5 / 12) for step in reversed(range(13))]
                canvas.polygon("#50d6a0" if segment == self.target else "#302b26", outer + inner)
                canvas.line("#c5a667", point(190, start), point(242, start), 2)
            canvas.circle("#d4b36e", center, 242, 2)
            canvas.circle("#d4b36e", center, 190, 2)
            angle = story_dodge_angle(self.elapsed())
            canvas.line("#fff2ce", center, point(228, angle), 6)
            canvas.circle("#fff2ce", point(228, angle), 7)
            canvas.circle("#e5bc69", center, 12)
            renpy.redraw(self, 0)
            return result

        def event(self, ev, x, y, st):
            if self.finished or self.started is None:
                return None
            if self.elapsed() >= STORY_DODGE_SECONDS:
                self.finished = True
                return False
            if ((ev.type == dodge_pygame.KEYDOWN and ev.key == dodge_pygame.K_SPACE)
                    or (ev.type == dodge_pygame.MOUSEBUTTONUP and ev.button == 1 and 0 <= x < 520 and 0 <= y < 520)):
                self.finished = True
                return story_dodge_hit(self.elapsed(), self.target)
            return None

screen story_fight_prompt(expected, round_index, score):
    modal True
    zorder 150
    default target_sector = renpy.random.randrange(STORY_DODGE_SEGMENTS)
    default dial = StoryDodgeDial(target_sector)
    timer STORY_DODGE_SECONDS action Return(False)
    frame:
        xalign .5 ypos 80
        padding (28, 18) background gold_panel()
        vbox:
            spacing 8
            text "БУЛТАХ МӨЧ" size 34 color "#f4d89a" xalign .5
            text ("Хөдөлгөөн %d / 6  ·  Зөв %d" % (round_index + 1, score)) size 22 color "#fff5df" xalign .5
            text "Зүү тод хэсэгт ирэхэд дар" size 26 color "#fff5df" xalign .5
    add dial xalign .5 ypos 270
    textbutton "БУЛТАХ":
        id "dodge_timing"
        xalign .5 ypos 830 xysize (460, 86)
        padding (20, 12)
        text_size 32 text_xalign .5 text_yalign .5
        text_color "#fff5df" text_hover_color "#ffffff"
        background device_panel("#51412f") hover_background device_panel("#80623b")
        action Function(dial.submit)
    text "SPACE · Тойрог эсвэл товч дээр дар" size 22 color "#cfbd9d" xalign .5 ypos 942

screen story_dodge_feedback(success, attack):
    modal True
    zorder 150
    if not success:
        add Solid("#b328282b")
    frame:
        xalign .5 yalign .5 xsize 650 padding (35, 30)
        background gold_panel()
        text ("Бултаж чадлаа" if success else "Цохилт авлаа") size 38 color ("#94d9bb" if success else "#ef938b") xalign .5
    timer .5 action Return()
