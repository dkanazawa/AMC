import math
import pandas as pd
import numpy as np
from django.shortcuts import redirect, resolve_url
from django.utils import timezone
from django.views import generic
from .models import Event, Player, Game, Result
from .forms import EventForm, PlayerForm, ResultForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden


class EventNew(generic.CreateView):
    model = Event
    template_name = 'event/event_new.html'
    form_class = EventForm

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        return redirect('event:event_detail', pk=event.pk)


class EventDetail(generic.DetailView):
    model = Event
    template_name = 'event/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        try:
            player = Player.objects.filter(event=self.kwargs['pk'])
            context['player_list'] = player
        except Player.DoesNotExist:
            context['player_list'] = None
        return context


class PlayerNew(generic.CreateView):
    model = Player
    template_name = 'event/player_new.html'
    form_class = PlayerForm
    event = None

    def get_initial(self):
        self.event = Event.objects.get(pk=self.kwargs['pk'])
        return {'event': self.event}

    def form_valid(self, form):
        player = form.save(commit=False)
        player.save()
        return redirect('event:event_detail', pk=self.kwargs['pk'])


class ResultNew(generic.FormView):
    template_name = 'event/result_new.html'
    form_class = ResultForm
    event = None

    def get_form_kwargs(self):
        kwargs = super(ResultNew, self).get_form_kwargs()
        self.event = Event.objects.get(pk=self.kwargs['pk'])
        kwargs['event'] = self.event
        return kwargs

    def form_valid(self, form):
        df = pd.DataFrame({'player': [form.cleaned_data['p1'],
                                      form.cleaned_data['p2'],
                                      form.cleaned_data['p3'],
                                      form.cleaned_data['p4']],
                           'point': [form.cleaned_data['point_p1'],
                                     form.cleaned_data['point_p2'],
                                     form.cleaned_data['point_p3'],
                                     form.cleaned_data['point_p4']]
                            })
        df = df.reset_index().sort_values(by=["point", "index"], ascending=[False, True])
        df = df.assign(rank=[1,2,3,4],
                       pt=np.floor(df["point"]/1000)-30,
                       pt_uma=[30,10,-10,-30])
        game = Game.objects.create(event=self.event, uma_pattern=1)
        for index, item in df.iterrows():
            Result.objects.create(game=game,
                                  player=item['player'],
                                  point=item['point'],
                                  rank=item['rank'],
                                  pt=item['pt'],
                                  pt_uma=item['pt_uma']
                                  )
        return redirect('event:event_detail', pk=self.kwargs['pk'])
