import subprocess
import json
import base64

BASE_URL = 'http://localhost:8080/api/2/things'
POLICY_URL = "http://localhost:8080/api/2/policies"
USERNAME = 'ditto'
PASSWORD = 'ditto'
AUTH_HEADER = f"Basic {base64.b64encode(f'{USERNAME}:{PASSWORD}'.encode('ascii')).decode('ascii')}"
POLICY = 'devices.policy:thing_policy'

blocks = 2
floors = 5
apartments = 4

DEVICE_POLICY = {
    "entries": {
        "DEFAULT": {
            "subjects": {
                "nginx:ditto": {
                    "type": "Ditto user authenticated via nginx"
                }
            },
            "resources": {
                "thing:/": {
                    "grant": ["READ", "WRITE"],
                    "revoke": []
                },
                "policy:/": {
                    "grant": ["READ", "WRITE"],
                    "revoke": []
                },
                "message:/": {
                    "grant": ["READ", "WRITE"],
                    "revoke": []
                }
            }
        },
        "HONO": {
            "subjects": {
                "pre-authenticated:hono-connection-my-tenant1": {
                    "type": "Connection to Eclipse Hono"
                }
            },
            "resources": {
                "thing:/": {
                    "grant": ["READ", "WRITE"],
                    "revoke": []
                },
                "message:/": {
                    "grant": ["READ", "WRITE"],
                    "revoke": []
                }
            }
        }
    }
}


def create_policy():
    curl_command_policy = [
        'curl',
        '--location',
        '--request', 'PUT',  # Corrected to PUT
        f'{POLICY_URL}/{POLICY}',  # Using the correct base URL and policy endpoint
        '--header', 'Content-Type: application/json',
        '--data-raw', json.dumps(DEVICE_POLICY),  # Serialize DEVICE_POLICY to JSON
        '--header', f'Authorization: Basic {base64.b64encode(f"{USERNAME}:{PASSWORD}".encode("ascii")).decode("ascii")}',
        '--insecure',  # Use this only for testing, consider removing in production
    ]
    try:
        print(curl_command_policy)
        subprocess.run(curl_command_policy, check=True, text=True)
        print("Policy created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating policy: {e.output}")

def generate_thing_payload(thing_id, definition_url, attributes):
    return {
        "definition": definition_url,
        "policy": POLICY,
        "policyId": POLICY,
        "attributes": attributes
    }

def generate_curl_command(thing_id, thing_payload):
    return [
        'curl',
        '--location',
        '--request', 'PUT',
        f'{BASE_URL}/{thing_id}',
        '--header', 'Content-Type: application/json',
        '--data-raw', json.dumps(thing_payload),
        '--header', f'Authorization: {AUTH_HEADER}'
    ]


def run_subprocess(command):
    try:
        subprocess.run(command, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(e.output)

def create_things():
    for block in range(1, blocks+1):
        thing_id = f'block:block{block}'
        definition_url = "https://raw.githubusercontent.com/life9systems/wot_life9/main/smartBuilding.json"
        block_attributes = {
            "BlockName": "blockName",
            "BlockID": thing_id,
            "Type":"Block"
        }
        
        block_thing_payload = generate_thing_payload(thing_id, definition_url, block_attributes)
        print(block_thing_payload)
        block_curl_command = generate_curl_command(thing_id, block_thing_payload)
        print(block_curl_command)
        run_subprocess(block_curl_command)

        for floor in range(1, floors+1):
            thing_id = f'floor:floor{floor}'
            definition_url = "https://raw.githubusercontent.com/life9systems/wot_life9/main/smartBuilding.json"
            floor_attributes = {
                "FloorName": "floorName",
                "FloorID": thing_id,
                "Type":"Floor"
            }
            
            floor_thing_payload = generate_thing_payload(thing_id, definition_url, floor_attributes)
            print(floor_thing_payload)
            floor_curl_command = generate_curl_command(thing_id, floor_thing_payload)
            print(floor_curl_command)
            run_subprocess(floor_curl_command)
            for apartment in range(1, apartments+1):
                thing_id = f'apartment:apartment{apartment}'
                definition_url = "https://raw.githubusercontent.com/life9systems/wot_life9/main/smartBuilding.json"
                apartment_attributes = {
                    "ApartmentName": "apartmentName",
                    "ApartmentID": thing_id,
                    "Type":"Apartment"
                }
                
                apartment_thing_payload = generate_thing_payload(thing_id, definition_url, apartment_attributes)
                print(apartment_thing_payload)
                apartment_curl_command = generate_curl_command(thing_id, apartment_thing_payload)
                print(apartment_curl_command)
                run_subprocess(apartment_curl_command)
                
                device_name = "sanitizer_life9"
                thing_id = f'wot.block{block}.floor{floor}.apartment{apartment}:{device_name}'
                definition_url = "https://raw.githubusercontent.com/life9systems/wot_life9/main/santizer_life9.json"
                common_attributes = {
                    "block": block,
                    "floor": floor,
                    "apartment": apartment,
                    "MACID": f'MACID_{block}_{floor}_{apartment}',
                    "serialNumber": f'SerialNumber_{block}_{floor}_{apartment}'
                    
                }

                thing_payload = generate_thing_payload(thing_id, definition_url, common_attributes)
                curl_command = generate_curl_command(thing_id, thing_payload)
                print(curl_command)
                run_subprocess(curl_command)



if __name__ == '__main__':
    # Creating Digital twin Thing in eclipse ditto
    create_policy()
    create_things()
