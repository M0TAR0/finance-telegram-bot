import csv
import datetime as dt

# Fechas
hoy = dt.date.today()
mes_actual = hoy.month
ano_actual = hoy.year

registro = {}
with open("gastos.csv", newline="") as archivo:
    reader = csv.reader(archivo)

    next(reader)

    for row in reader:
        fecha_gasto = dt.date.fromisoformat(row[0])
        if fecha_gasto.year != ano_actual or fecha_gasto.month != mes_actual:
            continue

        categoria = row[2]
        monto = float(row[1])

        if row[2] in registro:
            registro[categoria] += monto
        else:
            registro[categoria] = monto
print(registro)
