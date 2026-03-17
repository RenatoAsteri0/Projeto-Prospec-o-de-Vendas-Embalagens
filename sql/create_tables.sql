CREATE TABLE IF NOT EXISTS industrial_companies (

    id SERIAL PRIMARY KEY,
    nome TEXT,
    endereco TEXT,
    telefone TEXT,
    notas FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);