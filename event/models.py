from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, BaseValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import uuid


class IntegerUnitValidator(BaseValidator):
    message = _('Ensure this value is not in the units of %(limit_value).')
    code = 'unit_value'

    def compare(self, a, b):
        return a % b != 0


class Event(models.Model):

    PLAYERS = (
        (3, "三人麻雀"),
        (4, "四人麻雀"),
    )
    ROUNDING = (
        (1, "Truncate"),
        (2, "4/5"),
        (3, "5/6"),
    )
    UMA = (
        ("A1", "5-10"),
        ("A2", "10-20"),
        ("A3", "10-30"),
        ("B1", "マルA式"),
        ("B2", "B2"),
        ("B3", "B3"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='イベント名', max_length=50, blank=True, null=True, help_text='※入力任意')
    start_date = models.DateField(verbose_name='開催日')  # カレンダー用
    players = models.PositiveSmallIntegerField(default=4, choices=PLAYERS)
    point_at_start = models.PositiveSmallIntegerField(verbose_name='配給原点', default=25000, validators=[MinValueValidator(20000), MaxValueValidator(30000)])
    rounding_method = models.PositiveSmallIntegerField(verbose_name='端数処理', default=4, choices=ROUNDING)
    uma_method = models.CharField(verbose_name='ウマ計算方法', max_length=2, default='B1', choices=UMA)


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
    point = models.SmallIntegerField(validators=[MinValueValidator(-200000), MaxValueValidator(200000), IntegerUnitValidator(100)])
    rank = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    pt = models.SmallIntegerField(validators=[MinValueValidator(-200), MaxValueValidator(200)])
    pt_uma = models.SmallIntegerField()

