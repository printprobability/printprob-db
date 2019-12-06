-- SQL to create 'readonly' role on PP Postgres tables for remote analysis

CREATE ROLE readonly;
DO $$
DECLARE
  rec record;
BEGIN
  FOR rec IN SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'pp%'
  LOOP
    EXECUTE 'GRANT SELECT ON public.' || quote_ident(rec.table_name) || ' TO readonly;';
  END LOOP;
END $$;
