from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect 
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin

from .models import Event
from .forms import EventForm
   

class EventDetail(DetailView):
    
    model = Event

class EventList(ListView):
    
    model = Event

class EventListUser(LoginRequiredMixin, EventList):
    model = Event
    template_name = "events/event_list_user.html"
    
    def dispatch(self, request, *args, **kwargs):
        try:
            request.user.participant
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse_lazy('home'))
        return super(EventListUser, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super(EventListUser, self).get_queryset()    
        queryset.filter(participant=self.request.user.participant)
        return queryset
        
class EventModelOwnerRestrictedMixin(object):
    model = Event
    
    def get_queryset(self):
        "Restricting to only the Events the user owns."
        
        queryset = super(EventModelOwnerRestrictedMixin, self).get_queryset()
        queryset.filter(participant__user=self.request.user)
         
        return queryset        

class EventCreate(LoginRequiredMixin, CreateView):
    
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        
        form.instance.participant = self.request.user.participant
        form.save()
        return super(EventCreate, self).form_valid(form)
        

class EventUpdate(LoginRequiredMixin, EventModelOwnerRestrictedMixin, UpdateView):
    
    model = Event
    form_class = EventForm
    
class EventDelete(LoginRequiredMixin, EventModelOwnerRestrictedMixin, DeleteView):
    
    model = Event
    