import os
import copy
import requests
import json
import hashlib
import datetime
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

APIC_URL = os.getenv("APIC_URL")
APIC_USERNAME = os.getenv("APIC_USERNAME")
APIC_PASSWORD = os.getenv("APIC_PASSWORD")

def apic_login(APIC_URL, APIC_USERNAME, APIC_PASSWORD):
    apic_login_url = f"{APIC_URL}/api/aaaLogin.json"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "aaaUser": {
            "attributes": {
                "name": APIC_USERNAME,
                "pwd": APIC_PASSWORD
            }
        }
    }
    response = requests.post(url=apic_login_url, headers=headers, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        token = response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
        return token
    else:
        return None

def create_snapshot(APIC_URL, token):
    now_time = str(datetime.datetime.now())
    hash_object = hashlib.sha256()
    hash_object.update(now_time.encode('utf-8'))
    hash_value = hash_object.hexdigest()
    snapshot_id = hash_value[-8:]
    apic_create_snapshot_url = f"{APIC_URL}/api/mo.json"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Cookie': f'APIC-cookie={token}'
    }
    data = {
            "configExportP": {
                "attributes": {
                    "dn": f"uni/fabric/configexp-Before_tf_Apply_{snapshot_id}",
                    "snapshot": "true",
                    "adminSt": "triggered"
                }
              }
            }
    response = requests.post(url=apic_create_snapshot_url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        return True, snapshot_id
    else:
        return False, False

def get_snapshot_list(snapshot_id, APIC_URL, token):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Cookie': f'APIC-cookie={token}'
    }
    apic_snapshot_url = f"{APIC_URL}/api/node/mo/uni/backupst/snapshots-[uni/fabric/configexp-Before_tf_Apply_{snapshot_id}].json?query-target=children&target-subtree-class=configSnapshot"
    response = requests.get(url=apic_snapshot_url, headers=headers, verify=False)
    if response.status_code == 200:
        return_data = response.json()['imdata']
        return return_data
    else:
        return None


if __name__ == "__main__":
    token = apic_login(APIC_URL, APIC_USERNAME, APIC_PASSWORD)
    if token:
        create_snapshot_result, snapshot_id = create_snapshot(APIC_URL, token)
        if create_snapshot_result:
            end_time = time.time() + 5 * 60
            i = 1
            while time.time() <= end_time:
                check_snapshot_final_result = get_snapshot_list(snapshot_id, APIC_URL, token)
                if check_snapshot_final_result:
                    print("Successfully create APIC Snapshot.\nSnapshot File Name:")
                    final = copy.deepcopy(check_snapshot_final_result)
                    filename = final[0]['configSnapshot']['attributes']['fileName']
                    print(filename)
                    break
                else:
                    print(f"Pls wait for checking APIC snapshot...\n(retry {i}/150)")
                    i += 1
                    time.sleep(2)
                    if time.time() >= end_time:
                        raise ValueError("Can not check APIC snapshot.")
                    continue
        else:
            raise ValueError("Can not create APIC snapshot.")
    else:
        raise ValueError("Can not login or get APIC Token.")
