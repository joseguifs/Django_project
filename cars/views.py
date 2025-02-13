from django.shortcuts import render, redirect, get_object_or_404
from .models import Car
from cars.forms import CarModelForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.


def cars_home(request):
    carro = Car.objects.all().order_by('model') # pega todos objetos do bd e caso não passe parametro para o search
    search = request.GET.get('search')  # captura o paraemtro search passado pelo usuario 
    if search:
        carro = Car.objects.filter(model__icontains=search)
    # carro = Car.objects.filter(brand__name='Mustang') # filtrando carros da marca mustang no bd e a qryset só terá dados do tipo mustang
    # carro = Car.objects.filter(model__contains ='GTR') # dessa forma ele filta se o parâmetro for extamente igual
    return render(request, 'cars.html', {'carro':carro}) # o utimo parametro basicamente estamos passando o contexto(dados) carro para todo local no que tenha o objeto carro ou atributo de cars.html 

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
    
# get_queryset() é utilizado para definir o conjunto de objetos que será retornado e exibido na página de listagem. Ele retorna uma queryset que será usada para preencher o contexto da view com os dados que você deseja exibir.


def new_car_view(request):
    if request.method == 'POST':
        new_car_form = CarModelForm(request.POST, request.FILES)
        if new_car_form.is_valid():
            new_car_form.save()
            return redirect('cars_home')
        else:
            # Passa o formulário com os erros para o template
            return render(request, 'new_car.html', {'new_form': new_car_form})

    else:
        new_form = CarModelForm()
        return render(request, 'new_car.html', {'new_form': new_form}) # as_table é um método fornecido pelo Django que converte os campos do formulário em uma tabela HTML e new_form é o nome do seu formulário, que é um objeto Form ou ModelForm.


class NewCarView(View):
    def get(self, request):
        new_form = CarModelForm
        return render(request, 'new_car.html', {'new_form': new_form}) 
    
    def post(self, request):
        new_car_form = CarModelForm(request.POST, request.FILES)
        if new_car_form.is_valid():
            new_car_form.save()
            return redirect('cars_home')
        return render(request, 'new_car.html', {'new_form': new_car_form})

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
     
    