import pandas as pd
import re

# Ruta del archivo Excel reagrupado
df = pd.read_excel(r"C:\Users\juan_\Downloads\lista_reagrupada.xlsx")

# Heurística para identificar filas que parecen productos:
def es_producto(row):
    # Tomar el valor de la primera columna real
    primera_col = row.iloc[0]
    nombre = str(primera_col)
    # Consideramos producto si el nombre tiene mayúsculas y parece un nombre de artículo
    return bool(re.match(r"^[A-ZÁÉÍÓÚÑ0-9][A-ZÁÉÍÓÚÑa-záéíóúñ0-9\-\.\s]+", nombre)) and len(nombre) > 10

# Filtrar solo filas que parecen productos
productos = df[df.apply(es_producto, axis=1)]

# Seleccionar solo las primeras columnas relevantes (ajustar según necesidad)
primeras_columnas = list(df.columns[:5])
# Solo incluir 'Hoja_Origen' si existe en el DataFrame
columnas_relevantes = primeras_columnas.copy()
if 'Hoja_Origen' in productos.columns:
    columnas_relevantes.append('Hoja_Origen')
productos = productos[columnas_relevantes]

# Renombrar columnas para facilitar la futura carga a base de datos
productos = productos.rename(columns={
    primeras_columnas[0]: 'nombre',
    primeras_columnas[1]: 'col1',
    primeras_columnas[2]: 'col2',
    primeras_columnas[3]: 'col3',
    primeras_columnas[4]: 'col4',
})

# Guardar a CSV para revisión
productos.to_csv('articulos_limpios.csv', index=False)

print(f"Se detectaron {len(productos)} productos. Guardados en articulos_limpios.csv para revisión.")
print(productos.head(10))
