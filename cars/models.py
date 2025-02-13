from django.db import models

# Create your models here.

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Car(models.Model): # nome da class é o nome da tabela no bd
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='car_brand')
    factory_year = models.IntegerField(blank=True, null=True)
    plate = models.CharField(max_length=100, blank=True, null=True) 
    model_year = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='cars', blank=True, null=True)
    value = models.FloatField(blank=True, null=True) # blank=True, null=True significa que quando for preenche meu bd , posso deixar as colunas nulo ou branco incialmente (não é obrigatorio preencher incialmente)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.model


class Inventory(models.Model):
    cars_count = models.IntegerField()
    cars_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.cars_count} - {self.cars_value}'