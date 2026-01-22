from django.test import TestCase
from django.core.exceptions import ValidationError
from elections.models import Election
from election_types.models import ElectionType
from .models import DiasporaStat
from datetime import date


class DiasporaStatModelTest(TestCase):
    """Tests pour le modèle DiasporaStat"""
    
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
    
    def test_create_diaspora_stat(self):
        """Test de création d'une statistique diaspora"""
        stat = DiasporaStat.objects.create(
            election=self.election,
            zone='AFRIQUE',
            inscrits=5000,
            votants=3000,
            taux_participation=60.00,
            bulletins_nuls=50,
            suffrages_exprimes=2950
        )
        
        self.assertEqual(stat.zone, 'AFRIQUE')
        self.assertEqual(stat.inscrits, 5000)
        self.assertEqual(stat.votants, 3000)
        self.assertEqual(float(stat.taux_participation), 60.00)
    
    def test_diaspora_stat_str(self):
        """Test de la représentation en chaîne"""
        stat = DiasporaStat.objects.create(
            election=self.election,
            zone='EUROPE',
            inscrits=2000,
            votants=1500
        )
        
        expected = f"Europe - {self.election.title}"
        self.assertEqual(str(stat), expected)
    
    def test_unique_constraint(self):
        """Test de la contrainte d'unicité élection-zone"""
        DiasporaStat.objects.create(
            election=self.election,
            zone='ASIE',
            inscrits=1000,
            votants=800
        )
        
        # Tenter de créer un doublon devrait échouer
        with self.assertRaises(Exception):
            DiasporaStat.objects.create(
                election=self.election,
                zone='ASIE',
                inscrits=2000,
                votants=1500
            )
    
    def test_auto_calculate_taux_abstention(self):
        """Test du calcul automatique du taux d'abstention"""
        stat = DiasporaStat.objects.create(
            election=self.election,
            zone='AMERIQUE',
            inscrits=3000,
            votants=2100,
            taux_participation=70.00
        )
        
        # Le taux d'abstention devrait être calculé automatiquement
        stat.refresh_from_db()
        self.assertEqual(float(stat.taux_abstention), 30.00)
