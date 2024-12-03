from django.db import models
class ParentModel(models.Model):
    name=models.CharField(max_length=200, null=True)

class ChildModel(models.Model):
    parent = models.ForeignKey(ParentModel)
    name=models.CharField(max_length=200, null=True)

parent = ParentModel.objects.first()
parent.childmodel_set.all()