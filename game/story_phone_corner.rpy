# In-scene phone access and concept 02 incoming-message toast.
default story_corner_notice = None
default story_corner_remaining = 0.0

init python:
    def story_corner_open_phone(contact=None):
        renpy.store.story_corner_remaining = 0.0
        def open_phone():
            renpy.store.phone_unlocked = True
            if contact:
                moment_open_contact(contact)
            else:
                renpy.store.phone_view = "home"
            renpy.call_screen("phone_ui")
        # Closing the phone returns to the current dialogue/choice interaction.
        renpy.invoke_in_new_context(open_phone)
        renpy.restart_interaction()

    def story_corner_tick():
        renpy.store.story_corner_remaining = max(0.0, story_corner_remaining - .1)
        renpy.restart_interaction()

    config.overlay_screens.append("story_phone_corner")

transform story_corner_arrive:
    on show:
        alpha 0.0 xoffset 24
        ease .2 alpha 1.0 xoffset 0

screen story_phone_corner():
    zorder 110
    if story_active and not main_menu and not renpy.get_screen("phone_ui") and not renpy.get_screen("story_computer"):
        $ unread_count = sum(moment_contact_unread.values()) + sara_unread_messages
        button:
            xpos 1820 ypos 30 xysize (76, 76)
            padding (0, 0)
            background "gui/gold/phone_corner.svg"
            action Function(story_corner_open_phone)
            tooltip "Утас нээх"
            alt "Утас нээх"
        if unread_count:
            frame:
                xpos 1870 ypos 24 padding (8, 3)
                background Solid("#c84949")
                text str(min(99, unread_count)) size 19 color "#ffffff"
        if story_corner_notice and story_corner_remaining > 0:
            timer .1 repeat True action Function(story_corner_tick)
            $ person = STORY_CONTACTS.get(story_corner_notice["contact"], STORY_CONTACTS["anu"])
            button:
                xpos 1250 ypos 30 xsize 550
                padding (24, 20)
                background gold_panel()
                at story_corner_arrive
                action Function(story_corner_open_phone, story_corner_notice["contact"])
                hbox:
                    spacing 18
                    use device_avatar(story_corner_notice["contact"], 52)
                    vbox:
                        spacing 8 xsize 426
                        text (person["name"] + " · " + person["handle"]) size 23 color "#f7e8ca" bold True
                        viewport:
                            xsize 426 ymaximum 150
                            mousewheel True draggable True
                            text phone_escape_chat_text(story_corner_notice["text"]) size 23 color "#f1e5d5" xsize 426
