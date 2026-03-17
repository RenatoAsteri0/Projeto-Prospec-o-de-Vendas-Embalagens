import psycopg2

def load_dataframe(df):
    conn = psycopg2.connect(
        host="localhost",
        database="airflow",
        user="airflow",
        password="airflow"
    )

    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute("""
        INSERT INTO industrial_companies
        (nome, endereco, telefone, notas)
        VALUES (%s, %s, %s, %s)
        """, (
            row["nome"],
            row["endereco"],
            row["telefone"],
            row["notas"]
        ))

    conn.commit()

    cursor.close()
    conn.close()

    print("Dados inseridos no PostgreSQL com sucesso")