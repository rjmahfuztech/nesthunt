from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Advertisement(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')    
    ]
    title = models.CharField(max_length=300)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='advertisements')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    rental_amount = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=500)
    bedroom = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    bathroom = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    apartment_size = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_rented = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('advertisement_image')


class Review(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by `{self.user.first_name}` on `{self.advertisement.title}`"