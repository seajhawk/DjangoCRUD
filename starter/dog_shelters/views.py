from django.shortcuts import render, get_object_or_404
from . import models
from django.views import generic
from django.urls.base import reverse_lazy

def shelter_list(request):
    shelters = models.Shelter.objects.all()
    context = {'shelters': shelters}
    return render(request, 'shelter_list.html', context)

def shelter_detail(request, pk):
    shelter = get_object_or_404(models.Shelter, pk=pk)
    context = {'shelter': shelter}
    return render(request, 'shelter_detail.html', context)

def dog_detail(request, pk):
    dog = get_object_or_404(models.Dog, pk=pk)
    shelter = get_object_or_404(models.Shelter, pk=dog.shelter_id)
    context = {'dog': dog, 'shelter': shelter}
    return render(request, 'dog_detail.html', context)

# Generic views provide a way to create a view based on a model, often with less code
class DogDetailView(generic.DetailView):
    model = models.Dog #.objects.all() #.prefetch_related('shelter')
    template_name = 'dog_detail.html'
    # customize the queryset to get the full shelter object to display the shelter name
    queryset = models.Dog.objects.all().prefetch_related('shelter')
    context_object_name = 'dog'

class DogListView(generic.ListView):
    model = models.Dog #.objects.all() #.prefetch_related('shelter')
    template_name = 'dog_list.html'
    # customize the queryset to get the full shelter object to display the shelter name
    queryset = models.Dog.objects.all().prefetch_related('shelter')
    context_object_name = 'dogs'

class DogCreateView(generic.CreateView):
    model = models.Dog
    template_name = 'dog_form.html'
    fields = ['shelter', 'name', 'description']

class DogDeleteView(generic.DeleteView):
    model = models.Dog
    success_url = reverse_lazy('dog_list')