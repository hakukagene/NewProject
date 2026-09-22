# Moment chatbot client configuration.
#
# After the Render service is deployed, replace YOUR-RENDER-SERVICE with the
# service name shown in the Render dashboard. Never put OPENAI_API_KEY here.

define MOMENT_CHATBOT_API_URL = "https://moment-chatbot-e41p.onrender.com/api/chat"
# Render Free can take about a minute to wake after an idle spin-down. This is
# a background request, so the longer timeout does not freeze the game UI.
define MOMENT_CHATBOT_REQUEST_TIMEOUT = 75.0
define MOMENT_CHATBOT_HISTORY_LIMIT = 16

# Optional lightweight gate for the public endpoint. This value is shipped
# with the game and therefore is not a substitute for server-side rate limits.
# Leave both this and Render's GAME_CLIENT_TOKEN unset to disable the gate.
define MOMENT_CHATBOT_CLIENT_TOKEN = ""
