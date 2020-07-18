import requests
import datetime
import json
import csv
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
        raise Exception("Sorry, Error in API Call with HTTP Error :" 
                        + str(response.status_code))
    else:
        logging.info("Success code " + str(response.status_code))
        return response.json()

def calculate_prices(supplier_list, transaction_list):
    """Calculate the price for the charges"""
    logging.info("calculated_prices")
    calculated_price_list = []
    for supplier in supplier_list:
        for transaction in transaction_list:
            kwh_price = 0.0
            time_price = 0.0
            fee_price = 0.0
            total_price = 0.0
            if (supplier.evse_id == transaction.evseid 
                or supplier.product_id == transaction.partner_product_id):
                if supplier.has_kwh_price or supplier.has_time_based_kwh:
                    kwh_price = calculate_kwh(supplier, transaction)
                total_price = kwh_price + time_price + fee_price
                price = cpm.CalculatedPrice(fee_price,time_price,kwh_price,total_price,
                                                str(transaction.session_id),
                                                str(supplier.identifier))
                calculated_price_list.append(price)
                # transaction_list.remove(transaction)              
    return calculated_price_list

def find_timeprice_for_transaction(supplier: spm.SupplierPrice, transaction: tm.Transaction):
    sorted_time_price = sorted(supplier.time_price, key=lambda x: x.hour_from)
    charge_time = transaction.charging_end - transaction.charging_start
    duration_timeprice_dict = {"duration_in_tp" : 0, "time_price" : None}
    for time_price in sorted_time_price:
        #find timeprice to be used for calculation
        hour_from = transaction.charging_start.replace(
                    hour=int(time_price.hour_from), minute=0, second=0)
        time_diff_tp = time_price.hour_to - time_price.hour_from
        time_diff_tp = time_diff_tp if time_diff_tp > 0 else time_diff_tp+24
        if(transaction.charging_start.day == transaction.charging_end.day):
            hour_to = transaction.charging_end.replace(
                    hour=int(time_price.hour_to), minute=0, second=0)
        else:
            hour_to = hour_from + datetime.timedelta(hours=int(time_diff_tp))
        if(transaction.charging_start >= hour_from 
            or transaction.charging_start < hour_to):
            diff_charging = transaction.charging_end - transaction.charging_start
            diff_interval = hour_to - hour_from
            if(diff_charging > diff_interval or transaction.charging_end > hour_to):
                duration_in_tp = (hour_to - transaction.charging_start).seconds
            else :
                duration_in_tp = (transaction.charging_end - transaction.charging_start).seconds
            if(duration_in_tp >= duration_timeprice_dict["duration_in_tp"]):
                duration_timeprice_dict["duration_in_tp"] = duration_in_tp
                if supplier.has_time_based_kwh:
                    if(duration_in_tp == duration_timeprice_dict["duration_in_tp"] 
                        and duration_timeprice_dict["time_price"]
                        and duration_timeprice_dict["time_price"].kwh_price < time_price.kwh_price):
                        # Check for equal duration_in_tp set time price with greater kwH price.
                        duration_timeprice_dict["time_price"] = time_price
                    else:
                        duration_timeprice_dict["time_price"] = time_price
                else:
                    if(duration_in_tp == duration_timeprice_dict["duration_in_tp"] 
                        and duration_timeprice_dict["time_price"]
                        and duration_timeprice_dict["time_price"].minute_price < time_price.minute_price):
                        # Check for equal duration_in_tp set time price with greater kwH price.
                        duration_timeprice_dict["time_price"] = time_price
                    else:
                        duration_timeprice_dict["time_price"] = time_price
            else:
                duration_timeprice_dict["duration_in_tp"] = duration_in_tp
                duration_timeprice_dict["time_price"] = time_price
    return duration_timeprice_dict["time_price"]

def get_time_from_timeframe(timeframe, charge_time):
    pass

def calculate_kwh(supplier : spm.SupplierPrice, transaction : tm.Transaction):
    """Calculate the price for the charges from kwH data"""
    amount = 0.0
    kwH_consumed = transaction.meter_value_end - transaction.meter_value_start
    if supplier.min_consumed_energy and supplier.min_consumed_energy > kwH_consumed:
        # Charge if consumer energy less than minimum consumption
        amount += supplier.min_consumed_energy * supplier.kwh_price
    elif supplier.has_time_based_kwh:
        # Charge for complex kwH
        if supplier.has_hour_day:
            time_price = find_timeprice_for_transaction(supplier,transaction)
            if supplier.min_consumption > kwH_consumed:
                amount += supplier.min_consumption * float(time_price.kwh_price)
            else:
                amount += kwH_consumed * float(time_price.kwh_price)
        else:
            if supplier.min_consumption > kwH_consumed:
                amount += supplier.min_consumption * supplier.time_price[0].kwh_price
            else:
                amount += kwH_consumed * float(supplier.time_price[0].kwh_price)
    else:
        # Simple kwH Calculation
        amount += kwH_consumed * supplier.kwh_price
    return amount

def export_to_csv(calculated_price_dict):
    # Generating transaction price report  
    with open('result.csv','w') as csvfile:
        header = ['session_id', 'supplier_price_id', 'fee_price', 'time_price', 'total_price', 'kwh_price'] 
        wr = csv.DictWriter(csvfile, fieldnames=header)
        wr.writeheader()
        wr.writerows(calculated_price_dict)

def main():
    logging.basicConfig(level=logging.INFO)
    try:
        data = get_apidata()
        supplier_list, transaction_list = parse_data(data)
        calculated_price_list = calculate_prices(supplier_list, transaction_list)
        calculated_price_dict = cpm.calculated_price_to_dict(calculated_price_list)
        export_to_csv(calculated_price_dict)

    except Exception as e:
        logging.info("Exception")
        logging.error(logging.traceback.format_exc())


if __name__=="__main__":
    main()
