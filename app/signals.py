import time
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, TestModel
import threading

@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    print(f"Signal started at: {datetime.datetime.now()}")
    ## for testing a thread (running same thread or not)
    print(f"Signal running on Thread ID: {threading.get_ident()}")
    time.sleep(3)  # Simulating a long-running task for testing signal running as sychronously or not
    Profile.objects.create(user=instance, created_at=datetime.datetime.now())
    print(f"Signal finished at: {datetime.datetime.now()}") 



@receiver(post_save, sender=TestModel)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal executed: Instance saved with name =", instance.name)

    