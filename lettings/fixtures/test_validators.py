
data_validator_address = [
    (
        {
            "number": 15000, #value > 9999
            "street": "West 53 Street",
            "city": "Manhattan",
            "state": "NY",
            "zip_code": 10019,
            "country_iso_code": "USA",       
        },
        "Ensure this value is less than or equal to 9999."
    ),
        (
        {
            "number": 15,
            "street": "West 53 Street",
            "city": "Manhattan",
            "state": "ABC", # length > 2
            "zip_code": 10019,
            "country_iso_code": "USA",       
        },
        "Ensure this value has at most 2 characters (it has 3)."
    ),
        (
        {
            "number": 15,
            "street": "West 53 Street",
            "city": "Manhattan",
            "state": "NY",
            "zip_code": 123456, #value > 9999
            "country_iso_code": "USA",       
        },
        "Ensure this value is less than or equal to 99999."
    ),
        (
        {
            "number": 15,
            "street": "West 53 Street",
            "city": "Manhattan",
            "state": "NY",
            "zip_code": 10019,
            "country_iso_code": "ABCD", # length > 4       
        },
        "Ensure this value has at most 3 characters (it has 4)."
    )
]
