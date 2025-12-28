from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

#capture 

class CapturePaymentView(APIView):
    def post(self, request):
        payment_intent_id = request.data.get("payment_intent_id")

        if not payment_intent_id:
            return Response({"error": "payment_intent_id required"}, status=400)

        stripe.PaymentIntent.capture(payment_intent_id)

        return Response({"status": "captured"}, status=200)
    
#cancel payment view

class CancelPaymentView(APIView):
    def post(self, request):
        payment_intent_id = request.data.get("payment_intent_id")

        stripe.PaymentIntent.cancel(payment_intent_id)

        return Response({"status": "cancelled"}, status=200)


class CheckOutView(APIView):
    def post(self, request):
        amount = request.data.get("amount")

        if amount is None:
            return Response(
                {"amount": "Amount field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            amount = int(amount)
        except ValueError:
            return Response(
                {"amount": "Amount must be an integer (in cents)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount <= 0:
            return Response(
                {"amount": "Amount must be greater than zero"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            capture_method="manual",  # 🔐 ESCROW HOLD
            automatic_payment_methods={"enabled": True},

            metadata={
                "booking_id": request.data.get("booking_id", ""),
                "user_id": request.user.id if request.user.is_authenticated else "",
            },
        )

        return Response(
            {
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id,
                "status": intent.status,
            },
            status=status.HTTP_201_CREATED,
        )
