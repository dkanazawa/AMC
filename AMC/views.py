from django.views import generic


class Top(generic.TemplateView):
    template_name = 'top.html'
