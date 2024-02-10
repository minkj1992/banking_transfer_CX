from unittest import mock

from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from test_plus.test import APITestCase

from apps.certificates.models import Certificate, CertificateTransfer, User
from apps.certificates.utils import AttrDict


def create_certificate_with_transfers(user, transfers):
    """
    Helper method to create a certificate with associated transfers directly in the database.
    """
    certificate = Certificate.objects.create(user=user, status="CREATED")
    for order, transfer_id in enumerate(transfers):
        CertificateTransfer.objects.create(
            certificate=certificate, transfer_id=transfer_id, order=order
        )
    return certificate


class CertificateApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            name="testuser", bank_name="KB", bank_account="123-456-789"
        )

    def test_create_certificate_success(self):
        """Test successful certificate creation"""

        data = {
            "user": {
                "name": self.user.name,
                "bank_name": self.user.bank_name,
                "bank_account": self.user.bank_account,
            },
            "transfers": ["T0001", "T0002"],
        }
        response = self.client.post(
            reverse("certificate-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["name"], self.user.name)
        self.assertEqual(response.data["user"]["bank_name"], self.user.bank_name)
        self.assertTrue("id" in response.data)

    def test_list_certificates_success(self):
        """Test successful retrieval of certificates list."""

        create_certificate_with_transfers(self.user, ["T0001", "T0002", "T0003"])
        response = self.client.get(reverse("certificate-list"), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_certificate_invalid_bank(self):
        """Test certificate creation with an invalid bank name"""
        INVALID_BANK = "InvalidBank"

        data = {
            "user": {
                "name": self.user.name,
                "bank_name": INVALID_BANK,
                "bank_account": self.user.bank_account,
            },
            "transfers": ["T0001", "T0002"],
        }
        response = self.client.post(
            reverse("certificate-list"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("bank_name", response.data["user"])

    def test_create_and_retrieve_certificate_transfer_order(self):
        """Test certificate creation and then retrieve to check transfer order."""

        data = {
            "user": {
                "name": self.user.name,
                "bank_name": self.user.bank_name,
                "bank_account": self.user.bank_account,
            },
            "transfers": ["T0001", "T0002", "T0003"],
        }

        create_response = self.client.post(
            reverse("certificate-list"), data=data, format="json"
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        certificate_id = create_response.data["id"]

        response = self.client.get(reverse("certificate-list"), format="json")
        retrieve_response = AttrDict(response.data[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        retrieved_transfers = [tid for tid in retrieve_response.transfers]
        expected_transfers = ["T0001", "T0002", "T0003"]
        self.assertEqual(retrieved_transfers, expected_transfers)


class CertificateApiTransactionTestCase(APITestCase):
    def setUp(self):
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        self.user = User.objects.create(
            name="Test User", bank_name="KB", bank_account="123-456-789"
        )

    @mock.patch("apps.certificates.models.CertificateTransfer.create_transfers")
    def test_certificate_creation_raises_integrity_error(self, mocked_create_transfers):
        mocked_create_transfers.side_effect = IntegrityError(
            "Simulated database error."
        )

        data = {
            "user": {
                "name": self.user.name,
                "bank_name": self.user.bank_name,
                "bank_account": self.user.bank_account,
            },
            "transfers": ["T0001", "T0002", "T0003"],
        }

        with self.assertRaises(IntegrityError):
            self.client.post(reverse("certificate-list"), data=data, format="json")
