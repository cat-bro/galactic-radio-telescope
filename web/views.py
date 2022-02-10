import logging

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from api.models import GalaxyInstance
from registration.backends.simple.views import RegistrationView


log = logging.getLogger('django')


class GalaxyInstanceEdit(UpdateView):
    model = GalaxyInstance
    slug_field = 'id'
    fields = ('url', 'title', 'description')


class GalaxyInstanceView(DetailView):
    model = GalaxyInstance
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super(GalaxyInstanceView, self).get_context_data(**kwargs)
        context['url'] = "{}://{}{}".format(self.request.scheme, self.request.get_host(), reverse_lazy('home'))
        return context


class GalaxyInstanceConfig(DetailView):
    model = GalaxyInstance
    slug_field = 'id'
    template_name_suffix = '.yml'


class GalaxyInstanceCreateSuccess(GalaxyInstanceView):
    template_name_suffix = '_create_success'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_url'] = '/'.join(context['url'].strip('/').split('/')[:-1])
        context['telescope_conf_link'] = '/'.join(context['url'].strip('/').split('/') + ['api', 'conf.yml'])
        return context


class GalaxyInstanceCreate(CreateView):
    model = GalaxyInstance
    fields = ('url', 'title', 'description')
    template_name_suffix = '_create'

    def get_success_url(self):
        return reverse_lazy(
            'galaxy-instance-create-success',
            kwargs={'slug': self.object.id}
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.object.owners.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class GalaxyInstanceListView(ListView):
    model = GalaxyInstance


class CustomRegistrationView(RegistrationView):

    def get_success_url(self, user):
        return reverse_lazy('home')
