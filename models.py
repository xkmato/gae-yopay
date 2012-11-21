from google.appengine.ext import db
from yopay import api

__author__ = 'kenneth'

class Payment(db.Model):
    phoneNumber = db.StringProperty()
    amount = db.FloatProperty()
    status = db.StringProperty(choices=((u'New'),(u'ERROR'),((u'OK'))),default='New')
    statusCode = db.IntegerProperty()
    transaction_status = db.StringProperty()
    statusMessage = db.StringProperty()
    reference = db.StringProperty()


    def _makeTransaction(self,method,amount,phoneNumber):
        self.amount = float(amount)
        self.phoneNumber = phoneNumber
        self.put()
        try:
            pay = api.YoPay(method,str(self.amount),self.phoneNumber)
            result = pay.get_response()
            self.status = result.get('Status','error')
            self.statusCode = int(result.get('StatusCode',-122))
            self.transaction_status = result.get('TransactionStatus','')
            self.reference = result.get('TransactionReference','no_ref')
            if 'StatusMessage' in result.keys():
                self.statusMessage = result.get('StatusMessage','')
            self.put()
        except api.YoPaymentError,err:
            self.status = 'Error'
            self.reference = 'no_ref'
            self.status_code = -122
            self.transaction_status = str(err)
            self.put()
        return self.status == 'ok'

    def receiveMoney(self,amount,phoneNumber):
        return self._makeTransaction('acdepositfunds',amount,phoneNumber)


    def sendMoney(self,amount,phoneNumber):
        return self._makeTransaction('acwithdrawfunds',amount,phoneNumber)
