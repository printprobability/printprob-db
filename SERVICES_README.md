
![Print & Probability Workbench Architecture](https://github.com/printprobability/printprob-db/blob/master/docs/printprob-architecture.png)        

# Workbench Services

The Print & Probability 'workbench' site is comprised of a number of services as seen in the diagram below. The site utilizes Django, a Python app that interfaces with an underlying PostgreSQL database that maintains the project's data tables as well as admin tables for the site. Gunicorn acts as the HTTP web server that communicates with Django and Nginx acts as a proxy server to the outside web. A Vue front end (shown below as 'Front-end Artifacts') communicates the interactions of the site's visitors to the Django app. The workbench also uses an IIIF server to serve the site images. The Django App, Gunicorn, and the PostgreSQL database run on Bridges virtual machine `vm012.bridges2.psc.edu` while the IIIF server runs on Bridges virtual machine `vm013.bridges2.psc.edu`. The IIIF server itself runs within a singularity instance `iiif1`. In order to log onto any of these virtual machines type `ssh <your_bridges_username>@vm<vm_number>.bridges2.psc.edu`.

## Vue/Django/Gunicorn

*Restarting*
1. Log into `vm012.bridges2.psc.edu`
2. `cd /usr/local/bin` - This directory contains commands to start/stop the backend
3. `kill_gunicorn` - Stops the gunicorn server that works with the django app
4. `start_printprob` - Starts the django app and gunicorn

*App location*
- `/data/printprob-db` via any Bridges login
- NOTE: Any changes to the Django app or Vue frontend must be placed here.

## PostgreSQL database

*Preparation before use*
- Make a `.pgpass` file in your Bridges home directory containing:
    - `localhost:5432:pp:app:CwyYmvkA897FUy3ANCRiXDkMJjrZAohcrpcUL`

*Access to make queries*
- `psql -h localhost -p 5432 -U app -d pp`

*Restarting*
- `sudo /usr/bin/systemctl restart postgresql-12`

*Backup*

- As of May 2024, Sriram has been backing up the database weekly in `/ocean/projects/hum160002p/shared/db_backups`, removing the previous week's backup when done. Below is information on that backup process.

Backup steps
1. `vacuumdb --dbname=pp --host=localhost --username=app`
2. `reindexdb --dbname=pp --host=localhost --username=app --verbose`
3. `bash /data/backup_pg.sh`
4. Delete the old backup file from the `backups` directory in `/data`

*Weekly Vacuuming*

```
# Vacuum database at midnight every Sunday
0 0 * * SUN vacuumdb --dbname=pp --host=localhost --username=app --quiet
0 0 * * SUN touch /data/last_pp_db_vacuumed

# Re-index 'pp' database weekly once every Sunday at 01:00 - after vacuum finishes
0 1 * * SUN reindexdb --dbname=pp --host=localhost --username=app --quiet
0 1 * * SUN touch /data/last_pp_db_reindexed
```

## Nginx

*Status*
- `service nginx status`

*Restarting*
- `service nginx restart`
- NOTE: Nginx needs to be restarted every 6 months to a year. `server.crt` and `trustchain.crt` are both changed by Bridges staff. Need to communicate with them to do so.

## IIIF Server

*Restarting*

1. Log into `vm013.bridges2.psc.edu`
2. `cd /ocean/projects/hum160002p/shared/iiif-server`
3. `singularity instance stop iiif1` - Stop any currently-running instance
4. `./startup.sh` - Create the singularity instance
5. `nohup singularity run --env VIPS_DISC_THRESHOLD=250m instance://iiif1 > iiif.log &` - Activate the IIIF server inside the contianer

NOTE: The new argument `--env VIPS_DISC_THRESHOLD=250m` is necessary for an image memory cap we were exceeding with the IIIF server. This sets the environment variable `VIPS_DISC_THRESHOLD` inside the singularity instance in which the IIIF server program is running.


# Vue Frontend Development and Deployment