"""
This is to test the outcome with a pre-loaded data.
"""

import json, logging
import generate_billing as g


def main():
    # logging.basicConfig(level=logging.INFO)
    try:
        # f = open('tests/test_data.json')
        f = open('tests/single.json')
        data = json.load(f)
        supplier_list, transaction_list = g.parse_data(data)
        print("Supplier List: ",len(supplier_list))
        print("Transaction List: ", len(transaction_list))
        g.calculate_prices(supplier_list, transaction_list)

    except Exception as e:
        logging.info("Exception")
        logging.error(logging.traceback.format_exc())


if __name__=="__main__":
    main()