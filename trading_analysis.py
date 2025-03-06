import pandas as pd
import numpy as np
import yfinance as yf
import ta
import matplotlib.pyplot as plt

# Descargar datos de USD/JPY en la última semana con intervalos de 1 hora para análisis más profundo
data = yf.download("USDJPY=X", period="7d", interval="1h", auto_adjust=False)

# Asegurar que 'Close' es una Serie (1D)
close_prices = data["Close"].squeeze()

# Calcular indicadores técnicos detallados
data["RSI"] = ta.momentum.RSIIndicator(close_prices, window=14).rsi()
data["MACD"] = ta.trend.MACD(close_prices).macd()
data["Signal"] = ta.trend.MACD(close_prices).macd_signal()
data["Histogram"] = data["MACD"] - data["Signal"]  # Diferencia MACD para ver fuerza de cruce
data["EMA_50"] = ta.trend.EMAIndicator(close_prices, window=50).ema_indicator()
data["EMA_200"] = ta.trend.EMAIndicator(close_prices, window=200).ema_indicator()

# Definir señales más avanzadas de compra y venta
data["Buy_Signal"] = (data["RSI"] < 30) & (data["MACD"] > data["Signal"]) & (data["EMA_50"] > data["EMA_200"])
data["Sell_Signal"] = (data["RSI"] > 70) & (data["MACD"] < data["Signal"]) & (data["EMA_50"] < data["EMA_200"])

# Filtrar la última señal generada
last_signal = data.iloc[-1]

# Evaluar si hay una oportunidad de compra o venta más clara
if last_signal["Buy_Signal"].any():
    decision = f"📈 Señal de COMPRA detectada en USD/JPY\nPrecio: {last_signal['Close']}\nRSI: {last_signal['RSI']:.2f} (Sobreventa)\nMACD: {last_signal['MACD']:.4f} > Señal: {last_signal['Signal']:.4f}\nEMA 50: {last_signal['EMA_50']:.2f} > EMA 200: {last_signal['EMA_200']:.2f} (Tendencia alcista confirmada)"
elif last_signal["Sell_Signal"].any():
    decision = f"📉 Señal de VENTA detectada en USD/JPY\nPrecio: {last_signal['Close']}\nRSI: {last_signal['RSI']:.2f} (Sobrecompra)\nMACD: {last_signal['MACD']:.4f} < Señal: {last_signal['Signal']:.4f}\nEMA 50: {last_signal['EMA_50']:.2f} < EMA 200: {last_signal['EMA_200']:.2f} (Tendencia bajista confirmada)"
else:
    decision = "🔍 No hay señales claras de trading en este momento. Se recomienda esperar confirmación adicional."

# Mostrar decisión en consola
print("\n🚨 DECISIÓN FINAL DE TRADING 🚨")
print(decision)

# 📊 Graficar RSI y MACD
fig, ax = plt.subplots(2, 1, figsize=(12, 8))

# RSI
ax[0].plot(data.index, data["RSI"], label="RSI", color="blue")
ax[0].axhline(70, linestyle="--", color="red", label="Sobrecompra (70)")
ax[0].axhline(30, linestyle="--", color="green", label="Sobreventa (30)")
ax[0].legend()
ax[0].set_title("RSI USD/JPY")

# MACD
ax[1].plot(data.index, data["MACD"], label="MACD", color="purple")
ax[1].plot(data.index, data["Signal"], label="Señal MACD", color="orange")
ax[1].legend()
ax[1].set_title("MACD USD/JPY")

# Mostrar gráficos
plt.tight_layout()
plt.show()
