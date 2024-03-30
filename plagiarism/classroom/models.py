from django.db import models
from profiles.models  import Teacher,User,Student
import random
import string
import uuid

class Time(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class WorkSpace(Time):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=False, null=True)
    stream = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=8, blank=True, null=True) # random 
    details = models.TextField() 
    teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL, null=True,related_name='room')
    #tudent = models.ManyToManyField(Student,through='MemberShip', related_name='s_room')
    students = models.ManyToManyField(User, related_name='workspace', blank=True)


    def save(self, *args, **kwargs):
        if not self.code:
            # Generate a random code of length 8
            self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super(WorkSpace, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name 
    
# Group member
class MemberShip(models.Model):
    room = models.ForeignKey(WorkSpace,on_delete=models.CASCADE, null=True,related_name='classroom')
    student = models.ForeignKey(Student,on_delete=models.CASCADE, null=True, related_name='members')
    is_join = models.BooleanField(default=False)

    def __str__(self):
        return f"{ self.room } | { self.student }"
