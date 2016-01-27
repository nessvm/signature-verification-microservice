import base64
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rafah.serializers import SignatureSerializer

__author__ = 'Nestor Velazquez'


class EndpointTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls._client = APIClient()

    def setUp(self):
        self._signature = _create_dummy_signature()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_signature_creation(self):
        response = self._client.post(
            '/sign-contract/', data={
                'given_name': 'John', 'paternal_name': 'Doe',
                'maternal_name': 'Doe', 'birth_date': '1982-01-01',
                'paternal_maternal_name': 'Foe', 'loan_amount': '1000',
                'contract_number': 'N18391', 'request_date': '2015-06-06',
                'contract': 'http://domain.com/contract'
            }
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
            msg='Signature creation failed'
        )

    def test_malformed_signature_creation(self):
        response = self._client.post(
            '/sign-contract/', data={
                'given_name': 'John', 'paternal_name': 'Doe',
                'maternal_name': 'Doe', 'birth_date': '1982-01-01',
                'paternal_maternal_name': 'Foe', 'loan_amount': '1000',
                'contract_number': 'N18391'
            }
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )

    def test_signature_verification(self):
        response = self._client.post(
            '/verify-signature/'.format(self._signature.pk),
            {
                'given_name': 'John', 'paternal_name': 'Doe',
                'maternal_name': 'Doe', 'birth_date': '1982-01-01',
                'paternal_maternal_name': 'Foe', 'loan_amount': '1000',
                'contract_number': 'N18391', 'request_date': '2015-06-06',
                'contract': 'http://domain.com/contract'
            }
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['passed-verification'], True,
            msg='Signature authentication failed'
        )

    def test_false_positive(self):
        response = self._client.post(
            '/verify-signature/',
            {
                'given_name': 'John', 'paternal_name': 'Doe',
                'maternal_name': 'Doe', 'birth_date': '1982-01-01',
                'paternal_maternal_name': 'Foe', 'loan_amount': '2000',
                'contract_number': 'N18391', 'request_date': '2015-06-06',
                'contract': 'http://domain.com/contract'
            }
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['passed-verification'], False,
        )


def _create_dummy_signature():
    serializer = SignatureSerializer(
            data={
                'given_name': 'John', 'paternal_name': 'Doe',
                'maternal_name': 'Doe', 'birth_date': '1982-01-01',
                'paternal_maternal_name': 'Foe', 'loan_amount': '1000',
                'contract_number': 'N18391', 'request_date': '2015-06-06',
                'contract': 'http://domain.com/contract'
            }
        )
    serializer.is_valid()
    return serializer.save()
