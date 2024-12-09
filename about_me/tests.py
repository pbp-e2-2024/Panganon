from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from about_me.models import UserProfile, Recipe
from forum.models import Post

# Create your tests here.

class AboutMeViewsTests(TestCase):
    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, bio='Test bio')
        
        # Create test posts and recipes
        for i in range(3):
            Post.objects.create(created_by=self.user, content=f"Test content {i}", title=f"Test title {i}")
            Recipe.objects.create(user=self.user, name=f"Recipe {i}", description="Test description", ingredients="Test ingredients", steps="Test steps")

        # Client setup for login
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_profile_view(self):
        response = self.client.get(reverse('about_me:profile_detail', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test bio")

    def test_edit_name(self):
        url = reverse('about_me:edit_name', args=[self.user.id])
        response = self.client.post(url, {'name': 'New Test Name'}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, 'New Test Name')

    def test_add_recipe(self):
        url = reverse('about_me:add_recipe')
        response = self.client.post(url, {
            'name': 'New Recipe',
            'description': 'New description',
            'ingredients': 'New ingredients',
            'steps': 'New steps'
        }, follow=True)
        self.assertTrue(Recipe.objects.filter(name='New Recipe').exists())
        self.assertRedirects(response, reverse('about_me:profile_detail', args=[self.user.id]))

    def test_view_recipe(self):
        recipe = Recipe.objects.first()
        response = self.client.get(reverse('about_me:view_recipe', args=[recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, recipe.name)

# You need to replace 'profile_detail', 'edit_name', 'add_recipe', and 'view_recipe' with the correct URL name you used in your urls.py
