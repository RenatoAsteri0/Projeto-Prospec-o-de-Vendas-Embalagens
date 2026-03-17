from airflow import DAG
from datetime import datetime
from airflow.providers.standard.operators.python import PythonOperator
from src.integrations.google_drive_api import send_file_googledrive_api
from src.extract_data_google_scrapy import extract_places
from src.export_results import export_leads_report
from src.tranform_data_pandas import transform_places
from src.load_postgres import load_dataframe


def run_pipeline():
    data = extract_places()
    df = transform_places(data)
    load_dataframe(df)
    export_leads_report(df)

def upload_exports():
    send_file_googledrive_api()


with DAG(
    dag_id="google_maps_industrial_leads",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    run_etl = PythonOperator(
        task_id="run_google_maps_etl",
        python_callable=run_pipeline
    )
    upload_to_drive = PythonOperator(
        task_id="upload_to_google_drive",
        python_callable=upload_exports,
    )
    run_etl >> upload_to_drive