import requests
import json
import logging


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
       Connect to the server and get the base JSON file with all information.
    """
    pass

def calculate_prices():
    """Calculate the price for the charges"""
    pass

def main():
    logging.basicConfig(level=logging.INFO)


if __name__=="__main__":
    main()
