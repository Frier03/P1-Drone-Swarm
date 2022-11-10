import json

def insert_data(file_name, data):
    data_object = {
        data[0]: {
            'SPD(m/s)': 0,
            'ALT(m/s)': 0,
            'Signal(%)': 0,
            'Battery(%)': 0,
            'POS_X': 0,
            'POS_Y': 0,
            'STATUS': 'idle',
            'MAC_ADDRESS': data[1],
            'CURRENT_IP': data[3],
            'TYPE': data[2],
            'SSID': '',
            'NAME': data[0]
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

def find_data(file_name, arg):
    try:
        with open(f'{file_name}', 'r') as r:
            data = json.load(r)

            # Locate arg and return its object
            for key, value in data.items():
                if data[key]['NAME'] == arg:
                    return data[key]
            return '101'
    
    except Exception as e:
        print('Unwanted Error Occurred', e)
        return '101'

def request_data(file_name):
    try:
        with open(f'{file_name}', 'r') as r:
            data = json.load(r)
            return data

    except Exception as e:
        print('Unwanted Error Occurred', e)
        return '101'