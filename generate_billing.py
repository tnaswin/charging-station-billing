import requests
import json
import logging
import supplier_prices_model as spm
import transaction_model as tm
import calulated_prices_model as cpm
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
        result = spm.supplier_price_from_dict(x)
        supplier_list.append(result)
    logging.info(len(supplier_list))
    return supplier_list


def parse_transaction(data):
    """Parse Charges(transaction data)"""
    logging.info("parse_transaction")
    transaction_list = []
    for x in data:
        transaction = tm.transaction_from_dict(x)
        transaction_list.append(transaction)
    logging.info(len(transaction_list))
    return transaction_list

def get_apidata():
    """
       Connect to the server and get the base JSON file with all information
       and return the response received.
    """
    logging.info("get_apidata")
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

def calculate_prices(supplier_list, transaction_list):
    """Calculate the price for the charges"""
    logging.info("calculated_prices")
    calulated_price_list = []
    for supplier in supplier_list:
        for transaction in transaction_list:
            kwh_price = 0.0
            if supplier.evse_id == transaction.evseid or supplier.product_id == transaction.partner_product_id:
                if supplier.has_kwh_price:
                    kwh_price = calculate_kwh(supplier, transaction)
                    price = cpm.CalculatedPrice(0,0,kwh_price,0,
                                                transaction.session_id,
                                                supplier.identifier)
                    calulated_price_list.append(price)
                    transaction_list.remove(transaction)                
    logging.info(len(calulated_price_list))
    print(len(calulated_price_list))

def calculate_kwh(supplier, transaction):
    """Calculate the price for the charges from kwH data"""
    charges = 0.0
    kwH_consumed = transaction.meter_value_end - transaction.meter_value_start
    if supplier.min_cosumed_energy and supplier.min_cosumed_energy > kwH_consumed:
        charges += supplier.min_cosumed_energy * supplier.kwh_price
    elif supplier.has_complex_minute_price:
        pass
    else:
        charges += kwH_consumed * supplier.kwh_price
    return charges

def main():
    logging.basicConfig(level=logging.INFO)


if __name__=="__main__":
    main()
    try:
        data = get_apidata()
        supplier_list, transaction_list = parse_data(data)
        calculate_prices(supplier_list, transaction_list)

    except Exception as e:
        logging.info("Exception")
        logging.error(logging.traceback.format_exc())
