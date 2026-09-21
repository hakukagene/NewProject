# Moment chatbot — OpenAI + Render

Ren'Py тоглоом жижиг Render backend руу холбогдоно. Зөвхөн backend нь OpenAI
Responses API-г дууддаг тул `OPENAI_API_KEY` тоглоомын build дотор орохгүй.

## 1. Backend deploy хийх

1. Render дээр **New → Blueprint** сонгоод энэ repository-г холбоно.
2. Render root дахь `render.yaml`-г уншаад `moment-chatbot` web service үүсгэнэ.
3. `OPENAI_API_KEY` асуухад OpenAI dashboard-аас авсан key-г оруулна.
4. Deploy дууссаны дараа `/health` нь `{"status":"ok"}` буцааж байгааг шалгана.

Default model нь `gpt-5-mini`. Өөр дэмжигдсэн text model ашиглах бол Render
дээрх `OPENAI_MODEL` environment variable-г солино. Render Free service 15 минут
idle болсны дараа унтарч, дахин асахдаа ойролцоогоор нэг минут зарцуулдаг. Иймээс
Ren'Py request background-аар ажиллаж, 75 секунд timeout ашиглана. Paid instance
ашиглавал idle spin-down байхгүй.

## 2. Ren'Py-г холбох

`game/chatbot_config.rpy` доторх:

```renpy
define MOMENT_CHATBOT_API_URL = "https://YOUR-RENDER-SERVICE.onrender.com/api/chat"
```

гэсэн мөрийн URL-г Render-ийн service URL-аар солино. Төгсгөлд нь `/api/chat`
хэвээр үлдээнэ.

`OPENAI_API_KEY`-г `.rpy` файл, GitHub commit, game build эсвэл client header-д
**хийж болохгүй**. Тоглогч compiled build-ээс client талын утгыг гаргаж чадна.

## 3. Нэмэлт request gate

Энгийн хамгаалалт хэрэгтэй бол Render дээр `GAME_CLIENT_TOKEN` тохируулаад яг
ижил утгыг `MOMENT_CHATBOT_CLIENT_TOKEN`-д тавьж болно. Энэ утга тоглоомтой хамт
тархах тул жинхэнэ нууцлал биш, зөвхөн санамсаргүй хүсэлтийг хаана. Backend нь
мөн client IP бүрд rate limit хийдэг. Public release хийхдээ OpenAI project spend
limit тавьж, шаардлагатай бол жинхэнэ player authentication нэмнэ.

## Local backend test

Repository root-оос:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_key_here"
python app.py
```

Local game test хийхдээ Ren'Py URL-г түр хугацаанд ингэж солино:

```renpy
define MOMENT_CHATBOT_API_URL = "http://127.0.0.1:10000/api/chat"
```

Албан ёсны заавар: [OpenAI API quickstart](https://developers.openai.com/api/docs/quickstart),
[Render Flask deploy](https://render.com/docs/deploy-flask),
[Render Free хязгаарлалт](https://render.com/docs/free).
