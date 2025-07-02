# sri_ventas_etl_dag.py

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import logging
from scripts.transformaciones import (
    cargar_dim_tiempo,
    cargar_dim_ubicacion,
    cargar_dim_sector,
    cargar_fact_ventas
)

default_args = {
    'owner': 'Fernando',
    'start_date': datetime(2025, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'sri_ventas_etl',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    description='DAG ETL para cargar datos de ventas del SRI a BigQuery'
)

start = EmptyOperator(task_id='start', dag=dag)
end = EmptyOperator(task_id='end', dag=dag)

procesar_dim_tiempo = PythonOperator(
    task_id='procesar_dim_tiempo',
    python_callable=cargar_dim_tiempo,
    dag=dag
)

procesar_dim_ubicacion = PythonOperator(
    task_id='procesar_dim_ubicacion',
    python_callable=cargar_dim_ubicacion,
    dag=dag
)

procesar_dim_sector = PythonOperator(
    task_id='procesar_dim_sector',
    python_callable=cargar_dim_sector,
    dag=dag
)

procesar_fact_ventas = PythonOperator(
    task_id='procesar_fact_ventas',
    python_callable=cargar_fact_ventas,
    dag=dag
)

start >> [procesar_dim_tiempo, procesar_dim_ubicacion, procesar_dim_sector] >> procesar_fact_ventas >> end