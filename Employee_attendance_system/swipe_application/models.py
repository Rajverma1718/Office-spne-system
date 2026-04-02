from django.db import models
from django.contrib.auth.models import User

class SwipeApplication(models.Model):
    SWIPE_CATEGORIES = [
        ('miss_punch', 'Miss punch'),
        ('wfh', 'Work from home'),
        ('holiday_work', 'Worked on Sunday and Public Holiday'),
    ]

    INOUT_CHOICES = [
        ('in', 'In'),
        ('out', 'Out'),
        ('both', 'Both'),
    ]

    STATUS = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=SWIPE_CATEGORIES)
    request_date = models.DateField()
    inout_mode = models.CharField(max_length=10, choices=INOUT_CHOICES, blank=True)
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.request_date}"

