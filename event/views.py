import csv
import pandas as pd
import numpy as np
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, resolve_url, render
from django.utils import timezone
from django.views import generic
from .models import Event, Player, Game, Result
from .forms import EventForm, PlayerForm, PlayerEditForm, ResultForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden


def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def post_index(request):
    post_list = Result.objects.all()
    page_obj = paginate_queryset(request, post_list, 1)
    context = {
        'post_list': page_obj.object_list,
        'page_obj': page_obj,
    }
    return render(request, 'app/post_list.html', context)


class EventNew(generic.CreateView):
    model = Event
    template_name = 'event/event_new.html'
    form_class = EventForm

    def form_valid(self, form):
        event = form.save(commit=False)
        # default event name
        if event.title is None:
            event.title = str(event.start_date) + "の麻雀大会"
        event.save()
        return redirect('event:event_detail', pk=event.pk)


class EventDetail(generic.DetailView):
    model = Event
    template_name = 'event/event_detail.html'
    result_df = None

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        try:
            player = Player.objects.filter(event=self.kwargs['pk'])
            context['player_list'] = player
        except Player.DoesNotExist:
            context['player_list'] = None
        # Result Summary
        df = pd.DataFrame.from_records(Result.objects.filter(game__event=self.kwargs['pk']).values('pt', 'pt_uma', 'game', 'player__name'))
        if not df.empty:
            self.result_df = pd.pivot_table(df, values=["pt", "pt_uma"], index="game", columns="player__name", aggfunc="sum")  # .reorder_levels([1, 0], axis=1)
            self.result_df = pd.concat([self.result_df.xs('pt', level=0, axis=1).assign(pt_type='normal'),
                                        self.result_df.xs('pt_uma', level=0, axis=1).assign(pt_type='uma')])
            result_summary = self.result_df.drop('pt_type', axis=1).applymap(lambda x: str(int(x)) if not np.isnan(x) else 'nan').groupby(level=0).agg(lambda x: '（'.join(x) + '）')
            # Result Total
            result_total = self.result_df.groupby(by=['pt_type']).sum()
            result_total = result_total.T
            result_total['total'] = result_total['normal'] + result_total['uma']
            result_total = result_total.T
        else:
            result_summary = pd.DataFrame(index=[], columns=[])
            result_total = pd.DataFrame(index=[], columns=[])
        context['result_summary'] = result_summary
        context['result_total'] = result_total
        return context


class PlayerNew(generic.CreateView):
    model = Player
    template_name = 'event/player_new.html'
    form_class = PlayerForm
    event = None

    def get_initial(self):
        self.event = Event.objects.get(pk=self.kwargs['pk'])
        return {'event': self.event}

    def get_context_data(self, **kwargs):
        context = super(PlayerNew, self).get_context_data(**kwargs)
        context['event'] = self.event
        return context

    def form_valid(self, form):
        player = form.save(commit=False)
        player.save()
        return redirect('event:event_detail', pk=self.kwargs['pk'])


class PlayerEdit(generic.UpdateView):
    model = Player
    template_name = 'event/player_edit.html'
    form_class = PlayerEditForm

    def get_context_data(self, **kwargs):
        context = super(PlayerEdit, self).get_context_data(**kwargs)
        context['event_pk'] = self.kwargs['event_pk']
        return context

    def form_valid(self, form):
        player = form.save(commit=False)
        player.save()
        return redirect('event:event_detail', pk=self.kwargs['event_pk'])


class ResultNew(generic.FormView):
    template_name = 'event/result_new.html'
    form_class = ResultForm
    event = None

    def get_form_kwargs(self):
        kwargs = super(ResultNew, self).get_form_kwargs()
        self.event = Event.objects.get(pk=self.kwargs['pk'])
        kwargs['event'] = self.event
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ResultNew, self).get_context_data(**kwargs)
        context['event'] = self.event
        return context

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
        # column名indexに入っているのは最初の席順（起家=0）
        df = df.reset_index().sort_values(by=["point", "index"], ascending=[False, True])
        # uma
        uki_n = df.query("point >= 30000").shape[0]
        if self.event.uma_method in ['B1', 'B2', 'B3', 'B4']:
            uma_pattern = uki_n
            if uki_n == 1:
                pt_uma = [6, -1, -2, -3]
            elif uki_n == 2:
                pt_uma = [2, 1, -1, -2]
            elif uki_n == 3:
                pt_uma = [3, 2, 1, -6]
            pt_uma = [i * 5 for i in pt_uma]
        else:
            uma_pattern = 0
            if self.event.uma_method == 'A1':
                pt_uma = [10, 5, -5, 10]
            elif self.event.uma_method == 'A2':
                pt_uma = [20, 10, -10, 20]
            elif self.event.uma_method == 'A3':
                pt_uma = [30, 10, -10, 30]

        # game create
        game = Game.objects.create(event=self.event, uma_pattern=uma_pattern)

        # round
        if self.event.rounding_method == 1:     # Truncate
            pt_round_func = (lambda x: np.trunc(x / 1000 - 30))
        elif self.event.rounding_method == 2:     # 4/5
            pt_round_func = (lambda x: np.floor((x + 500) / 1000) - 30)
        elif self.event.rounding_method == 3:     # 5/6
            pt_round_func = (lambda x: np.floor((x + 400) / 1000) - 30)

        df = df.assign(rank=[1, 2, 3, 4], pt=pt_round_func(df["point"]), pt_uma=pt_uma)
        # Top pt recalc
        df = df.reset_index(drop=True)
        df.loc[0, 'pt'] = -sum(df.loc[1:3, 'pt'])
        for index, item in df.iterrows():
            Result.objects.create(game=game,
                                  player=item['player'],
                                  point=item['point'],
                                  rank=item['rank'],
                                  pt=item['pt'],
                                  pt_uma=item['pt_uma']
                                  )
        return redirect('event:event_detail', pk=self.kwargs['pk'])


class GameDelete(generic.DeleteView):
    model = Game
    template_name = 'event/game_delete_confirm.html'

    def get_success_url(self):
        return resolve_url('event:event_detail', pk=self.kwargs['event_pk'])


def result_export(request, pk):
    response = HttpResponse(content_type='text/csv', charset='cp932')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    # Result Summary
    df = pd.DataFrame.from_records(
        Result.objects.filter(game__event=pk).values('pt', 'pt_uma', 'game', 'player__name'))
    if not df.empty:
        result_df = pd.pivot_table(df, values=["pt", "pt_uma"], index="game", columns="player__name",
                                        aggfunc="sum")  # .reorder_levels([1, 0], axis=1)
        result_df.reset_index(inplace=True, drop=True)
        result_df.index = result_df.index + 1
        result_df = pd.concat([result_df.xs('pt', level=0, axis=1).assign(pt_type='normal'),
                               result_df.xs('pt_uma', level=0, axis=1).assign(pt_type='uma')])
    else:
        result_df = pd.DataFrame(index=[], columns=[])
    # for p in Result.objects.filter(game__event__pk=pk).order_by('game').select_related('player'):
    #     writer.writerow([i, p.player.name, p.participant.first_name, p.participant.email, p.status])
    result_df.to_csv(path_or_buf=response)
    return response
