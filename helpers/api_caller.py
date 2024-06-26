from configparser import ConfigParser
import json
import logging
import requests
import helpers.utils as utils


class APICaller:
    ''' Implement calls to any API
    '''

    CONFIG_SECTION=""
    CONFIG_KEY="CONFIG"


    _config: None
    _logger = logging.getLogger(__name__)


    def __init__(self, config_file) -> None:
        config_parser = ConfigParser()
        config_parser.read(config_file)

        try:
            if config_parser.has_option(self.CONFIG_SECTION, self.CONFIG_KEY):
                self._config = utils.json_to_object(config_parser.get(self.CONFIG_SECTION, self.CONFIG_KEY))
            else:
                self._logger.fatal(f"CONFIG is NOT found under {self.CONFIG_SECTION} section")
        except:
            self._logger.fatal("Configuration setup failed!")
    

    def construct_url(self, url:str):
        return f'{self._config.url}{url}'


    def get_header(self):
        return ""


    def construct_auth_header(self):
        auth_header = self.get_header()
        if len(auth_header) != 0:
            header_key = utils.base64_encode(auth_header)
            return {'Authorization': f'Basic {header_key}'}
        
        return None


    ########## Common GET/POST methods ##########
    def do_get(self, url, params=None):
        url = self.construct_url(url)

        self._logger.info ('Initiating GET call to: {}'.format(url))
        
        result = requests.get(url, params=params, headers=self.construct_auth_header())
        response = result.json() if len(result.content) > 0 else {}
        
        self._logger.debug (f'GET from [{url}] receiving response:{response} with status code {result.status_code}')
        
        return utils.json_to_object(json.dumps(response))


    def do_post(self, url, json_body):
        url = self.construct_url(url)

        self._logger.info ('Initiating POST call to: {}'.format(url))
        
        result = requests.post(url, json=json_body, headers=self.construct_auth_header())
        response = result.json() if len(result.content) > 0 else {}
        
        self._logger.debug (f'POST to [{url}] receiving response:{response} with status code {result.status_code}')
        
        return utils.json_to_object(json.dumps(response))
    

    def do_put(self, url, json_body=None):
        url = self.construct_url(url)

        self._logger.info ('Initiating PUT call to: {}'.format(url))
        
        result = requests.put(url, json=json_body, headers=self.construct_auth_header())
        response = result.json() if len(result.content) > 0 else {}
        
        self._logger.debug (f'PUT to [{url}] receiving response:{response} with status code {result.status_code}')
        
        return utils.json_to_object(json.dumps(response))
    

    def do_delete(self, url, json_body=None):
        url = self.construct_url(url)

        self._logger.info ('Initiating DELETE call to: {}'.format(url))
        
        result = requests.delete(url, json=json_body, headers=self.construct_auth_header())
        response = result.json() if len(result.content) != 0 else {}
            
        self._logger.debug (f'DELETE to [{url}] receiving response:{response} with status code {result.status_code}')
        
        return utils.json_to_object(json.dumps(response))