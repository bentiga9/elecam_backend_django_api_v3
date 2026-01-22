from django.test import TestCase
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()

class UserCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.user_data = {
            'email': self.fake.email(),
            'nom': self.fake.name(),
            'password': self.fake.password()
        }
        self.superuser_data = {
            'email': self.fake.email(),
            'nom': self.fake.name(),
            'password': self.fake.password()
        }

    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = User.objects.create_superuser(**self.superuser_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(superuser.email, self.superuser_data['email'])
        self.assertTrue(superuser.check_password(self.superuser_data['password']))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_email(self):
        """Test creating a user without an email raises an error."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, nom='test', password='test')

    def test_create_user_without_name(self):
        """Test creating a user without a name raises an error."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='test@test.com', nom=None, password='test')
            
    def test_update_user(self):
        """Test updating a user."""
        user = User.objects.create_user(**self.user_data)
        new_name = self.fake.name()
        user.nom = new_name
        user.save()
        updated_user = User.objects.get(id=user.id)
        self.assertEqual(updated_user.nom, new_name)
        
    def test_delete_user(self):
        """Test deleting a user."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(User.objects.count(), 1)
        user.delete()
        self.assertEqual(User.objects.count(), 0)