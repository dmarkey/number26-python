import requests


class N26Exception(Exception):
    pass


class N26Client(object):
    base_url = 'https://api.tech26.de'

    def __init__(self, username, password):
        self.token = None
        self.headers = {}
        self.authenticate(username, password)

    def authenticate(self, username, password):
        url = self.base_url + '/oauth/token'
        headers = {}
        bearer = 'YW5kcm9pZDpzZWNyZXQ='

        headers['Authorization'] = 'Basic ' + bearer

        data = {
            'username': username,
            'password': password,
            'grant_type': 'password'
        }

        resp = requests.post(url=url, data=data, headers=headers)
        if resp.status_code == 200:
            self.token = resp.json()
            self.headers['Authorization'] = "bearer " + self.token['access_token']
        else:
            raise N26Exception("Return code not 200: " + resp.content.decode("utf-8"))

    def do_transfer(self, name, iban, bic, amount, pin, reference=''):
        transaction_wrapper = {'pin': pin,
                               'transaction': {
                                   "partnerBic": bic,
                                   "amount": amount,
                                   "type": "DT",
                                   "partnerIban": iban,
                                   "partnerName": name,
                                   "referenceText": reference
                               }}
        resp = requests.post(self.base_url + '/api/transactions', json=transaction_wrapper, headers=self.headers)

        if resp.status_code != 200:
            raise N26Exception("Return code not 200: " + resp.content.decode("utf-8"))

        return resp.json()

    def cards(self, params=None):
        return self._request("/api/cards", params)

    def transactions(self, params=None):
        return self._request("/api/transactions", params)

    def accounts(self, params=None):
        return self._request("/api/accounts", params)

    def me(self, params=None):
        return self._request("/api/me", params)

    def _request(self, url, params):
        resp = requests.get(self.base_url + url, headers=self.headers, params=params)

        if resp.status_code != 200:
            raise N26Exception("Return code not 200: " + resp.content.decode("utf-8"))

        return resp.json()
