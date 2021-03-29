from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *
import requests

# Code has been adopted from https://developer.authorize.net/hello_world.html
def initialize_merchant_auth():
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name =''
    merchantAuth.transactionKey =''
    return merchantAuth

# Code has been adopted from https://developer.authorize.net/hello_world.html
def initialize_credit_card(data):
    cc = apicontractsv1.creditCardType()
    cc.cardNumber = data["cardNumber"]
    cc.expirationDate =data["expirationDate"]
    return cc

# Code has been adopted from https://developer.authorize.net/hello_world.html
def create_transaction_request(data, payment, merchantAuth):
    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType ="authCaptureTransaction"
    transactionrequest.amount = Decimal(data["amount"])
    transactionrequest.payment = payment
    
    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId ="MerchantID-0001"
    
    createtransactionrequest.transactionRequest = transactionrequest
    return createtransactionrequest

def email(to):
	return requests.post(
		"https://api.mailgun.net/v3/sandboxfc3ae9aaf5e94106ab5b5d35da585230.mailgun.org/messages",
		auth=("api", ""),
		data={"from": "Excited User <mailgun@sandboxfc3ae9aaf5e94106ab5b5d35da585230.mailgun.org>",
			"to": [to],
			"subject": "Payment Received",
			"text": "Your payment has been received! Thank you for your support!"})