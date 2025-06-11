from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import RideSerializer
from django.db import transaction
from rest_framework import status
from .models import Ride

class BookRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(rider=request.user)
            return Response({'message': 'Ride booked successfully', 'ride': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AvailableRidesView(ListAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != 'driver':
            return Ride.objects.none()
        return Ride.objects.filter(status='pending')



class AcceptRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        user = request.user

        if user.role != 'driver':
            return Response({"detail": "Only drivers can accept rides."}, status=status.HTTP_403_FORBIDDEN)

        try:
            with transaction.atomic():
                ride = Ride.objects.select_for_update().get(id=ride_id)

                if ride.status != 'pending':
                    return Response({"detail": "Ride already accepted."}, status=status.HTTP_400_BAD_REQUEST)

                ride.driver = user
                ride.status = 'accepted'
                ride.save()

        except Ride.DoesNotExist:
            return Response({"detail": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Ride accepted successfully."}, status=status.HTTP_200_OK)



class UserRideHistoryView(ListAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Ride.objects.filter(rider=user).order_by('-created_at')
