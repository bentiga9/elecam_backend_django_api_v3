from django.test import TestCase
from faker import Faker
from .models import Region

class RegionCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()

    def test_create_region(self):
        """Test creating a Region instance."""
        region = Region.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5),
            region_type='national',
            chef_lieu=self.fake.city()
        )
        self.assertIsInstance(region, Region)
        self.assertEqual(Region.objects.count(), 1)

    def test_read_region(self):
        """Test reading a Region instance."""
        region_name = self.fake.city()
        region = Region.objects.create(
            name=region_name,
            code=self.fake.unique.pystr(min_chars=2, max_chars=5)
        )
        found_region = Region.objects.get(id=region.id)
        self.assertEqual(found_region.name, region_name)

    def test_update_region(self):
        """Test updating a Region instance."""
        region = Region.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5)
        )
        new_name = self.fake.city()
        region.name = new_name
        region.save()
        updated_region = Region.objects.get(id=region.id)
        self.assertEqual(updated_region.name, new_name)

    def test_delete_region(self):
        """Test deleting a Region instance."""
        region = Region.objects.create(
            name=self.fake.city(),
            code=self.fake.unique.pystr(min_chars=2, max_chars=5)
        )
        self.assertEqual(Region.objects.count(), 1)
        region.delete()
        self.assertEqual(Region.objects.count(), 0)
