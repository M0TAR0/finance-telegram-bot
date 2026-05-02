import csv
from datetime import date

# OBTENER DATOS DEL USUARIO

fecha = date.today()

while True:
    monto = input("Ingresa el monto: ")
    try:
        monto = float(monto)
        break
    except ValueError:
        print("Error: Por favor ingresa un número válido (ej. 150, 150.50")

categoria = input("Ingresa categoría: ").strip().lower()
descripcion = input("Ingresa descripcion: ").strip().lower()

# AGREGAR AL CSV

nuevo_gasto = [fecha, monto, categoria, descripcion]
with open("gastos.csv", mode="a", newline="", encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(nuevo_gasto)

print("Gasto guardado:")
print(nuevo_gasto)
