from django.test import TestCase
from faker import Faker
from .models import PartiePolitique

class PartiePolitiqueCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()

    def test_create_partie_politique(self):
        """Test creating a PartiePolitique instance."""
        partie = PartiePolitique.objects.create(
            name=self.fake.company(),
            abbreviation=self.fake.company_suffix(),
            color_hex=self.fake.hex_color()
        )
        self.assertIsInstance(partie, PartiePolitique)
        self.assertEqual(PartiePolitique.objects.count(), 1)

    def test_read_partie_politique(self):
        """Test reading a PartiePolitique instance."""
        partie_name = self.fake.company()
        partie = PartiePolitique.objects.create(name=partie_name)
        found_partie = PartiePolitique.objects.get(id=partie.id)
        self.assertEqual(found_partie.name, partie_name)

    def test_update_partie_politique(self):
        """Test updating a PartiePolitique instance."""
        partie = PartiePolitique.objects.create(name=self.fake.company())
        new_name = self.fake.company()
        partie.name = new_name
        partie.save()
        updated_partie = PartiePolitique.objects.get(id=partie.id)
        self.assertEqual(updated_partie.name, new_name)

    def test_delete_partie_politique(self):
        """Test deleting a PartiePolitique instance."""
        partie = PartiePolitique.objects.create(name=self.fake.company())
        self.assertEqual(PartiePolitique.objects.count(), 1)
        partie.delete()
        self.assertEqual(PartiePolitique.objects.count(), 0)