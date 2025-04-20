import ntplib
import datetime

def get_gmt_datetime():
    """
    Fetches the current time from a public NTP server and returns a UTC datetime object.
    """
    client = ntplib.NTPClient()
    response = client.request("pool.ntp.org", version=3)
    return datetime.datetime.utcfromtimestamp(response.tx_time)