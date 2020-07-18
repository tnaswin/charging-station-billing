import requests
import json
import logging
from configparser import ConfigParser


def parse_data():
    """
        Parse the data received, using meaningful names for the variables, 
        convert values to the correct data types and 
        any other cleaning/conversion that is suitable for the data.
        {
            "supplier_prices": [...],
            "transactions": [...]
        }
    """
    pass

def parse_supplier_price():
    """Parse supplier data"""
    pass


def parse_transaction():
    """Parse Charges(transaction data)"""
    pass

def get_apidata():
    """
       Connect to the server and get the base JSON file with all information
       and return the response received.
    """
    config = ConfigParser() 
    config.read('config.ini')  # Read config from the file path given
    url = config.get('auth', 'endpoint')  
    username = config.get('auth', 'username')  
    password = config.get('auth', 'password')
    response = requests.get(url, auth=(username, password))
    if response.status_code != 200:
        raise Exception("Sorry, Error in API Call with HTTP Error :" + str(response.status_code))
    else:
        logging.info("Success code " + str(response.status_code))
        return response.json()

def calculate_prices():
    """Calculate the price for the charges"""
    pass

def main():
    logging.basicConfig(level=logging.INFO)


if __name__=="__main__":
    main()
    try:
        data = get_apidata()

    except Exception as e:
        logging.info("Exception")
        logging.error(logging.traceback.format_exc())