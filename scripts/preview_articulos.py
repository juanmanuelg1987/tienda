import pandas as pd

archivo = r"C:\Users\juan_\Downloads\lista_reagrupada.xlsx"
df = pd.read_excel(archivo)

# Mostrar las primeras 10 filas para ver estructura y columnas
print(df.head(10))
print("\nColumnas detectadas:", list(df.columns))
