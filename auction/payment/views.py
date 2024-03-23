import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from lot.models import Lot, LotShippingStatus
from payment.models import Transaction
import xml.etree.ElementTree as ET
import requests
from django.urls import reverse_lazy


def esewa_request(request):
    if request.method == 'GET':
        lot_id = request.GET.get("lot_id")
        highest_amount = request.GET.get("amount")
        lot = get_object_or_404(Lot, id=lot_id)
        context = {
            "lot": lot,
            "amount": highest_amount,
        }
        return render(request, 'esewa_request.html', context)
    
def esewa_verify(request):
    if request.method == 'GET':
        lot_id = request.GET.get('oid')
        amount = request.GET.get('amt')
        refId = request.GET.get('refId')
        print(lot_id, amount, refId)
        url = "https://uat.esewa.com.np/epay/transrec"
        data = {
            'amt': amount,
            'scd': 'EPAYTEST',
            'rid': refId,
            'pid': lot_id,
        }
        resp = requests.post(url, data)
        print(resp)
        root = ET.fromstring(resp.content)
        print(root)
        status = root[0].text.strip()
        print(status)
        lot_id = lot_id.split("_")[1]
        print(lot_id)
        lot = Lot.objects.get(id=lot_id)
        print(lot)
        if status == "Success":
            print("successs.............")
            print(lot)
            transaction = Transaction.objects.create(
                lot=lot, 
                buyer=request.user, 
                final_price=int(float(amount)), 
                status=True,
                payment_method="Esewa")
            shipping_status = LotShippingStatus.objects.create(lot=lot)
            return redirect(reverse_lazy('lots:won_lots'))
        else:
            url = reverse_lazy('payment:esewa_request')
            url += f'?lot_id={lot_id}&amount={amount}'
            return redirect(url)

def khalti_request(request):
    lot_id = request.GET.get('lot_id')
    amount = request.GET.get('amount')
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = 'http://127.0.0.1:8000/payment/verify/khalti/'
    payload = json.dumps({
            "return_url": return_url,
            "website_url": "http://127.0.0.1:8000/",
            "amount": int(amount) * 100,
            "purchase_order_id": f"{lot_id}",
            "purchase_order_name": "customer_name",
            "customer_info": {
                "name": str(request.user.get_user_full_name()),
                "email": str(request.user.email),
                "phone": str(request.user.phone_number),
            }
        })
    
    headers = {
            'Authorization': 'key 93c4d5cb81ef4b8caf41ff6fa52889d0',
            'Content-Type': 'application/json',
        }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    new_res = json.loads(response.text)
    print(new_res)
    return redirect(new_res['payment_url'])

def khalti_verify(request):
    pidx = request.GET.get('pidx')
    headers = {
            'Authorization': 'key 93c4d5cb81ef4b8caf41ff6fa52889d0',
            'Content-Type': 'application/json',
        }
    payload = json.dumps({
            'pidx': pidx
        })
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    response = requests.request("POST", url, headers=headers, data=payload)
    response = json.loads(response.text)

    if response['status'] == 'Completed':
        # transaction = Transaction.objects.create(
        #         lot=lot, 
        #         buyer=request.user, 
        #         final_price=int(float(amount)), 
        #         status=True,
        #         payment_method="Esewa")
        #     shipping_status = LotShippingStatus.objects.create(lot=lot)
        return JsonResponse(response)
    else:
        return JsonResponse(response)