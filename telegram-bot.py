import telebot as telegram
import csv
import datetime as dt
import os
from dotenv import load_dotenv


# CONFIGURACIÓN INICIAL
load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")
if not TOKEN:
    raise ValueError("No se encuentra el token. Revisa el archivo .env!")
telegram_bot = telegram.TeleBot(TOKEN)


# LECTURA Y ANÁLISIS
@telegram_bot.message_handler(commands=["reporte"])
def enviar_reporte(mensaje):
    today = dt.datetime.today()
    actual_year = today.year
    actual_month = today.month
    reporte_gastos = {}

    with open("gastos.csv", "r", newline="") as archivo:
        reader = csv.reader(archivo)

        next(reader)
        for gasto in reader:
            gasto_fecha = dt.datetime.fromisoformat(gasto[0])
            gasto_monto = float(gasto[1])
            gasto_categoria = gasto[2]

            if (gasto_fecha.month != actual_month) or (gasto_fecha.year != actual_year):
                continue

            if gasto_categoria in reporte_gastos:
                reporte_gastos[gasto_categoria] += gasto_monto
            else:
                reporte_gastos[gasto_categoria] = gasto_monto

    reporte_final = "REPORTE DEL MES! 📑 \n\n"
    monto_total = 0.0

    for categoria, monto in reporte_gastos.items():
        reporte_final += f"▫️ {categoria.capitalize()}: ${monto:.2f} \n"
        monto_total += monto

    reporte_final += f"\n💰TOTAL GASTADO: ${monto_total}"

    telegram_bot.reply_to(mensaje, str(reporte_final))


# AGREGAR GASTO
@telegram_bot.message_handler(func=lambda _: True)
def agregar_gasto(mensaje):
    # VARIALES GLOBALES
    today = dt.date.today()
    texto = mensaje.text

    informacion_gastos = texto.split(maxsplit=2)

    if len(informacion_gastos) != 3:
        telegram_bot.reply_to(mensaje, "Te faltó mandar más datos, vuelve a intentarlo")
        return

    monto = informacion_gastos[0]
    try:
        monto = float(monto)
    except ValueError:
        telegram_bot.reply_to(mensaje, "Manda un número valido!")
        return

    categoria = informacion_gastos[1].strip().lower()
    descripcion = informacion_gastos[2].strip().lower()
    gasto_nuevo = [today, monto, categoria, descripcion]

    with open("gastos.csv", "a", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(gasto_nuevo)

    telegram_bot.reply_to(mensaje, "Gasto agregado correctamente:")


print("Bot escuchando...")
telegram_bot.infinity_polling()
