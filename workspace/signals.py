from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from news.models import News


@receiver(post_save, sender=News)
def post_save_news(sender, instance, created, *args, **kwargs):

    print('Signal is going to work')
    
    if created:
        print(f'Created news {instance.name}')

    else:
        print(f'Updated news {instance.name}')



@receiver(pre_save, sender=News)
def pre_save_news(sender, instance, *args, **kwargs):

    print('Pre signal is going to work')
  
    print(f'Working with news {instance.name}')