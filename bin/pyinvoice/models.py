from __future__ import unicode_literals
from decimal import Decimal


class PDFInfo(object):
    """
    PDF Properties
    """
    def __init__(self, title=None, author=None, subject=None):
        """
        PDF Properties
        :param title: PDF title
        :type title: str or unicode
        :param author: PDF author
        :type author: str or unicode
        :param subject: PDF subject
        :type subject: str or unicode
        """
        self.title = title
        self.author = author
        self.subject = subject
        self.creator = 'PyInvoice (https://ciciapp.com/pyinvoice)'


class InvoiceInfo(object):
    """
    Invoice information
    """
    def __init__(self, invoice_id=None, invoice_datetime=None, due_datetime=None):
        """
        Invoice info
        :param invoice_id: Invoice id
        :type invoice_id: int or str or unicode or None
        :param invoice_datetime: Invoice create datetime
        :type invoice_datetime: str or unicode or datetime or date
        :param due_datetime: Invoice due datetime
        :type due_datetime: str or unicode or datetime or date
        """
        self.invoice_id = invoice_id
        self.invoice_datetime = invoice_datetime
        self.due_datetime = due_datetime


class AddressInfo(object):
    def __init__(self, name=None, street=None, city=None, mobileNumber=None, country=None, post_code=None):
        """
        :type name: str or unicode or None
        :type street: str or unicode or None
        :type city: str or unicode or None
        :type mobileNumber: str or unicode or None
        :type country: str or unicode or None
        :type post_code: str or unicode or int or None
        """
        self.name = name
        self.street = street
        self.city = city
        self.mobileNumber = mobileNumber
        self.country = country
        self.post_code = post_code


class ServiceProviderInfo(AddressInfo):
    """
    Service provider/Merchant information
    """
    def __init__(self, name=None, street=None, city=None, mobileNumber=None, country=None, post_code=None,
                 discount_number=None):
        """
        :type name: str or unicode or None
        :type street: str or unicode or None
        :type city: str or unicode or None
        :type state: str or unicode or None
        :type country: str or unicode or None
        :type post_code: str or unicode or None
        :type vat_tax_number: str or unicode or int or None
        """
        super(ServiceProviderInfo, self).__init__(name, street, city, mobileNumber, country, post_code)
        self.discount_number = discount_number


class ClientInfo(AddressInfo):
    """
    Client/Custom information
    """
    def __init__(self, name=None, street=None, city=None, mobileNumber=None, country=None, post_code=None,
                 email=None, client_id=None):
        """
        :type name: str or unicode or None
        :type street: str or unicode or None
        :type city: str or unicode or None
        :type mobileNumber: str or unicode or None
        :type country: str or unicode or None
        :type post_code: str or unicode or None
        :type email: str or unicode or None
        :type client_id: str or unicode or int or None
        """
        super(ClientInfo, self).__init__(name, street, city, mobileNumber, country, post_code)
        self.email = email
        self.client_id = client_id


class Item(object):
    """
    Product/Item information
    """
    def __init__(self, name, description, units, unit_price, unit_price_discounted):
        """
        Item modal init
        :param name: Item name
        :type name: str or unicode or int
        :param description: Item detail
        :type description: str or unicode or int
        :param units: Amount
        :type units: int or str or unicode
        :param unit_price: Unit price
        :type unit_price: Decimal or str or unicode or int or float
        :return:
        """
        self.name = name
        self.description = description
        self.units = units
        self.unit_price = unit_price
        self.unit_price_discounted = unit_price_discounted

    @property
    def amount(self):
        return int(self.units) * Decimal(str(self.unit_price_discounted))


class Transaction(object):
    """
    Transaction information
    """
    def __init__(self, gateway, transaction_id, transaction_datetime, amount):
        """
        :param gateway: Payment gateway like Paypal, Stripe etc.
        :type gateway: str or unicode
        :param transaction_id:
        :type transaction_id: int or str or unicode
        :param transaction_datetime:
        :type transaction_datetime: date or datetime or str or unicode
        :param amount: $$
        :type amount: int or float or str or unicode
        :return:
        """
        self.gateway = gateway
        self.transaction_id = transaction_id
        self.transaction_datetime = transaction_datetime
        self.amount = amount
