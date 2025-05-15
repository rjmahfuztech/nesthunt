from django.db import models
from advertisement.models import Advertisement
from users.models import User
from uuid import uuid4

class RentRequest(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')    
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='rent_request')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_request')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"`{self.user.first_name}` request for rent {self.advertisement.title}"


class Favourite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='favourite')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourite')

    def __str__(self):
        return f"`{self.user.first_name}` Save as Favourite {self.advertisement.title}"
    

class Order(models.Model):
    NOT_PAID = 'Not Paid'
    BOOKED = 'Booked'
    CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (NOT_PAID, 'Not Paid'),
        (BOOKED, 'Booked'),
        (CANCELLED, 'Cancelled')
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=NOT_PAID)
    full_name = models.CharField(max_length=250)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    payment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}'s order for {self.advertisement.title}"