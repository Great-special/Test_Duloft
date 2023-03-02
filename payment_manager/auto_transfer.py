import time
import schedule 
from django.utils import timezone
from django.conf import settings


from users.models import LandLordPaymentDetails

from .models import Payment, TransactionDetail
# from .paystack import PayStack

# Paystack = PayStack(settings.PAY_SECRET_KEY)

# Paystack = settings.PAYSTACK

true = True

TRANSFER_DETAILS = []
DATA = []


def get_paymentdate():
    today_date = str(timezone.now().date())
    print(today_date)
    date_list = today_date.split('-')
    day = int(date_list[2]) - 5
    print(day)
    date_list.pop(2)
    date_list.append(str(day))
   
    payment_date = f"{date_list[0]}-{date_list[1]}-{date_list[2]}"
    
    return payment_date
    

def get_payment_qurey():
    obj_qurey_set = Payment.objects.filter(date_created__contains=get_paymentdate()).filter(verified=True).all()
    print(obj_qurey_set, 'returned')
    return obj_qurey_set




def create_bulk_transfer_recipient(data: list):
    status, bulk_recipient_response = Paystack.bulktransferrecipient(data)
    print('done with bulk transfer recipients creation moving on -->')
    print(bulk_recipient_response)
    success_data = bulk_recipient_response['success']
    error_data = bulk_recipient_response['errors']
    
    if status == true:
        return success_data
    else:
        return error_data
    
    
    # { "type": "nuban",
    #   "name": "Tolu Robert",
    #   "account_number": "01000000010",
    #   "bank_code": "058",
    #   "currency": "NGN"
    # }


def get_transfer_details():
    payment_qurey = get_payment_qurey()
    # print(payment_qurey, 'respond')
    for payment in payment_qurey:
        # print(payment, 'for loop')
        try:
            print(payment.amount, payment.description, payment.recipient_name.get_full_name(), )
        except:
            print('error')
        else:
            transaction_charge = float(payment.amount) * 0.02
            new_amount = float(payment.amount) - transaction_charge
            payment_details = LandLordPaymentDetails.objects.filter(user_profile=payment.recipient_name).first()
            print('payment details', payment_details, payment_details.bank_name, payment_details.account_number)
            print(Paystack.verify_account_number(payment_details.account_number, payment_details.bank_name))
            DATA.append(
                {   "type": "nuban",
                    "name": payment.recipient_name.get_full_name(),
                    "account_number": payment_details.account_number,
                    "bank_code": Paystack.get_bank_code(payment_details.bank_name),
                    "currency": "NGN",
                    "amount": new_amount,
                    'description':payment.description,
                    "reference":payment.ref
                }
            )

    if DATA:
        # print(DATA, 'data')
        response = create_bulk_transfer_recipient(DATA)
        for D in DATA:
            for res in response:
                # print('res', res)
                if D['name'] == res['name'] and D['account_number'] == res['details']['account_number']:
                    TRANSFER_DETAILS.append(
                        {
                            "type": "nuban",
                            'amount': D['amount'],
                            'description':res['description'],
                            'name':res['name'],
                            'account_number':res['details']['account_number'],
                            'bank_code':res['details']['bank_code'],
                            'reference':D['reference'],
                            'recipient':res['recipient_code'],
                            "currency": "NGN",
                        }
                    )




def clearer():
    TRANSFER_DETAILS.clear()
    DATA.clear()



def autoTransfer():
    # get_transfer_details()
    # response_b = Paystack.bulkbankTransfer(TRANSFER_DETAILS)
    # print(response_b)
    # after the transfers haven been verferied create a TransactionsDetails object and store the transaction details
    # using the reference_id or ref to store each transaction to it payment counterpart.
    pass

    
# autoTransfer()


# name = 'Godisgreat Nwachukwu'
# acc_name = 'Godisgreat Special Nwachukwu'

# if name in acc_name: # acc_name.find(name)
#     print('yes!!!')
