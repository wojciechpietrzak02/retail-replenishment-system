import numpy as np
import pandas as pd

def engineer_features(df):
    """
    Transformacja surowych danych w cechy zrozumiałe dla modelu ML.
    """
    # 1. CYKLICZNE KODOWANIE CZASU (Cyclic Time Encoding)
    # Problem: Tydzień 1 i 52 są blisko siebie, ale numerycznie daleko.
    # Rozwiązanie: Transformacja na koło (sin/cos).
    df['week_start_date'] = pd.to_datetime(df['week_start_date'])
    
    df['week_sin'] = np.sin(2 * np.pi * df['week_start_date'].dt.isocalendar().week / 52.0)
    df['week_cos'] = np.cos(2 * np.pi * df['week_start_date'].dt.isocalendar().week / 52.0)

    # 2. DYNAMIKA SPRZEDAŻY (Trends)
    # Wyliczamy, czy sprzedaż w ostatnim tygodniu rośnie/spada względem historii
    # Dodajemy 0.01 w mianowniku, aby uniknąć dzielenia przez zero (Division by Zero protection)
    df['trend_short'] = df['sales_lag_1'] / (df['sales_lag_2'] + 0.01)       # Dynamika 1-tygodniowa
    df['trend_long']  = df['sales_lag_1'] / (df['sales_roll_mean_4'] + 0.01) # Dynamika miesięczna

    # 3. RELACJA CENY (Price Elasticity Proxy)
    # Czy obecna cena jest atrakcyjna względem średniej ceny z 30 dni?
    df['price_ratio'] = df['avg_price'] / (df['avg_price_30d'] + 0.01)

    return df