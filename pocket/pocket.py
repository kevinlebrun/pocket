import json
import requests

headers = {'Content-Type': 'application/json; charset=UTF8', 'X-Accept': 'application/json'}

def authenticate(consumer_key):
    request_token = _get_request_token(consumer_key)

    print 'go to https://getpocket.com/auth/authorize?request_token=' + request_token
    raw_input('type ENTER when the application is authorized')

    return _get_access_token(consumer_key, request_token)


def _get_request_token(consumer_key):
    payload = {'consumer_key': consumer_key, 'redirect_uri': 'no-use-here'}
    r = _requests(method='post', resource='/oauth/request.php', data=payload)
    return r['code']


def _get_access_token(consumer_key, request_token):
    payload = {'consumer_key': consumer_key, 'code': request_token}
    r = _requests(method='post', resource='/oauth/authorize.php', data=payload)
    return r['access_token']


def count(consumer_key, access_token, favorite=False, archive=False, unread=False):
    payload = {'consumer_key': consumer_key, 'access_token': access_token, 'state': 'all', 'detailType': 'simple', 'count': 30000}

    if favorite:
        payload.update({'favorite': 1})

    if archive:
        payload.update({'state': 'archive'})

    if unread:
        payload.update({'state': 'unread'})

    r = _requests(method='get', resource='/get', data=payload)

    items = r['list']
    return len(items.values())

# TODO raise a nice exception when resource is invalid (ex: 'get' instead of '/get')
def _requests(method, resource, data, version=3):
    headers = {'Content-Type': 'application/json; charset=UTF8', 'X-Accept': 'application/json'}

    uri = 'https://getpocket.com/v{version}{resource}'.format(version=version, resource=resource)

    r = getattr(requests, method)(uri, data=json.dumps(data), headers=headers)

    if r.status_code >= 400:
        raise Exception('{status_code}, {x-error-code} - {x-error}'.format(status_code=r.status_code, **r.headers))

    return r.json()
