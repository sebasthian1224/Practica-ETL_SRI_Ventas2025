# transformaciones.py

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Inicializar cliente BigQuery
# (Solo si lo usas localmente, en Composer usa autenticación implícita)
# credentials = service_account.Credentials.from_service_account_file('ruta/credenciales.json')
# client = bigquery.Client(credentials=credentials, project='tu-proyecto')
client = bigquery.Client()

def transformar_dim_tiempo(df):
    dim = df[['AÑO', 'MES']].drop_duplicates().copy()
    dim = dim.dropna()
    dim = dim.sort_values(by=['AÑO', 'MES']).reset_index(drop=True)
    dim['id_tiempo'] = dim.index + 1
    dim = dim[['id_tiempo', 'AÑO', 'MES']].rename(columns={'AÑO': 'anio', 'MES': 'mes'})
    return dim

def transformar_dim_ubicacion(df):
    dim = df[['PROVINCIA', 'CANTON']].drop_duplicates().copy()
    dim = dim.dropna()
    dim = dim.sort_values(by=['PROVINCIA', 'CANTON']).reset_index(drop=True)
    dim['id_ubicacion'] = dim.index + 1
    dim = dim[['id_ubicacion', 'PROVINCIA', 'CANTON']]
    return dim

def transformar_dim_sector(df):
    dim = df[['CODIGO_SECTOR_N1']].drop_duplicates().copy()
    dim = dim.dropna().sort_values(by='CODIGO_SECTOR_N1').reset_index(drop=True)
    dim['id_sector'] = dim.index + 1
    dim = dim[['id_sector', 'CODIGO_SECTOR_N1']]
    return dim

def transformar_tabla_hechos(df, dim_tiempo, dim_ubicacion, dim_sector):
    df = df.dropna(subset=['AÑO', 'MES', 'PROVINCIA', 'CANTON', 'CODIGO_SECTOR_N1'])
    
    df = df.merge(dim_tiempo, left_on=['AÑO', 'MES'], right_on=['anio', 'mes'])
    df = df.merge(dim_ubicacion, on=['PROVINCIA', 'CANTON'])
    df = df.merge(dim_sector, on='CODIGO_SECTOR_N1')

    df['ventas_tarifa_gravada'] = df['VENTAS_NETAS_TARIFA_GRAVADA'].fillna(0).astype(float)
    df['ventas_tarifa_0'] = df['VENTAS_NETAS_TARIFA_0'].fillna(0).astype(float)
    df['ventas_tarifa_variable'] = df['VENTAS_NETAS_TARIFA_VARIABLE'].fillna(0).astype(float)
    df['ventas_tarifa_5'] = df['VENTAS_NETAS_TARIFA_5'].fillna(0).astype(float)
    df['exportaciones'] = df['EXPORTACIONES'].fillna(0).astype(float)
    df['compras_tarifa_gravada'] = df['COMPRAS_NETAS_TARIFA_GRAVADA'].fillna(0).astype(float)
    df['compras_tarifa_0'] = df['COMPRAS_NETAS_TARIFA_0'].fillna(0).astype(float)
    df['importaciones'] = df['IMPORTACIONES'].fillna(0).astype(float)
    df['compras_rise'] = df['COMPRAS_RISE'].fillna(0).astype(float)
    df['total_compras'] = df['TOTAL_COMPRAS'].fillna(0).astype(float)
    df['total_ventas'] = df['TOTAL_VENTAS'].fillna(0).astype(float)

    df_fact = df[[
        'id_tiempo', 'id_ubicacion', 'id_sector',
        'ventas_tarifa_gravada', 'ventas_tarifa_0', 'ventas_tarifa_variable',
        'ventas_tarifa_5', 'exportaciones', 'compras_tarifa_gravada',
        'compras_tarifa_0', 'importaciones', 'compras_rise',
        'total_compras', 'total_ventas'
    ]].copy()

    df_fact['id_fact_ventas'] = df_fact.reset_index().index + 1
    df_fact = df_fact[['id_fact_ventas'] + df_fact.columns[:-1].tolist()]

    return df_fact