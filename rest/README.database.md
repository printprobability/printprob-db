## Re-indexing and Re-vacuuming of database - Cron Schedule

The re-indexing and re-vacuuming of the `pp` database is scheduled as per below `crontab` - 

```shell
# Vacuum database at midnight every Sunday
0 0 * * SUN vacuumdb --dbname=pp --host=localhost --username=app --quiet
0 0 * * SUN touch /data/last_pp_db_vacuumed

# Re-index 'pp' database weekly once every Sunday at 01:00 - after vacuum finishes
0 1 * * SUN reindexdb --dbname=pp --host=localhost --username=app --quiet
0 1 * * SUN touch /data/last_pp_db_reindexed
```
