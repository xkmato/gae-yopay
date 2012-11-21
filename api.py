from google.appengine.ext import db

__author__ = 'kenneth'

from xml.dom.minidom import Document
from xml.dom import minidom
from urllib2 import Request, urlopen, HTTPError, URLError


class YoPaymentError(RuntimeError):
    pass

class ErrorLog(db.Model):
    text = db.StringProperty()

class YoPay(object):
    url = 'http://41.220.12.206/services/yopaymentsdev/task.php'
    _username = '90001666301'
    _password = '1228058850'


    def __init__(self,method,amount,account):
        self.method = method
        self.amount = amount
        self.account = account

    def _build_request(self):
        doc = Document()
        root  = doc.createElement('AutoCreate')
        doc.appendChild(root)

        request_ = doc.createElement('Request')
        root.appendChild(request_)

        username = doc.createElement('APIUsername')
        username_text = doc.createTextNode(self._username)
        username.appendChild(username_text)
        request_.appendChild(username)

        password = doc.createElement('APIPassword')
        password_text = doc.createTextNode(self._password)
        password.appendChild(password_text)
        request_.appendChild(password)

        method = doc.createElement('Method')
        method_text = doc.createTextNode(self.method)
        method.appendChild(method_text)
        request_.appendChild(method)

        amount = doc.createElement('Amount')
        amount_text = doc.createTextNode(self.amount)
        amount.appendChild(amount_text)
        request_.appendChild(amount)

        account = doc.createElement('Account')
        account_text = doc.createTextNode(self.account)
        account.appendChild(account_text)
        request_.appendChild(account)

        narrative = doc.createElement('Narrative')
        narrative_text = doc.createTextNode('Testing one... Testing one two')
        narrative.appendChild(narrative_text)
        request_.appendChild(narrative)

        return doc.toxml(encoding='utf-8')

    def _parse_response(self,response_xml):
        xml_doc = minidom.parseString(response_xml)
        root = xml_doc.documentElement
        response = root.childNodes[0]
        result = {}
        for node in response.childNodes:
            if node.firstChild:
                result[node.tagName] = node.firstChild.wholeText
            else:
                error = ErrorLog(text = str(node)).put()
        return result

    def _create_request(self):
        request_ =self._build_request()
        request=Request(url=self.url, data=request_)
        request.add_header('Content-Type','text/xml')
        request.add_header('Content-transfer-encoding','text')
        return request

    def get_response(self):
        request = self._create_request()
        try:
            response_xml = urlopen(request).read()
        except HTTPError, err:
            raise YoPaymentError(err)
        except  URLError,err:
            raise YoPaymentError(err)
        else:
            return self._parse_response(response_xml)

