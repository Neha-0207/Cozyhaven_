from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .models import Hotel, Room, Booking
from .serializers import BookingSerializer, HotelSerializer, RoomSerializer
from rest_framework.permissions import IsAuthenticated


def calculate_total_fare(check_in_date, check_out_date, base_fare):
    nights = (check_out_date - check_in_date).days
    total_fare = nights * base_fare
    return total_fare


class UserRegistration(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class HotelListAPIView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer

    def get_queryset(self):
        city = self.request.query_params.get('city', '')
        min_price = self.request.query_params.get('minPrice')
        max_price = self.request.query_params.get('maxPrice')

        queryset = Hotel.objects.filter(city__icontains=city)

        if min_price is not None:
            queryset = queryset.filter(cheapestPrice__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(cheapestPrice__lte=max_price)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HotelDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


from .serializers import RoomSerializer, BookingSerializer


class RoomListAPIView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        queryset = Room.objects.filter(hotel_id=hotel_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking_list(request):
    if request.method == 'GET':
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            # Set the user for the booking to the authenticated user
            serializer.validated_data['user'] = request.user

            # Save the booking
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user != request.user:
        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            # Set the user for the booking to the authenticated user
            serializer.validated_data['user'] = request.user
            check_in_date = serializer.validated_data.get('check_in_date')
            check_out_date = serializer.validated_data.get('check_out_date')
            room = serializer.validated_data.get('room')
            existing_bookings = Booking.objects.filter(
                room=room,
                check_in_date__lte=check_out_date,
                check_out_date__gte=check_in_date
            ).exclude(id=booking_id)  # Exclude the current booking from the check
            if existing_bookings.exists():
                return Response({"detail": "The selected room is not available for the chosen dates."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Calculate and include the total fare in the serializer data
            total_fare = calculate_total_fare(check_in_date, check_out_date, room.baseFare)
            serializer.validated_data['total_fare'] = total_fare

            # Save the updated booking
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# views.py
from django.http import JsonResponse
from django.contrib.auth.models import User


def user_detail(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Add more user details as needed
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Room
from .serializers import RoomSerializer


class RoomDetailView(APIView):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found'}, status=404)
