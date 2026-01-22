from django.test import TestCase
from django.utils import timezone
from faker import Faker
from .models import VoterStatistics
from elections.models import Election, ElectionType

class VoterStatisticsCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        election_type = ElectionType.objects.create(name=self.fake.word())
        self.election = Election.objects.create(
            title=self.fake.sentence(),
            type=election_type,
            date=timezone.now().date()
        )

    def test_create_voter_statistics(self):
        """Test creating a VoterStatistics instance."""
        stats = VoterStatistics.objects.create(
            election=self.election,
            total_inscrits=self.fake.random_int(min=1000000, max=10000000),
            total_votants=self.fake.random_int(min=500000, max=5000000),
            taux_participation=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100),
            total_bulletins_nuls=self.fake.random_int(min=10000, max=100000),
            total_suffrages_exprimes=self.fake.random_int(min=400000, max=4000000)
        )
        self.assertIsInstance(stats, VoterStatistics)
        self.assertEqual(VoterStatistics.objects.count(), 1)

    def test_read_voter_statistics(self):
        """Test reading a VoterStatistics instance."""
        stats = VoterStatistics.objects.create(
            election=self.election,
            total_inscrits=1000000
        )
        found_stats = VoterStatistics.objects.get(id=stats.id)
        self.assertEqual(found_stats.total_inscrits, 1000000)

    def test_update_voter_statistics(self):
        """Test updating a VoterStatistics instance."""
        stats = VoterStatistics.objects.create(
            election=self.election,
            total_inscrits=self.fake.random_int(min=1000000, max=10000000)
        )
        new_total_inscrits = self.fake.random_int(min=1000000, max=10000000)
        stats.total_inscrits = new_total_inscrits
        stats.save()
        updated_stats = VoterStatistics.objects.get(id=stats.id)
        self.assertEqual(updated_stats.total_inscrits, new_total_inscrits)

    def test_delete_voter_statistics(self):
        """Test deleting a VoterStatistics instance."""
        stats = VoterStatistics.objects.create(election=self.election)
        self.assertEqual(VoterStatistics.objects.count(), 1)
        stats.delete()
        self.assertEqual(VoterStatistics.objects.count(), 0)
