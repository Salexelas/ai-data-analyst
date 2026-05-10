import os

from dotenv import load_dotenv

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from core.llm_service import LLMService
from agents.service import answer_question

from connectors.factory import create_connector

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# SLACK
# =========================

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

# =========================
# LLM
# =========================

llm = LLMService()

# =========================
# DATASET
# =========================

DATA_PATH = "data"

files = sorted(os.listdir(DATA_PATH), reverse=True)

last_file = files[0]

file_path = os.path.join(DATA_PATH, last_file)

if last_file.endswith(".csv"):
    file_type = "csv"

elif last_file.endswith(".xlsx"):
    file_type = "excel"

else:
    raise ValueError("Unsupported dataset")

connector = create_connector(
    file_type,
    {"file_path": file_path}
)

# =========================
# EVENTS
# =========================

@app.event("message")
def handle_message(body, say):

    event = body["event"]

    if event.get("bot_id"):
        return

    question = event.get("text", "")

    try:

        result = answer_question(
            question=question,
            connector=connector,
            dataset_id=last_file,
            semantic_layer=None,
            llm=llm
        )

        if result["type"] == "table":

            explanation = result.get(
                "explanation",
                ""
            )

            data = result["data"]

            preview = data.head(10).to_string(index=False)

            response = f"""
{explanation}

```{preview}```
"""

        else:

            response = result.get(
                "message",
                "Error"
            )

    except Exception as e:

        response = f"❌ Error: {e}"

    say(response)

# =========================
# START
# =========================

if __name__ == "__main__":

    handler = SocketModeHandler(
        app,
        os.getenv("SLACK_APP_TOKEN")
    )

    handler.start()