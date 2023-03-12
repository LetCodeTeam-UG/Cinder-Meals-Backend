from enum import Enum

class MealType(Enum):
    BREAKFAST = 'Break Fast'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'
    ANY = 'Any'
    

class OrderStatus(Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    PROCESSING = 'Processing'
    CANCELLED = 'Cancelled'
    ON_THE_WAY = 'On the Way'
    COMPLETED = 'Completed'

class PaymentMethod(Enum):
    CASH = 'Cash'
    # CARD = 'Card'
    # PAYPAL = 'Paypal'
    MOBILE_MONEY = 'Mobile Money'

class PaymentStatus(Enum):
    PENDING = 'Pending'
    SUCCESS = 'Success'
    CANCELLED = 'Cancelled'

