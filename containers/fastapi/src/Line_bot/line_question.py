"""質問応答を行うプログラム."""
import datetime
import json
from typing import Any

import ginza
import mysql.connector as mydb
import ndjson
import spacy


def question_about_department(text: str) -> str:
    """
    Parameters.

    ----------
    text : str

    Returns:
    ----------
    str
    """
    nlp = spacy.load("ja_ginza")
    json_open = open("学科に関する質問.json", "r")
    json_load = json.load(json_open)
    return question_about_department_program(json_load, nlp, text)


def question_about_school(text: str) -> str:
    """
    Parameters.

    ----------
    text : str

    Returns:
    ----------
    str
    """
    nlp = spacy.load("ja_ginza")
    json_open = open("本校に関する質問.json", "r")
    json_load = json.load(json_open)
    return question_about_department_program(json_load, nlp, text)


def question_about_other(text: str) -> str:
    """
    Parameters.

    ----------
    text : str

    Returns:
    ----------
    str
    """
    nlp = spacy.load("ja_ginza")
    json_open = open("その他に関する質問.json", "r")
    json_load = json.load(json_open)
    return question_about_department_program(json_load, nlp, text)


def question_about_department_program(json_load: Any, nlp: Any, text: str) -> Any:
    """
    Parameters.

    ----------
    json_load : str
    nlp : Any
    text : str

    Returns:
    ----------
    str

    """
    for v in json_load.values():
        count = 0
        # caregoryパターンの定義
        category = v["category"]
        # sub_caregoryパターンの定義
        sub_category = v["sub_category"]

        doc = nlp(text)
        # 文節分割
        for sent in doc.sents:
            for span in ginza.bunsetu_spans(sent):
                if category in span.text:
                    count += 1
                if sub_category in span.text:
                    count += 1

        if count == 2:
            return v["answer"]

    if count != 2:
        db_connector(text)
        return "現在その質問にお答えすることはできません"


def db_connector(text: str) -> None:
    """
    Parameters.

    ----------
    text : str
    """
    conn = mydb.connect(
        host="mysql_container",
        user="admin",
        passwd="password",
        port=3306,
        database="testdb",
    )

    # カーソルを取得する
    cur = conn.cursor()

    # SQL(データベースを操作するコマンド)を実行する
    # userテーブルから、HOSTとUSER列を取り出す
    sql = """INSERT INTO messages (message,time,add_rule) VALUES (%s, %s, %s)"""
    data = [(text, datetime.datetime.now(), True)]
    cur.executemany(sql, data)
    conn.commit()

    cur.close
    conn.close
    change_json(text)


def change_json(text: str) -> None:
    """
     Parameters .

    ----------
     text : str
    """
    filename = "答えられなかった質問.ndjson"

    # 現在時刻取得
    dt_now = datetime.datetime.now()
    date = dt_now.strftime("%Y年%m月%d日 %H:%M:%S")

    # 答えられなかった質問をdict形式に入れる
    question_dict = {"date": date, "question": text}

    with open(filename, "a") as f:
        writer = ndjson.writer(f, ensure_ascii=False)
        writer.writerow(question_dict)
