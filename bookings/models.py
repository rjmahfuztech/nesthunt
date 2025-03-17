from django.db import models
from advertisement.models import Advertisement
from users.models import User

class RentRequest(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')    
    ]
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='rent_request')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_request')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"`{self.user.first_name}` request for rent {self.advertisement.title}"


class Favourite(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='favourite')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourite')

    def __str__(self):
        return f"`{self.user.first_name}` Save as Favourite {self.advertisement.title}"

