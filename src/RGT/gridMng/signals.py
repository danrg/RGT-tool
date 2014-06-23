from datetime import date

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from RGT.gridMng.models import Grid, GridDiff, Alternatives, DiffType, Concerns, Ratings


@receiver(post_save, sender=Grid)
def diff_creation_handler(sender, **kwargs):
    if kwargs.get('created'):
        grid = kwargs.get('instance')
        GridDiff.objects.ensure_initial_diff_exists(grid)


@receiver(post_save, sender=Alternatives)
def alternative_save_handler(sender, **kwargs):
    if kwargs.get('created'):
        __update_diff(kwargs.get('instance'), DiffType.ALTERNATIVES, 1)
    else:
        __update_diff(kwargs.get('instance'), DiffType.ALTERNATIVES, 0)


@receiver(post_delete, sender=Alternatives)
def alternative_delete_handler(sender, **kwargs):
    __update_diff(kwargs.get('instance'), DiffType.ALTERNATIVES, -1)


@receiver(post_save, sender=Concerns)
def concern_save_handler(sender, **kwargs):
    if kwargs.get('created'):
        __update_diff(kwargs.get('instance'), DiffType.CONCERNS, 1)
    else:
        __update_diff(kwargs.get('instance'), DiffType.CONCERNS, 0)


@receiver(post_delete, sender=Concerns)
def alternative_delete_handler(sender, **kwargs):
    __update_diff(kwargs.get('instance'), DiffType.CONCERNS, -1)


@receiver(post_save, sender=Ratings)
def ratings_creation_handler(sender, **kwargs):
    __update_diff(kwargs.get('instance').concern, DiffType.RATINGS, 0)


def __update_diff(instance, type, diff_count):
    grid = instance.grid
    user = instance.grid.user
    diff, created = GridDiff.objects.get_or_create(grid=grid, user=user, date=date.today(), type=type)
    if diff_count > 0:
        diff.added += 1
    elif diff_count < 0:
        diff.deleted += 1
    else:
        diff.changed += 1
    diff.save()
