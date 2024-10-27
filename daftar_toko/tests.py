from django.test import TestCase, Client
from django.urls import reverse

class RestaurantViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Set 'user_id' in session to simulate a logged-in user
        session = self.client.session
        session['user_id'] = 1  # Example user ID
        session.save()
        
    def test_restaurant_list_view(self):
        # Test GET request to restaurant_list
        response = self.client.get(reverse('restaurant_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'daftar_toko.html')

    def test_restaurant_list_view_with_filters(self):
        # Test filtering by name (even if no results, it should return 200)
        response = self.client.get(reverse('restaurant_list'), {'name': 'Nonexistent Restaurant'})
        self.assertEqual(response.status_code, 200)

        # Test filtering by minimum rating
        response = self.client.get(reverse('restaurant_list'), {'min_rating': '4.0'})
        self.assertEqual(response.status_code, 200)

    def test_restaurant_list_view_ajax(self):
        # Test AJAX request
        response = self.client.get(reverse('restaurant_list'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_view(self):
        # Test XML response
        response = self.client.get(reverse('show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_view(self):
        # Test JSON response
        response = self.client.get(reverse('show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_by_id_view(self):
        # Test XML response by ID (expecting no data)
        response = self.client.get(reverse('show_xml_by_id', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_by_id_view(self):
        # Test JSON response by ID (expecting no data)
        response = self.client.get(reverse('show_json_by_id', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
