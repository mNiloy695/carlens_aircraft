from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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
    if event_type=="payment_intent.created":
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
    elif event_type=="payment_intent.canceled":
        print(" i  am canceld")

    return HttpResponse(status=200)

