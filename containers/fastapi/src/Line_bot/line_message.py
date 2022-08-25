"""ログファイルの出力を行うプログラム."""
import datetime


def file_write(text: str, reply: str) -> None:
    """
    Parameters.

    ----------
    text : str
    reply : str
    """
    # 現在時刻取得
    dt_now = datetime.datetime.now()
    date = dt_now.strftime("%Y年%m月%d日 %H:%M:%S")

    f = open("message.txt", "a", encoding="UTF-8")
    f.write(date + ":" + text + ":" + reply + "\n")
    f.close()


def file_read() -> str:
    """
    Parameters.

    returns:
    ----------
    str
    """
    f = open("message.txt", "r")
    # 全テキストをリスト配列で読み込む
    alltxt = f.readlines()
    f.close()
    # テキストの行数（最終行）を代入
    endgyou = len(alltxt)
    # 配列で最終行を取り出し代入。strip()で改行を取り除く
    endtxt = alltxt[endgyou - 1].strip()
    return endtxt
