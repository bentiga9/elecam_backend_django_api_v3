from django.test import TestCase
from faker import Faker
from .models import PickupPoint
from departments.models import Department
from regions.models import Region

class PickupPointCRUDTests(TestCase):
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

    def test_create_pickup_point(self):
        """Test creating a PickupPoint instance."""
        pickup_point = PickupPoint.objects.create(
            name=self.fake.company(),
            department=self.department,
            latitude=self.fake.pydecimal(left_digits=2, right_digits=6, min_value=0, max_value=90),
            longitude=self.fake.pydecimal(left_digits=3, right_digits=6, min_value=0, max_value=180)
        )
        self.assertIsInstance(pickup_point, PickupPoint)
        self.assertEqual(PickupPoint.objects.count(), 1)

    def test_read_pickup_point(self):
        """Test reading a PickupPoint instance."""
        pickup_point_name = self.fake.company()
        pickup_point = PickupPoint.objects.create(
            name=pickup_point_name,
            department=self.department,
            latitude=self.fake.pydecimal(left_digits=2, right_digits=6, min_value=0, max_value=90),
            longitude=self.fake.pydecimal(left_digits=3, right_digits=6, min_value=0, max_value=180)
        )
        found_pickup_point = PickupPoint.objects.get(id=pickup_point.id)
        self.assertEqual(found_pickup_point.name, pickup_point_name)

    def test_update_pickup_point(self):
        """Test updating a PickupPoint instance."""
        pickup_point = PickupPoint.objects.create(
            name=self.fake.company(),
            department=self.department,
            latitude=self.fake.pydecimal(left_digits=2, right_digits=6, min_value=0, max_value=90),
            longitude=self.fake.pydecimal(left_digits=3, right_digits=6, min_value=0, max_value=180)
        )
        new_name = self.fake.company()
        pickup_point.name = new_name
        pickup_point.save()
        updated_pickup_point = PickupPoint.objects.get(id=pickup_point.id)
        self.assertEqual(updated_pickup_point.name, new_name)

    def test_delete_pickup_point(self):
        """Test deleting a PickupPoint instance."""
        pickup_point = PickupPoint.objects.create(
            name=self.fake.company(),
            department=self.department,
            latitude=self.fake.pydecimal(left_digits=2, right_digits=6, min_value=0, max_value=90),
            longitude=self.fake.pydecimal(left_digits=3, right_digits=6, min_value=0, max_value=180)
        )
        self.assertEqual(PickupPoint.objects.count(), 1)
        pickup_point.delete()
        self.assertEqual(PickupPoint.objects.count(), 0)