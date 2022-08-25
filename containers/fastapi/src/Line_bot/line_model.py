"""雑談を行うプログラム."""
import random
from typing import Any

from gensim.models import word2vec
from janome.tokenizer import Tokenizer


def chat(text: str, userName: str) -> Any:
    """
     Parameters .

    ----------
     text : str
     userName: str

     Returns:
     ----------
     answer : Any
    """
    # wikimediaモデル呼出し
    model = word2vec.Word2Vec.load("./models/wiki.model")

    noun = ""
    t = Tokenizer()
    malist = t.tokenize(text)
    for word in malist:
        part1 = word.part_of_speech.split(",")[0]
        part2 = word.part_of_speech.split(",")[1]
        part3 = word.part_of_speech.split(",")[2]
        if part1 == "名詞" and part2 == "一般":
            noun = word.surface
        elif part1 == "名詞" and part2 == "代名詞" and part3 == "一般":
            answer = random.choice((model.wv.most_similar(positive=noun)))
            return answer[0] + "です!"
        elif part1 == "感動詞":
            return userName + "さん" + text + "!"
        else:
            answer = random.choice((model.wv.most_similar(positive=noun)))
            return answer[0]
