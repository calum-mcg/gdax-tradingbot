import hmac, hashlib, requests, base64
from requests.auth import AuthBase

#Authentication for Exchange for GDAX
#Adapted from GDAX: https://docs.gdax.com/#signing-a-message
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase, api_url):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.api_url = api_url

    def __call__(self, request):
        r = requests.get(self.api_url + 'time')
        timestamp = str((r.json())['epoch'])
        message = timestamp + request.method + request.path_url + (request.body or '')
        request.headers.update(get_auth_headers(timestamp, message, self.api_key, self.secret_key,
                                                self.passphrase))
        return request

def get_auth_headers(timestamp, message, api_key, secret_key, passphrase):
    message = message.encode('ascii')
    hmac_key = base64.b64decode(secret_key)
    signature = hmac.new(hmac_key, message, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
    return {
        'Content-Type': 'Application/JSON',
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-KEY': api_key,
        'CB-ACCESS-PASSPHRASE': passphrase
}