from django.shortcuts import render, redirect, get_object_or_404
from .models import Car
from cars.forms import CarModelForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

class CarListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'carro'

    def get_queryset(self):
        carro = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')
        if search:
            carro = carro.filter(model__icontains=search)
        return carro
    
@method_decorator(login_required(login_url = 'login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/home/'
    context_object_name = 'form'
    
class DetailCar(DetailView):
    model = Car
    template_name = 'details.html'
    context_object_name = 'cars'
    slug_field = 'model'  # Campo no banco que será usado na buscar o argumento passado parametro 'carro'
    slug_url_kwarg = 'carro'  # Nome do parâmetro na URL


@method_decorator(login_required(login_url = 'login'), name='dispatch') #proteção pr view só sera acessada quando o usuario estiver logado
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'cars_update.html'
    context_object_name = 'car'

    def get_object(self, queryset=None):
        # como estamos utilizando parametro do tipo str na url e o dajngo espera um parametro do tipo <int:pk> ou <slug:slug>, precisamos sobreescrever o metodo get_object
        carro_model = self.kwargs['carro']
        return get_object_or_404(Car, model=carro_model)
    
    def get_success_url(self): # função personalizada para redirecionar o usuario 
        return reverse_lazy('details' , kwargs={'carro':self.object.model}) # redirecionando o usuario de volta pra tela de details


@method_decorator(login_required(login_url = 'login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/home/'
    context_object_name = 'carro'
    
    def get_object(self, queryset=None):
        carro = self.kwargs['carro']
        return get_object_or_404(Car, model=carro)
     
    