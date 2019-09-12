from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class Event(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='イベント名', max_length=50, blank=True, null=True)
    start_date = models.DateField(verbose_name='開催日')  # カレンダー用
    players = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    point_at_start = models.PositiveSmallIntegerField()
    rounding_method = models.PositiveSmallIntegerField()
    uma_method = models.PositiveSmallIntegerField()


class Player(models.Model):

    event = models.ForeignKey('Event', on_delete=models.CASCADE)  # イベントのID
    name = models.CharField(max_length=20)

    class Meta:
        # unique_together = ('event', 'participant')  # depreciated
        constraints = [
            models.UniqueConstraint(fields=['event', 'name'], name='player name of constraint')
        ]

    def __str__(self):
        return self.name


class Game(models.Model):

    event = models.ForeignKey('Event', on_delete=models.CASCADE)  # イベントのID
    uma_pattern = models.SmallIntegerField()


class Result(models.Model):

    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    point = models.SmallIntegerField()
    rank = models.PositiveSmallIntegerField()
    pt = models.SmallIntegerField()
    pt_uma = models.SmallIntegerField()
