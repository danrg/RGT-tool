from django.db.models.signals import post_save
from django.dispatch import receiver
from RGT.gridMng.models import Grid, GridDiff, DiffType


@receiver(post_save, sender=Grid)
def diff_creation_handler(sender, **kwargs):
    if kwargs.get('created'):
        grid = kwargs.get('instance')
        GridDiff.objects.ensure_initial_diff_exists(grid)