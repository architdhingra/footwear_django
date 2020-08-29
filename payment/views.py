from django.shortcuts import render
import requests
import json
# Create your views here.
def payment(request):

    paytmParams = dict()

    paytmParams["body"] = {
        "requestType": "Payment",
        "mid": "kfQlcK24726195886126",
        "websiteName": "dreamwalk",
        "orderId": "ORDERID_98765",
        "callbackUrl": "http://dreamwalk.in/payment.html",
        "txnAmount": {
            "value": "1.00",
            "currency": "INR",
        },
        "userInfo": {
            "custId": "CUST_001",
        },
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys

    return render(request, "payment.html", {})

