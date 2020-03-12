import numpy as np
from django import forms
from .models import Event, Player, Result


class EventForm(forms.ModelForm):
    """イベントフォーム"""

    start_date = forms.DateTimeField(label='開催日時',
                                     widget=forms.DateTimeInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = Event
        fields = '__all__'
        widget = {
            'start_date': forms.DateTimeInput(attrs={'autocomplete': 'off'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['players'].disabled = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_point_at_start(self):
        point_at_start = self.cleaned_data['point_at_start']
        if point_at_start % 1000 != 0:
            raise forms.ValidationError('配給原点は1000点単位で入力してください。')
        return point_at_start


class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = ('event', 'name', )
        widgets = {'event': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PlayerEditForm(PlayerForm):

    class Meta(PlayerForm.Meta):
        exclude = ('event', )


class ResultForm(forms.Form):

    p1 = forms.ModelChoiceField(label="参加者", queryset=None)
    p2 = forms.ModelChoiceField(label="参加者", queryset=None)
    p3 = forms.ModelChoiceField(label="参加者", queryset=None)
    p4 = forms.ModelChoiceField(label="参加者", queryset=None)
    point_p1 = forms.IntegerField(max_value=100000, min_value=-100000)
    point_p2 = forms.IntegerField(max_value=100000, min_value=-100000)
    point_p3 = forms.IntegerField(max_value=100000, min_value=-100000)
    point_p4 = forms.IntegerField(max_value=100000, min_value=-100000)
    pt_ex_p1 = forms.IntegerField(max_value=100, min_value=-100)
    pt_ex_p2 = forms.IntegerField(max_value=100, min_value=-100)
    pt_ex_p3 = forms.IntegerField(max_value=100, min_value=-100)
    pt_ex_p4 = forms.IntegerField(max_value=100, min_value=-100)

    event = None

    def __init__(self, queryset=None, *args, **kwargs):
        self.event = kwargs.pop('event')
        super(ResultForm, self).__init__(*args, **kwargs)
        qs = Player.objects.filter(event=self.event)
        self.fields['p1'].queryset = qs
        self.fields['p2'].queryset = qs
        self.fields['p3'].queryset = qs
        self.fields['p4'].queryset = qs

    def clean_point_p1(self):
        point_p1 = self.cleaned_data['point_p1']
        if point_p1 % 100 != 0:
            raise forms.ValidationError('点数は100点単位で入力してください。')
        return point_p1

    def clean_point_p2(self):
        point_p2 = self.cleaned_data['point_p2']
        if point_p2 % 100 != 0:
            raise forms.ValidationError('点数は100点単位で入力してください。')
        return point_p2

    def clean_point_p3(self):
        point_p3 = self.cleaned_data['point_p3']
        if point_p3 % 100 != 0:
            raise forms.ValidationError('点数は100点単位で入力してください。')
        return point_p3

    def clean_point_p4(self):
        point_p4 = self.cleaned_data['point_p4']
        if point_p4 % 100 != 0:
            raise forms.ValidationError('点数は100点単位で入力してください。')
        return point_p4

    def clean(self):
        cleaned_data = super().clean()
        # distinct players check
        if len({cleaned_data[i] for i in ['p1', 'p2', 'p3', 'p4']}) < 4:
            raise forms.ValidationError('Duplicate player')
        # point total check
        diff = sum([cleaned_data[i] for i in ['point_p1', 'point_p2', 'point_p3', 'point_p4']]) - self.event.point_at_start * self.event.players
        if diff != 0:
            raise forms.ValidationError('Sum of points is incorrect.(' + str(diff) + ')')
        # ex-point total check
        diff = sum([cleaned_data[i] for i in ['pt_ex_p1', 'pt_ex_p2', 'pt_ex_p3', 'pt_ex_p4']])
        if diff != 0:
            raise forms.ValidationError('Sum of ex-points is incorrect.(' + str(diff) + ')')
        return cleaned_data
