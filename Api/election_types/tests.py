from django.test import TestCase
from faker import Faker
from .models import ElectionType

class ElectionTypeCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()

    def test_create_election_type(self):
        """Test creating an ElectionType instance."""
        election_type = ElectionType.objects.create(name=self.fake.word())
        self.assertIsInstance(election_type, ElectionType)
        self.assertEqual(ElectionType.objects.count(), 1)

    def test_read_election_type(self):
        """Test reading an ElectionType instance."""
        election_type_name = self.fake.word()
        election_type = ElectionType.objects.create(name=election_type_name)
        found_election_type = ElectionType.objects.get(id=election_type.id)
        self.assertEqual(found_election_type.name, election_type_name)

    def test_update_election_type(self):
        """Test updating an ElectionType instance."""
        election_type = ElectionType.objects.create(name=self.fake.word())
        new_name = self.fake.word()
        election_type.name = new_name
        election_type.save()
        updated_election_type = ElectionType.objects.get(id=election_type.id)
        self.assertEqual(updated_election_type.name, new_name)

    def test_delete_election_type(self):
        """Test deleting an ElectionType instance."""
        election_type = ElectionType.objects.create(name=self.fake.word())
        self.assertEqual(ElectionType.objects.count(), 1)
        election_type.delete()
        self.assertEqual(ElectionType.objects.count(), 0)
