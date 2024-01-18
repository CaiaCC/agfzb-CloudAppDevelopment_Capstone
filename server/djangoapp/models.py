from django.db import models
from django.utils.timezone import now


# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(null=False, max_length=250)

    def __str__(self):
        return f"Name: {self.name}," + \
                f"Description: {self.description}"


# Car model
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon')
    ]
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=20, choices=CAR_TYPES)
    year = models.DateField()

    def __str__(self):
        return f"Name: {self.name}," + \
                f"Dealer ID: {str(self.dealer_id)}," + \
                f"Type: {self.car_type}," + \
                f"Year: {str(self.year.year)}"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
