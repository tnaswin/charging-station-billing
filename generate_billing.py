import requests
import json
import logging
import supplier_prices_model
import transaction_model
from configparser import ConfigParser


def parse_data(data):
    """
        Parse the data received, using meaningful names for the variables, 
        convert values to the correct data types and 
        any other cleaning/conversion that is suitable for the data.
        {
            "supplier_prices": [...],
            "transactions": [...]
        }
    """
    supplier_list = parse_supplier_price(data['supplier_prices'])
    transaction_list = parse_transaction(data['transactions'])
    return supplier_list, transaction_list

def parse_supplier_price(data):
    """Parse supplier data"""
    logging.info("parse_supplier_price")
    supplier_list = []
    for x in data:
        result = supplier_prices_model.supplier_price_from_dict(x)
        supplier_list.append(result)
    logging.info(len(supplier_list))
    return supplier_list


def parse_transaction(data):
    """Parse Charges(transaction data)"""
    logging.info("parse_transaction")
    transaction_list = []
    for x in data:
        transaction = transaction_model.transaction_from_dict(x)
        transaction_list.append(transaction)
    logging.info(len(transaction_list))
    return transaction_list

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
        supplier_list, transaction_list = parse_data(data)

    except Exception as e:
        logging.info("Exception")
        logging.error(logging.traceback.format_exc())