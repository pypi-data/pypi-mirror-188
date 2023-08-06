import requests
from lxml import etree
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client as ZeepClient
from zeep import Plugin
from zeep.cache import SqliteCache
from zeep.transports import Transport

from correos_preregistro.errors import UndefinedCredentials, UnknownApiResponse
from correos_preregistro.vars import PRE_URL, URL


class MyLoggingPlugin(Plugin):
    def ingress(self, envelope, http_headers, operation):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers

    def egress(self, envelope, http_headers, operation, binding_options):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers


class Client:
    def __init__(self, user, password, environment="pre"):
        session = Session()
        session.auth = HTTPBasicAuth(user, password)
        self.client = ZeepClient(
            "{url}?wsdl".format(url=PRE_URL if environment == "pre" else URL),
            transport=Transport(
                session=session,
                cache=SqliteCache(),
            ),
        )

    def send_request(self, payload):
        return self.client.service.PreRegistro(**payload)


# TODO: Use the Client instead of RawClient
# The RawClient is transient classes until
# we can implement correctly the Zeep integration
class RawClient:
    def __init__(self, user, password, environment="pre"):
        if not user or not password:
            raise UndefinedCredentials()
        self.url = PRE_URL if environment == "pre" else URL
        self.auth = (user, password)

    def send_request(self, payload):
        payload = payload.decode()
        response = requests.post(
            self.url, headers={"content-type": "text/xml"}, data=payload, auth=self.auth
        )
        if not response.ok or response.status_code != 200:
            raise UnknownApiResponse(response.text)
        return response.text
