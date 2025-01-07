from .models import Country, Hotel, Room, Rating
from modeltranslation.translator import TranslationOptions,register

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('city', 'address', 'hotel_description')


@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = ('room_description',)


