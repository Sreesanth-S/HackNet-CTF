from django.db import models
from django.utils import timezone

class CTFUser(models.Model):
    """Model to store CTF user sessions and attempts."""
    session_key = models.CharField(max_length=40, unique=True)
    username = models.CharField(max_length=100)
    is_authenticated = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.session_key[:8]}...)"

class FlagSubmission(models.Model):
    """Model to store flag submission attempts."""
    ctf_user = models.ForeignKey(CTFUser, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40)
    submitted_flag = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"Flag: {self.submitted_flag} - {'✓' if self.is_correct else '✗'}"
    
    class Meta:
        ordering = ['-submitted_at']

class Challenge(models.Model):
    """Model to store challenge information."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    correct_flag = models.CharField(max_length=200)
    points = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name