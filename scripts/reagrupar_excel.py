import pandas as pd
import os

# Ruta del archivo original y del archivo de salida
archivo_entrada = r"C:\Users\juan_\Downloads\lista.xlsx"
archivo_salida = r"C:\Users\juan_\Downloads\lista_reagrupada.xlsx"

# Leer los nombres de las hojas
hojas = pd.ExcelFile(archivo_entrada).sheet_names

# Tomar solo las primeras 14 hojas
hojas_a_leer = hojas[:14]

# Lista para almacenar los DataFrames
dfs = []

for hoja in hojas_a_leer:
    df = pd.read_excel(archivo_entrada, sheet_name=hoja)
    df['Hoja_Origen'] = hoja
    dfs.append(df)

# Concatenar todos los DataFrames
resultado = pd.concat(dfs, ignore_index=True)

# Guardar en un nuevo archivo Excel
resultado.to_excel(archivo_salida, index=False)

print(f"Archivo reagrupado guardado en: {archivo_salida}")
