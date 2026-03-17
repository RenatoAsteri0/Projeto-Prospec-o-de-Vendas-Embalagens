import pandas as pd

def transform_places(data):

    df = pd.DataFrame(data)

    df = df.rename(columns={
        "title": "nome",
        "address": "endereco",
        "phone": "telefone",
        "rating": "notas"
    })

    # garante que as colunas existem
    expected_columns = ["nome", "endereco", "telefone", "notas"]

    for col in expected_columns:
        if col not in df.columns:
            df[col] = None

    df = df[expected_columns]

    df = df.drop_duplicates(subset=["nome", "endereco"])

    return df