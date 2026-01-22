from django.test import TestCase
from django.core.exceptions import ValidationError
from elections.models import Election
from election_types.models import ElectionType
from regions.models import Region
from .models import RegionStat
from datetime import date


class RegionStatModelTest(TestCase):
    """Tests pour le modèle RegionStat"""
    
    def setUp(self):
        """Préparation des données de test"""
        # Créer un type d'élection
        self.election_type = ElectionType.objects.create(
            name="Présidentielle",
            description="Élection présidentielle"
        )
        
        # Créer une élection
        self.election = Election.objects.create(
            title="Présidentielle 2025",
            type=self.election_type,
            date=date(2025, 10, 7)
        )
        
        # Créer une région
        self.region = Region.objects.create(
            name="Centre",
            code="CE",
            region_type="national"
        )
    
    def test_create_region_stat(self):
        """Test de création d'une statistique régionale"""
        stat = RegionStat.objects.create(
            election=self.election,
            region=self.region,
            inscrits=50000,
            votants=30000,
            taux_participation=60.00,
            bulletins_nuls=500,
            suffrages_exprimes=29500
        )
        
        self.assertEqual(stat.region.name, 'Centre')
        self.assertEqual(stat.inscrits, 50000)
        self.assertEqual(stat.votants, 30000)
        self.assertEqual(float(stat.taux_participation), 60.00)
    
    def test_region_stat_str(self):
        """Test de la représentation en chaîne"""
        stat = RegionStat.objects.create(
            election=self.election,
            region=self.region,
            inscrits=20000,
            votants=15000
        )
        
        expected = f"{self.region.name} - {self.election.title}"
        self.assertEqual(str(stat), expected)
    
    def test_unique_constraint(self):
        """Test de la contrainte d'unicité élection-région"""
        RegionStat.objects.create(
            election=self.election,
            region=self.region,
            inscrits=10000,
            votants=8000
        )
        
        # Tenter de créer un doublon devrait échouer
        with self.assertRaises(Exception):
            RegionStat.objects.create(
                election=self.election,
                region=self.region,
                inscrits=20000,
                votants=15000
            )
    
    def test_auto_calculate_taux_abstention(self):
        """Test du calcul automatique du taux d'abstention"""
        stat = RegionStat.objects.create(
            election=self.election,
            region=self.region,
            inscrits=30000,
            votants=21000,
            taux_participation=70.00
        )
        
        # Le taux d'abstention devrait être calculé automatiquement
        stat.refresh_from_db()
        self.assertEqual(float(stat.taux_abstention), 30.00)
