from datetime import datetime
from os import getenv
from pathlib import Path
import pandas as pd


DEFAULT_EXPORT_DIR = "exports"


def export_leads_report(df: pd.DataFrame, output_dir: str | None = None) -> dict[str, str]:
    export_df = _build_accessible_dataframe(df)
    export_path = Path(output_dir or getenv("EXPORT_DIR") or DEFAULT_EXPORT_DIR)
    export_path.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now().strftime("%Y%m%d_%H:%M")
    csv_path = export_path / f"provaveis_industrias_{generated_at}.csv"
    export_df.to_csv(csv_path, index=False, encoding="utf-8")

    return {
        "csv": str(csv_path)
    }


def _build_accessible_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    export_df = df.copy()

    export_df["nome"] = export_df["nome"].fillna("Nao informado").astype(str).str.strip()
    export_df["endereco"] = export_df["endereco"].fillna("Nao informado").astype(str).str.strip()
    export_df["telefone"] = export_df["telefone"].fillna("Nao informado").astype(str).str.strip()
    export_df["notas"] = pd.to_numeric(export_df["notas"], errors="coerce")

    export_df["avaliacao_google"] = export_df["notas"].map(
        lambda value: f"{value:.1f}" if pd.notna(value) else "Nao informado"
    )
    export_df["possui_telefone"] = export_df["telefone"].map(
        lambda value: "Sim" if value and value != "Nao informado" else "Nao"
    )
    export_df["data_coleta"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    export_df["origem"] = "Google Maps via Apify"

    export_df = export_df.rename(
        columns={
            "nome": "Empresa",
            "endereco": "Endereco",
            "telefone": "Telefone",
        }
    )

    export_df = export_df[
        [
            "Empresa",
            "Endereco",
            "Telefone",
            "possui_telefone",
            "avaliacao_google",
            "origem",
            "data_coleta",
        ]
    ]

    export_df = export_df.sort_values(by=["Empresa", "Endereco"]).reset_index(drop=True)
    export_df.index = export_df.index + 1
    export_df.insert(0, "Lead", export_df.index)
    return export_df