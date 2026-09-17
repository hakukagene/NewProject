# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


# The game starts here.

label start:
    scene bg room

    e "Утасны интерфейсийн эхний хувилбарыг туршиж үзье."

    $ phone_unlocked = False
    $ phone_view = "lock"
    call screen phone_ui

    e "Утас хаагдлаа. Дараагийн шатанд AI сервертэй холбоно."

    return
