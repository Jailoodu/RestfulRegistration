from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *
import os
import requests

# Code has been adopted from https://developer.authorize.net/hello_world.html
# Set up merchant authorization
def initialize_merchant_auth():
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name ='2b4dU77zM5Mp'
    merchantAuth.transactionKey ='6n2X9k277FJNTGaZ'
    return merchantAuth

# Code has been adopted from https://developer.authorize.net/hello_world.html
# Set up credit card object
def initialize_credit_card(data):
    cc = apicontractsv1.creditCardType()
    cc.cardNumber = data["cardNumber"]
    cc.expirationDate =data["expirationDate"]
    return cc

# Code has been adopted from https://developer.authorize.net/hello_world.html
# Create a transaction request
def create_transaction_request(data, payment, merchantAuth):
    transaction_request = apicontractsv1.transactionRequestType()
    transaction_request.transactionType ="authCaptureTransaction"
    transaction_request.amount = Decimal(data["amount"])
    transaction_request.payment = payment
    
    create_request = apicontractsv1.createTransactionRequest()
    create_request.merchantAuthentication = merchantAuth
    create_request.refId ="MerchantID-0001"
    
    create_request.transactionRequest = transaction_request
    return create_request

# Mailgun API used to send emails
def email(to):
    key = os.getenv('KEY')
    domain = os.getenv('DOMAIN')

    addr = "https://api.mailgun.net/v3/" + domain + "/messages"
    from_user = "The Company <mailgun@" + domain + ">"

    return requests.post(
		addr,
		auth=("api", key),
		data={"from": from_user,
			"to": [to],
			"subject": "Payment Received",
			"text": "Your payment has been received! Thank you for your support!"})