import os
import unittest
from unittest.mock import patch

import app as chatbot


class ChatbotApiTests(unittest.TestCase):
    def setUp(self):
        self.env_patcher = patch.dict(
            os.environ,
            {"GAME_CLIENT_TOKEN": "", "CHAT_RATE_LIMIT_PER_MINUTE": "12"},
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

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False)
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

    @patch.dict(os.environ, {"OPENAI_MODEL": "gpt-5-mini"}, clear=False)
    @patch.object(chatbot, "OpenAI")
    def test_generate_reply_uses_responses_api(self, mocked_openai):
        mocked_openai.return_value.responses.create.return_value.output_text = (
            "Тийм ээ, санаж байна."
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
        call = mocked_openai.return_value.responses.create.call_args.kwargs
        self.assertEqual(call["model"], "gpt-5-mini")
        self.assertEqual(call["input"][-1]["role"], "user")
        self.assertEqual(len(call["input"]), 2)
        self.assertFalse(call["store"])
        mocked_openai.assert_called_once_with(timeout=25.0, max_retries=0)

    @patch.dict(
        os.environ,
        {"OPENAI_API_KEY": "test-key", "GAME_CLIENT_TOKEN": "gate-token"},
        clear=False,
    )
    def test_optional_game_token(self):
        response = self.client.post("/api/chat", json={"message": "Сайн уу?"})
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
