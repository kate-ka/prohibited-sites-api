from rest_framework.test import APITestCase
from rest_framework import status

from registry.factories import BlockRequestFactory, RegistryFactory, SuperUserFactory, UserFactory


class SendBlockRequestApiTests(APITestCase):
    """Test API for sending block requests"""

    def setUp(self):
        self.list_url = '/api-v1/block-requests/'
        self.detail_url = lambda id: '/api-v1/block-requests/{}/'.format(id)

    def test_list_block_requests_returns_403_for_not_unauthorized(self):
        """Test that login is required to access this endpoint"""
        block_request = BlockRequestFactory(user_ip='172.211.150.213',
                                            site='https://russian.rt.com/',
                                            description='entrance to hell')
        res = self.client.get(self.detail_url(block_request.pk))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_block_request(self):
        """Test block requests is created successfully for unauthorized user."""
        data = {'site': 'https://life.ru/',
                'description': 'fake news'}
        res = self.client.post(self.list_url, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()['site'], data['site'])


class AddSiteToRegistry(APITestCase):
    """Test API for adding blocked sites to registry by admin."""

    def setUp(self):
        self.list_url = '/api-v1/registries/'
        self.detail_url = lambda id: '/api-v1/registries/{}/'.format(id)

    def test_list_admin_permission_is_required(self):
        """Test that page is available only to admins."""
        user = UserFactory()
        user.set_password('qwerty')
        user.save()
        assert self.client.login(username=user.username, password='qwerty')
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_registry_detail_returns_403_for_not_unauthorised(self):
        registry = RegistryFactory(ip='172.201.160.213', description='fake news')
        res = self.client.get(self.detail_url(registry.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_registry_detail_by_admin(self):
        """Test that admin can add site to registry successfully."""
        superuser = self._create_superuser()
        assert self.client.login(username=superuser.username, password='qwerty')
        registry = RegistryFactory(ip='172.201.160.213', user=superuser, description='fake news')
        res = self.client.get(self.detail_url(registry.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_registry_by_admin(self):
        superuser = self._create_superuser()
        assert self.client.login(username=superuser.username, password='qwerty')
        data = {
            'ip': '172.201.160.213',
            'description': 'fake news'
        }
        res = self.client.post(self.list_url, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()['ip'], data['ip'])

    def _create_superuser(self):
        superuser = SuperUserFactory()
        superuser.set_password('qwerty')
        superuser.save()

        return superuser


class TestAuthApi(APITestCase):
    """Test authentication API."""
    def setUp(self):
        self.login = '/api-v1/api-auth/login/'
        self.logout = '/api-v1/api-auth/logout/'

    def test_login(self):
        superuser = SuperUserFactory()
        superuser.set_password('qwerty')
        superuser.save()
        res = self.client.post(self.login, data={'username': superuser.username, 'password': superuser.password})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_logout(self):
        res = self.client.post(self.logout)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
