from django.test import TestCase
from django.utils import timezone
from faker import Faker
from .models import DepartmentStat
from elections.models import Election, ElectionType
from departments.models import Department
from regions.models import Region

class DepartmentStatCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        election_type = ElectionType.objects.create(name=self.fake.word())
        self.election = Election.objects.create(
            title=self.fake.sentence(),
            type=election_type,
            date=timezone.now().date()
        )
        region = Region.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5)
            )
        self.department = Department.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5),
            region=region
        )

    def test_create_department_stat(self):
        """Test creating a DepartmentStat instance."""
        stat = DepartmentStat.objects.create(
            election=self.election,
            department=self.department,
            inscrits=self.fake.random_int(min=10000, max=1000000),
            votants=self.fake.random_int(min=5000, max=500000),
            taux_participation=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100),
            bulletins_nuls=self.fake.random_int(min=100, max=1000),
            suffrages_exprimes=self.fake.random_int(min=4000, max=400000)
        )
        self.assertIsInstance(stat, DepartmentStat)
        self.assertEqual(DepartmentStat.objects.count(), 1)

    def test_read_department_stat(self):
        """Test reading a DepartmentStat instance."""
        stat = DepartmentStat.objects.create(
            election=self.election,
            department=self.department,
            inscrits=100000,
            votants=50000,
            taux_participation=50.00,
            bulletins_nuls=500,
            suffrages_exprimes=49500
        )
        found_stat = DepartmentStat.objects.get(id=stat.id)
        self.assertEqual(found_stat.inscrits, 100000)

    def test_update_department_stat(self):
        """Test updating a DepartmentStat instance."""
        stat = DepartmentStat.objects.create(
            election=self.election,
            department=self.department,
            inscrits=self.fake.random_int(min=10000, max=1000000),
            votants=self.fake.random_int(min=5000, max=500000)
        )
        new_inscrits = self.fake.random_int(min=10000, max=1000000)
        stat.inscrits = new_inscrits
        stat.save()
        updated_stat = DepartmentStat.objects.get(id=stat.id)
        self.assertEqual(updated_stat.inscrits, new_inscrits)

    def test_delete_department_stat(self):
        """Test deleting a DepartmentStat instance."""
        stat = DepartmentStat.objects.create(
            election=self.election,
            department=self.department
        )
        self.assertEqual(DepartmentStat.objects.count(), 1)
        stat.delete()
        self.assertEqual(DepartmentStat.objects.count(), 0)