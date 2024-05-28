import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy.stats import norm

def download_data(stock, start_date, end_date):
    try:
        data = yf.download(stock, start=start_date, end=end_date, progress=False)
        return data['Close']
    except Exception as e:
        st.error(f"Erro ao baixar dados: {e}")
        return pd.Series()

def calculate_var_historical(prices, confidence_interval, holding_period):
    returns = prices.pct_change()
    sorted_returns = np.sort(returns)
    index = int((1 - confidence_interval) * len(sorted_returns))
    var = np.abs(sorted_returns[index]) * np.sqrt(holding_period)
    return var

def calculate_var_parametric(prices, confidence_interval, holding_period):
    returns = prices.pct_change().dropna()
    mean = np.mean(returns)
    sigma = np.std(returns)
    var = norm.ppf(1 - confidence_interval, mean, sigma) * np.sqrt(holding_period)
    return var

def plot_prices_and_var(prices, var, confidence_interval, holding_period, exposure):
    plt.figure(figsize=(10, 5))
    plt.plot(prices.index, prices, label='Price')
    var_line = prices.iloc[-1] - var * exposure
    plt.axhline(y=var_line, color='r', linestyle='-', label=f'VaR {confidence_interval * 100}%')
    plt.title(f'Price and VaR at {confidence_interval * 100}% Confidence')
    plt.legend()
    st.pyplot(plt)

def main():
    st.title("Sistema de VaR para Ativos Lineares")

    # A chave ('key') é adicionada para garantir que cada widget seja único
    stock = st.text_input("Digite o símbolo da ação (ex: AAPL, GOOGL)", value='AAPL', key="stock_input")
    exposure = st.number_input("Digite o valor de exposição ($)", value=100000, key="exposure_input")
    confidence_interval = st.slider("Intervalo de Confiança", 90, 99, 95, key="confidence_interval_slider") / 100.0
    holding_period = st.slider("Holding Period (dias)", 1, 30, 1, key="holding_period_slider")
    method = st.selectbox("Método de Cálculo do VaR", ['Histórico', 'Paramétrico', 'Monte Carlo'], key="var_method_select")

    start_date = st.date_input("Data de Início", datetime.now() - timedelta(days=365 * 5), key="start_date_input")
    end_date = st.date_input("Data de Término", datetime.now(), key="end_date_input")

    if st.button("Carregar dados e calcular VaR", key="calculate_var_button"):
        prices = download_data(stock, start_date, end_date)
        if prices.empty:
            st.error("Nenhum dado foi retornado. Verifique as datas e o símbolo da ação.")
        else:
            var = 0
            if method == 'Histórico':
                var = calculate_var_historical(prices, confidence_interval, holding_period)
            elif method == 'Paramétrico':
                var = calculate_var_parametric(prices, confidence_interval, holding_period)
            
            var_amount = exposure * var
            st.write(f"VaR: ${var_amount:,.2f}")

            plot_prices_and_var(prices, var, confidence_interval, holding_period, exposure)

if __name__ == "__main__":
    main()


