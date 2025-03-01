from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from ..models import Car


@receiver(post_save, sender=Car)
def send_email_on_new_car(sender, instance, created, **kwargs):
    if created:
        subject = "New Car Added 🚙"
        message = f"A new car '{instance.name}' has been added to the collection!"

        recipient_list = [user.email for user in User.objects.filter(is_active=True) if user.email]

        if recipient_list:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list
            )
