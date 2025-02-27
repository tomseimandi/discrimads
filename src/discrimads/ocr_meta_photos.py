""""""
from pathlib import Path
from discrimads.ocr import ocr
import os
import pandas as pd
import easyocr


def tessract_ocr():
    results = []
    files = os.listdir("ads")
    files = filter(lambda x: x.endswith(".jpg"), files)
    files = list(files)
    paths = list(map(lambda x: Path("ads") / x, files))
    for path in paths:
        results.append(ocr(str(path)))
    df = pd.DataFrame(data={
        "file": files,
        "text": results,
    })
    df.to_csv("data/meta_img_ocr.csv", sep=";")
    return


def easy_ocr():
    results = []
    files = os.listdir("ads")
    files = filter(lambda x: x.endswith(".jpg"), files)
    files = list(files)
    paths = list(map(lambda x: Path("ads") / x, files))

    reader = easyocr.Reader(['fr'])
    for path in paths:
        result = reader.readtext(str(path), detail=0)
        results.append(" ".join(result))
    df = pd.DataFrame(data={
        "file": files,
        "text": results,
    })
    df.to_csv("data/meta_img_ocr.csv", sep=";")
    return


if __name__ == "__main__":
    easy_ocr()
