from django.shortcuts import render, get_object_or_404
from . import models
from django.views import generic
from django.urls.base import reverse_lazy

# API
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from . import serializers
from rest_framework.decorators import api_view


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

class ShelterCreateView(generic.CreateView):
    model = models.Dog
    fields = ['name', 'location']


# API
@api_view(['GET', 'POST', 'DELETE'])
def api_shelter(request, pk = None):
    if request.method == 'GET':
        params = request.data

        if pk is None:
            # return all shelters
            shelters = models.Shelter.objects.all()
            response_serializer = serializers.ShelterSerializer(shelters, many=True)
        else:
            shelters = get_object_or_404(models.Shelter, pk=pk)
            response_serializer = serializers.ShelterSerializer(shelters, many=False)

        return JsonResponse(response_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        params = request.data
        try:
            shelter = models.Shelter.objects.create(name=params["name"], location=params["location"])
        except Exception as error:
            # [TODO] - Improve error handling, potentially using ErrorSerializer
            response_message = f"{error.__class__} - {str(error)}"
            return JsonResponse(response_message, status=status.HTTP_400_BAD_REQUEST, safe=False)    
        
        if shelter.pk >= 0:
            response_serializer = serializers.ShelterSerializer(shelter, many=False)
            return JsonResponse(response_serializer.data, status=status.HTTP_201_CREATED, safe=False)

        return JsonResponse("Unknown error", status=status.HTTP_400_BAD_REQUEST, safe=False)
    
    elif request.method == 'DELETE':
        # [TODO] - to support delete of Shelters, need to first delete all dogs at the shelter
        #          or move them to another shelter, because Shelters are protected from deletion
        #          while there are dogs that reference them
        count = models.Shelter.objects.all().delete()
        return JsonResponse({'message': f'{count[0]} Shelters were deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
