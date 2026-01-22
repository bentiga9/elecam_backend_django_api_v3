"""
Commande Django pour importer les 4 régions restantes
Régions: Nord-Ouest (7), Ouest (8), Sud (4), Sud-Ouest (6) = 25 départements
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
    help = "Importe les 4 régions restantes (Nord-Ouest, Ouest, Sud, Sud-Ouest)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=" * 80))
        self.stdout.write(self.style.NOTICE("IMPORT DES 4 RÉGIONS RESTANTES"))
        self.stdout.write(self.style.NOTICE("Source: PDF Officiel pages 16-23"))
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
                self.stdout.write(self.style.SUCCESS("IMPORT TERMINÉ!"))
                self.stdout.write(self.style.SUCCESS("=" * 80))
                
                # Résumé
                total_results = CandidateDepartmentResult.objects.count()
                total_stats = DepartmentStat.objects.count()
                self.stdout.write(f"\nTotal résultats: {total_results}")
                self.stdout.write(f"Total statistiques: {total_stats}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur: {e}"))
            raise

    def insert_data(self, election, candidates, region_name, dept_name, stats, results):
        """Insère les données pour un département"""
        try:
            dept = Department.objects.get(name=dept_name, region__name=region_name)
            
            # Statistiques
            DepartmentStat.objects.update_or_create(
                election=election,
                department=dept,
                defaults=stats
            )
            
            # Résultats
            count = 0
            for candidate_name, result_data in results.items():
                candidate = candidates.get(candidate_name)
                if candidate:
                    CandidateDepartmentResult.objects.update_or_create(
                        election=election,
                        candidate=candidate,
                        department=dept,
                        defaults={
                            'suffrages': result_data['votes'],
                            'pourcentage': Decimal(str(result_data['percentage']))
                        }
                    )
                    count += 1
            
            self.stdout.write(f"  ✓ {dept_name}: {count} résultats + stats")
            return True
        except Department.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"  ✗ {dept_name}: Département non trouvé"))
            return False

    def import_nord_ouest(self, election, candidates):
        """Importe Nord-Ouest (7 départements) - Pages 16-17 du PDF"""
        self.stdout.write("\n### RÉGION NORD-OUEST ###")
        
        # Boyo
        self.insert_data(election, candidates, "Nord-Ouest", "Boyo",
            {"inscrits": 56828, "votants": 9775, "taux_participation": Decimal("17.20"),
             "taux_abstention": Decimal("82.80"), "bulletins_nuls": 60, "suffrages_exprimes": 9715},
            {
                "ATEKI SETA CAXTON": {"votes": 29, "percentage": 0.30},
                "BELLO BOUBA MAIGARI": {"votes": 1189, "percentage": 12.24},
                "BIYA PAUL": {"votes": 6614, "percentage": 68.08},
                "BOUGHA HAGBE JACQUES": {"votes": 18, "percentage": 0.18},
                "ISSA TCHIROMA": {"votes": 771, "percentage": 7.94},
                "IYODI HIRAM SAMUEL": {"votes": 32, "percentage": 0.33},
                "KWEMO PIERRE": {"votes": 17, "percentage": 0.17},
                "LIBII LI NGUE NGUE CABRAL": {"votes": 31, "percentage": 0.32},
                "MATOMBA SERGE ESPOIR": {"votes": 18, "percentage": 0.18},
                "MUNA AKERE TABENG": {"votes": 26, "percentage": 0.27},
                "OSIH JOSHUA NAMBANGI": {"votes": 945, "percentage": 9.73},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 25, "percentage": 0.26}
            }
        )
        
        # Bui
        self.insert_data(election, candidates, "Nord-Ouest", "Bui",
            {"inscrits": 104230, "votants": 16364, "taux_participation": Decimal("15.70"),
             "taux_abstention": Decimal("84.30"), "bulletins_nuls": 71, "suffrages_exprimes": 16293},
            {
                "ATEKI SETA CAXTON": {"votes": 7, "percentage": 0.04},
                "BELLO BOUBA MAIGARI": {"votes": 50, "percentage": 0.31},
                "BIYA PAUL": {"votes": 13923, "percentage": 85.46},
                "BOUGHA HAGBE JACQUES": {"votes": 2, "percentage": 0.01},
                "ISSA TCHIROMA": {"votes": 320, "percentage": 1.96},
                "IYODI HIRAM SAMUEL": {"votes": 7, "percentage": 0.04},
                "KWEMO PIERRE": {"votes": 1, "percentage": 0.01},
                "LIBII LI NGUE NGUE CABRAL": {"votes": 15, "percentage": 0.09},
                "MATOMBA SERGE ESPOIR": {"votes": 6, "percentage": 0.04},
                "MUNA AKERE TABENG": {"votes": 2, "percentage": 0.01},
                "OSIH JOSHUA NAMBANGI": {"votes": 1953, "percentage": 11.99},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 7, "percentage": 0.04}
            }
        )
        
        # Donga-Mantung
        self.insert_data(election, candidates, "Nord-Ouest", "Donga-Mantung",
            {"inscrits": 96778, "votants": 40630, "taux_participation": Decimal("41.98"),
             "taux_abstention": Decimal("58.02"), "bulletins_nuls": 508, "suffrages_exprimes": 40122},
            {
                "ATEKI SETA CAXTON": {"votes": 254, "percentage": 0.63},
                "BELLO BOUBA MAIGARI": {"votes": 1758, "percentage": 4.38},
                "BIYA PAUL": {"votes": 29219, "percentage": 72.83},
                "BOUGHA HAGBE JACQUES": {"votes": 58, "percentage": 0.14},
                "ISSA TCHIROMA": {"votes": 4806, "percentage": 11.98},
                "IYODI HIRAM SAMUEL": {"votes": 95, "percentage": 0.24},
                "KWEMO PIERRE": {"votes": 73, "percentage": 0.18},
                "LIBII LI NGUE NGUE CABRAL": {"votes": 253, "percentage": 0.63},
                "MATOMBA SERGE ESPOIR": {"votes": 137, "percentage": 0.34},
                "MUNA AKERE TABENG": {"votes": 426, "percentage": 1.06},
                "OSIH JOSHUA NAMBANGI": {"votes": 2760, "percentage": 6.88},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 283, "percentage": 0.71}
            }
        )
        
        # Menchum
        self.insert_data(election, candidates, "Nord-Ouest", "Menchum",
            {"inscrits": 52568, "votants": 10520, "taux_participation": Decimal("20.01"),
             "taux_abstention": Decimal("79.99"), "bulletins_nuls": 158, "suffrages_exprimes": 10362},
            {
                "ATEKI SETA CAXTON": {"votes": 151, "percentage": 1.46},
                "BELLO BOUBA MAIGARI": {"votes": 221, "percentage": 2.13},
                "BIYA PAUL": {"votes": 5517, "percentage": 53.24},
                "BOUGHA HAGBE JACQUES": {"votes": 53, "percentage": 0.51},
                "ISSA TCHIROMA": {"votes": 1972, "percentage": 19.03},
                "IYODI HIRAM SAMUEL": {"votes": 46, "percentage": 0.44},
                "KWEMO PIERRE": {"votes": 46, "percentage": 0.44},
                "LIBII LI NGUE NGUE CABRAL": {"votes": 44, "percentage": 0.43},
                "MATOMBA SERGE ESPOIR": {"votes": 154, "percentage": 1.49},
                "MUNA AKERE TABENG": {"votes": 29, "percentage": 0.28},
                "OSIH JOSHUA NAMBANGI": {"votes": 2072, "percentage": 20.00},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 57, "percentage": 0.55}
            }
        )
        
        # Mezam
        self.insert_data(election, candidates, "Nord-Ouest", "Mezam",
            {"inscrits": 208476, "votants": 169952, "taux_participation": Decimal("81.52"),
             "taux_abstention": Decimal("18.48"), "bulletins_nuls": 731, "suffrages_exprimes": 169221},
            {
                "ATEKI SETA CAXTON": {"votes": 71, "percentage": 0.04},
                "BELLO BOUBA MAIGARI": {"votes": 789, "percentage": 0.47},
                "BIYA PAUL": {"votes": 155885, "percentage": 92.12},
                "BOUGHA HAGBE JACQUES": {"votes": 73, "percentage": 0.04},
                "ISSA TCHIROMA": {"votes": 6447, "percentage": 3.81},
                "IYODI HIRAM SAMUEL": {"votes": 166, "percentage": 0.10},
                "KWEMO PIERRE": {"votes": 37, "percentage": 0.02},
                "LIBII LI NGUE NGUE CABRAL": {"votes": 197, "percentage": 0.12},
                "MATOMBA SERGE ESPOIR": {"votes": 79, "percentage": 0.05},
                "MUNA AKERE TABENG": {"votes": 160, "percentage": 0.09},
                "OSIH JOSHUA NAMBANGI": {"votes": 5213, "percentage": 3.08},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 104, "percentage": 0.06}
            }
        )
        
        # Momo
        self.insert_data(election, candidates, "Nord-Ouest", "Momo",
            {"inscrits": 57183, "votants": 26317, "taux_participation": Decimal("46.02"),
             "taux_abstention": Decimal("53.98"), "bulletins_nuls": 154, "suffrages_exprimes": 26163},
            {
                "ATEKI SETA CAXTON": {"votes": 15, "percentage": 0.06},
                "BELLO BOUBA MAIGARI": {"votes": 1044, "percentage": 3.99},
                "BIYA PAUL": {"votes": 21303, "percentage": 81.42},
                "BOUGHA HAGBE JACQUES": {"votes": 4, "percentage": 0.02},
                "ISSA TCHIROMA": {"votes": 738, "percentage": 2.82},
                "IYODI HIRAM SAMUEL": {"votes": 7, "percentage": 0.03},
                "KWEMO PIERRE": {"votes": 3, "percentage": 0.01},
                "LIBII LI NGUE NGUE CABRAL": {"votes": 19, "percentage": 0.07},
                "MATOMBA SERGE ESPOIR": {"votes": 13, "percentage": 0.05},
                "MUNA AKERE TABENG": {"votes": 8, "percentage": 0.03},
                "OSIH JOSHUA NAMBANGI": {"votes": 3004, "percentage": 11.48},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 5, "percentage": 0.02}
            }
        )
        
        # Ngo-Ketunjia
        self.insert_data(election, candidates, "Nord-Ouest", "Ngo-Ketunjia",
            {"inscrits": 52033, "votants": 24317, "taux_participation": Decimal("46.73"),
             "taux_abstention": Decimal("53.27"), "bulletins_nuls": 528, "suffrages_exprimes": 23789},
            {
                "ATEKI SETA CAXTON": {"votes": 7, "percentage": 0.03},
                "BELLO BOUBA MAIGARI": {"votes": 274, "percentage": 1.15},
                "BIYA PAUL": {"votes": 22727, "percentage": 95.54},
                "BOUGHA HAGBE JACQUES": {"votes": 14, "percentage": 0.06},
                "ISSA TCHIROMA": {"votes": 338, "percentage": 1.42},
                "IYODI HIRAM SAMUEL": {"votes": 14, "percentage": 0.06},
                "KWEMO PIERRE": {"votes": 10, "percentage": 0.04},
                "LIBII LI NGUE NGUE CABRAL": {"votes": 34, "percentage": 0.14},
                "MATOMBA SERGE ESPOIR": {"votes": 2, "percentage": 0.01},
                "MUNA AKERE TABENG": {"votes": 5, "percentage": 0.02},
                "OSIH JOSHUA NAMBANGI": {"votes": 345, "percentage": 1.45},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 19, "percentage": 0.08}
            }
        )
