import json, time

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

def find_name_by_mac(file_name, arg):
    try:
        with open(f'{file_name}', 'r') as r:
            data = json.load(r)

            # Locate arg and return its object
            for key, value in data.items():
                if data[key]['MAC_ADDRESS'][-8:] == arg:
                    return data[key]['NAME']
            return '101'
    
    except Exception as e:
        print('Unwanted Error Occurred', e)
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
    
def edit_data(file_name, *args):
    try:
        with open(f'{file_name}', 'r') as r:
            data = json.load(r)
            # Locate arg and return its object
            for key, value in data.items():
                if data[key]['NAME'] == args[0]:
                    data[key][args[1]] = args[2]

            # Write back to the file
            with open(f'{file_name}', 'w') as w:
                json.dump(data, w)

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