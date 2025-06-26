from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from users.models import UserProxy
import logging
import jwt


class HasuraAuthTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # avoid cluttered console output (for instance logging all the http requests)
        logging.disable(logging.WARNING)

        cls.url = reverse('hasura-auth')

        cls.username = 'cube'
        cls.password = 'cubepass'
        cls.email = 'dev@babymri.org'
        cls.user = UserProxy.objects.create_user(
            username=cls.username, email=cls.email, password=cls.password
        )
        cls.group, _ = Group.objects.get_or_create(name='test_group')
        cls.user.groups.set([cls.group])

    @classmethod
    def tearDownClass(cls):
        # re-enable logging
        logging.disable(logging.NOTSET)

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bad_duration(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url + '?duration=bad')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_duration(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url + '?duration=-10')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_too_big_duration(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url + '?duration=9999')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt(self):
        self.client.login(username=self.username, password=self.password)
        now = int(timezone.now().timestamp())
        response = self.client.get(self.url + '?duration=60')
        token = response.data['token']
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        self.assertAlmostEqual(data['iat'], now, delta=1)
        self.assertEqual(data['exp'], data['iat'] + 60)
        self.assertEqual(data['sub'], str(self.user.id))
        self.assertEqual(data['name'], self.username)
        claims = data['https://hasura.io/jwt/claims']
        self.assertEqual(claims['x-hasura-user-id'], str(self.user.id))
        self.assertEqual(claims['x-hasura-default-role'], 'all_users')
        self.assertIn(self.group.name, claims['x-hasura-allowed-roles'])
        self.assertIn(f'{self.group.id}', claims['x-hasura-group-ids'])
        self.assertTrue(claims['x-hasura-group-ids'].startswith('{'))
        self.assertTrue(claims['x-hasura-group-ids'].endswith('}'))
