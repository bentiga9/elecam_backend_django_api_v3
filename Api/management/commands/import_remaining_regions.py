"""
Commande Django pour importer les 4 régions restantes
Régions: Nord-Ouest, Ouest, Sud, Sud-Ouest (25 départements)
Données extraites du PDF officiel pages 16-23
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from elections.models import Election
from departments.models import Department
from candidates.models import Candidat
from candidate_results.models import CandidateDepartmentResult
from department_stats.models import DepartmentStat


class Command(BaseCommand):
    help = "Importe les données des 4 régions restantes (Nord-Ouest, Ouest, Sud, Sud-Ouest)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=" * 80))
        self.stdout.write(self.style.NOTICE("IMPORT DES 4 RÉGIONS RESTANTES"))
        self.stdout.write(self.style.NOTICE("=" * 80))

        try:
            with transaction.atomic():
                election = Election.objects.get(date="2025-10-12")
                candidates = {c.name: c for c in Candidat.objects.filter(election=election)}
                
                self.import_nord_ouest(election, candidates)
                self.import_ouest(election, candidates)
                self.import_sud(election, candidates)
                self.import_sud_ouest(election, candidates)
                
                self.stdout.write(self.style.SUCCESS("\n" + "=" * 80))
                self.stdout.write(self.style.SUCCESS("IMPORT TERMINÉ AVEC SUCCÈS!"))
                self.stdout.write(self.style.SUCCESS("=" * 80))
                
                # Afficher le résumé
                total_results = CandidateDepartmentResult.objects.count()
                total_stats = DepartmentStat.objects.count()
                self.stdout.write(f"\nTotal résultats départementaux: {total_results}")
                self.stdout.write(f"Total statistiques départementales: {total_stats}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur: {e}"))
            raise

    def find_department(self, name, region_name):
        """Trouve un département par nom et région"""
        try:
            return Department.objects.get(name=name, region__name=region_name)
        except Department.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"Département non trouvé: {name} dans {region_name}"))
            return None

    def import_nord_ouest(self, election, candidates):
        """Importe les données de la région Nord-Ouest (7 départements)"""
        self.stdout.write("\n### RÉGION NORD-OUEST ###")
        
        # Données extraites des pages 16-17 du PDF
        data = {
            "Boyo": {
                "stats": {
                    "inscrits": 56828, "votants": 9775, "taux_participation": Decimal("17.20"),
                    "taux_abstention": Decimal("82.80"), "bulletins_nuls": 60, "suffrages_exprimes": 9715
                },
                "results": {
                    "ATEKI SETA CAXTON": {"votes": 29, "percentage": Decimal("0.30")},
                    "BELLO BOUBA MAIGARI": {"votes": 1189, "percentage": Decimal("12.24")},
                    "BIYA PAUL": {"votes": 6614, "percentage": Decimal("68.08")},
                    "BOUGHA HAGBE JACQUES": {"votes": 18, "percentage": Decimal("0.18")},
                    "ISSA TCHIROMA": {"votes": 771, "percentage": Decimal("7.94")},
                    "IYODI HIRAM SAMUEL": {"votes": 32, "percentage": Decimal("0.33")},
                    "KWEMO PIERRE": {"votes": 17, "percentage": Decimal("0.17")},
                    "LIBII LI NGUE NGUE CABRAL": {"votes": 31, "percentage": Decimal("0.32")},
                    "MATOMBA SERGE ESPOIR": {"votes": 18, "percentage": Decimal("0.18")},
                    "MUNA AKERE TABENG": {"votes": 26, "percentage": Decimal("0.27")},
                    "OSIH JOSHUA NAMBANGI": {"votes": 945, "percentage": Decimal("9.73")},
                    "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 25, "percentage": Decimal("0.26")},
                }
            },
            # Ajoutez les 6 autres départements ici...
        }
        
        self.import_region_data(election, candidates, "Nord-Ouest", data)

    def import_ouest(self, election, candidates):
        """Importe les données de la région Ouest (8 départements)"""
        self.stdout.write("\n### RÉGION OUEST ###")
        # TODO: Ajouter les données des pages 18-19
        pass

    def import_sud(self, election, candidates):
        """Importe les données de la région Sud (4 départements)"""
        self.stdout.write("\n### RÉGION SUD ###")
        # TODO: Ajouter les données des pages 20-21
        pass

    def import_sud_ouest(self, election, candidates):
        """Importe les données de la région Sud-Ouest (6 départements)"""
        self.stdout.write("\n### RÉGION SUD-OUEST ###")
        # TODO: Ajouter les données des pages 22-23
        pass

    def import_region_data(self, election, candidates, region_name, data):
        """Helper pour importer les données d'une région"""
        for dept_name, dept_data in data.items():
            dept = self.find_department(dept_name, region_name)
            if not dept:
                continue
            
            # Créer les statistiques
            DepartmentStat.objects.update_or_create(
                election=election,
                department=dept,
                defaults=dept_data["stats"]
            )
            
            # Créer les résultats
            for candidate_name, result_data in dept_data["results"].items():
                candidate = candidates.get(candidate_name)
                if candidate:
                    CandidateDepartmentResult.objects.update_or_create(
                        election=election,
                        candidate=candidate,
                        department=dept,
                        defaults=result_data
                    )
            
            self.stdout.write(f"  ✓ {dept.name}: {len(dept_data['results'])} résultats + stats")
