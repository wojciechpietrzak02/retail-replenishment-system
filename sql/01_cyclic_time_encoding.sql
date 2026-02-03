-- ------------------------------------------------------------------
-- CECHA: Cykliczne kodowanie czasu (Cyclic Time Encoding)
-- PROBLEM: Dla modelu ML tydzień 1 i 52 są odległe (51 jednostek różnicy),
--          podczas gdy w rzeczywistości sąsiadują ze sobą.
-- ROZWIĄZANIE: Transformacja czasu na współrzędne kołowe (Sinus/Cosinus).
-- ------------------------------------------------------------------

CREATE VIEW view_calendar_features AS
SELECT
    d.id_data,
    c.data,
    
    -- Transformacja cykliczna (Pory roku / Bliskość dat)
    -- Dzięki temu model "wie", że koniec roku jest blisko początku roku
    SIN(2 * PI() * EXTRACT(doy FROM c.data) / 365.25) as year_sin,
    COS(2 * PI() * EXTRACT(doy FROM c.data) / 365.25) as year_cos

FROM id_data d
JOIN calendar_events c ON d.data = c.data;