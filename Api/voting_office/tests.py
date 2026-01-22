from django.test import TestCase
from faker import Faker
from .models import VotingOffice
from departments.models import Department
from regions.models import Region

class VotingOfficeCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.region = Region.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5)
        )
        self.department = Department.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5),
            region=self.region
        )

    def test_create_voting_office(self):
        """Test creating a VotingOffice instance."""
        voting_office = VotingOffice.objects.create(
            name=self.fake.company(),
            department=self.department,
            latitude=self.fake.pydecimal(left_digits=2, right_digits=6, min_value=0, max_value=90),
            longitude=self.fake.pydecimal(left_digits=3, right_digits=6, min_value=0, max_value=180)
        )
        self.assertIsInstance(voting_office, VotingOffice)
        self.assertEqual(VotingOffice.objects.count(), 1)

    def test_read_voting_office(self):
        """Test reading a VotingOffice instance."""
        voting_office_name = self.fake.company()
        voting_office = VotingOffice.objects.create(
            name=voting_office_name,
            department=self.department,
            latitude=self.fake.pydecimal(left_digits=2, right_digits=6, min_value=0, max_value=90),
            longitude=self.fake.pydecimal(left_digits=3, right_digits=6, min_value=0, max_value=180)
        )
        found_voting_office = VotingOffice.objects.get(id=voting_office.id)
        self.assertEqual(found_voting_office.name, voting_office_name)

    def test_update_voting_office(self):
        """Test updating a VotingOffice instance."""
        voting_office = VotingOffice.objects.create(
            name=self.fake.company(),
            department=self.department,
            latitude=self.fake.pydecimal(left_digits=2, right_digits=6, min_value=0, max_value=90),
            longitude=self.fake.pydecimal(left_digits=3, right_digits=6, min_value=0, max_value=180)
        )
        new_name = self.fake.company()
        voting_office.name = new_name
        voting_office.save()
        updated_voting_office = VotingOffice.objects.get(id=voting_office.id)
        self.assertEqual(updated_voting_office.name, new_name)

    def test_delete_voting_office(self):
        """Test deleting a VotingOffice instance."""
        voting_office = VotingOffice.objects.create(
            name=self.fake.company(),
            department=self.department,
            latitude=self.fake.pydecimal(left_digits=2, right_digits=6, min_value=0, max_value=90),
            longitude=self.fake.pydecimal(left_digits=3, right_digits=6, min_value=0, max_value=180)
        )
        self.assertEqual(VotingOffice.objects.count(), 1)
        voting_office.delete()
        self.assertEqual(VotingOffice.objects.count(), 0)