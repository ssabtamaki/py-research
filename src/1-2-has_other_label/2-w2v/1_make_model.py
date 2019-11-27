from pathlib import Path
from typing import List
from gensim.models.word2vec import Word2Vec
from pandas import read_csv


def make_w2v(sentence: List[List[str]], model_path: str):
    '''
    CSVからモデル作成し保存
    '''
    model = Word2Vec(sentence, size=100, window=5, min_count=4, workers=4)
    model.save(model_path)


if __name__ == "__main__":
    cwd = Path().cwd()
    csv_path = cwd / 'data' / 'trend-死刑求刑.csv'
    model_path = cwd/'src'/'1-2-has_other_label'/'data'/"trend-死刑求刑.model"
    make_w2v(
        [row.split(" ") for row in read_csv(csv_path)['wakati_text'].dropna()],
        str(model_path)
    )
