'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: pay_constants.py
# Project: core.wecare.id
# File Created: Wednesday, 5th December 2018 12:07:34 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 5th December 2018 12:07:34 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love
# Copyright - 2018 Wecare.Id, wecare.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from decimal import Decimal

AVAILABLE_PAYMENT_TYPE = [
    "wallet",
    "credit-card",
    "debit-card",
    "credit-card-direct"
]

# fees
YUNA_SHARE = Decimal(0.1)
FASPAY_CREDIT_CARD_FEES = Decimal(0.0285)

BILL_TYPE_CHOICES = (
    ("shipping", "Shipping Fee"),
    ("handling fee", "Handling Fee"),
    ("Campaign", "Campaign / Discount / Promotion"),
)
DELIVERY_STATUSES = (
    ('delivered', "Delivered"),
    ('not-received', "Not Received"),
)
CONFIRM_STATUSES = (
    ('accept', "Accept"),
    ('cancel', "Cancel/Refund"),
)
WEIGHT_UNIT_CHOICES = (
    (1, 'Kg'),
)
QUANTITY_UNIT = (
    (1, 'Pieces'),
    (2, 'Roll'),
)
STORE_TYPE_CHOICES = (
    (1, 'Virtual'),
    (2, 'Physical'),
)
TRANSACTION_TYPE_CHOICES = (
    (1, 'Online'),
    (2, 'Offline'),
)
CLEARENCE_TYPE_CHOICES = (
    ("order", "Order"),
    ("discount", "Discount or Coupon"),
)
CLEARENCE_STATUSES = (
    ("pending", "Pending"),
    ("success", "Success"),
    ("failed", "Failed"),
)
PREORDER_STATUSES = (
    ("requested", "Requested"),
    ("order-ready", "Order Ready"),
    ("not-available", "Product Not Available"),
)
TRANSACTION_STATE_CHOICES = (
    ('transaction-start', 'Start Transaction'),  # ORDER BEGIN
    ('payment-waiting', 'Waiting for Payment'),
    ('payment-paid', 'Paid by Buyer'),
    ('payment-expired', 'Payment Expired'),
    ('ordered-pre', 'Pre Ordered'),  # BUYER PRE ORDER
    ('order-on-process', 'Order On Process'),  # BUYER ORDER ON PROCESS
    ('ready-to-pickup', 'Ready to Pick Up'),
    ('picked-up', 'Picked Up'),
    ('on-delivery', 'On Delivery'),  # SELLER ON DELIVERY : COD OR SHIPPING
    ('received', 'Received'),  # SELLER ON DELIVERY : COD OR SHIPPING
    # ORDER DONE. PRODUCT ALREADY RECEIVED BY BUYER
    ('transaction-end', 'End Transaction'),
    # PURGE / CANCEL EVERYTHING; NOT YET USED
    ('order-cancelled', 'Cancel Order'),
    ('not-available', 'Order Not Available'),  # ITEM OR ORDER NOT AVAILABLE
    ('not-received', 'Not Received'),  # BUYER NOT RECEIVED
)
PAYMENT_TYPE_CHOICES = (
    ('order', 'Order'),
    ('topup', 'Top Up')
)
ORDER_STATUSES = TRANSACTION_STATE_CHOICES
ITEM_STATUSES = ORDER_STATUSES
ORDER_TYPE_CHOICES = (
    (1, 'Retail'),
    (2, 'Booking'),
    (3, 'Subscription'),
)
HANDLE_COST_CHOICES = (
    (1, 'Credit Card Payment Gateway Fee'),
    (2, 'Credit Card MDR (Merchant Discount Rate)'),
)
BILL_STATUSES = (
    ('authorize', 'Authorized'),
    ('capture', 'Captured'),
    ('settlement', 'Settled'),
    ('deny', 'Denied'),
    ('pending', 'Pending'),
    ('cancel', 'Canceled'),
    ('refund', 'Refunded'),
    ('partial_refund', 'Partially Refunded'),
    ('chargeback', 'Charged Back'),
    ('partial_chargeback', 'Partially Charged Back'),
    ('expire', 'Expired'),
    ('failure', 'Failed'),
)
PAYMENT_STATUSES = BILL_STATUSES
INVOICE_STATUSES = BILL_STATUSES
CASHOUT_STATUSES = (
    ('pending', 'Pending'),
    ('processed', 'On Process'),
    ('paid', 'Paid'),
    ('not-paid', 'Not Paid'),
)
TOPUP_STATUSES = (
    ("pending", "Pending"),
    ("success", "Approved"),
    ("failed", "Failed"),
)
SUBSCRIPTION_CHARGE_METHOD = (
    (1, "Credit Card"),
    (2, "Wallet")
)
BANK_CHOICES = (
    ('bca', "BCA"),
    ('bni', "BNI"),
    ('mandiri', "Mandiri"),
    ('permata', "Permata"),
    ('bri', "BRI")
)
