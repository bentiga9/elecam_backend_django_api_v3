from django.test import TestCase
from faker import Faker
from .models import Department
from regions.models import Region

class DepartmentCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.region = Region.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5)
        )

    def test_create_department(self):
        """Test creating a Department instance."""
        department = Department.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5),
            region=self.region,
            chef_lieu=self.fake.city()
        )
        self.assertIsInstance(department, Department)
        self.assertEqual(Department.objects.count(), 1)

    def test_read_department(self):
        """Test reading a Department instance."""
        department_name = self.fake.city()
        department = Department.objects.create(
            name=department_name,
            code=self.fake.unique.pystr(min_chars=2, max_chars=5),
            region=self.region
        )
        found_department = Department.objects.get(id=department.id)
        self.assertEqual(found_department.name, department_name)

    def test_update_department(self):
        """Test updating a Department instance."""
        department = Department.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5),
            region=self.region
        )
        new_name = self.fake.city()
        department.name = new_name
        department.save()
        updated_department = Department.objects.get(id=department.id)
        self.assertEqual(updated_department.name, new_name)

    def test_delete_department(self):
        """Test deleting a Department instance."""
        department = Department.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5),
            region=self.region
        )
        self.assertEqual(Department.objects.count(), 1)
        department.delete()
        self.assertEqual(Department.objects.count(), 0)