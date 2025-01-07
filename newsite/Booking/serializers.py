from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }






class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']



class CountryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']



class CountryDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']




class ReviewListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user_name', 'stars']



class ReviewDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user_name', 'hotel', 'text', 'stars']



class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['hotel_book', 'room_book', 'user_book', 'check_in',
                  'check_out', 'total_price', 'status_book']



class HotelImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel', 'hotel_image']



class RoomImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room', 'room_image', 'room_videos']



class RoomDetailSerializers(serializers.ModelSerializer):
    created_date = serializers.DateTimeField('%Y')
    room_images = RoomImageSerializers(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['room_number', 'hotel_room', 'room_price', 'all_inclusive',
                  'room_description', 'created_date', 'types', 'modality', 'room_images']



class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['number', 'contact_info']




class RatingSerializers(serializers.ModelSerializer):
    user_name = UserProfileSimpleSerializers()
    class Meta:
        model = Rating
        fields = ['user_name', 'hotel', 'staff', 'amenities',
                  'cleanliness', 'free_WiFi', 'value_for_money']



class RoomListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['room_number', 'room_price', 'all_inclusive',  'types', 'modality']



class HotelListSerializers(serializers.ModelSerializer):
    country = CountryListSerializers()
    review_hotel = ReviewListSerializers(many=True, read_only=True)
    hotel_images = HotelImageSerializers(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = ['hotel_name', 'country', 'city', 'address',
                  'country', 'review_hotel', 'hotel_images']






class HotelDetailSerializers(serializers.ModelSerializer):
    date = serializers.DateTimeField(format('%d-%m-%Y  %H:%M'))
    rooms = RoomDetailSerializers(many=True, read_only=True)
    hotel_images = HotelImageSerializers(many=True, read_only=True)
    room_images = RoomImageSerializers(many=True, read_only=True)
    contact = ContactSerializers(many=True, read_only=True)
    review_hotel = ReviewDetailSerializers(many=True, read_only=True)
    country = CountryDetailSerializers()
    avg_staff = serializers.SerializerMethodField()
    avg_free_WiFi = serializers.SerializerMethodField()
    avg_amenities = serializers.SerializerMethodField()
    avg_cleanliness = serializers.SerializerMethodField()
    avg_value_for_money = serializers.SerializerMethodField()


    class Meta:
        model = Hotel
        fields = ['hotel_name', 'owner', 'country', 'city', 'address', 'review_hotel',
                  'hotel_description', 'date', 'rooms', 'rating_hotel', 'hotel_images', 'room_images',
                  'contact', 'avg_staff', 'avg_free_WiFi', 'avg_amenities', 'avg_cleanliness', 'avg_value_for_money']


    def get_avg_staff(self, obj):
        return obj.get_avg_staff()

    def get_avg_free_WiFi(self, obj):
        return obj.get_avg_free_WiFi()

    def get_avg_amenities(self, obj):
        return obj.get_avg_amenities()

    def get_avg_cleanliness(self, obj):
        return obj.get_avg_cleanliness()

    def get_avg_value_for_money(self, obj):
        return obj.get_avg_value_for_money()







