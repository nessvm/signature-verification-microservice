from jericho.models import Signature
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rafah.serializers import SignatureSerializer

__author__ = 'Nestor Velazquez'


@api_view(['POST'])
def sign_contract(request):
    serializer = SignatureSerializer(
        data=request.data, context={'request': request}
    )
    if not serializer.is_valid():
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    serializer.save()
    return Response(
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def verify_signature(request):
    serializer = SignatureSerializer(
        data=request.data, context={'request': request}
    )
    if not serializer.is_valid():
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    instance = Signature.objects.filter(
        contract_number=request.data['contract_number']
    ).latest('created')
    serializer = SignatureSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    valid = instance.verify_signature(**serializer.validated_data)
    return Response(
        status=status.HTTP_200_OK,
        data={'passed-verification': valid}
    )


def _verify_query_params(**kwargs):
    verification_params = {
        'given_name', 'paternal_name', 'maternal_name', 'birth_date',
        'paternal_maternal_name', 'loan_amount', 'contract_number',
        'request_date'
    }
    for key, value in kwargs.items():
        if key in verification_params:
            verification_params.remove(key)
    if len(verification_params) == 0:
        return True, set()
    return False, verification_params
