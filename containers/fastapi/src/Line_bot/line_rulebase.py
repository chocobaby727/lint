"""学校に関する質問のセレクトボックスを表示するプログラム."""
from typing import Any

from linebot.models import ButtonsTemplate, MessageAction, TemplateSendMessage


def make_button_template() -> Any:
    """
    Parameters.

    Returns:
    ----------
    Any
    """
    message_template = TemplateSendMessage(
        alt_text="学校に関する質問",
        template=ButtonsTemplate(
            text="どれについて知りたいですか?",
            title=None,
            image_size=None,
            thumbnail_image_url=None,
            actions=[
                MessageAction(text="学科について", label="学科について"),
                MessageAction(text="本校について", label="本校について"),
                MessageAction(text="その他", label="その他"),
            ],
        ),
    )
    return message_template
