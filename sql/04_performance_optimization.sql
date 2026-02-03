-- ------------------------------------------------------------------
-- CECHA: Optymalizacja wydajności Big Data (Performance Tuning)
-- CEL: Przyspieszenie czasu treningu modelu w Pythonie poprzez preprocessing w SQL.
-- ------------------------------------------------------------------

-- 1. Wyjaśnianie planu zapytania (Query Plan Analysis)
EXPLAIN SELECT * FROM view_dataset_weekly_ml;

-- 2. Materializacja widoku (Caching)
-- Zamiast liczyć agregacje przy każdym zapytaniu, zapisujemy wynik fizycznie.
CREATE MATERIALIZED VIEW mat_view_dataset_weekly_ml AS
SELECT * FROM view_dataset_weekly_ml;

-- 3. Strategia Indeksowania (Indexing Strategy)
-- Indeks złożony dla błyskawicznego grupowania po kluczowych wymiarach
CREATE INDEX IF NOT EXISTS idx_sprzedaz_grupowanie 
ON sprzedaz_dane(data, salon, kategoria_podrzedna, rozmiar);

-- Indeks na dacie dla szybkiego filtrowania szeregów czasowych
CREATE INDEX idx_mat_date ON mat_view_dataset_weekly_ml(week_start_date);