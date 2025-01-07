from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
     age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(90)],
                                            null=True, blank=True,)
     phonenumbers = PhoneNumberField(null=True, blank=True)
     STATUS_CHOICES = (
        ('simple', 'simple'),
        ('owner', 'owner'),
     )
     status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='simple')

     def __str__(self):
        return f'{self.first_name}, {self.last_name}'




class Country(models.Model):
     country_name = models.CharField(max_length=32, unique=True)
     def __str__(self):
         return f'{self.country_name}'


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=90)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owner_profile')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_hotel')
    city = models.CharField(max_length=32)
    address = models.TextField()
    hotel_description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel_name}, {self.country}, {self.city}'


    def get_avg_staff(self):
        rating = self.rating_hotel.all()
        if rating.exists():
            return round(sum([i.staff for i in rating]) / rating.count(), 1)
        return 0

    def get_avg_free_WiFi(self):
        rating = self.rating_hotel.all()
        if rating.exists():
            return round(sum([i.staff for i in rating]) / rating.count(), 1)
        return 0

    def get_avg_amenities(self):
        rating = self.rating_hotel.all()
        if rating.exists():
            return round(sum([i.staff for i in rating]) / rating.count(), 1)
        return 0

    def get_avg_cleanliness(self):
        rating = self.rating_hotel.all()
        if rating.exists():
            return round(sum([i.staff for i in rating]) / rating.count(), 1)
        return 0

    def get_avg_value_for_money(self):
        rating = self.rating_hotel.all()
        if rating.exists():
            return round(sum([i.staff for i in rating]) / rating.count(), 1)
        return 0


class Contact(models.Model):
    number = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='contact')
    contact_info = PhoneNumberField()

    def __str__(self):
        return f'{self.contact_info}'



class HotelImage(models.Model):
     hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
     hotel_image = models.ImageField(upload_to='hotel_image/', null=True, blank=True)

     def __str__(self):
        return f'{self.hotel_image}'



class Room(models.Model):
     hotel_room = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
     room_number = models.PositiveSmallIntegerField()
     room_price = models.PositiveSmallIntegerField()
     all_inclusive = models.BooleanField(default=False)
     room_description = models.TextField()
     created_date = models.DateTimeField(auto_now_add=True)
     TYPE_CHOICES = (
            ('люкс', 'люкс'),
            ('семейный', 'семейный'),
            ('одноместный', 'одноместный'),
            ('двувхместный', 'двухместный')
     )
     types = models.CharField(max_length=32, choices=TYPE_CHOICES)
     ROOM_CHOICES = (
            ('свободно', 'свободно'),
            ('забронировано', 'забронировано'),
            ('занято', 'занято')
     )
     modality = models.CharField(max_length=32, choices=ROOM_CHOICES, default='свободно')

     def __str__(self):
        return f'{self.hotel_room}, {self.room_number}, {self.modality}'



class RoomImage(models.Model):
     room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_images')
     room_image = models.ImageField(upload_to='room_image/', null=True, blank=True)
     room_videos = models.FileField(upload_to='room_videos/', null=True, blank=True)

     def __str__(self):
        return f'{self.room}'



class Review (models.Model):
     user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_names')
     hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='review_hotel')
     text =models.TextField(null=True,blank=True)
     stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)

     def __str__(self):
        return f'{self.user_name},{self.hotel},{self.stars}'




class Booking(models.Model):
     hotel_book = models.ForeignKey(Hotel,on_delete=models.CASCADE)
     room_book = models.ForeignKey(Room,on_delete=models.CASCADE)
     user_book = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
     check_in = models.DateTimeField(auto_now_add=True)
     check_out = models.DateTimeField(auto_now_add=True)
     total_price = models.PositiveSmallIntegerField(default=0)
     BOOKING_CHOICES = (
       ('отменено ', 'отменено'),
       ('подтверждено', 'подтверждено '),

     )
     status_book = models.CharField(max_length=32, choices=BOOKING_CHOICES)

     def __str__(self):
        return  f'{self.user_book},{self.hotel_book},{self.room_book},{self.status_book}'



class Rating(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rating_hotel')
    staff = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)
    amenities = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)
    cleanliness = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)
    free_WiFi = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)
    value_for_money = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)

    def __str__(self):
        return (f' {self.hotel},{self.staff}, {self.amenities}, '
                f'{self.cleanliness}, {self.value_for_money}, {self.free_WiFi}')


