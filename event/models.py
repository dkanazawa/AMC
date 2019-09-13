from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class Event(models.Model):

    ROUNDING = (
        (1, "Truncate"),
        (2, "4/5"),
        (3, "5/6"),
    )
    UMA = (
        ("A1", "A1"),
        ("A2", "A2"),
        ("A3", "A3"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("B3", "B3"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='イベント名', max_length=50, blank=True, null=True)
    start_date = models.DateField(verbose_name='開催日')  # カレンダー用
    players = models.PositiveSmallIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(4)])
    point_at_start = models.PositiveSmallIntegerField(default=25000, validators=[MinValueValidator(20000), MaxValueValidator(30000)])
    rounding_method = models.PositiveSmallIntegerField(default=4, choices=ROUNDING)
    uma_method = models.CharField(max_length=2, default='B1', choices=UMA)


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
    point = models.SmallIntegerField(validators=[MinValueValidator(-200000), MaxValueValidator(200000)])
    rank = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    pt = models.SmallIntegerField(validators=[MinValueValidator(-200), MaxValueValidator(200)])
    pt_uma = models.SmallIntegerField()
