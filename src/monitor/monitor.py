import requests
import ssl
from config import Config
import urllib3
from datetime import datetime

#Monitor the website
def is_site_up(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        # Visit the website to know if it is up
        status = requests.get(url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'},
                timeout=Config["timeout"], verify=False).status_code
        # If it returns 200, the website is up
        return (status == 200, datetime.utcnow())
    except Exception as e:
        return (False, datetime.utcnow())
