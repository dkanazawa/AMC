import numpy as np
from django import forms
from .models import Event, Player, Result


class EventForm(forms.ModelForm):
    """イベントフォーム"""

    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = ('event', 'name', )
        widgets = {'event': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ResultForm(forms.Form):

    p1 = forms.ModelChoiceField(label="参加者", queryset=None)
    p2 = forms.ModelChoiceField(label="参加者", queryset=None)
    p3 = forms.ModelChoiceField(label="参加者", queryset=None)
    p4 = forms.ModelChoiceField(label="参加者", queryset=None)
    point_p1 = forms.IntegerField(max_value=100000, min_value=-100000)
    point_p2 = forms.IntegerField(max_value=100000, min_value=-100000)
    point_p3 = forms.IntegerField(max_value=100000, min_value=-100000)
    point_p4 = forms.IntegerField(max_value=100000, min_value=-100000)

    event = None

    def __init__(self, queryset=None, *args, **kwargs):
        self.event = kwargs.pop('event')
        super(ResultForm, self).__init__(*args, **kwargs)
        qs = Player.objects.filter(event=self.event)
        self.fields['p1'].queryset = qs
        self.fields['p2'].queryset = qs
        self.fields['p3'].queryset = qs
        self.fields['p4'].queryset = qs

    def clean(self):
        cleaned_data = super().clean()
        # distinct players check
        if len({cleaned_data[i] for i in ['p1', 'p2', 'p3', 'p4']}) < 4:
            raise forms.ValidationError('Duplicate player')
        # point total check
        diff = sum([cleaned_data[i] for i in ['point_p1', 'point_p2', 'point_p3', 'point_p4']]) - self.event.point_at_start * self.event.players
        if diff != 0:
            raise forms.ValidationError('Sum of points is incorrect.(' + str(diff) + ')')
        return cleaned_data
