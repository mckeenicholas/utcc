import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from results.models import Competition, CompetitionSession, Result

logger = logging.getLogger("utcc")


@receiver(post_save, sender=CompetitionSession)
def log_session_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(f"Academic Session {action}: id={instance.id}, name='{instance.name}'")


@receiver(post_delete, sender=CompetitionSession)
def log_session_delete(sender, instance, **kwargs):
    logger.info(f"Academic Session deleted: id={instance.id}, name='{instance.name}'")


@receiver(post_save, sender=Competition)
def log_competition_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(
        f"Competition {action}: id={instance.id}, name='{instance.name}', date={instance.date}, student_designator='{instance.student_designator}'"
    )


@receiver(post_delete, sender=Competition)
def log_competition_delete(sender, instance, **kwargs):
    logger.info(f"Competition deleted: id={instance.id}, name='{instance.name}'")


@receiver(post_save, sender=Result)
def log_result_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(
        f"Result {action}: id={instance.id}, person_id={instance.person_id}, "
        f"competition_id={instance.competition_id}, event='{instance.event}', "
        f"round='{instance.round}', single={instance.single}, average={instance.average}"
    )


@receiver(post_delete, sender=Result)
def log_result_delete(sender, instance, **kwargs):
    logger.info(
        f"Result deleted: id={instance.id}, person_id={instance.person_id}, "
        f"competition_id={instance.competition_id}, event='{instance.event}', round='{instance.round}'"
    )
