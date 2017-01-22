import requests

HTTP_RESPONSE_CODES = {
    200: 'Success',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'API Not found',
    500: 'Internal Server Error'
}


class Viptela(object):
    """
    Class for use with Viptela vManage API.
    """

    @staticmethod
    def parse_response():
        """
        Parse a request response object
        :return:
        """
        pass

    @staticmethod
    def _get(session, url, headers=None):
        """
        Perform a HTTP get
        :param session: requests session
        :param url: url to get
        :param headers: HTTP headers
        :return:
        """
        if headers is None:
            headers = {'Connection': 'keep-alive', 'Content-Type': 'application/json'}

        return session.get(url=url, headers=headers)

    @staticmethod
    def _put(session, url, headers, data):
        """
        Perform a HTTP put
        :param session: requests session
        :param url: url to get
        :param headers: HTTP headers
        :param data: Data payload
        :return:
        """
        pass

    @staticmethod
    def _post(session, url, headers, data):
        """
        Perform a HTTP post
        :param session: requests session
        :param url: url to post
        :param headers: HTTP headers
        :param data: Data payload
        :return:
        """
        return session.post(url=url, headers=headers, data=data)

    @staticmethod
    def _delete(session, url, headers, data):
        """
        Perform a HTTP delete
        :param session: requests session
        :param url: url to delete
        :param headers: HTTP headers
        :param data: Data payload
        :return:
        """
        pass

    def __init__(self, user, user_pass, vmanage_server, vmanage_server_port=8443, verify=False):
        """
        Init method for Viptela class
        :param user: API user name
        :param user_pass: API user password
        :param vmanage_server: vManage server IP address or Hostname
        :param vmanage_server_port: vManage API port
        :param verify: Verify HTTPs certificate
        """
        self.user = user
        self.user_pass = user_pass
        self.vmanage_server = vmanage_server
        self.vmanage_server_port = vmanage_server_port
        self.verify = verify

        self.base_url = 'https://{0}:{1}/dataservice'.format(self.vmanage_server,
            self.vmanage_server_port)

        self.session = requests.session()
        if not self.verify:
            self.session.verify = self.verify

        # login
        self.login_result = Viptela._post(
            session=self.session,
            url='{0}/j_security_check'.format(self.base_url),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'j_username': self.user, 'j_password': self.user_pass}
        )

    def get_devices(self, device_type='vedges'):
        """
        Get devices from vManage server
        :param device_type: Type of device
        :return:
        """
        if device_type not in ['vedges', 'controllers']:
            raise ValueError('Invalid device type: {0}'.format(device_type))
        url = '{0}/system/device/{1}'.format(self.base_url, device_type)
        return self._get(self.session, url)

    def get_running_config(self, device_id, xml=False):
        """
        Get running config of a device
        :param device_id: Device's ID
        :param xml: Return config in XML format
        :return:
        """
        url = '{0}/template/config/running/{1}'.format(self.base_url, device_id)
        return self._get(self.session, url)

    def get_device_maps(self):
        """
        Get devices geo location data
        :return:
        """
        url = '{0}/group/map/devices'.format(self.base_url)
        return self._get(self.session, url)
