import json
import requests

class PocketException(Exception):
    pass

def authenticate(consumer_key):
    request_token = _get_request_token(consumer_key)

    # TODO accept a handler here
    print 'go to https://getpocket.com/auth/authorize?request_token=' + request_token
    raw_input('type ENTER when the application is authorized')

    # TODO return credentials
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


# TODO handle random
# TODO handle filters
def take(consumer_key, access_token, number, oldest=False, attributes=None, archive=False, delete=False):
    payload = {'consumer_key': consumer_key, 'access_token': access_token, 'state': 'unread', 'detailType': 'complete', 'count': number, 'sort': 'newest'}

    if oldest:
        payload.update({'sort': 'oldest'})

    r = _requests(method='get', resource='/get', data=payload)
    items = r['list'].values()

    if attributes:
        items = [filter_attributes(attributes, item) for item in items]

    if archive:
        ids = [item['item_id'] for item in items]
        archive(consumer_key, access_token, ids)

    if delete:
        ids = [item['item_id'] for item in items]
        delete(consumer_key, access_token, ids)

    return items


def filter_attributes(attributes, item):
    return {key: value for key, value in item.items() if key in attributes}


# TODO handle errors
def archive(consumer_key, access_token, ids):
    actions = [{'action': 'archive', 'item_id': item_id} for item_id in ids]
    payload = {'consumer_key': consumer_key, 'access_token': access_token, 'actions': actions}
    _requests(method='post', resource='/send', data=payload)


# TODO handle errors
def delete(consumer_key, access_token, ids):
    actions = [{'action': 'delete', 'item_id': item_id} for item_id in ids]
    payload = {'consumer_key': consumer_key, 'access_token': access_token, 'actions': actions}
    _requests(method='post', resource='/send', data=payload)


# TODO handle errors
def add(consumer_key, access_token, links):
    actions = [{'action': 'add', 'url': link} for link in links]
    payload = {'consumer_key': consumer_key, 'access_token': access_token, 'actions': actions}
    _requests(method='post', resource='/send', data=payload)


# TODO raise a nice exception when resource is invalid (ex: 'get' instead of '/get')
def _requests(method, resource, data, version=3):
    headers = {'Content-Type': 'application/json; charset=UTF8', 'X-Accept': 'application/json'}

    uri = 'https://getpocket.com/v{version}{resource}'.format(version=version, resource=resource)

    # TODO json.dumps to be deleted
    r = getattr(requests, method)(uri, data=json.dumps(data), headers=headers)

    if r.status_code >= 400:
        raise PocketException('{status_code}, {x-error-code} - {x-error}'.format(status_code=r.status_code, **r.headers))

    return r.json()
