# Save-backed story state. Existing Sara saves retain their original UI.
default story_active = False
default story_day_one_complete = False
default story_location = "Өдөр 1"
default story_relationships = {"khulan": 20, "anu": 35, "chingun": 40, "family": 20, "badral": 20, "dad": 40, "confidence": 20}
default story_flags = {}
default story_inspected = []
default story_following_saruul = False
default story_night_feed = False
default story_notice = ""
default story_post_likes = []
default story_phone_tab = "feed"
default story_story_contact = "khulan"
default story_dm_replied = []

init python:
    STORY_CONTACTS = {
        "sara": {"name": "Болор", "handle": "bolor.bolor", "initial": "Б", "color": "#55c9bc", "status": "Америк · Businesswoman", "preview": "Өглөөний мэнд."},
        "khulan": {"name": "Хулан", "handle": "khulan.art", "initial": "Х", "color": "#ed95b3", "status": "Зураг зурж байна", "preview": "Хариад бичээрэй."},
        "anu": {"name": "Ану", "handle": "anu.cover", "initial": "А", "color": "#b4a0ea", "status": "Cover дуу", "preview": "Сайхан амраарай."},
        "saruul": {"name": "Саруул", "handle": "saruul.star", "initial": "С", "color": "#f3ad6b", "status": "Сургуулийн од", "preview": "Таныг дагалаа."},
        "chingun": {"name": "Чингүн", "handle": "chingun", "initial": "Ч", "color": "#87baf1", "status": "Идэвхтэй", "preview": "Анда, гэртээ харьсан уу?"},
    }
    STORY_POSTS = (
        ("khulan", "Өдрийн гэрэл. Шинэ дэвтэр. Шинэ танил.", "Шинэ зураг"),
        ("anu", "Зарим дууг ганцхан хүнд зориулж дуулдаг.", "Гитартай орой"),
        ("saruul", "Шинэ улирал эхэллээ.", "Campus day"),
        ("chingun", "Өнөөдөр гүйлтийн нормоо давуулчихлаа.", "Найзууд"),
    )
    STORY_INSPECTIONS = {
        "classroom": [
            ("class_window", "Цонх", "Нар Билгүүний ширээн дээр тусжээ. Хулан дэвтрээ яаран хаав."),
            ("class_students", "Ангийнхан", "Чингүн Хулангийн дэргэд сууна. Хулан зургийн дэвтэртэйгээ иржээ."),
            ("class_board", "Самбар", "Өнөөдрийн сэдэв — хүн өөрийн авьяасыг хэрхэн таних вэ?"),
        ],
        "khulan_room": [
            ("room_drawing", "Өлгөөтэй зургууд", "Хулан өдөр тутмын энгийн мөчүүдийг зурдаг ажээ."),
            ("room_awards", "Шагналууд", "Сурлага, урлагийн олон шагнал өрөөний нэг буланг дүүргэжээ."),
            ("piano_award", "Хамгийн дээд талын цом", "Төгөлдөр хуур — 1-р байр. Хулан зурахаас гадна хөгжимд авьяастай юм байна."),
        ],
    }

    def change_story_relationship(person, amount):
        state = dict(renpy.store.story_relationships)
        state[person] = max(0, min(100, state.get(person, 20) + amount))
        renpy.store.story_relationships = state

    def story_background(scene_id):
        path = "images/story/%s.webp" % scene_id
        if renpy.loadable(path):
            return Transform(path, xysize=(1920, 1080))
        night = scene_id in ("police_car", "bilguun_home", "bilguun_room", "dream")
        return Solid("#152132" if night else "#34424b")

    def start_chapter_one():
        renpy.store.story_active = True
        renpy.store.story_device_drafts = {}
        renpy.store.story_desktop_app = "moment"
        renpy.store.story_desktop_page = "messages"
        renpy.store.story_desktop_minimized = False
        renpy.store.story_desktop_maximized = False
        renpy.store.moment_profile_name = "Билгүүн"
        renpy.store.moment_profile_handle = "bilguun"
        renpy.store.moment_profile_bio = "Оюутан · Эхний өдөр"
        renpy.store.moment_other_dm_messages = {}
        renpy.store.moment_contact_unread = {}
        renpy.store.moment_notifications = []
        renpy.store.moment_relationship_events = []
        renpy.store.sara_messages = []
        renpy.store.sara_unread_messages = 0
        renpy.store.phone_unlocked = True

    def story_receive(contact, text):
        messages = dict(renpy.store.moment_other_dm_messages)
        thread = list(messages.get(contact, []))
        thread.append({"sender": "contact", "text": text, "time": "Өнөөдөр"})
        messages[contact] = thread
        renpy.store.moment_other_dm_messages = messages

        renpy.store.story_latest_contact = contact
        unread = dict(renpy.store.moment_contact_unread)
        unread[contact] = unread.get(contact, 0) + 1
        renpy.store.moment_contact_unread = unread

    def story_prepare_bolor():
        renpy.store.moment_relationship = 55
        renpy.store.sara_mood = "warm"
        renpy.store.sara_boundary_strikes = 0
        renpy.store.sara_blocked = False
        renpy.store.sara_cooldown_until = 0.0
        renpy.store.phone_chat_input = ""
        renpy.store.sara_messages = [
            {"sender": "sara", "text": "ogloonii mend. Egch n say l serlee. Hicheeliin ehnii odor her baiv", "time": "23:10"},
            {"sender": "player", "text": "Hi. Hicheel ntr yah ve. Onoodor manai angiin ohin nmg zurj baigaad chingvnd barigdaad angiar duuren ym bolloo", "time": "23:10"},
            {"sender": "sara", "text": "yeee. Emegtei huuhdiig yaj baigan. Chvs chi huurhun l haragdsan ym blgude", "time": "23:11"},
            {"sender": "player", "text": "Harin tiimee. Tgd bi argadaad bur geriinhentei n hool ntr ideed say irleeshd yooo XD", "time": "23:11"},
            {"sender": "sara", "text": "Aay chi neeree amjuuldag hun ym aa. Sayhan salsan ym baij XD", "time": "23:12"},
            {"sender": "player", "text": "Guee tanii bodoj baigaa shig bish XD", "time": "23:12"},
            {"sender": "sara", "text": "Zaa tiim bailgui dee gants duugee hund aldchihlaa gej ailaashd", "time": "23:13"},
            {"sender": "sara", "text": "Zaa jk shu XD", "time": "23:13"},
        ]
        story_receive("khulan", "Маргааш уулзъя. Хариад бичээрэй.")
        story_receive("chingun", "Анда, гэртээ харьсан уу?")

    def story_send_scripted_dm():
        contact = renpy.store.moment_active_contact
        message = renpy.store.phone_chat_input.strip()
        if not message:
            return
        messages = dict(renpy.store.moment_other_dm_messages)
        thread = list(messages.get(contact, []))
        thread.append({"sender": "player", "text": message, "time": phone_current_time()})
        if contact not in renpy.store.story_dm_replied:
            responses = {
                "khulan": "Бичсэнийг чинь харлаа. Маргааш уулзъя.",
                "anu": "Хариулсанд баярлалаа. Сайхан амраарай.",
                "chingun": "За анда, маргааш уулзъя.",
                "saruul": "Мессежийг чинь харлаа. Одоо завгүй байна аа.",
            }
            thread.append({"sender": "contact", "text": responses.get(contact, "Seen"), "time": phone_current_time()})
            renpy.store.story_dm_replied = renpy.store.story_dm_replied + [contact]
        messages[contact] = thread
        renpy.store.moment_other_dm_messages = messages
        renpy.store.phone_chat_input = ""
        renpy.store.phone_chat_scroll_pending = True
        renpy.restart_interaction()

    def story_toggle_like(contact):
        liked = list(renpy.store.story_post_likes)
        if contact in liked:
            liked.remove(contact)
        else:
            liked.append(contact)
        renpy.store.story_post_likes = liked

screen story_scene_header():
    zorder 5
    frame:
        xpos 45
        ypos 35
        padding (24, 15)
        background Solid("#101725dc")
        text story_location size 24 color "#ffffff"

screen story_timed_choice(options, seconds):
    modal True
    default remaining = seconds
    timer 0.1 repeat True action If(remaining > 0.1, SetScreenVariable("remaining", remaining - 0.1), Return(len(options) - 1))
    frame:
        xalign 0.5
        yalign 0.65
        xsize 900
        padding (35, 30)
        background Solid("#101725f5")
        vbox:
            spacing 14
            text "Юу асуух вэ?" size 30
            bar value remaining range seconds xsize 830 ysize 8
            for i, option in enumerate(options):
                textbutton option action Return(i) xfill True

label story_inspect(room):
    $ story_inspection_finished = False
    while not story_inspection_finished:
        call screen story_inspection(room)
        if _return == "done":
            $ story_inspection_finished = True
        else:
            $ story_item = STORY_INSPECTIONS[room][_return]
            if story_item[0] not in story_inspected:
                $ story_inspected = story_inspected + [story_item[0]]
                if story_item[0] == "piano_award":
                    $ story_flags["knows_piano"] = True
            $ renpy.say(None, story_item[2])
    return

screen story_inspection(room):
    modal True
    frame:
        xalign 0.5
        yalign 0.45
        xsize 1000
        padding (35, 35)
        background Solid("#152132ef")
        vbox:
            spacing 20
            text "Орчноо ажиглах" size 38
            for i, item in enumerate(STORY_INSPECTIONS[room]):
                textbutton (item[1] + (" · Үзсэн" if item[0] in story_inspected else "")) action Return(i)
            textbutton "Үргэлжлүүлэх":
                action Return("done")
                sensitive all(item[0] in story_inspected for item in STORY_INSPECTIONS[room])

screen story_computer():
    modal True
    use story_desktop_shell

screen story_phone_home():
    use story_device_launcher

screen story_moment_page():
    use story_device_moment

screen story_day_summary():
    modal True
    add Solid("#0b1020")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1000
        padding (50, 40)
        background Solid("#192337")
        vbox:
            spacing 20
            text "ӨДӨР 1 ДУУСЛАА" size 50 color "#ed95b3"
            text "Өдөр 2 — Үргэлжлэл" size 30
            text ("Хулан: %d · Ану: %d · Бадрал: %d" % (story_relationships["khulan"], story_relationships["anu"], story_relationships["badral"])) size 26
            text ("Төгөлдөр хуурын шагналыг анзаарсан" if story_flags.get("knows_piano") else "Шагналын нууц нээгдээгүй") size 24
            text "Үргэлжлэлийн зохиол хараахан нэмэгдээгүй." size 24
            textbutton "Дуусгах" action Return()
