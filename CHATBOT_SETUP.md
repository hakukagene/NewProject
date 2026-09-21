# Moment chatbot — Gemini free tier + Render

Ren'Py тоглоом Render дээрх `moment-chatbot` backend руу холбогдоно. Backend нь
Google Gemini API-г дуудна. Тоглоомын DM, Сарагийн дүрийн заавар, Relationship,
Story Reply болон өмнөх 16 мессежийн урсгал хэвээр ажиллана.

## 1. Үнэгүй Gemini API key авах

1. [Google AI Studio API Keys](https://aistudio.google.com/api-keys)-д орж
   **Create API key** сонго. Шинээр үүсгэсэн **auth key** ашигла.
2. Google AI Studio-д project-ийн tier **Free** гэдгийг шалга. Төлбөртэй tier
   рүү шилжүүлэх шаардлагагүй. `gemini-2.5-flash-lite` model-ийн стандарт
   текст оролт/гаралт Free tier-д үнэгүй, харин хүсэлтийн тоо болон хурдны
   хязгаартай. Хязгаарыг өөрийн AI Studio-ийн Rate limits хэсгээс харна.
3. Free tier-р илгээсэн чат контентыг Google бүтээгдэхүүнээ сайжруулахад
   ашиглаж болохыг харгалз. Тоглогчийн бодит хувийн мэдээллийг чатаар
   явуулахгүй байх тухай нийтэд нээлттэй хувилбарт тайлбарлах нь зүйтэй.

Албан ёсны мэдээлэл: [үнэ ба контентын нөхцөл](https://ai.google.dev/gemini-api/docs/pricing),
[үнэгүй квот](https://ai.google.dev/gemini-api/docs/rate-limits),
[API key](https://ai.google.dev/gemini-api/docs/api-key).

## 2. Render-ийн одоо байгаа service-д key нэмэх

GitHub-ийн шинэ `main` commit Render-т deploy хийгдсэний дараа Render Dashboard
→ **moment-chatbot** → **Environment** → **Add Environment Variable**:

| Key | Value |
| --- | --- |
| `GEMINI_API_KEY` | AI Studio-оос авсан хувийн key |
| `GEMINI_MODEL` | `gemini-2.5-flash-lite` (Blueprint-д бэлэн) |

**Save and deploy** дар. `render.yaml`-д `GEMINI_API_KEY`-г `sync: false` гэж
зарласан ч **өмнө нь үүссэн Blueprint** шинэ secret-ийг автоматаар асуухгүй;
Render service-ийн Environment хэсэгт гараар оруулах хэрэгтэй. Хуучин
`OPENAI_API_KEY` одоо ашиглагдахгүй.

Key-г `.rpy`, `render.yaml`, GitHub commit, тоглоомын build эсвэл client header-д
битгий оруул. Тэр зөвхөн Render-ийн Environment-д байна.

## 3. Холболтыг шалгах

`https://moment-chatbot.onrender.com/health` хаяг `{"status":"ok"}` буцаавал
Render backend ажиллаж байна. Энэ нь AI key ажиллаж байгааг шалгахгүй.

PowerShell-оос бодит чат хүсэлт явуулж туршиж болно:

```powershell
$chatBody = @{ message = "Сайн уу?"; history = @(); relationship = 0 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "https://moment-chatbot.onrender.com/api/chat" -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($chatBody))
```

Амжилттай бол `reply` ирнэ. `503` = Render дээр `GEMINI_API_KEY` байхгүй;
`429` = backend эсвэл Gemini free quota хэтэрсэн; `502` = Gemini хүсэлт
бүтэлгүй (Render Logs-ийг шалга). Тоглоомоос мессеж явуулсны дараа Logs-д
`POST /api/chat` байхгүй бол локал тоглоомын URL-г шалга.

Тоглоомын [game/chatbot_config.rpy](game/chatbot_config.rpy) файлд
`MOMENT_CHATBOT_API_URL` нь яг Render service-ийн `/api/chat` хаяг байх ёстой.
URL солигдсон бол шинэ хаягаар нь солиод Ren'Py-г дахин эхлүүл.

## Нэмэлт client gate

Render дээр `GAME_CLIENT_TOKEN` тохируулсан бол тоглоомын
`MOMENT_CHATBOT_CLIENT_TOKEN` ижил байх ёстой. Client доторх token-г тоглогч
гаргаж авдаг тул жинхэнэ нууц биш. Туршилтад хоёуланг нь хоосон байлгаж болно.
Backend IP бүрт минутын rate limit хийнэ. Free tier нийт project-ийн
хязгаартай тул олон тоглогч зэрэг ашиглахад түр хугацаанд `429` гарч болно.

## Local backend test

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export GEMINI_API_KEY="your_key_here"
python app.py
```

Локал тест хийхдээ `MOMENT_CHATBOT_API_URL`-г түр хугацаанд
`http://127.0.0.1:10000/api/chat` болго.
