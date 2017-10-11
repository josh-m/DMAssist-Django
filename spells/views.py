from django.shortcuts import render
from django.views import generic

from .models import SpellInfo
from .filters import SpellFilter

def spell_list(request):
    spells = SpellInfo.objects.all()
    filter = SpellFilter(request.GET, queryset = spells)

    return render(request, 'spells/index.html', {'filter':filter})

class IndexView(generic.ListView):
    template_name = 'spells/index.html'
    context_object_name = 'spell_list'

    def get_queryset(self):
        return SpellInfo.objects.order_by('name')

class DetailView(generic.DetailView):
    model = SpellInfo
    template_name = 'spells/detail.html'
    context_object_name = 'spell'
