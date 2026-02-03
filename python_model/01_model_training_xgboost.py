import xgboost as xgb
import pandas as pd
import os

# Konfiguracja treningu modelu
# Wybór algorytmu Gradient Boosting ze względu na skuteczność w danych tabelarycznych
def train_model(X_train, y_train, X_test, y_test):
    print("--- Inicjalizacja treningu XGBoost ---")
    
    # Zastosowanie rozkładu Tweediego (reg:tweedie)
    # Kluczowe dla retailu: modeluje dane z dużą liczbą zer (brak sprzedaży) 
    # oraz gwarantuje nieujemne prognozy (tweedie_variance_power=1.5 to kompromis między rozkładem Poissona a Gamma)
    model = xgb.XGBRegressor(
        n_estimators=1500,          # Duża liczba drzew
        learning_rate=0.03,         # Wolne uczenie dla lepszej generalizacji
        max_depth=10,               # Głębokie drzewa dla wychwycenia złożonych relacji (produkt-sklep)
        subsample=0.8,              # Stochastic Gradient Boosting (redukcja overfittingu)
        colsample_bytree=0.8,
        n_jobs=-1,                  # Wykorzystanie wszystkich rdzeni CPU
        random_state=42,
        objective='reg:tweedie',    # <--- KILLER FEATURE
        tweedie_variance_power=1.5, 
        early_stopping_rounds=50    # Zapobieganie przeuczeniu
    )

    # Trening z walidacją w czasie rzeczywistym
    model.fit(
        X_train, y_train, 
        eval_set=[(X_test, y_test)], 
        verbose=100
    )
    
    # Zapis modelu do formatu JSON (lżejszy i przenośny)
    model.save_model("model_output/model_xgboost.json")
    return model