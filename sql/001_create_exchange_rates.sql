CREATE TABLE IF NOT EXISTS exchange_rates (
    rate_date     DATE          NOT NULL,
    currency_code CHAR(3)       NOT NULL,
    currency_name TEXT          NOT NULL,
    mid_rate      NUMERIC(12,6) NOT NULL,
    table_no      TEXT          NOT NULL,
    loaded_at     TIMESTAMPTZ   NOT NULL DEFAULT now(),
    PRIMARY KEY (rate_date, currency_code)
);