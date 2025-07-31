from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models.user_profile import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Evita erro se perfil já existir
        if not hasattr(instance, "userprofile"):
            UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
