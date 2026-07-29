from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'sqft', 'bedrooms', 'bathrooms', 'age_of_house', 'location', 'predicted_price', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('user__username', 'location')