from django.test import TestCase
from django.utils import timezone
from faker import Faker
from .models import CandidateRegionResult, CandidateDepartmentResult, CandidateGlobalResult
from elections.models import Election, ElectionType
from candidates.models import Candidat
from regions.models import Region
from departments.models import Department
from political_parties.models import PartiePolitique

class CandidateResultsCRUDTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        election_type = ElectionType.objects.create(name=self.fake.word())
        self.election = Election.objects.create(
            title=self.fake.sentence(),
            type=election_type,
            date=timezone.now().date()
        )
        partie_politique = PartiePolitique.objects.create(name=self.fake.company(), abbreviation=self.fake.company_suffix())
        self.candidat = Candidat.objects.create(
            election=self.election,
            partie_politique=partie_politique,
            name=self.fake.name()
        )
        self.region = Region.objects.create(name=self.fake.city())
        self.department = Department.objects.create(name=self.fake.city(), region=self.region)

    def test_create_candidate_region_result(self):
        result = CandidateRegionResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            region=self.region,
            suffrages=self.fake.random_int(min=1000, max=100000),
            pourcentage=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100)
        )
        self.assertIsInstance(result, CandidateRegionResult)
        self.assertEqual(CandidateRegionResult.objects.count(), 1)

    def test_read_candidate_region_result(self):
        result = CandidateRegionResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            region=self.region,
            suffrages=5000,
            pourcentage=50.0
        )
        found_result = CandidateRegionResult.objects.get(id=result.id)
        self.assertEqual(found_result.suffrages, 5000)

    def test_update_candidate_region_result(self):
        result = CandidateRegionResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            region=self.region,
            suffrages=self.fake.random_int(min=1000, max=100000),
            pourcentage=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100)
        )
        new_suffrages = self.fake.random_int(min=1000, max=100000)
        result.suffrages = new_suffrages
        result.save()
        updated_result = CandidateRegionResult.objects.get(id=result.id)
        self.assertEqual(updated_result.suffrages, new_suffrages)

    def test_delete_candidate_region_result(self):
        result = CandidateRegionResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            region=self.region,
            suffrages=self.fake.random_int(min=1000, max=100000),
            pourcentage=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100)
        )
        self.assertEqual(CandidateRegionResult.objects.count(), 1)
        result.delete()
        self.assertEqual(CandidateRegionResult.objects.count(), 0)

    def test_create_candidate_department_result(self):
        result = CandidateDepartmentResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            department=self.department,
            suffrages=self.fake.random_int(min=1000, max=100000),
            pourcentage=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100)
        )
        self.assertIsInstance(result, CandidateDepartmentResult)
        self.assertEqual(CandidateDepartmentResult.objects.count(), 1)
        
    def test_read_candidate_department_result(self):
        result = CandidateDepartmentResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            department=self.department,
            suffrages=5000,
            pourcentage=50.0
        )
        found_result = CandidateDepartmentResult.objects.get(id=result.id)
        self.assertEqual(found_result.suffrages, 5000)
        
    def test_update_candidate_department_result(self):
        result = CandidateDepartmentResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            department=self.department,
            suffrages=self.fake.random_int(min=1000, max=100000),
            pourcentage=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100)
        )
        new_suffrages = self.fake.random_int(min=1000, max=100000)
        result.suffrages = new_suffrages
        result.save()
        updated_result = CandidateDepartmentResult.objects.get(id=result.id)
        self.assertEqual(updated_result.suffrages, new_suffrages)
        
    def test_delete_candidate_department_result(self):
        result = CandidateDepartmentResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            department=self.department,
            suffrages=self.fake.random_int(min=1000, max=100000),
            pourcentage=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100)
        )
        self.assertEqual(CandidateDepartmentResult.objects.count(), 1)
        result.delete()
        self.assertEqual(CandidateDepartmentResult.objects.count(), 0)

    def test_create_candidate_global_result(self):
        result = CandidateGlobalResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            rang=1,
            total_suffrages=self.fake.random_int(min=100000, max=1000000),
            pourcentage_national=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100),
            is_winner=True
        )
        self.assertIsInstance(result, CandidateGlobalResult)
        self.assertEqual(CandidateGlobalResult.objects.count(), 1)

    def test_read_candidate_global_result(self):
        result = CandidateGlobalResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            rang=1,
            total_suffrages=500000,
            pourcentage_national=50.00,
            is_winner=True
        )
        found_result = CandidateGlobalResult.objects.get(id=result.id)
        self.assertEqual(found_result.total_suffrages, 500000)
        
    def test_update_candidate_global_result(self):
        result = CandidateGlobalResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            rang=1,
            total_suffrages=self.fake.random_int(min=100000, max=1000000),
            pourcentage_national=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100),
            is_winner=True
        )
        new_total_suffrages = self.fake.random_int(min=100000, max=1000000)
        result.total_suffrages = new_total_suffrages
        result.save()
        updated_result = CandidateGlobalResult.objects.get(id=result.id)
        self.assertEqual(updated_result.total_suffrages, new_total_suffrages)
        
    def test_delete_candidate_global_result(self):
        result = CandidateGlobalResult.objects.create(
            election=self.election,
            candidate=self.candidat,
            rang=1,
            total_suffrages=self.fake.random_int(min=100000, max=1000000),
            pourcentage_national=self.fake.pydecimal(left_digits=2, right_digits=2, min_value=0, max_value=100),
            is_winner=True
        )
        self.assertEqual(CandidateGlobalResult.objects.count(), 1)
        result.delete()
        self.assertEqual(CandidateGlobalResult.objects.count(), 0)
