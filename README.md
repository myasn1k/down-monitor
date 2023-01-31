# Down-monitor

Monitor for reachability of a number of websites passed as input

## Configuration

In `config_vol/`, please copy `config.sample.yaml` to `config.yaml`, and customize.

Additionally, there are a few environment variables you may need to set:

* `RW_DB_PATH`: Path for the SQLite database to use
* `RW_CONFIG_PATH`: Path to the `config.yaml` file

These are both set in the provided `docker-compose.yml`.

## Usage

This is intended to be run in Docker via a cronjob on whatever increment you decide to use.

First, build the container: `docker-compose build app`

Then, add it to your crontab. Example crontab entry (running every 10 minutes):

```
*/10 * * * * cd /home/USER/down-monitor && ./run.sh
```

## CSV export

Simply run this command: `sqlite3 -header -csv down-monitor.db "select * from downs where [WHATEVER YOU WANT];" > ../downs.csv`
