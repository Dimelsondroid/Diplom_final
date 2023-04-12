from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from backend.models import User, UserManager, Shop, Category, Product, ProductInfo, ProductParameter, Parameter, \
    Contact, ConfirmEmailToken, Order, OrderItem
from rest_framework.authtoken.models import Token
import json


class TestCreateUser(APITestCase):
    """
    User creation test
    """

    @classmethod
    def setUp(self):
        # print('# Run once for every test method to setup clean data')
        pass

    @classmethod
    def tearDown(self):
        # print('# Run once for every test method to clear data after testing')
        pass

    def test_create_account(self):
        """
        Create account test
        """

        url = reverse('backend:user-register')
        # url = '/api/v1/user/register'
        data = {
            'first_name': 'aaa',
            'last_name': 'bbb',
            'email': 'aaa@aaa.com',
            'password': 'aaa',
            'company': 'bbb',
            'position': 'ccc',
            'type': 'buyer',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class YourTestClass(APITestCase):
    """
    User related tests
    """

    fixtures = ['test_user_data.json', 'test_user_contacts.json', ]

    @classmethod
    def setUpTestData(cls):
        """
        Setting up active user, details for it and token for Auth
        """
        # print('# Run once to set up non-modified data for all class methods')
        cls.user_from_fixture = User.objects.get(id=1)
        cls.contacts_from_fixture = Contact.objects.get(id=1)
        cls.token, _ = Token.objects.get_or_create(user=cls.user_from_fixture)

    @classmethod
    def setUp(self):
        # print('# Run once for every test method to setup clean data')
        pass

    @classmethod
    def tearDown(self):
        # print('# Run once for every test method to clear data after testing')
        pass

    def test_login_user(self):
        """
        User login test
        """

        url = reverse('backend:user-login')
        response = self.client.post(url, {'email': self.user_from_fixture.email,
                                          'password': self.user_from_fixture.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     tried incorrect data for POST but it still returns 200 somewhy, while Postman request works correctly

    def test_get_user_anon(self):
        """
        Get user details with Anon test - fail expected
        """

        details_url = reverse('backend:user-details')
        response = self.client.get(details_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user(self):
        """
        Get user details test
        """
        self.client.login(email=self.user_from_fixture.email, password=self.user_from_fixture.password)
        response = self.client.get(
            reverse('backend:user-details'),
            # data={
            #   "first_name":"aaa",
            #   "last_name":"bbb",
            #   "email":"aaa@aaa.com",
            #   "password":"aaa",
            #   "company":"bbb",
            #   "position":"ccc"},
            HTTP_AUTHORIZATION='Token {}'.format(self.token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'aaa@aaa.com')
        self.assertEqual(response.data['contacts'][0]['id'], 1)
        self.assertEqual(response.data['contacts'][1]['id'], 6)

    def test_edit_user(self):
        """
        Edit user data test
        """
        self.client.login(email=self.user_from_fixture.email, password=self.user_from_fixture.password)
        response = self.client.post(
            reverse('backend:user-details'),
            data={
                "first_name": "ccc",
                "last_name": "ddd",
                "email": "aaa@aaa.com",
                "password": "aaa",
                "company": "bbb",
                "position": "qqq"},
            HTTP_AUTHORIZATION='Token {}'.format(self.token),
        )
        response_after = self.client.get(
            reverse('backend:user-details'),
            HTTP_AUTHORIZATION='Token {}'.format(self.token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_after.data['first_name'], 'ccc')
        self.assertEqual(response_after.data['last_name'], 'ddd')
        self.assertEqual(response_after.data['position'], 'qqq')

    def test_get_contacts(self):
        """
        Get user contacts test
        """
        self.client.login(email=self.user_from_fixture.email, password=self.user_from_fixture.password)
        response = self.client.get(
            reverse('backend:user-contact-list'),
            HTTP_AUTHORIZATION='Token {}'.format(self.token),
        )
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[1]['id'], 6)

    def test_create_contact(self):
        """
        Create contact test
        """
        response = self.client.post(
            reverse('backend:user-contact-list'),
            data={
                'city': 'St Peterburg',
                'street': 'Lomonosova street 40',
                'house': 'Apartament 56',
                'structure': '4321',
                'building': '4321',
                'apartment': '4321',
                'phone': '+4950987654',
            },
            HTTP_AUTHORIZATION='Token {}'.format(self.token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.login(email=self.user_from_fixture.email, password=self.user_from_fixture.password)
        new_data = self.client.get(
            reverse('backend:user-contact-list'),
            HTTP_AUTHORIZATION='Token {}'.format(self.token),
        )

        self.assertEqual(new_data.data[2]['id'], 7)
        self.assertEqual(new_data.data[2]['house'], 'Apartament 56')
        self.assertNotEqual(new_data.data[2]['city'], 'Moscow')

    def test_edit_contacts(self):
        """
        Edit contact test
        """
        self.client.login(email=self.user_from_fixture.email, password=self.user_from_fixture.password)
        response = self.client.patch(
            reverse('backend:user-contact-detail', args=[str(self.user_from_fixture.id)]),
            data={
                'city': 'St Peterburg',
                'street': 'Lomonosova street 40',
                'house': 'Apartament 56',
                'structure': '4321',
                'building': '4321',
                'apartment': '4321',
                'id': '1',
                'phone': '+4950987654',
            },
            HTTP_AUTHORIZATION='Token {}'.format(self.token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_data = self.client.get(
            reverse('backend:user-contact-list'),
            HTTP_AUTHORIZATION='Token {}'.format(self.token),
        )
        self.assertEqual(new_data.data[0]['id'], 1)
        self.assertNotEqual(new_data.data[0]['structure'], '1234')
        self.assertNotEqual(new_data.data[0]['city'], 'Moscow')

    def test_delete_contact(self):
        """
        Delete contact test
        """
        response = self.client.delete(
            reverse('backend:user-contact-detail', args=[str(self.user_from_fixture.id)]),
            data={
                'items': '1',
            },
            HTTP_AUTHORIZATION='Token {}'.format(self.token),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_data = self.client.get(
            reverse('backend:user-contact-list'),
            HTTP_AUTHORIZATION='Token {}'.format(self.token),
        )

        # checking all user contacts if requested contact deleted
        for contact in new_data.data:
            self.assertNotEqual(contact['id'], 1)

        # checking that first contact is the one with 'id' == 6 after deletion
        self.assertEqual(new_data.data[0]['id'], 6)
