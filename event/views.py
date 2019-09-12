import math
from django.shortcuts import redirect, resolve_url
from django.utils import timezone
from django.views import generic
from .models import Event, Player, Result
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
        rank_p1 = 1
        rank_p2 = 2
        rank_p3 = 3
        rank_p4 = 4
        pt_p1 = math.floor(form.cleaned_data['point_p1']/1000)
        pt_p2 = math.floor(form.cleaned_data['point_p2']/1000)
        pt_p3 = math.floor(form.cleaned_data['point_p3']/1000)
        pt_p4 = math.floor(form.cleaned_data['point_p4']/1000)
        pt_uma_p1 = 30
        pt_uma_p2 = 10
        pt_uma_p3 = -10
        pt_uma_p4 = -30
        Result.objects.create(event=self.event,
                              player=form.cleaned_data['p1'],
                              point=form.cleaned_data['point_p1'],
                              rank=rank_p1,
                              pt=pt_p1,
                              pt_uma=pt_uma_p1
                              )
        Result.objects.create(event=self.event,
                              player=form.cleaned_data['p2'],
                              point=form.cleaned_data['point_p2'],
                              rank=rank_p2,
                              pt=pt_p2,
                              pt_uma=pt_uma_p2
                              )
        Result.objects.create(event=self.event,
                              player=form.cleaned_data['p3'],
                              point=form.cleaned_data['point_p3'],
                              rank=rank_p3,
                              pt=pt_p3,
                              pt_uma=pt_uma_p3
                              )
        Result.objects.create(event=self.event,
                              player=form.cleaned_data['p4'],
                              point=form.cleaned_data['point_p4'],
                              rank=rank_p4,
                              pt=pt_p4,
                              pt_uma=pt_uma_p4
                              )
        return redirect('event:event_detail', pk=self.kwargs['pk'])
