# Notify Me SenPy can be used is to suscribe to real time events using `notify_me`.
# For example, real time updates are critical in trading currencies.
# We show here a basic implementation of a subscriber system that 
# notifies us when the Bitcoin drops below a specified threshold.

import requests
from time import sleep
from senpy import notify_me

THRESHOLD = 60000 # in USD, currently 1 bitcoin = $60300
URL = "https://data.messari.io/api/v1/assets/bitcoin/metrics"

def subscribe_to_bitcoin():
    while True:
        # Query the API
        response = requests.get(URL).json() 
        if 'data' in response:
            # Extract the USD price
            value = response['data']['market_data']['price_usd']
            
            # Send a notification when the price drops
            if value < THRESHOLD:
                notify_me(f"The bitcoin is worth less than ${THRESHOLD}. It is currently at ${value}.")

        # Wait 1 second between each update
        sleep(1)

if __name__ == '__main__':
    subscribe_to_bitcoin()