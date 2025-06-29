import requests
import time
import json
def get_status(correlation_id):
    url = f'http://127.0.0.1:4001/get-progress?correlation_id={correlation_id}'
    try:
        res = requests.get(url)
        progress = res.json()
        status_code = res.status_code
        print(status_code)
        if status_code not in [200,201,202]:
            return False
        if isinstance(progress,str):
            return False
        
        else:
            print("Checking Progress Now")
            if progress == 100:
                return True
            else:
                print(progress)
                time.sleep(20)
                get_status(correlation_id)
    except Exception as e:
        raise e

def get_completion_status(correlation_id,retries = 4):
    while retries:
        status = get_status(correlation_id)
        if status:
            return "Completed"
        else:
            print(f"Retrying..., {retries} left.")
            time.sleep(10)
        retries = retries -1
    return "Problem with api or process not started"

print(get_completion_status("CORR145819"))