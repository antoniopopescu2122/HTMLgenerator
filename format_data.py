import os
import json

formatted_file = 'formatted.json'

if not os.path.exists(formatted_file):
    # Read data from data.json
    data_file = 'data.json'
    with open(data_file) as f:
        data = json.load(f)

    # Write formatted data to formatted.json
    with open(formatted_file, 'w') as f:
        json.dump(data, f, indent=4)

    print("Data has been formatted and written to formatted.json.")
else:
    print("The formatted.json file already exists.")
