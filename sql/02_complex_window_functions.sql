-- ------------------------------------------------------------------
-- CECHA: Inżynieria cech wewnątrz bazy (In-Database Feature Engineering)
-- ZASTOSOWANIE: Wyliczenie trendów i historii sprzedaży per SKU.
-- ------------------------------------------------------------------

SELECT 
    *,
    -- 1. LAGI: Co działo się w sklepie 1, 2 i 4 tygodnie temu?
    LAG(target, 1) OVER (
        PARTITION BY salon, kategoria_podrzedna, grupa_glowna, kolor, rozmiar 
        ORDER BY week_start_date
    ) as sales_lag_1,
    
    -- 2. TREND KRÓTKOTERMINOWY: Średnia krocząca (Moving Average) z 4 tygodni
    -- Użycie 'ROWS BETWEEN' pozwala wygładzić szum w danych dziennych
    AVG(target) OVER (
        PARTITION BY salon, kategoria_podrzedna, grupa_glowna, kolor, rozmiar 
        ORDER BY week_start_date 
        ROWS BETWEEN 4 PRECEDING AND 1 PRECEDING
    ) as sales_roll_mean_4,
    
    -- 3. RELACJA CENY (Price Ratio)
    -- Czy obecna cena odbiega od średniej z ostatniego miesiąca? (Wykrywanie promocji)
    CASE 
        WHEN AVG(avg_price) OVER (PARTITION BY ... ROWS BETWEEN 4 PRECEDING AND 1 PRECEDING) = 0 THEN 1.0 
        ELSE avg_price / NULLIF(AVG(avg_price) OVER (PARTITION BY ... ROWS BETWEEN 4 PRECEDING AND 1 PRECEDING), 0) 
    END as price_ratio

FROM base_data;