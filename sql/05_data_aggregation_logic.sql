-- ------------------------------------------------------------------
-- CECHA: Budowa Dataseta Analitycznego (CTE & Aggregation)
-- CEL: Sprowadzenie danych o różnej granularności (paragon, dzień, tydzień) 
--      do wspólnego mianownika (Tydzień-Produkt-Sklep).
-- ------------------------------------------------------------------

WITH weekly_sales AS (
    -- Agregacja milionów rekordów paragonowych do poziomu tygodnia
    SELECT 
        DATE_TRUNC('week', d.data)::date as week_start_date,
        s.id_store,
        s.id_sub_category,
        s.id_size,
        SUM(s.sales_quantity) as sum_sales_qty,
        AVG(s.retail_price) as avg_price
    FROM view_sale s
    JOIN dates_map d ON s.id_date = d.id_data
    GROUP BY 1, 2, 3, 4
),
stock_aligned AS (
    -- Przesunięcie zapasu (zapas na koniec dnia -> zapas otwarcia tygodnia)
    SELECT
        (d.data + INTERVAL '1 day')::date as week_start_date,
        z.id_store,
        SUM(z.stock) as opening_stock
    FROM view_stock z
    JOIN dates_map d ON z.id_date = d.id_data
    GROUP BY 1, 2
)
-- Łączenie (Join) z obsługą braków danych (Handling Nulls)
SELECT
    ws.week_start_date,
    ws.id_store,
    COALESCE(ws.sum_sales_qty, 0) as target, -- Zero filling dla braku sprzedaży
    COALESCE(st.opening_stock, -1) as stock, -- Flaga -1 dla braku danych o zapasie
    ww.avg_temp
FROM weekly_sales ws
LEFT JOIN stock_aligned st ON ws.week_start_date = st.week_start_date AND ...
LEFT JOIN weekly_weather ww ON ws.week_start_date = ww.week_start_date AND ...