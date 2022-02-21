from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from .managers import UserManager


AUTH_PROVIDERS = {'facebook': 'facebook', 
                  'google': 'google',  
                  'email': 'email'}

class User(AbstractBaseUser, PermissionsMixin):
    
    ROLE_CHOICES = (
        ('escalator', 'Escalator'),
        ('agent', 'Agent'),
        ('first_responder', 'First Responder'),
        ('admin', "Admin")
    )    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+2341234567890'. Up to 15 digits allowed.")
    
    
    first_name    = models.CharField(_('first name'),max_length = 250)
    last_name     = models.CharField(_('last name'),max_length = 250)
    email         = models.EmailField(_('email'), unique=True)
    gender        = models.CharField(_('gender'),max_length = 250, null=True)
    phone         = models.CharField(_('phone'), max_length = 20, unique = True, validators=[phone_regex])
    address       = models.CharField(_('address'), max_length = 250, null = True)
    local_gov       = models.CharField(_('local government'), max_length = 250, null = True)
    role          = models.CharField(_('role'),max_length = 250, choices=ROLE_CHOICES)
    password      = models.CharField(_('password'), max_length=300)
    is_staff      = models.BooleanField(_('staff'), default=False)
    is_admin      = models.BooleanField(_('admin'), default= False)
    is_active     = models.BooleanField(_('active'), default=True)
    date_joined   = models.DateTimeField(_('date joined'), auto_now_add=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
    
    def delete(self):
        self.is_active = False
        self.save()


