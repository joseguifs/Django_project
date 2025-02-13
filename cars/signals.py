from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.db.models import Sum
from cars.models import Car, Inventory

def car_invetory_update():
    cars_count = Car.objects.all().count()
    cars_value = Car.objects.aggregate(
        total_value = Sum('value') # Sum('value') soma o valor da coluna value do nosso bd/models
    )['total_value'] # aggregate retorna um dict {'total_value':Sum('value')}, no caso estamos pegando so o valor da chave total_value
    Inventory.objects.create(
        cars_count = cars_count,
        cars_value = cars_value
    )

@receiver(post_save, sender=Car) #trate minha função como alguem que esteja observando eventos que estão cheagando na minha tabela/bd Car
def car_pre_save(sender, instance, **kwargs): # basicamente esse função será disparada em todo evento post save da tabela Car
    car_invetory_update()

receiver(post_delete, sender=Car)
def car_pre_delete(sender, instance, **kwargs): # Essa será disparada em todo evento post delete da tabela Car
    car_invetory_update()

@receiver(pre_save, sender=Car)
def car_pre_save_bio(sender, instance, **kwargs):
    if not instance.bio:
        instance.bio = 'bio gerada automáticamente'