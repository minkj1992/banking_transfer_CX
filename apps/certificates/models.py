import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# mock
class Bank(models.TextChoices):
    TS = "TS", _("토스은행")
    KB = "KB", _("KB국민은행")
    SH = "SH", _("신한은행")
    WO = "WO", _("우리은행")
    NH = "NH", _("NH농협은행")
    # TODO: 기타 은행 추가


class User(models.Model):
    name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=50, choices=Bank.choices)
    bank_account = models.CharField(max_length=100, help_text="bank account number")

    def __str__(self):
        return self.name


class CertificateStatus(models.TextChoices):
    CREATED = "CREATED", _("Created")
    DOWNLOADED = "DOWNLOADED", _("Downloaded")


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=CertificateStatus.choices,
        default=CertificateStatus.CREATED,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CertificateTransfer(models.Model):
    certificate = models.ForeignKey(
        Certificate, on_delete=models.CASCADE, related_name="transfers"
    )
    transfer_id = models.CharField(max_length=100)
    order = models.IntegerField(validators=[MinValueValidator(0)])  # started from 0 ..

    def __str__(self):
        return self.name

    @classmethod
    def create_transfers(cls, certificate, transfers_data):
        for idx, transfer_id in enumerate(transfers_data):
            cls.objects.create(
                certificate=certificate, transfer_id=transfer_id, order=idx
            )
