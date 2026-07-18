import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from users.models import Person

logger = logging.getLogger("utcc")


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User login successful: username='{user.username}'")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user:
        logger.info(f"User logout: username='{user.username}'")


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    username = credentials.get("username", "unknown")
    logger.warning(f"User login failed: username='{username}'")


@receiver(post_save, sender=Person)
def log_person_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(
        f"Person {action}: id={instance.id}, name='{instance.name}', student_designator='{instance.student_designator}'"
    )


@receiver(post_delete, sender=Person)
def log_person_delete(sender, instance, **kwargs):
    logger.info(f"Person deleted: id={instance.id}, name='{instance.name}'")
