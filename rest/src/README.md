## Standoff scripts for image manipulation and loading test data.

**Not used in production.**

* `loadbooks.py` does a practice run writing book, spread, page, and line information into the database using the REST endpoint

* `loadchars.py` does a practice run writing character information into the database using the REST endpoint


# Restarting backend service on Bridges node

SSH into the bridges node first - `vm012.bridges2.psc.edu`

The `sudo` scripts are located in the `/usr/local/bin` directory and they should run in the following order -

1. Kill the backend processes - `sudo /usr/local/bin/kill_gunicorn`
2. Restart the postgres instance - `sudo /usr/local/bin/start_postgres`
3. Start the backend app - `sudo /usr/local/bin/start_printprob`

You can verify that the app has started successfully by viewing the logs at - `/data/printprob-db/rest/app/gunicorn.log`.

If there are any errors in this log, then we have a problem which needs further debugging. 