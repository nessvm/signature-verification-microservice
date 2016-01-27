from datetime import date
import re

from django.test import TestCase

from jericho.models import Signature

__author__ = 'Nestor Velazquez'


class SignatureTests(TestCase):
    def test_signature_creation(self):
        signature = Signature.objects.create_signature(
            given_name='John', paternal_name='Doe', maternal_name='Doe',
            birth_date=date(1982, 1, 1), paternal_maternal_name='Foe',
            loan_amount='1000', contract_number='N18391',
            request_date=date(2015, 6, 6)
        )
        hex_re = r'[A-Z0-9]*'
        hex_match = re.match(hex_re, signature.mac)
        self.assertIsNotNone(
            hex_match.string, msg='MAC is not being generated'
        )
        self.assertIsNot(
            hex_match.string, ''
        )

    def test_verification(self):
        signature = Signature.objects.create_signature(
            given_name='John', paternal_name='Doe', maternal_name='Doe',
            birth_date=date(1982, 1, 1), paternal_maternal_name='Foe',
            loan_amount='1000', contract_number='N18391',
            request_date=date(2015, 6, 6)
        )
        self.assertTrue(signature.verify_signature(
            given_name='John', paternal_name='Doe', maternal_name='Doe',
            birth_date=date(1982, 1, 1), paternal_maternal_name='Foe',
            loan_amount='1000', contract_number='N18391',
            request_date=date(2015, 6, 6)
        ), msg='MAC verification is not being processed properly')

    def test_false_positive(self):
        signature = Signature.objects.create_signature(
            given_name='John', paternal_name='Doe', maternal_name='Doe',
            birth_date=date(1982, 1, 1), paternal_maternal_name='Foe',
            loan_amount='1000', contract_number='N18391',
            request_date=date(2015, 6, 6)
        )
        self.assertFalse(signature.verify_signature(
            given_name='John', paternal_name='Doe', maternal_name='Doe',
            birth_date=date(1982, 1, 1), paternal_maternal_name='Foe',
            loan_amount='700', contract_number='N18391',
            request_date=date(2015, 6, 6)
        ), msg='MAC verification is verifying a modified contract string')
