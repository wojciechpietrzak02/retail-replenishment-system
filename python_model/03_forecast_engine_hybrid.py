import numpy as np
import datetime

def recursive_forecasting_loop(model, initial_df, weeks_horizon, calibration_factor=1.0):
    """
    Symulacja przyszłości tydzień po tygodniu.
    Wynik prognozy z tygodnia T staje się wejściem (Lag) dla tygodnia T+1.
    """
    current_date = datetime.date.today()
    predictions_timeline = []
    
    # Pobranie początkowych opóźnień (Lags)
    current_lags = initial_df['hist_sales'].values
    
    print(f"Start prognozy na {weeks_horizon} tygodni. Kalibracja: {calibration_factor}")

    for i in range(weeks_horizon):
        t_date = current_date + datetime.timedelta(weeks=i)
        
        # Aktualizacja cech czasowych dla przyszłej daty
        initial_df['week_sin'] = np.sin(2*np.pi*t_date.isocalendar().week/52.0)
        initial_df['week_cos'] = np.cos(2*np.pi*t_date.isocalendar().week/52.0)
        
        if i > 0:
            # Recursive update: Wstawiamy naszą własną prognozę jako historię
            initial_df['sales_lag_1'] = current_lags
            
        # 1. PURE ML PREDICTION
        preds = model.predict(initial_df)
        preds = np.maximum(preds, 0) # Safety clip (brak ujemnej sprzedaży)
        
        # 2. HYBRID CONTROL (Biznesowa korekta)
        # Nakładamy mapę sezonowości i ręczny mnożnik (kalibrację) od usera
        preds = preds * calibration_factor
        
        # Logika symulacji ceny (Price Impact Simulation)
        # Jeśli cena jest wyższa o 20% od średniej -> obniż prognozę o 50%
        mask_high_price = initial_df['price_ratio'] > 1.2
        preds = np.where(mask_high_price, preds * 0.5, preds)

        # 3. STOCK CONSTRAINT
        # Nie sprzedamy więcej niż mamy na magazynie (chyba że to alokacja)
        preds = np.minimum(preds, initial_df['stock'])
        
        # Zapis wyników i przygotowanie pod kolejną pętlę
        current_lags = preds
        predictions_timeline.append((t_date, np.sum(preds)))

    return predictions_timeline