from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)

import jwt

_DEFAULT_DURATION = 900
"""
Default duration of a JWT before it expires (15 minutes).
"""


@extend_schema(
    description='Creates a JWT for authorization of requests to Hasura graphql-engine.',
    parameters=[
        OpenApiParameter(
            name='duration',
            description='Number of seconds the requested JWT should be valid for',
            type={
                'type': 'integer',
                'minimum': 1,
                'maximum': _DEFAULT_DURATION,
            },
            location='query',
            default=_DEFAULT_DURATION,
        )
    ],
    responses=OpenApiResponse(
        response={
            'type': 'object',
            'properties': {
                'token': {
                    'type': 'string',
                    'format': 'password',
                    'description': 'JWT token using HS256 algorithm',
                }
            },
        },
        examples=[
            OpenApiExample(
                name='JWT token response',
                value={
                    'token': (
                        r'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1Iiw'
                        r'ibmFtZSI6InJ1ZG9scGgiLCJpYXQiOjE3NTA5NzIyMjUsImV4cCI'
                        r'6MTc1MDk3MzEyNSwiaHR0cHM6Ly9oYXN1cmEuaW8vand0L2NsYWl'
                        r'tcyI6eyJ4LWhhc3VyYS1kZWZhdWx0LXJvbGUiOiJhbGxfdXNlcnM'
                        r'iLCJ4LWhhc3VyYS1hbGxvd2VkLXJvbGVzIjpbImFsbF91c2VycyI'
                        r'sInBhY3NfdXNlcnMiLCJjdXN0b21fZ3JvdXAiXSwieC1oYXN1cmE'
                        r'tdXNlci1pZCI6IjUiLCJ4LWhhc3VyYS1ncm91cC1pZHMiOiJ7MSw'
                        'yLDN9In19.xRUv04_RVWfFqf8Alfa3yddOBnc6Ft7sEgfkVWDwBBE'
                    )
                },
            )
        ],
    ),
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hasura_token(request):
    try:
        duration = int(request.query_params.get('duration', _DEFAULT_DURATION))
    except ValueError:
        return Response({'error': '"duration" is not an int'}, status=400)
    if duration < 1:
        return Response(
            {'error': '"duration" must be more 1 second or more.'}, status=400
        )
    if duration > _DEFAULT_DURATION:
        return Response(
            {'error': f'maximum "duration" is {_DEFAULT_DURATION} seconds'},
            status=400,
        )

    iat = int(timezone.now().timestamp())
    groups = [g.name for g in request.user.groups.all()]

    data = {
        'sub': str(request.user.id),
        'name': request.user.username,
        'iat': iat,
        'exp': iat + duration,
        'https://hasura.io/jwt/claims': {
            'x-hasura-default-role': 'all_users',  # hard-coded
            'x-hasura-allowed-roles': groups,
            'x-hasura-user-id': str(request.user.id),
            'x-hasura-group-ids': f'{{{",".join(str(g.id) for g in request.user.groups.all())}}}'
        },
    }
    token = jwt.encode(data, settings.SECRET_KEY)
    return Response({'token': token})
