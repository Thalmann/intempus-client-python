#!/usr/bin/env python
import requests


class Resource(object):
    url = 'https://intempus.dk/web/v1'

    def __init__(self, username, api_key, resource):
        self.username = username
        self.api_key = api_key
        self.resource = resource

    @property
    def _headers(self):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'ApiKey {user}:{apikey}'.format(
                user=self.username, apikey=self.api_key),
        }
        return headers

    def get(self, _next_url=None):
        if _next_url is None:
            url = self.url + self.resource
        else:
            url = 'https://intempus.dk/' + _next_url
        response = requests.get(url, headers=self._headers)
        return response.json()

    def get_all(self):
        response = self.get()
        _next = response['meta']['next']
        for _object in response['objects']:
            yield _object

        while _next:
            response = self.get(_next_url=_next)
            _next = response['meta']['next']
            for _object in response['objects']:
                yield _object


if __name__ == '__main__':
    # Example put in username and api_key
    username = 'some_username'
    api_key = 'some_api_key'

    resources = [
        '/employee',
        '/contract',
        '/case',
        '/customer',
        '/work_report',
    ]

    for resource in resources:
        resource = Resource(
            username=username,
            api_key=api_key,
            resource=resource,
        )
        for _object in resource.get_all():
            print(_object)
