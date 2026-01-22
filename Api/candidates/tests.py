from django.test import TestCase
from django.utils import timezone
from faker import Faker
from .models import Candidat
from elections.models import Election, ElectionType
from political_parties.models import PartiePolitique

class CandidatCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        election_type = ElectionType.objects.create(name=self.fake.word())
        self.election = Election.objects.create(
            title=self.fake.sentence(),
            type=election_type,
            date=timezone.now().date()
        )
        self.partie_politique = PartiePolitique.objects.create(
            name=self.fake.company(),
            abbreviation=self.fake.company_suffix()
        )

    def test_create_candidat(self):
        """Test creating a Candidat instance."""
        candidat = Candidat.objects.create(
            election=self.election,
            partie_politique=self.partie_politique,
            name=self.fake.name()
        )
        self.assertIsInstance(candidat, Candidat)
        self.assertEqual(Candidat.objects.count(), 1)

    def test_read_candidat(self):
        """Test reading a Candidat instance."""
        candidat_name = self.fake.name()
        candidat = Candidat.objects.create(
            election=self.election,
            partie_politique=self.partie_politique,
            name=candidat_name
        )
        found_candidat = Candidat.objects.get(id=candidat.id)
        self.assertEqual(found_candidat.name, candidat_name)

    def test_update_candidat(self):
        """Test updating a Candidat instance."""
        candidat = Candidat.objects.create(
            election=self.election,
            partie_politique=self.partie_politique,
            name=self.fake.name()
        )
        new_name = self.fake.name()
        candidat.name = new_name
        candidat.save()
        updated_candidat = Candidat.objects.get(id=candidat.id)
        self.assertEqual(updated_candidat.name, new_name)

    def test_delete_candidat(self):
        """Test deleting a Candidat instance."""
        candidat = Candidat.objects.create(
            election=self.election,
            partie_politique=self.partie_politique,
            name=self.fake.name()
        )
        self.assertEqual(Candidat.objects.count(), 1)
        candidat.delete()
        self.assertEqual(Candidat.objects.count(), 0)