from django.db import models


class TestModel(models.Model):
    name = models.CharField(max_length=255)


class BusinessModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512)


class ServiceModel(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2)

    business = models.ForeignKey(BusinessModel, on_delete=models.CASCADE)


class ClientModel(models.Model):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2)

    business = models.ForeignKey(BusinessModel, on_delete=models.CASCADE)


class ManagerModel(models.Model):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)


class ClientBonusTransactionModel(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE)
    authorized_by = models.ForeignKey(ManagerModel, on_delete=models.SET_NULL, null=True)
    from_service = models.ForeignKey(ServiceModel, on_delete=models.SET_NULL, null=True)
