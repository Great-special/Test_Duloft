def make_payment(request, id):
    # the id is for the house object selected and to get the amount 
    # the request user must be auth and first, last/sur name with the email and phone must present
    
  
    if request.method == "POST":
        form = MakePaymentForm(request.POST)
        if form.is_valid():
            cardNo = form.cleaned_data["card_no"]
            cvv = form.cleaned_data["cvv"]
            expirydate = form.cleaned_data["expirydate"]

            try:
                # print(expirydate.split("/"))
                edate = expirydate.split("/")
                emonth = edate[0]
                eyear = edate[1]
                # print(type(eyear), emonth)
            except:
                message = "Invalid date format"
            
            
            commission_rate = 0.1 # 10% of whatever the price is 
            transaction_rate = 0.015 # 1.5% of whatever the price is 

                
    else:
        form = MakePaymentForm()
        
    context = {'form': form,}
    return render(request, 'flutterwave_payment.html', context)         
            # # Payload with pin
            # payload = {
            # 'tx_ref': "hooli-tx-1920bbtytty",
            # "cardno": "5531886652142950",
            # "cvv": "564",
            # "expirymonth": "09",
            # "expiryyear": "32",
            # "amount": "2500",
            # "email": "user@gmail.com",
            # "phonenumber": "0902620185",
            # "firstname": "temi",
            # "lastname": "desola",
            # "IP": "355426087298442",
            # }
            
            # newPayload = {
            #     'tx_ref': "hooli-tx-1920bbtytty",
            #     'amount': "100",
            #     'currency': "NGN",
            #     'redirect_url': "https://webhook.site/9d0b00ba-9a69-44fa-a43d-a82c33c36fdc",
            #     'meta' : {
            #         'consumer_id': 23,
            #         'consumer_mac': "92a3-912ba-1192a"
            #     },
            #     'customer': {
            #         'email': "user@gmail.com",
            #         'phonenumber': "080****4528",
            #         'name': "Yemi Desola"
            #     },
            #     'customizations': {
            #         'title': "Pied Piper Payments",
            #         'logo': "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
            #     }
            # }

            # try:
            #     response = requests.post(url, data=payload, headers=headers)
            #     print(response)
            # except requests.exceptions.HTTPError as e:
            #     print("HTTP error: %s" % e)

            # try:
            #     res = rave.Card.charge(payload)
            #     print("result-->", res)
            #     if res["suggestedAuth"]:
            #         arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

            #         if arg == "pin":
            #             Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
            #         if arg == "address":
            #             Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})
                    
            #         res = rave.Card.charge(payload)

            #     if res["validationRequired"]:
            #         rave.Card.validate(res["flwRef"], "")

            #     res = rave.Card.verify(res["txRef"])
            #     print(res["transactionComplete"])

            # except RaveExceptions.CardChargeError as e:
            #     print(e.err["errMsg"])
            #     print(e.err["flwRef"])

            # except RaveExceptions.TransactionValidationError as e:
            #     print(e.err)
            #     print(e.err["flwRef"])

            # except RaveExceptions.TransactionVerificationError as e:
            #     print(e.err["errMsg"])
            #     print(e.err["txRef"])
            
            
            
            
            


# const got = require("got");
# try {
#     const response = await got.post("https://api.flutterwave.com/v3/payments", {
#         headers: {
#             Authorization: `Bearer ${process.env.FLW_SECRET_KEY}`
#         },
#         json: {
#             tx_ref: "hooli-tx-1920bbtytty",
#             amount: "100",
#             currency: "NGN",
#             redirect_url: "https://webhook.site/9d0b00ba-9a69-44fa-a43d-a82c33c36fdc",
#             meta: {
#                 consumer_id: 23,
#                 consumer_mac: "92a3-912ba-1192a"
#             },
#             customer: {
#                 email: "user@gmail.com",
#                 phonenumber: "080****4528",
#                 name: "Yemi Desola"
#             },
#             customizations: {
#                 title: "Pied Piper Payments",
#                 logo: "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
#             }
#         }
#     }).json();
# } catch (err) {
#     console.log(err.code);
#     console.log(err.response.body);
# }
         
         
         
         
         
###################################################################
for details in transferdetails:
            account_number = details.get('account_number')
            bank_name = details.get('bank_name')
            account_name = details.get('account_name')
            amount = details.get('amount')
            description = details.get('description')
            
            # checking if the account is valid
            status, resolve_response = self.verify_account_number(account_number, bank_name)
            print(resolve_response)
            
            # If account is valid, create a transfer recipient
            if status:
                reci_status, recipient_response = self.createRecipient(
                    resolve_response, account_name, account_number, bank_name, description)
                
                if reci_status:
                    Transfers.append(
                        {
                            "recipient" : recipient_response["data"]["recipient_code"],
                            "amount":amount,
                        }
                    )