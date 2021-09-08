# gensim
# from gensim.test.utils import common_texts
from gensim.models import Word2Vec

# ORM
from models import init_models

DB_NAME = "2021-09-05 15:24:22.024041.db"
SESSION, BASE, ENGINE, Unit = init_models(db_file_name=DB_NAME)


def train_model():
    # создаём текста для обучения алгоритма
    units = SESSION.query(Unit).all()
    learning_texts = []
    for unit in units:
        unit_text = unit.title.split(" ")
        unit_text.append(f"{unit.price} руб")
        learning_texts.append(unit_text)

    model = Word2Vec(sentences=learning_texts, vector_size=100, window=5, min_count=1, workers=4)
    model.save("word2vec.model")


if __name__ == "__main__":
    model = Word2Vec.load("word2vec.model")
    # vector = model.wv['принтер']
    sims = model.wv.most_similar('чехол', topn=10)
    print(sims)
