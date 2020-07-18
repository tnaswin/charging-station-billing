# Charging Station Billing

Charging-Station-Billing coding challenge using Python.  
Request and fetch data from the given API and perform the given operations:
1. Get JSON with Data
    ```json
    {
    "supplier_prices": [  ],
    "transactions": [  ]
    }
    ```
2. Parse Data
3. Calculate Prices
    - Category Fee
    - Category Time
    - Category kWh
4. Export the Data to CSV and JSON

## Setup 

### Sample config.ini file:
Provide the required values for each key.
```ini
[auth]
endpoint: <API Endpoint>
username: <username>
password: <password>
```

### To execute the script:

Install the dependencies and run the script.

```sh
$ pip install requirements.txt
$ python3 generate_billing.py
```
