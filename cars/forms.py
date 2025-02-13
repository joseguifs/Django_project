from django import forms
from cars.models import Brand, Car
    
class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

    
    def clean_value(self):  # função de validação do campo 'value'
        value = self.cleaned_data.get('value')
        if value < 20000:
            self.add_error('value', 'O valor mínimo de carro é de R$20000') # função de validação do campo
            return None  # Retorna None Isso indica que o valor do campo é inválido.
            # O Django não "salva" o valor inválido, e a função de validação do campo (onde você usou add_error()) marca o campo como inválido.
        # O formulário detecta que o campo é inválido (por causa de add_error() ou o retorno de None) e, em seguida, não marca o formulário como válido. Os erros de validação serão armazenados no formulário (em form.errors).
        # Quando a view tenta validar o formulário com form.is_valid(), ele retorna False, já que há erros de validação. A view pode então verificar se o formulário é inválido, renderizando novamente a página e passando o formulário com os erros para o template, onde os erros serão exibidos.
        return value
    
    def clean_factory_year(self):
        factory_year = self.cleaned_data.get('factory_year')
        if factory_year < 2000:
            self.add_error('factory_year','Não cadastramos carros com ano de fabricação antes de 2000')
            return None
        return factory_year
    

    def clean_model_year(self):
        model_year = self.cleaned_data.get('model_year') # pegando o valor do campo model_year
        if model_year < 2000:
            self.add_error('model_year','O modelo de carro não pode ser antes dos anos 2000')
            return None
        return model_year
    

    
