# Practica-ETL_SRI_Ventas2025
PROYECTO :CONSTRUCCIÓN DE PROCESOS ETL CON APACHE AIRFLOW Y GOOGLE BIGQUERY

ETL Ventas SRI – Apache Airflow & BigQuery
Este proyecto implementa un proceso ETL (Extracción, Transformación y Carga) utilizando Apache Airflow (mediante Cloud Composer en GCP) para integrar y analizar datos de ventas registrados por el Servicio de Rentas Internas (SRI) del Ecuador.

 Descripción
El flujo de trabajo orquestado por Airflow permite cargar un archivo .csv con datos de ventas por provincia, cantón, sector económico y mes, y transformarlos en un modelo dimensional en estrella en Google BigQuery, ideal para análisis OLAP.

Estructura del Repositorio
bash
Copiar
Editar
sri-etl-ventas/
├── dags/
│   └── sri_ventas_etl_dag.py           # DAG principal de Airflow
├── scripts/
│   ├── __init__.py
│   └── transformaciones.py             # Funciones auxiliares ETL
├── README.md
 Modelo Dimensional
El modelo estrella está compuesto por:

Fact_VentasSRI: ventas y compras agregadas por ubicación, sector y tiempo.

Dim_Tiempo: año y mes.

Dim_Ubicacion: provincia y cantón.

Dim_Sector: código del sector económico.

 Tecnologías
Apache Airflow (via Cloud Composer)

Google Cloud Storage (GCS)

Google BigQuery

Python (Pandas, Google Cloud Client Libraries)

Requisitos
Cuenta en Google Cloud Platform

Proyecto con Composer, BigQuery y Storage habilitados

Archivo CSV: sri_ventas_2025.csv

Archivo de credenciales JSON con acceso a BigQuery y GCS

 Ejecución del DAG
Subir el archivo .csv al bucket de Cloud Storage en /data/sri_ventas_2025.csv.

Cargar el DAG sri_ventas_etl_dag.py en el directorio /dags/ del entorno Composer.

Lanzar manualmente el DAG desde la UI de Airflow.

Verificar que las tablas Dim_Tiempo, Dim_Ubicacion, Dim_Sector y Fact_VentasSRI se generen en BigQuery sin errores.
