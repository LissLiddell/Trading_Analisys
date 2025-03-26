import pandas as pd
import numpy as np
import yfinance as yf
import ta
import requests

# Descargar datos de USD/JPY en la última semana con intervalos de 1 hora
data = yf.download("USDJPY=X", period="7d", interval="15m", auto_adjust=False)

# Asegurar que 'Close' es una Serie (1D)
close_prices = data["Close"].squeeze()

# Calcular indicadores técnicos
data["RSI"] = ta.momentum.RSIIndicator(close_prices, window=14).rsi()
data["MACD"] = ta.trend.MACD(close_prices).macd()
data["Signal"] = ta.trend.MACD(close_prices).macd_signal()

# Última fila (el dato más reciente)
last_price = close_prices.iloc[-1]  # Último precio de cierre
last_rsi = data["RSI"].iloc[-1]  # Último RSI
last_macd = data["MACD"].iloc[-1]  # Último MACD
last_signal_macd = data["Signal"].iloc[-1]  # Última Señal de MACD

# 📊 Mostrar RSI y MACD en Consola
print("\n📌 Últimos Valores de USD/JPY 📊")
print(f"🔹 Precio: {last_price:.2f}")
print(f"📈 RSI: {last_rsi:.2f}")
print(f"📊 MACD: {last_macd:.4f}")
print(f"📊 Señal MACD: {last_signal_macd:.4f}")

# 📌 Evaluar si hay señal de compra o venta
if last_rsi > 50 and last_macd > last_signal_macd:
    print("\n✅ 📈 Señal de COMPRA detectada")
elif last_rsi < 45 and last_macd < last_signal_macd:
    print("\n❌ 📉 Señal de VENTA detectada")
else:
    print("\n🔍 No hay señales claras, seguir monitoreando.")

# 🔔 Enviar alerta a Telegram
TOKEN = '8090692206:AAHGDuQMx1RdjxuwV1FWdTJYXtDz6Nkgko4'
CHAT_ID = '1380161872'

def enviar_alerta_telegram(mensaje):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': mensaje}
    requests.post(url, data=data)

# Detectar y enviar señal según condiciones
if last_rsi > 50 and last_macd > last_signal_macd:
    mensaje = f"✅ Señal de COMPRA detectada para USD/JPY\n📈 RSI: {last_rsi:.2f} | 📊 MACD: {last_macd:.4f}"
    print("\n" + mensaje)
    enviar_alerta_telegram(mensaje)
elif last_rsi < 45 and last_macd < last_signal_macd:
    mensaje = f"❌ Señal de VENTA detectada para USD/JPY\n📈 RSI: {last_rsi:.2f} | 📊 MACD: {last_macd:.4f}"
    print("\n" + mensaje)
    enviar_alerta_telegram(mensaje)
else:
    mensaje = f"🔍 No hay señal clara para USD/JPY\n📈 RSI: {last_rsi:.2f} | 📊 MACD: {last_macd:.4f}"
    print("\n" + mensaje)
    enviar_alerta_telegram(mensaje)
