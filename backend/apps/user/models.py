from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    
    # Role definition
    class Role(models.TextChoices):
        FARMER = "FARMER", "Farmer" # 'FARMER' stored in db while 'Farmer' for django admin/panel
        BUYER = "BUYER", "Buyer"
    
    # Enforce role-based classification
    role = models.CharField(
        max_length=10,
        choices=Role.choices, # Picks between the two choices offered in the Roles class
        default=Role.BUYER, # Defaults to Buyer (Safe to have it even if we won't need it)
        help_text="Role of the user on the platform.",)
    
    phone_number = models.CharField(
        max_length=15,
        null=True, blank=True,
        verbose_name='Phone Number')

    # email field is unique
    email = models.EmailField(
        unique=True,
        null=False, blank=False, # cannot be empty
        error_messages={'unique': "A user with that email already exists."})
    
    # Ease the process late on when working on views and serializers (instead of verbose logical lookups)
    @property
    def is_farmer(self) -> bool:
        return self.role == self.Role.FARMER

    @property
    def is_buyer(self) -> bool:
        return self.role == self.Role.BUYER

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})" # For shell/panel