from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


# Create your models here.
class Address(models.Model):
    """
    Store a single adress

    :param int number: address number
    :param str street: street name
    :param str city: city name
    :param str state: state abbreviations
    :param int zip_code: 5 number zip code
    :param str country_iso_code: 3 letters iso code
    """

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    def __str__(self):
        return f'{self.number} {self.street}'

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Letting(models.Model):
    """
    Model to store a letting adress

    :param str title: title of the letting
    :param address: address linked to the letting model
    :type address: :class:`lettings.Address`
    """
    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Letting"
        verbose_name_plural = "Lettings"
