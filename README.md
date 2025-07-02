# ETL de Ventas del SRI con Apache Airflow y BigQuery

Este repositorio contiene la solución completa para la implementación de un pipeline ETL (Extracción, Transformación y Carga) sobre los datos públicos de ventas del Servicio de Rentas Internas (SRI) del Ecuador. El flujo fue desarrollado utilizando Apache Airflow en Cloud Composer y los datos son almacenados y analizados en Google BigQuery.

## 🗂 Estructura del Proyecto

- `dags/`: Contiene el DAG de Airflow (`etl_ventas_sri_dag.py`).
- `scripts/`: Scripts Python auxiliares para transformación de datos.
- `data/`: Carpeta para el CSV de entrada y otros recursos.
- `README.md`: Este archivo.

## 📊 Dataset y Modelo Dimensional

El dataset utilizado corresponde a datos agregados del SRI sobre ventas, importaciones y exportaciones por sector, ubicación y tiempo. El modelo dimensional propuesto incluye:

### Tabla de Hechos: `Fact_VentasSRI`
- Claves foráneas: `id_tiempo`, `id_ubicacion`, `id_sector`
- Métricas: `ventas_tarifa_gravada`, `ventas_tarifa_0`, `exportaciones`, `total_ventas`, entre otras.

### Dimensiones
- `Dim_Tiempo`: año, mes
- `Dim_Ubicacion`: provincia, cantón
- `Dim_Sector`: código del sector económico

## ☁️ Arquitectura en la Nube

El pipeline fue implementado en GCP utilizando:
- **Cloud Composer (Apache Airflow)** para orquestación
- **BigQuery** como destino de datos
- **Cloud Storage** para almacenamiento temporal
- **IAM** con cuenta de servicio dedicada

## 🛠 DAG de Airflow

El DAG incluye tareas para:
- Carga inicial del CSV fuente
- Procesamiento y carga de dimensiones
- Procesamiento y carga de la tabla de hechos
- Validaciones de integridad referencial

## ✅ Ejecución y Resultados

El DAG fue ejecutado exitosamente desde Cloud Composer y los datos fueron cargados a BigQuery con integridad garantizada. Se verificaron los registros cargados, los joins con dimensiones y las métricas numéricas.

## 📌 Conclusiones

- El modelo estrella permite análisis eficientes por tiempo, ubicación y sector económico.
- Airflow en Cloud Composer facilitó la orquestación robusta del flujo ETL.
- BigQuery permitió consultas rápidas sobre grandes volúmenes de datos.

