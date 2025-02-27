""""""
from transformers import pipeline
import pandas as pd
import numpy as np
import openai


csp = [
        'Cadres et professions intellectuelles supérieures',
        'Ouvriers',
        'Retraités',
        'Professions intermédiaires',
        'Agriculteurs exploitants',
        'Autres personnes sans activité professionnelle',
        "Artisans, commerçants et chefs d'entreprise"
    ]


def zero_shot_openai():
    model = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
    client = openai.Client(base_url="http://localhost:8000/v1", api_key="key")
    df = pd.read_csv("data/meta_img_ocr.csv", sep=";")
    occupations = []
    for index, row in df.iterrows():
        text = row["text"].strip(".")
        prompt = f"Voici le texte qui figure dans une publicité: '{text}'. Peux-tu me dire à laquelle des catégories d'emploi suivantes ce texte correspond le mieux ? 'Cadres et professions intellectuelles supérieures', 'Ouvriers', 'Retraités', 'Professions intermédiaires', 'Agriculteurs exploitants', 'Autres personnes sans activité professionnelle', ou 'Artisans, commerçants et chefs d'entreprise' ? Donne moi un choix parmi ces options."
        output = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20
        )
        occupation = output.choices[0].message.content.split(".")[0]
        occupations.append(occupation)
        print(occupation)
    df["occupation"] = occupations
    df.to_csv("data/meta_occupations_llm.csv", sep=";")


def zero_shot_roberta_xnli():
    # TODO: You seem to be using the pipelines sequentially on GPU.
    # TODO: In order to maximize efficiency please use a dataset.
    classifier = pipeline(
        "zero-shot-classification",
        model="joeddav/xlm-roberta-large-xnli"
    )

    df = pd.read_csv("data/meta_img_ocr.csv", sep=";")
    occupations = []
    for index, row in df.iterrows():
        output = classifier(row["text"], csp)
        i = np.array(output["scores"]).argmax().item()
        occupation = csp[i]
        occupations.append(occupation)
    df["occupation"] = occupations
    df.to_csv("data/meta_occupations.csv", sep=";")


if __name__ == "__main__":
    zero_shot_openai()
