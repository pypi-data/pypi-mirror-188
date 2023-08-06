import yfinance as yf
import numpy as np
import pandas as pd

def data(ticker):
  ohlcv_data={}
  temp = yf.download(ticker,period='6mo',interval='1d')
  temp.dropna(how="any",inplace=True)
  ohlcv_data[ticker] = temp
  return ohlcv_data[ticker]

def CAGR(ticker):
    DF=data(ticker)
    df = DF.copy()
    df["return"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252
    CAGR = (df["cum_return"][-1])**(1/n) - 1
    return CAGR

def Volatility(ticker):
    DF=data(ticker)
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    vol = df["daily_ret"].std() * np.sqrt(252)
    return vol

def SharpeRatio(ticker, rf):
    DF=data(ticker)
    df = DF.copy()
    return (CAGR(df) - rf)/Volatility(df)

def Sortino(ticker, rf):
    DF=data(ticker)
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    neg_return = np.where(df["return"]>0,0,df["return"])
    neg_vol = pd.Series(neg_return[neg_return!=0]).std() * np.sqrt(252)
    return (CAGR(df) - rf)/neg_vol

def MaxDrawdown(ticker):
    DF=data(ticker)
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    df["cum_return"] = (1+df["return"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    return (df["drawdown"]/df["cum_roll_max"]).max()

def Calmar(ticker):
    DF=data(ticker)
    df = DF.copy()
    return CAGR(df)/MaxDrawdown(df)