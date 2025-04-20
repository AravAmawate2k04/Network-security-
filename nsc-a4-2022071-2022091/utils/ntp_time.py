import ntplib
import datetime

def get_gmt_datetime():
    """
    Attempts to fetch UTC from several NTP servers.
    Raises an exception if all attempts fail.
    """
    client = ntplib.NTPClient()
    servers = [
        "pool.ntp.org",
        "time.google.com",
        "time.cloudflare.com"
    ]
    last_exc = None

    for host in servers:
        try:
            # 5-second timeout per request
            response = client.request(host, version=3, timeout=5)
            return datetime.datetime.utcfromtimestamp(response.tx_time)
        except Exception as e:
            last_exc = e
            # try next server

    # if none succeeded, raise the last exception
    raise last_exc