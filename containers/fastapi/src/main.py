"""LINEのメインプログラム."""
import json
import os
from typing import Any, Dict

from aiolinebot import AioLineBotApi
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Request
from linebot import WebhookParser
from linebot.models import TextMessage

from .Line_bot import line_message, line_model, line_question, line_rulebase

# os.environを用いて環境変数を表示させます
load_dotenv()
line_api = AioLineBotApi(channel_access_token=os.getenv("CHANNEL_ACCSESS_TOKEN"))
parser = WebhookParser(channel_secret=os.getenv("CHANNEL_SECRET"))

app = FastAPI()

# パス変更
os.chdir("containers/fastapi/src/Line_bot")


@app.get("/")
def main() -> Dict[str, str]:
    """
    RETRUNS.

    ----------
    Dict[str, str]
        おはようのあいさつをする。使用されることはない
    """
    return {"次の一手": "おはよう"}


@app.post("/callback")
async def callback(request: Request, background_tasks: BackgroundTasks) -> str:
    """
    Parameters.

    ----------
    request : Request
    background_tasks : BackgroundTasks

    Returns:
    ----------
    str
    """
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", ""),
    )
    background_tasks.add_task(handle_events, events=events)
    return "ok"


async def handle_events(events: Any) -> None:
    """
    Parameters.

    ----------
    events: Any

    Returns:
    ----------
    str
    """
    for event in events:
        try:
            message_text = line_message.file_read()
            json_load = json.loads(str(events[0].source))
            user_information = json.loads(str(line_api.get_profile(str(json_load["userId"]))))
            await line_program(event, message_text, user_information["displayName"])
        except Exception:
            pass


async def line_program(event: Any, message_text: str, userName: str) -> None:
    """
    Parameters.

    ----------
    event : parser
    message_text : str
    """
    if "学校に関する質問" in event.message.text:
        messages = line_rulebase.make_button_template()
        await line_api.reply_message_async(event.reply_token, messages)
    elif "学科について" in event.message.text:
        await line_api.reply_message_async(event.reply_token, TextMessage(text="学科についてですね!!質問ください!!"))
        line_message.file_write(
            "学科に関する質問",
            "未返信",
        )
    elif "本校について" in event.message.text:
        await line_api.reply_message_async(event.reply_token, TextMessage(text="本校についてですね!!質問ください!!"))
        line_message.file_write("本校に関する質問", "未返信")
    elif "その他" in event.message.text:
        await line_api.reply_message_async(event.reply_token, TextMessage(text="なんでもご質問ください!!"))
        line_message.file_write("その他に関する質問", "未返信")
    elif ("学科" in message_text) and ("未返信" in message_text):
        await line_api.reply_message_async(
            event.reply_token,
            TextMessage(text=line_question.question_about_department(event.message.text)),
        )
        line_message.file_write("学科に関する質問", "返信済")
    elif ("本校" in message_text) and ("未返信" in message_text):
        await line_api.reply_message_async(
            event.reply_token,
            TextMessage(text=line_question.question_about_school(event.message.text)),
        )
        line_message.file_write("本校に関する質問", "返信済")
    elif ("その他" in message_text) and ("未返信" in message_text):
        await line_api.reply_message_async(
            event.reply_token,
            TextMessage(text=line_question.question_about_other(event.message.text)),
        )
        line_message.file_write("その他に関する質問", "返信済")
    else:
        await line_api.reply_message_async(
            event.reply_token,
            TextMessage(text=line_model.chat(event.message.text, userName)),
        )
