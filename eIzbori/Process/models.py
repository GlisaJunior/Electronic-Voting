from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin  
from django.conf import settings
from django.utils.translation import gettext_lazy as _   
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import UserManager
from django.utils.crypto import get_random_string
from .managers import CustomUserManager

    
class CustomUser(AbstractUser,PermissionsMixin):
    
    username = models.CharField(max_length=150, unique=False, default='')
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=200,unique=True)
    licence = models.CharField(max_length=50)
    objects = CustomUserManager()

    CHOICES = (
    (0, 'Candidacy Phase'),
    (1, 'Voting Phase'),
    (2, 'Election Over')
    ) 

    votestatus = models.IntegerField(choices = CHOICES, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class regional_center(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Regional Centers'
    
class local_center(models.Model):
    name = models.CharField(max_length=40)
    regional_center = models.ForeignKey(regional_center,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Local Centers'

class is_within(models.Model):
    local_center = models.ForeignKey(local_center, on_delete=models.CASCADE)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='is_within')
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = 'Is Within'

class election(models.Model):
    CHOICES = (
        (0, 'Candidacy Phase'),
        (1, 'Voting Phase'),
        (2, 'Election Over')
    )   # this gives us the possible values for the "Phase" field, which will determine which phase we are in, in the election process. This will be important later when checking which phase we are in in several functions, and is a field we will change throughout each step of the election process.
    date = models.DateTimeField()
    name_of_election = models.CharField(max_length=50)
    Phase = models.IntegerField(choices=CHOICES)

class ballot(models.Model):
    # voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="voter") # defines who placed the vote
    votes = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes") # defines who the vote is for
    votetype = models.BooleanField() #determines whether the vote is placed for candidacy (False) or final voting (True) if user does NOT have a vote for current votetype then they can vote.
    election = models.ForeignKey(election, on_delete=models.CASCADE ) #Ballot model got changed to keep track of which election it is tied to instead of keeping track of previous versions of the ballot table.
    
class key_of(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Keys Of'