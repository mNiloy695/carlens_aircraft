from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe
from rest_framework.permissions import IsAuthenticated
from .serializers import BookedModelSerializer
stripe.api_key = settings.STRIPE_SECRET_KEY
from .models import BookedModel
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


class BookedModelView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        booked_request=BookedModel.objects.all()
        if not request.user.is_staff:
            booked_request=booked_request.filter(user=request.user)
        serializer=BookedModelSerializer(booked_request,many=True)
        return Response(serializer.data)





class CheckOutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        data=request.data
        amount = data.get("amount",None)
        operator_id=data.get('operator_id',None)
        aircraft_id=data.get('aircraft_id',None)
        flight_date=data.get('flight_date',None)
        passengers=data.get('passengers',None)
        form=data.get('form',None)
        to=data.get('to',None)
        currency=data.get('currency',None)
        booking_id=data.get('booking_id',None)

        if booking_id is None:
            return Response(
                {"booking_id": "Booking id field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


        if amount is None:
            return Response(
                {"amount": "Amount field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if operator_id is None:
            return Response(
                {"operator_id": "Operator id field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if aircraft_id is None:
             return Response(
                {"aircraft_id": "Aircraft id field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if flight_date is None:
             return Response(
                {"flight_date": "Flight date field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if passengers is None:
             return Response(
                {"passengers": "Passengers field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if form is None:
             return Response(
                {"form": "Form field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if to is None:
             return Response(
                {"to": "To field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if currency is None:
             return Response(
                {"currency": "Currency field is required"},
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
            currency=currency,
            capture_method="manual",  # 🔐 ESCROW HOLD
            automatic_payment_methods={"enabled": True},

            metadata={
                "booking_id": request.data.get("booking_id", ""),
                "user_id": request.user.id if request.user.is_authenticated else "",
                "amount":amount,
                "operator_id":operator_id,
                "aircraft_id":aircraft_id,
                "form":form,
                "to":to,
                "passengers":passengers,
                "amount":amount,
                "currency":currency,
                "flight_date":flight_date

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
