import pdfplumber
import csv

PDF_PATH = r"C:\Users\juan_\Downloads\LISTA DE PRECIOS  CH 27.06.2025.pdf"
CSV_OUT = "precios_extraidos_pdf.csv"

rows = []
with pdfplumber.open(PDF_PATH) as pdf:
    for i, page in enumerate(pdf.pages):
        # Intenta extraer todas las tablas de la página
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                # Filtra filas vacías
                if row and any(cell and cell.strip() for cell in row):
                    rows.append([cell.strip() if cell else '' for cell in row])

# Guarda como CSV para revisión
with open(CSV_OUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

print(f"Extraídas {len(rows)} filas del PDF. Guardado en {CSV_OUT}")
