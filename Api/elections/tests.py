from django.test import TestCase
from django.utils import timezone
from faker import Faker
from .models import Election
from election_types.models import ElectionType

class ElectionCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.election_type = ElectionType.objects.create(name=self.fake.word())

    def test_create_election(self):
        """Test creating an Election instance."""
        election = Election.objects.create(
            title=self.fake.sentence(),
            type=self.election_type,
            date=timezone.now().date(),
            status='pending',
            is_active=True
        )
        self.assertIsInstance(election, Election)
        self.assertEqual(Election.objects.count(), 1)

    def test_read_election(self):
        """Test reading an Election instance."""
        election_title = self.fake.sentence()
        election = Election.objects.create(
            title=election_title,
            type=self.election_type,
            date=timezone.now().date()
        )
        found_election = Election.objects.get(id=election.id)
        self.assertEqual(found_election.title, election_title)

    def test_update_election(self):
        """Test updating an Election instance."""
        election = Election.objects.create(
            title=self.fake.sentence(),
            type=self.election_type,
            date=timezone.now().date()
        )
        new_title = self.fake.sentence()
        election.title = new_title
        election.save()
        updated_election = Election.objects.get(id=election.id)
        self.assertEqual(updated_election.title, new_title)

    def test_delete_election(self):
        """Test deleting an Election instance."""
        election = Election.objects.create(
            title=self.fake.sentence(),
            type=self.election_type,
            date=timezone.now().date()
        )
        self.assertEqual(Election.objects.count(), 1)
        election.delete()
        self.assertEqual(Election.objects.count(), 0)
