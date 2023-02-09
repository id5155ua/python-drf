from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
import uuid
import smtplib
import os

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-id']

    email            = models.EmailField(_('email address'), unique=True)
    is_staff         = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    date_joined      = models.DateTimeField(default=timezone.now)
    is_verified      = models.BooleanField(default=False)
    verification_key = models.UUIDField(default=uuid.uuid4, editable=False)
    username         = models.CharField(max_length=30, unique=True, blank=True, null=True)
    phone_number     = models.CharField(verbose_name="phone", max_length=15, blank=True, null=True, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_auth_token(self):
        token = Token.objects.create()
        return token.key

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def send_verification_email(self):
        smtp = smtplib.SMTP('smtp.gmail.com')
        smtp.connect('smtp.gmail.com','587')
        smtp.ehlo()
        smtp.starttls()
        email = os.environ.get("EMAIL_HOST_USER")
        password = os.environ.get("EMAIL_HOST_PASSWORD")
        smtp.login(email, password)
        subject = 'Verify your email address'
        key = uuid.uuid4()
        self.verification_key = key
        self.save()
        message = 'Follow this link to verify your email address: ' + os.environ.get("APPLICATION_URL") + 'verify/' + str(key)
        from_email = os.environ.get("DEFAULT_FROM_EMAIL")
        recipient_list = [self.email]
        send_mail(subject, message, from_email, recipient_list)
        smtp.quit()