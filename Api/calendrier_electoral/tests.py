from django.test import TestCase
from django.utils import timezone
from faker import Faker
from .models import CalendrierElectoral
from election_types.models import ElectionType
from elections.models import Election

class CalendrierElectoralCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.election_type = ElectionType.objects.create(name=self.fake.word())
        self.election = Election.objects.create(
            title=self.fake.sentence(),
            type=self.election_type,
            date=timezone.now() + timezone.timedelta(days=30),
            is_active=True
        )

    def test_create_calendrier_electoral(self):
        """Test creating a CalendrierElectoral instance."""
        calendrier = CalendrierElectoral.objects.create(
            type_election=self.election_type,
            election=self.election,
            title=self.fake.sentence(),
            event_type='election',
            date=timezone.now() + timezone.timedelta(days=20),
            status='planifie'
        )
        self.assertIsInstance(calendrier, CalendrierElectoral)
        self.assertEqual(CalendrierElectoral.objects.count(), 1)

    def test_read_calendrier_electoral(self):
        """Test reading a CalendrierElectoral instance."""
        calendrier = CalendrierElectoral.objects.create(
            type_election=self.election_type,
            election=self.election,
            title="My Event",
            event_type='election',
            date=timezone.now() + timezone.timedelta(days=20),
            status='planifie'
        )
        found_calendrier = CalendrierElectoral.objects.get(id=calendrier.id)
        self.assertEqual(found_calendrier.title, "My Event")

    def test_update_calendrier_electoral(self):
        """Test updating a CalendrierElectoral instance."""
        calendrier = CalendrierElectoral.objects.create(
            type_election=self.election_type,
            election=self.election,
            title=self.fake.sentence(),
            event_type='election',
            date=timezone.now() + timezone.timedelta(days=20),
            status='planifie'
        )
        new_status = 'en_cours'
        calendrier.status = new_status
        calendrier.save()
        updated_calendrier = CalendrierElectoral.objects.get(id=calendrier.id)
        self.assertEqual(updated_calendrier.status, new_status)

    def test_delete_calendrier_electoral(self):
        """Test deleting a CalendrierElectoral instance."""
        calendrier = CalendrierElectoral.objects.create(
            type_election=self.election_type,
            election=self.election,
            title=self.fake.sentence(),
            event_type='election',
            date=timezone.now() + timezone.timedelta(days=20),
            status='planifie'
        )
        self.assertEqual(CalendrierElectoral.objects.count(), 1)
        calendrier.delete()
        self.assertEqual(CalendrierElectoral.objects.count(), 0)