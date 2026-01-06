from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import stripe
from .views import CancelPaymentView
stripe.api_key = settings.STRIPE_SECRET_KEY
from .models import BookedModel
from django.contrib.auth import get_user_model
User=get_user_model()

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    if not sig_header:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.WEBHOOK_SECRET,
        )
    except Exception:
        return HttpResponse(status=400)

    event_type = event["type"]
   
    payment_intent = event["data"]["object"]
    metadata = payment_intent.get("metadata", {})
    booking_id=metadata.get("booking_id")
    operator_id=metadata.get("operator_id")
    amount=metadata.get('amount')
    passengers=metadata.get('passengers')
    currency=metadata.get('currency')
    flight_date=metadata.get('flight_date')
    aircraft_id=metadata.get('aircraft_id')
    form=metadata.get('form')
    to=metadata.get('to')
    user_id=metadata.get('user_id')

    try:
        
        user=User.objects.get(id=user_id)

    except User.DoesNotExist:

        raise ValueError("Invalid user id")
    



    if event_type=="payment_intent.created":

        id=payment_intent["id"]
        print(passengers)
        BookedModel.objects.create(
            user=user,
            payment_id=id,
            passengers=int(passengers),
            booking_id=booking_id,
            operator_id=operator_id,
            amount=int(amount),
            currency=currency,
            flight_date=flight_date,
            aircraft_id=aircraft_id,
            form=form,
            to=to

        )
        
        print("payment intent created")

    if event_type == "payment_intent.amount_capturable_updated":
        # ✅ FUNDS HELD (ESCROW)
        print("🔐 Funds held:", payment_intent["id"])
        # Save status = HELD in DB

    elif event_type == "payment_intent.succeeded":
        # ✅ FUNDS CAPTURED
        print("💰 Funds captured:", payment_intent["id"])
        # Save status = PAID

    elif event_type == "payment_intent.payment_failed":
        print("❌ Payment failed:", payment_intent["id"])
        # Save status = FAILED
    elif event_type=="payment_intent.cancelled":
        print(" i  am canceld")

    return HttpResponse(status=200)

