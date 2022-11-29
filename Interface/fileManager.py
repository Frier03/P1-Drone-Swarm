import json

def insert_data(file_name, data):
    data_object = {
        data[0]: {
            'MISSION_STATUS': 'idle',
            'MAC_ADDRESS': data[1],
            'CURRENT_IP': data[3],
            'TYPE': data[2],
            'SSID': '',
            'NAME': data[0],
            'STATUS': 'Connect'
        }
    }

    try:
        with open(f'{file_name}', 'r') as r:
            stored_data = json.load(r)
        
        merged_dict = {**data_object, **stored_data}

        with open(f'{file_name}', 'w') as wr:
            json.dump(merged_dict, wr)
        return 'OK'

    except Exception as e:
        print('Unwanted Error Occurred', e)

        with open(f'{file_name}', 'w') as wr:
            json.dump(stored_data, wr)

        return '101'

def request_data(file_name):
    try:
        with open(f'{file_name}', 'r') as r:
            data = json.load(r)
            return data

    except Exception as e:
        print('Unwanted Error Occurred', e)
        return '101'