-- ------------------------------------------------------------------
-- CECHA: Dynamiczne wyznaczanie wydarzeń handlowych
-- CEL: Model musi wiedzieć o ruchomych świętach i sezonach specyficznych dla branży.
-- ------------------------------------------------------------------

-- 1. Black Friday (Zawsze 4. piątek listopada)
UPDATE calendar_events 
SET event_name = 'Black Friday', is_black_friday = 1
WHERE EXTRACT(MONTH FROM data) = 11 
  AND EXTRACT(ISODOW FROM data) = 5 -- Piątek
  AND to_char(data, 'W')::int = 4;  -- 4. tydzień miesiąca

-- 2. Niedziele Handlowe (Algorytm zgodny z polskim prawem)
-- Grudzień + ostatnie niedziele kwartałów (uproszczenie dla modelu)
UPDATE calendar_events 
SET is_trading_sunday = 1
WHERE EXTRACT(ISODOW FROM data) = 7 -- Niedziela
  AND (
      EXTRACT(MONTH FROM data) = 12 
      OR (EXTRACT(DAY FROM data) > 24 AND EXTRACT(MONTH FROM data) IN (1, 4, 6, 8))
  );

-- 3. Sezony (Specyfika asortymentu: Garnitury vs Stroje kąpielowe)
UPDATE calendar_events 
SET season_type = CASE 
    WHEN EXTRACT(MONTH FROM data) = 5 THEN 'Sezon Komunijny'
    WHEN EXTRACT(MONTH FROM data) BETWEEN 5 AND 9 THEN 'Sezon Ślubny'
    WHEN EXTRACT(MONTH FROM data) BETWEEN 7 AND 8 THEN 'Wakacje'
    ELSE 'Standard'
END;