import decimal
import hashlib
from urllib import parse

merchant_login = "PLV_DOSTUP"
merchant_test_password_1 = "YCbRZ48dZaeAr5ga88te"


def calculate_signature(*args) -> str:
    """Create signature MD5."""
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def generate_payment_link(
        is_test=1,
        number=0,
        robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx',
        sum=100
) -> str:
    """URL for redirection of the customer to the service.
    """
    signature = calculate_signature(
        merchant_login,
        sum,
        number,
        merchant_test_password_1
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': sum,
        'InvId': number,
        'Description': "Оплата товара",
        'SignatureValue': signature,
        'IsTest': is_test
    }
    return f'{robokassa_payment_url}?{parse.urlencode(data)}'
    