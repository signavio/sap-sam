import sys
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
        dir_name = entry["rep"].get("name", None)
        root_dir_ids[dir_name] = dir_id
    return root_dir_ids

def get_object_ids(response, target_dir_name, root_dir_ids: dict, object_type: str):
    object_ids = []
    for entry in response:
        href = entry.get("href", "")
        if href.startswith(object_type):
            dir_id = urlparse(href).path.split(object_type)[-1]
            if root_dir_ids[target_dir_name] not in dir_id:
                object_ids.append(dir_id)
    return object_ids

def get_latest_rev(response):
    for entry in response:
        href = entry.get("href", "")
        if href.startswith("/revision/"):
            href = href.replace("/revision/", "")
            return href

def change_dir_names(folder_ids: list, dir_url, cookies, headers):
    n = 0
    for folder_id in folder_ids:
        data = {'name': f'd{n}', 'description': ''}
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

def change_mod_names(model_ids: list, mod_url, cookies, headers):
    n = 0
    for model_id in model_ids:
        data = {'name': f'm{n}'}
        change_mod_name_request = requests.put(
            mod_url + f'/{model_id}' + '/info',
            cookies=cookies,
            headers=headers,
            data=data)
        if change_mod_name_request.status_code == 200:
            print(f"Successfully renamed model with ID {model_id}")
        else:
            print(f"Error while renaming model with ID {model_id}")
            break
        n += 1
        time.sleep(1.2)

def main():
    if len(sys.argv) < 2:
        print("Script requires an argument: 'rename' or 'fetch' or 'conventions'")
        return
    if sys.argv[1] == 'rename' or sys.argv[1] == 'fetch' or sys.argv[1] == 'conventions':
        pass
    else:
        print("Unknown argument")
        return

    auth_data = SignavioAuthenticator.authenticate()
    dir_url = system_instance + '/p/directory'
    mod_url = system_instance + '/p/model'
    rev_url = system_instance + '/p/revision'
    bp_check_url = system_instance + '/p/mgeditorchecker'
    target_dir_name = "Shared documents"
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

    if sys.argv[1] == 'rename':
        list_all_ids = requests.get(
            dir_url + '/' + root_dir_ids[target_dir_name],
            cookies=cookies,
            headers=headers)
        response_status = list_all_ids.status_code
        if response_status != 200:
            print(f"API error: expected 200 but received {response_status} from server")
            return
        response = list_all_ids.json()
        folder_ids = get_object_ids(response, target_dir_name, root_dir_ids, "/directory/")
        #change_dir_names(folder_ids, dir_url, cookies, headers)

        model_ids = get_object_ids(response, target_dir_name, root_dir_ids, "/model/")
        #change_mod_names(model_ids, mod_url, cookies, headers)
        print("Function currently deactivated")
    elif sys.argv[1] == 'fetch':
        fetch_diagram = requests.post(
            mod_url + '/10ac4ca1ccfc4c7cb8de451d92ba04aa/json',
            cookies=cookies,
            headers=headers)
        print(fetch_diagram.text)
    elif sys.argv[1] == 'conventions':
        #get_guideline_id = requests.get()
        get_diagram_revisions = requests.get(
            mod_url + '/10ac4ca1ccfc4c7cb8de451d92ba04aa/revisions',
            cookies=cookies,
            headers=headers)
        rev_id = get_latest_rev(get_diagram_revisions.json())

        get_diagram_request = requests.get(
            rev_url + '/' + rev_id + '/json',
            cookies=cookies,
            headers=headers)

        data = {'comments': '{}',
                'guidelineId': '4551c2229baa4c79a151b5a0cc1010d2', #to do next, find out how to retrieve guidelineid
                                                                    #w/o using the console
                'name': 'Getränkebestellung',
                'model_json': get_diagram_request.content,
                'id': '10ac4ca1ccfc4c7cb8de451d92ba04aa',
                'checkLinking': 'false'}

        bp_check_request = requests.post(
            bp_check_url,
            cookies=cookies,
            headers=headers,
            data=data)

        rep_data = bp_check_request.json().get('rep', [])
        violations_count = {
            'errors': len(rep_data[0].get('must', [])),
            'warnings': len(rep_data[0].get('should', [])),
            'info': len(rep_data[0].get('info', []))
        }
        print(violations_count)
    else:
        print("Unknown arg")

if __name__ == "__main__":
    main()