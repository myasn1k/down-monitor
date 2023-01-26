import logging
import sys
import traceback
import requests
import os
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from datetime import datetime

from db.database import Session
from db.models import Down

from integrations.ctis import CTIS 

from config import Config
from monitor.monitor import is_site_up

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y/%m/%d %H:%M:%S",
    handlers=[
        #logging.FileHandler(filename="enum.log", mode="a"),
        logging.StreamHandler()
    ]
)

def main(argv):
    logging.info("Getting operations and urls from CTIS...")
    
    ctis = CTIS(Config["ctis_url"], Config["ctis_username"], Config["ctis_password"])
    ops_urls = ctis.get_operations_and_urls(Config["op_label"])

    logging.info(f"Found {len(ops_urls.keys())} operations")

    try:
        r = requests.get("http://ifconfig.me/ip", timeout = 60)
        if r.status_code >= 400:
            logging.error(f"The web service for public IP fetch isn't working")
            os._exit(1)
        else:
            logging.info(f"Public IP address: {r.text}")
    except Exception as e:
        logging.error(f"We are down")
        os._exit(1)

    is_up = dict.fromkeys(ops_urls.keys(), {})

    db_sess = Session()

    for operation, urls in ops_urls.items():
        logging.info(f"Starting process for {operation}")

        logging.info(f"Found {len(urls)} urls for {operation}")

        with ThreadPoolExecutor(max_workers = len(urls)) as executor:
            future_to_url = {executor.submit(is_site_up, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                res = future.result()
                q = db_sess.query(Down).filter_by(
                        operation=operation,
                        url=url,
                        end=None)
                if q.count() == 0:
                    if not res[0]:
                        down = Down(operation=operation, url=url, start=res[1])
                        db_sess.add(down)
                else:
                    if res[0]:
                        down = q.first()
                        down.end = res[1]
                        down.delta = down.end - down.start
                if not res[0]:
                    logging.info(f"{operation} - {url} is DOWN")
                else:
                    logging.info(f"{operation} - {url} is UP")
            except:
                tb = traceback.format_exc()
                logging.error(f"{operation} - {url} generated an exception")
                logging.error(tb.strip())
                    
        logging.info(f"Finished {operation}")

    db_sess.commit()
    db_sess.close()

    to_sleep = random.randrange(1, Config["rand"])
    logging.info(f"Sleeping for {to_sleep} seconds")
    sleep(to_sleep)

    logging.info("Finished, exiting")

if __name__ == "__main__":
    try:
        main(sys.argv)
    except:
        logging.error(f"Got a fatal error, aborting")

        tb = traceback.format_exc()

        # log exception
        logging.error(tb.strip())  # there is a trailing newline
