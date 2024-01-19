import requests
import time
from SignavioAuthenticator import *
from urllib.parse import urlparse
from conf import *

def get_root_dir_ids(response):
    root_dir_ids = {}
    for entry in response:
        dir_path = urlparse(entry["href"]).path
        dir_id = dir_path.split("/directory/")[-1]
        dir_name = entry["rep"].get("name_en_us", None)
        root_dir_ids[dir_name] = dir_id
    return root_dir_ids

def get_folder_ids(response, root_dir_ids: dict):
    folder_ids = []
    for entry in response:
        href = entry.get("href", "")
        if href.startswith("/directory/"):
            dir_id = urlparse(href).path.split("/directory/")[-1]
            if root_dir_ids["My documents"] not in dir_id:
                folder_ids.append(dir_id)
    return folder_ids

def change_dir_names(folder_ids: list, dir_url, cookies, headers):
    n = 0
    for folder_id in folder_ids:
        data = {'name': f'{n}', 'description': ''}
        change_dir_name_request = requests.put(
            dir_url + f'/{folder_id}' + '/info',
            cookies=cookies,
            headers=headers,
            data=data)
        if change_dir_name_request.status_code == 200:
            print(f"Successfully renamed folder with ID {folder_id}")
        else:
            print(f"Error while renaming folder with ID {folder_id}")
            break
        n += 1
        time.sleep(1.2)

def main():
    auth_data = SignavioAuthenticator.authenticate()
    dir_url = system_instance + '/p/directory'
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'X-Signavio-ID': auth_data['auth_token']}

    get_dir_meta_request = requests.get(
        dir_url,
        cookies=cookies,
        headers=headers)
    response_status = get_dir_meta_request.status_code
    if response_status != 200:
        print(f"API error: expected 200 but received {response_status} from server")
        return
    response = get_dir_meta_request.json()
    root_dir_ids = get_root_dir_ids(response)
    
    get_dir_ids = requests.get(
        dir_url + '/' + root_dir_ids["My documents"],
        cookies=cookies,
        headers=headers)
    response_status = get_dir_ids.status_code
    if response_status != 200:
        print(f"API error: expected 200 but received {response_status} from server")
        return
    response = get_dir_ids.json()
    folder_ids = get_folder_ids(response, root_dir_ids)

    change_dir_names(folder_ids, dir_url, cookies, headers)

if __name__ == "__main__":
    main()