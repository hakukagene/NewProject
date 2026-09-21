import io
import json
import os
import urllib.error
import unittest
from unittest.mock import patch

import app as chatbot


class ChatbotApiTests(unittest.TestCase):
    def setUp(self):
        self.env_patcher = patch.dict(
            os.environ,
            {
                "GEMINI_API_KEY": "",
                "GEMINI_MODEL": "gemini-2.5-flash-lite",
                "GAME_CLIENT_TOKEN": "",
                "CHAT_RATE_LIMIT_PER_MINUTE": "12",
            },
            clear=False,
        )
        self.env_patcher.start()
        self.addCleanup(self.env_patcher.stop)
        chatbot.app.config.update(TESTING=True)
        chatbot._rate_hits.clear()
        self.client = chatbot.app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_message_is_required(self):
        response = self.client.post("/api/chat", json={"message": ""})
        self.assertEqual(response.status_code, 400)

    def test_missing_gemini_key(self):
        response = self.client.post("/api/chat", json={"message": "Сайн уу?"})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json(), {"error": "service_not_configured"})

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=False)
    @patch.object(chatbot, "generate_reply", return_value="Тэгье, дараа ярья 😊")
    def test_chat_reply(self, mocked_reply):
        response = self.client.post(
            "/api/chat",
            json={
                "message": "Маргааш уулзах уу?",
                "history": [],
                "relationship": 28,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["reply"], "Тэгье, дараа ярья 😊")
        mocked_reply.assert_called_once()

    @patch.dict(
        os.environ,
        {"GEMINI_API_KEY": "test-key", "GEMINI_MODEL": "gemini-2.5-flash-lite"},
        clear=False,
    )
    @patch.object(chatbot.urllib.request, "urlopen")
    def test_generate_reply_uses_gemini_and_deduplicates_history(self, mocked_urlopen):
        mocked_urlopen.return_value = io.BytesIO(
            json.dumps(
                {"candidates": [{"content": {"parts": [{"text": "Тийм ээ, санаж байна."}]}}]}
            ).encode("utf-8")
        )
        reply = chatbot.generate_reply(
            {
                "message": "Тэр газрыг санаж байна уу?",
                "history": [
                    {"sender": "sara", "text": "Нуур үнэхээр гоё байсан."},
                    {"sender": "player", "text": "Тэр газрыг санаж байна уу?"},
                ],
                "relationship": 42,
            }
        )

        self.assertEqual(reply, "Тийм ээ, санаж байна.")
        gemini_request = mocked_urlopen.call_args.args[0]
        self.assertEqual(mocked_urlopen.call_args.kwargs["timeout"], 25)
        self.assertEqual(gemini_request.get_method(), "POST")
        self.assertEqual(
            gemini_request.full_url,
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent",
        )
        self.assertEqual(gemini_request.get_header("X-goog-api-key"), "test-key")
        body = json.loads(gemini_request.data.decode("utf-8"))
        self.assertIn("Сара", body["system_instruction"]["parts"][0]["text"])
        self.assertEqual([turn["role"] for turn in body["contents"]], ["user", "model", "user"])
        self.assertEqual(body["contents"][-1]["parts"], [{"text": "Тэр газрыг санаж байна уу?"}])
        self.assertEqual(
            chatbot._gemini_contents([], "Сайн уу?"),
            [{"role": "user", "parts": [{"text": "Сайн уу?"}]}],
        )

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=False)
    @patch.object(chatbot.urllib.request, "urlopen")
    def test_gemini_quota_error_maps_to_429(self, mocked_urlopen):
        mocked_urlopen.side_effect = urllib.error.HTTPError(
            "https://generativelanguage.googleapis.com/", 429, "Quota exceeded", {}, None
        )
        response = self.client.post("/api/chat", json={"message": "Сайн уу?"})
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.get_json(), {"error": "free_tier_limit"})

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=False)
    @patch.object(chatbot.urllib.request, "urlopen")
    def test_gemini_auth_error_maps_to_502(self, mocked_urlopen):
        mocked_urlopen.side_effect = urllib.error.HTTPError(
            "https://generativelanguage.googleapis.com/", 403, "Invalid key", {}, None
        )
        response = self.client.post("/api/chat", json={"message": "Сайн уу?"})
        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.get_json(), {"error": "upstream_error"})

    @patch.dict(
        os.environ,
        {"GEMINI_API_KEY": "test-key", "GAME_CLIENT_TOKEN": "gate-token"},
        clear=False,
    )
    def test_optional_game_token(self):
        response = self.client.post("/api/chat", json={"message": "Сайн уу?"})
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
