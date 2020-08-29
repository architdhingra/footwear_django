from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
import razorpay
# Create your views here.


def payment(request):
    context = {}
    client = razorpay.Client(auth=("rzp_test_oKQ9jz6Gyo5PdO", "yg3w0rMlvRA8OTUN8pLIKtF4"))
    order_amount = 100
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    notes = {
        'Shipping address': 'Bommanahalli, Bangalore'}
    print('Amount::', order_amount)
    # CREAING ORDER
    response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
    order_id = response['id']
    order_status = response['status']

    if order_status == 'created':
        context['product_id'] = 'product'
        context['price'] = 'order_amount'
        context['name'] = 'name'
        context['phone'] = 'phone'
        context['email'] = 'email'

        # data that'll be send to the razorpay for
        context['order_id'] = order_id
        print('created order')
        return render(request, 'payment.html', context)

    return HttpResponse('<h1>Error in  create order function</h1>')

