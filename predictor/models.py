from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sqft = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    age_of_house = models.IntegerField()
    location = models.CharField(max_length=100)
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.predicted_price}"