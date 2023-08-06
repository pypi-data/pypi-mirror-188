#   ______ __| _/  | __         _____  ______ |__|
#  /  ___// __ ||  |/ /  ______ \__  \ \____ \|  |
#  \___ \/ /_/ ||    <  /_____/  / __ \|  |_> >  |
# /____  >____ ||__|_ \         (____  /   __/|__|
#      \/     \/     \/              \/|__|

"""
sdk.api
~~~~~~~
This module abstracts access to various services of the superb data kraken (SDK) via the SDKClient class:
To use this module a valid user for the configured sdk is required.

:copyright: (c) 2023 e:fs Techhub GmbH
:license: Apache2, see LICENSE for more details.
"""

import os
import sys
from copy import deepcopy

import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from ._internal_utils import TokenHolder
from .config import _env_configurations

_ACCESS_TOKEN_ENV_KEY = 'SDK_ACCESS_TOKEN'
_REFRESH_TOKEN_ENV_KEY = 'SDK_REFRESH_TOKEN'


class SDKClient:
    f"""
    client class providing methods for accessing SDK services: 
        - organizationmanager (access to organizations/spaces)
        - opensearch
        - ... (to be expanded)

    Authorization at the sdk services is done using JWT tokens which are kept in-memory.
    On every request the access token gets refreshed, if it is about to or has alreadyexpired.
    If no Login information are passed to this module's main class 'SDKClient' on initialization, access/refresh token are expected to be stored in environment 
    variables of the execution environment.

    Usage::
        If access/refresh token can be found int the env-variables {_ACCESS_TOKEN_ENV_KEY} / {_REFRESH_TOKEN_ENV_KEY}
        >>> import sdk.api
        >>> client = sdk.api.SDKClient()
        >>> client.get_all_organizations()

        or with explicit login:
        >>> import sdk.api
        >>> sdk.api.SDKClient(username='hasslethehoff', password='lookingforfreedom')
        >>> client.get_all_organizations()
        
        this module is pre configured for usage with the default instance of the SDK (found here {_env_configurations['sdk-prod']['domain']}) and comes with settings for various different instances
        
        choosing different environment:
        >>> client = sdk.api.SDKClient(env='sdk-dev')
        
        overwriting settings:
        >>> client = sdk.api.SDKClient(domain='mydomain.ai', client_id='my-client-id', api_version='v13.37')
        
    """

    def __init__(self, **kwargs):
        self._env = deepcopy(_env_configurations.get(kwargs.get('env', 'sdk-prod')))
        self.domain = kwargs.get('domain', self._env['domain'])
        self.realm = kwargs.get('realm', self._env['realm'])
        self.client_id = kwargs.get('client_id', self._env['client_id'])
        self.api_version = kwargs.get('api_version', self._env['api_version'])
        self.org_endpoint = f'https://{self.domain}/organizationmanager/api/{self.api_version}/organization'
        self.space_endpoint = f'https://{self.domain}/organizationmanager/api/{self.api_version}/space'

        if 'username' in kwargs and 'password' in kwargs:
            self._token_holder = TokenHolder(domain=self._env['domain'], realm=self._env['realm'], client_id=self._env['client_id'])
            self._token_holder.get_tokens_with_credentials(kwargs['username'], kwargs['password'])
        else:
            try:
                access_token = os.environ[_ACCESS_TOKEN_ENV_KEY]
                refresh_token = os.environ[_REFRESH_TOKEN_ENV_KEY]
                self._token_holder = TokenHolder(domain=self._env['domain'], realm=self._env['realm'], client_id=self._env['client_id'],
                                                 access_token=access_token,
                                                 refresh_token=refresh_token)
            except KeyError:
                print(f'Cannot read token environment variables {_ACCESS_TOKEN_ENV_KEY}, {_REFRESH_TOKEN_ENV_KEY}', file=sys.stderr)
                print('Assert that variables are set or try login initializing with username and password.', file=sys.stderr)

    def get_all_organizations(self):
        """
        Retrieves all Organization the user has access to.

        :return:
            organizations
        """
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(self.org_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_organization_by_id(self, org_id):
        """
        Fetch organization by id.

        :param org_id:
            id of the organization to be fetched
        :return:
            dictionary of the organization
        """
        url = f'{self.org_endpoint}/{org_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_organization_by_name(self, org_name):
        """
        Fetches organization by name.

        :param org_name:
            name of the organization
        :return:
            dictionary of the organization
        """
        url = f'{self.org_endpoint}/name/{org_name}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_all_spaces(self, org_id):
        """
        Gets all spaces of a given organization if the user has access to.
        :param org_id:
            Organization id.
        :return:
            list of spaces
        """
        url = f'{self.space_endpoint}/{org_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_space_by_id(self, space_id):
        """
        Fetch space by id.

        :param space_id:
            id of the space to be fetched
        :return:
            dictionary of the space
        """
        url = f'{self.space_endpoint}/{space_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_space_by_name(self, space_name):
        """
        Fetches space by name.

        :param space_name:
            name of the space
        :return:
            dictionary of the space
        """
        url = f'{self.org_endpoint}/name/{space_name}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def create_space(self, org_id, space):
        """
        Creates a space within the organization specified by id.
        :param org_id:
            organization id within which the space should be created.
        :param space:
            dictionary defining space properties
        :return:
            response body of the http request
        """
        url = f'{self.space_endpoint}/{org_id}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.post(url, json=space, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_document(self, index: str, doc_id: str) -> dict:
        """
        Fetches a document from a given opensearch index and returns it's content
        :param index:
            index name
        :param doc_id:
            document id
        :return:
            document
        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        payload = {
            "index_name": index,
            "filter": [{
                "operator": "EQ",
                "property": "uuid",
                "value": doc_id
            }]
        }
        url = f'https://{self.domain}/search/{self.api_version}/'
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        doc = response.json()['hits'][0]

        return doc

    def index_documents(self, data, index_name: str):
        """
        indexes multiple documents to a given index.
        :param data:
            list of documents to index
        :param index_name:
            index name to index documents to
        :return:
        """
        es = Elasticsearch(['opensearch-cluster-client.elasticsearch.svc.cluster.local:9200'], use_ssl=True, verify_certs=False,
                           headers={"Authorization": "Bearer " + self._token_holder.get_token()}, timeout=60)
        actions = [
            {
                "_index": index_name,
                "_source": entry
            } for entry in data
        ]
        bulk(es, actions, chunk_size=10000)
        es.close()
