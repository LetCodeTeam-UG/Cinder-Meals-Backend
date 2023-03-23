from enum import Enum

currency = '₵ '

class MealType(Enum):
    ANY = 'Any'
    BREAKFAST = 'Break Fast'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'
    BEVERAGES = 'Beverages'
    

class OrderStatus(Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    PROCESSING = 'Processing'
    CANCELLED = 'Cancelled'
    ON_THE_WAY = 'On the Way'
    COMPLETED = 'Completed'
    ASSIGNED = 'Assigned'
    DELIVERED = 'Delivered'

class PaymentMethod(Enum):
    CASH = 'Cash'
    # CARD = 'Card'
    # PAYPAL = 'Paypal'
    MOBILE_MONEY = 'Mobile Money'

class PaymentStatus(Enum):
    PENDING = 'Pending'
    SUCCESS = 'Success'
    CANCELLED = 'Cancelled'

