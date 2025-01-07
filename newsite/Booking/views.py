from django.views.defaults import permission_denied
from rest_framework import viewsets, generics, permissions,status
from .serializers import *
from .models import *
from .permissions import CheckStatus
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)





class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializers


class CountryDetailAPIView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializers



class HotelListAPIView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['country', 'city']
    search_filter = ['hotel_name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class HotelDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializers
    permission_classes = [CheckStatus]


class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializers



class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializers



class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializers



class ReviewDetailAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializers


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializers



class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers
