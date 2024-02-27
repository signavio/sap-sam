import requests
from sapsam.conf import *

class SignavioAuthenticator:
    """
    Takes care of authentication against Signavio systems
    """

    def authenticate():
        """
        Authenticates user at Signavio system instance and initiates session.
        Returns:
            dictionary: Session information
        """
        login_url = system_instance + '/p/login'
        data = {
            'name': email,
            'password': pw,
            'tokenonly': 'true',
            'tenant': tenant_id
        }
    
        # authenticate
        login_request = requests.post(login_url, data)

        # retrieve token and session ID
        auth_token = login_request.content.decode('utf-8')
        jsesssion_ID = login_request.cookies['JSESSIONID']

        # The cookie is named 'LBROUTEID' for base_url 'editor.signavio.com'
        # and 'editor.signavio.com', and 'AWSELB' for base_url
        # 'app-au.signavio.com' and 'app-us.signavio.com'
        lb_route_ID = login_request.cookies['LBROUTEID']

        # return credentials
        return {
            'jsesssion_ID': jsesssion_ID,
            'lb_route_ID': lb_route_ID,
            'auth_token': auth_token
        }
