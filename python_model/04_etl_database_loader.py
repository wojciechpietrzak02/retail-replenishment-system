import pandas as pd
import json
import os
import urllib.parse
# --- [POST-THESIS ENHANCEMENT] ---
# W oryginalnej pracy używano print(). Na potrzeby portfolio dodano profesjonalne logowanie.
import logging 
# ---------------------------------
from sqlalchemy import create_engine, text
from sklearn.preprocessing import LabelEncoder

# --- [POST-THESIS ENHANCEMENT: LOGGING CONFIG] ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - ETL LOADER - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
# ------------------------------------------------

# --- KONFIGURACJA BAZY ---
# (Hasło zahardkodowane w celach demonstracyjnych. W produkcji użyłbym zmiennych środowiskowych.)
DB_USER = 'postgres'
DB_PASS = urllib.parse.quote_plus('TwojeHaslo')
DB_HOST = 'localhost'
DB_NAME = 'Project_Sales_DB'
DB_STRING = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}?client_encoding=utf8'

OUTPUT_DIR = "model_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================================================================
# [POST-THESIS ENHANCEMENT: DATA QUALITY CHECKS]
# Ta funkcja nie była częścią oryginalnej pracy inżynierskiej.
# Została dodana, aby zademonstrować zrozumienie potrzeby weryfikacji danych
# w środowisku produkcyjnym przed podaniem ich do modelu ML.
# ==============================================================================
def run_data_quality_checks(df):
    """
    Kluczowy element ETL: Weryfikacja, czy dane nadają się do modelu.
    """
    logger.info("--- Rozpoczynam Data Quality Checks (DQ) ---")
    
    # 1. Sprawdzenie pustych wartości w kluczowych kolumnach
    critical_cols = ['salon', 'kategoria_podrzedna', 'rozmiar', 'week_start_date']
    if df[critical_cols].isnull().any().any():
        null_counts = df[critical_cols].isnull().sum()
        logger.error(f"CRITICAL DQ FAILURE: Znaleziono NULLe w kluczowych kolumnach:\n{null_counts}")
        raise ValueError("Dane zawierają niedozwolone wartości NULL. Przerywam proces.")

    # 2. Sprawdzenie sensowności biznesowej
    if (df['avg_price'] < 0).any():
        logger.error("CRITICAL DQ FAILURE: Wykryto ujemne ceny!")
        raise ValueError("Błąd logiczny w danych: ujemna cena.")

    logger.info("✅ Wszystkie testy DQ zakończone sukcesem. Dane są bezpieczne.")
    return True
# ==============================================================================

def load_and_clean_data():
    # Użycie loggera zamiast print()
    logger.info("--- ETL START: Ekstrakcja danych z PostgreSQL ---")
    
    try:
        engine = create_engine(DB_STRING)
        logger.info("Połączenie z bazą danych nawiązane.")
        
        logger.info("Wykonywanie zapytania SELECT z widoku zmaterializowanego...")
        df_db = pd.read_sql("SELECT * FROM final_dataset_ml ORDER BY week_start_date", engine)
        logger.info(f"Pobrano surowych wierszy: {len(df_db)}")
        
    except Exception as e:
        logger.critical(f"Nie można pobrać danych z bazy. Szczegóły błędu: {e}")
        return None

    # --- [POST-THESIS ENHANCEMENT: URUCHOMIENIE DQ] ---
    try:
        run_data_quality_checks(df_db)
    except ValueError as e:
        logger.error("Proces ETL przerwany z powodu błędów jakości danych.")
        return None # Zatrzymujemy pipeline
    # -------------------------------------------------

    # Cleaning: Usuwanie wierszy z błędami mapowania
    df_db = df_db.dropna()
    
    logger.info(f"Gotowy dataset do treningu: {len(df_db)} wierszy.")
    return df_db

# ... (reszta funkcji build_encoders bez zmian, tylko z logger.info zamiast print)