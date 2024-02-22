import requests
import time
from sapsam.SignavioAuthenticator import *
from urllib.parse import urlparse
from sapsam.conf import *
import json

def get_latest_rev(response):
    for entry in response:
        href = entry.get("href", "")
        if href.startswith("/revision/"):
            href = href.replace("/revision/", "")
            return href

def syntax_checker(model_json):
    auth_data = SignavioAuthenticator.authenticate()
    syntax_check_url = system_instance + '/p/syntaxchecker'
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'X-Signavio-ID': auth_data['auth_token']}
    '''
    # Uncomment and adapt this part for using the function directly in a workspace
    mod_url = system_instance + '/p/model'
    rev_url = system_instance + '/p/revision'
    get_diagram_request = requests.get(
        rev_url + '/' + rev_id + '/json',
        cookies=cookies,
        headers=headers)
    response_status = get_diagram_request.status_code
    if response_status != 200:
        print(f"API error: expected 200 but received {response_status} from server")
        return
    '''
    data = {'isJson': 'true',
            'data_json': model_json,
            'ns': 'http://b3mn.org/stencilset/bpmn2.0#'}

    syntax_check_request = requests.post(
        syntax_check_url,
        cookies=cookies,
        headers=headers,
        data=data)
    response_status = syntax_check_request.status_code
    if response_status != 200:
        print(f"API error: expected 200 but received {response_status} from server")
        return
    
    rep_data = syntax_check_request.json().get('rep', [])
    syntax_errors = {
        'errors': rep_data[0].get('must', []),
        'warnings': rep_data[0].get('should', []),
    }
    time.sleep(0.8) # limitation for API calls (50/minute)
    return json.dumps(syntax_errors)
    

def bp_conventions_checker(name:str, model_id: str, guideline_id: str, model_json):
    auth_data = SignavioAuthenticator.authenticate()
    bp_check_url = system_instance + '/p/mgeditorchecker'
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'X-Signavio-ID': auth_data['auth_token']}
    '''
    # Uncomment and adapt this part for using the function directly in a workspace
    mod_url = system_instance + '/p/model'
    rev_url = system_instance + '/p/revision'
    get_diagram_revisions = requests.get(
        mod_url + '/' + model_id + '/revisions',
        cookies=cookies,
        headers=headers)
    response_status = get_diagram_revisions.status_code
    if response_status != 200:
        print(f"API error: expected 200 but received {response_status} from server")
        return
    #rev_id = get_latest_rev(get_diagram_revisions.json())
    
    get_diagram_request = requests.get(
        rev_url + '/' + rev_id + '/json',
        cookies=cookies,
        headers=headers)
    response_status = get_diagram_request.status_code
    if response_status != 200:
        print(f"API error: expected 200 but received {response_status} from server")
        return
    '''
    data = {'comments': '{}',
            'guidelineId': guideline_id,
            'name': name,
            'model_json': model_json,
            'id': model_id,
            'checkLinking': 'false'}

    bp_check_request = requests.post(
        bp_check_url,
        cookies=cookies,
        headers=headers,
        data=data)
    response_status = bp_check_request.status_code
    if response_status != 200:
        print(f"API error: expected 200 but received {response_status} from server")
        return
    
    rep_data = bp_check_request.json().get('rep', [])
    violations_count = {
        'errors': len(rep_data[0].get('must', [])),
        'warnings': len(rep_data[0].get('should', [])),
        'info': len(rep_data[0].get('info', []))
    }
    time.sleep(0.8) # limitation for API calls (50/minute)
    return json.dumps(violations_count)