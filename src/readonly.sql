-- SQL to create 'readonly' role on PP Postgres tables for remote analysis

CREATE ROLE readonly LOGIN;
SELECT 'GRANT SELECT ON public.' || table_name || ' TO readonly;' FROM information_schema.tables WHERE table_name LIKE 'pp%';
