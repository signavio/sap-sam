import json, requests
from sapsam.conf import system_instance
from sapsam.SignavioAuthenticator import SignavioAuthenticator

class ImageGenerator:
    """
    Class that generates images based on JSON or XML representations
    """

    def _delete_diagram(self, id: str):
        """Deletes a diagram in a SAP Signavio Process Manager workspace (by ID)

        Args:
            id (str): diagram/model ID
        """
        auth_data = SignavioAuthenticator.authenticate()
        model_url = system_instance + '/p/model'
        cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
        headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
        requests.delete(f'{model_url}/{id}', cookies=cookies, headers=headers)

    def _setup_folder(self):
        """Creates a folder named 'SAP-SAM' in the 'Shared Documents' directory
        of the workspace, if a folder with such a name does not exist

        Returns:
            str: Folder ID
        """
        auth_data = SignavioAuthenticator.authenticate()
        dir_url = system_instance + '/p/directory'
        cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
        headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
        get_dir_meta_request = requests.get(
            dir_url,
            cookies=cookies,
            headers=headers)
        shared_docs_id = get_dir_meta_request.json()[0]['href'].replace('/directory/', '')
        get_shared_docs_meta_request = requests.get(
            f'{dir_url}/{shared_docs_id}',
            cookies=cookies,
            headers=headers)
        results = get_shared_docs_meta_request.json()
        folder_names_hrefs = [(result['rep']['name'], result['href']) for result in results if 'rep' in result and 'name' in result['rep']]
        sapsam_id = None
        for (x, y) in folder_names_hrefs:
            if x == 'SAP-SAM' and 'directory' in y:
                sapsam_id = y.replace('/directory/', '')
        if not sapsam_id == None:
            return sapsam_id
        else:
            create_dir_request = requests.post(
            f'{dir_url}',
            cookies=cookies,
            headers=headers,
            data={'name': 'SAP-SAM', 'parent': f'/directory/{shared_docs_id}'})
            return json.loads(create_dir_request.content)['href'].replace('/directory/', '')

    def generate_representation(self, name, data, namespace, rep, deletes=True):
        """Uploads a diagram to the SAP-SAM folder in Signavio Process Manager
        and returns a diagram representation, e.g., as PNG or XML.

        Args:
            name (str): Name of the diagram
            data (str): JSON representation of the diagram
            namespace (str): Namespace of the diagram
            rep (str): The representation that should be returned: 'json', 'bpmn2_0_xml', 'png', or 'svg'
            deletes (bool): If True, deletes diagram after content has been generated and returned.
                            Default: True



        Returns:
            Representation of the diagram in the desired format
        """
        auth_data = SignavioAuthenticator.authenticate()
        model_url = system_instance + '/p/model'
        cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
        headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
        data = {
            'parent': '/directory/' + self._setup_folder(),
            'name': name,
            'namespace': namespace,
            'json_xml': data
        }
        create_diagram_request = requests.post(
            model_url,
            cookies=cookies,
            headers=headers,
            data=data)
        result = json.loads(create_diagram_request.content)
        model_id = result['href'].replace('/model/', '')
        revision_id = result['rep']['revision'].replace('/revision/', '')
        diagram_url = system_instance + '/p/revision'
        rep_request = requests.get(
            f'{diagram_url}/{revision_id}/{rep}',
            cookies=cookies,
            headers=headers)
        if deletes:
            self._delete_diagram(model_id)
        return rep_request.content

    def generate_image(self, name, data, namespace, deletes=True):
        """Uploads a diagram to the SAP-SAM folder in Signavio Process Manager
        and returns a diagram representation as PNG.

        Args:
            name (str): Name of the diagram
            data (str): JSON representation of the diagram
            namespace (str): Namespace of the diagram
            deletes (bool): If True, deletes diagram after content has
                            been generated and returned. Default: True


        Returns:
            PNG representation of the diagram
        """
        return self.generate_representation(name, data, namespace, 'png', deletes)
    
    def generate_xml(self, name, data, namespace, deletes=True):
        """Uploads a diagram to the SAP-SAM folder in Signavio Process Manager
        and returns a diagram representation as BPMN 2.x XML.

        Args:
            name (str): Name of the diagram
            data (str): JSON representation of the diagram
            namespace (str): Namespace of the diagram
            deletes (bool): If True, deletes diagram after content has
                been generated and returned. Default: True

        Returns:
            BPMN 2.x XML representation of the diagram
        """
        return self.generate_representation(name, data, namespace, 'bpmn2_0_xml', deletes)

    
