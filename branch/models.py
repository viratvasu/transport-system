from django.db import models
from accounts.models import MyUser

class BranchProfile(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE,related_name='profile')
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Truck(models.Model):
    name = models.CharField(max_length=50)
    in_use = models.BooleanField(default=False)
    branch =  models.ForeignKey(BranchProfile,on_delete=models.CASCADE,related_name='trucks')

    def __str__(self):
        return self.name
choices = (
    ('Pending','Pending'),
    ('Completed','Completed'),
)
class Trip(models.Model):
    source = models.ForeignKey(BranchProfile,on_delete=models.CASCADE,related_name='trips_from')
    destination = models.ForeignKey(BranchProfile,on_delete=models.CASCADE,related_name='trips_to')
    truck = models.ForeignKey(Truck,on_delete=models.CASCADE,related_name='truck_trips')
    time = models.DateTimeField(auto_now_add = True)
    space = models.IntegerField(default=0)
    status = models.CharField(choices = choices,max_length=50)

    def __str__(self):
        return self.truck.name