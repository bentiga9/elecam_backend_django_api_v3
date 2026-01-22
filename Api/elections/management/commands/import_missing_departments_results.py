"""
Commande Django pour importer les résultats manquants de 20 départements
Données extraites du PDF officiel
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from elections.models import Election
from departments.models import Department
from candidates.models import Candidat
from candidate_results.models import CandidateDepartmentResult


class Command(BaseCommand):
    help = "Importe les résultats manquants pour 20 départements"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=" * 80))
        self.stdout.write(self.style.NOTICE("IMPORT DES RESULTATS MANQUANTS - 20 DEPARTEMENTS"))
        self.stdout.write(self.style.NOTICE("=" * 80))

        try:
            with transaction.atomic():
                election = Election.objects.get(date="2025-10-12")
                candidates = {c.name: c for c in Candidat.objects.filter(election=election)}
                
                # Import par région
                self.import_est(election, candidates)
                self.import_nord(election, candidates)
                self.import_ouest(election, candidates)
                self.import_sud(election, candidates)
                self.import_sud_ouest(election, candidates)
                
                self.stdout.write(self.style.SUCCESS("\n" + "=" * 80))
                self.stdout.write(self.style.SUCCESS("IMPORT TERMINÉ AVEC SUCCÈS!"))
                self.stdout.write(self.style.SUCCESS("=" * 80))
                
                # Résumé
                total_results = CandidateDepartmentResult.objects.count()
                self.stdout.write(f"\nTotal résultats départementaux: {total_results}")

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

    def import_est(self, election, candidates):
        """Importe Lom-et-Djérem (Page 9 PDF)"""
        self.stdout.write("\n### RÉGION EST - Lom-et-Djérem ###")
        
        data = {
            "Lom-et-Djérem": {
                "ATEKI SETA CAXTON": {"suffrages": 569, "pourcentage": Decimal("0.66")},
                "BELLO BOUBA MAIGARI": {"suffrages": 2318, "pourcentage": Decimal("2.69")},
                "BIYA PAUL": {"suffrages": 39078, "pourcentage": Decimal("45.38")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 206, "pourcentage": Decimal("0.24")},
                "ISSA TCHIROMA": {"suffrages": 38554, "pourcentage": Decimal("44.77")},
                "IYODI HIRAM SAMUEL": {"suffrages": 362, "pourcentage": Decimal("0.42")},
                "KWEMO PIERRE": {"suffrages": 192, "pourcentage": Decimal("0.22")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 3391, "pourcentage": Decimal("3.94")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 391, "pourcentage": Decimal("0.45")},
                "MUNA AKERE TABENG": {"suffrages": 208, "pourcentage": Decimal("0.24")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 384, "pourcentage": Decimal("0.45")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 469, "pourcentage": Decimal("0.54")},
            }
        }
        
        self.import_region_data(election, candidates, "Est", data)

    def import_nord(self, election, candidates):
        """Importe Faro (Page 15 PDF)"""
        self.stdout.write("\n### RÉGION NORD - Faro ###")
        
        data = {
            "Faro": {
                "ATEKI SETA CAXTON": {"suffrages": 503, "pourcentage": Decimal("2.05")},
                "BELLO BOUBA MAIGARI": {"suffrages": 725, "pourcentage": Decimal("2.95")},
                "BIYA PAUL": {"suffrages": 15550, "pourcentage": Decimal("63.34")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 104, "pourcentage": Decimal("0.42")},
                "ISSA TCHIROMA": {"suffrages": 6527, "pourcentage": Decimal("26.59")},
                "IYODI HIRAM SAMUEL": {"suffrages": 103, "pourcentage": Decimal("0.42")},
                "KWEMO PIERRE": {"suffrages": 131, "pourcentage": Decimal("0.53")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 219, "pourcentage": Decimal("0.89")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 123, "pourcentage": Decimal("0.50")},
                "MUNA AKERE TABENG": {"suffrages": 111, "pourcentage": Decimal("0.45")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 109, "pourcentage": Decimal("0.45")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 345, "pourcentage": Decimal("1.41")},
            }
        }
        
        self.import_region_data(election, candidates, "Nord", data)

    def import_ouest(self, election, candidates):
        """Importe les 8 départements de l'Ouest (Pages 18-19 PDF)"""
        self.stdout.write("\n### RÉGION OUEST - 8 départements ###")
        
        data = {
            "Bamboutos": {
                "ATEKI SETA CAXTON": {"suffrages": 421, "pourcentage": Decimal("0.59")},
                "BELLO BOUBA MAIGARI": {"suffrages": 1477, "pourcentage": Decimal("2.08")},
                "BIYA PAUL": {"suffrages": 23997, "pourcentage": Decimal("33.81")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 205, "pourcentage": Decimal("0.29")},
                "ISSA TCHIROMA": {"suffrages": 40912, "pourcentage": Decimal("57.64")},
                "IYODI HIRAM SAMUEL": {"suffrages": 182, "pourcentage": Decimal("0.26")},
                "KWEMO PIERRE": {"suffrages": 245, "pourcentage": Decimal("0.35")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 632, "pourcentage": Decimal("0.89")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 505, "pourcentage": Decimal("0.71")},
                "MUNA AKERE TABENG": {"suffrages": 184, "pourcentage": Decimal("0.26")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 1454, "pourcentage": Decimal("2.05")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 762, "pourcentage": Decimal("1.07")},
            },
            "Haut-Nkam": {
                "ATEKI SETA CAXTON": {"suffrages": 206, "pourcentage": Decimal("0.55")},
                "BELLO BOUBA MAIGARI": {"suffrages": 685, "pourcentage": Decimal("1.83")},
                "BIYA PAUL": {"suffrages": 7382, "pourcentage": Decimal("19.69")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 109, "pourcentage": Decimal("0.29")},
                "ISSA TCHIROMA": {"suffrages": 27223, "pourcentage": Decimal("72.62")},
                "IYODI HIRAM SAMUEL": {"suffrages": 81, "pourcentage": Decimal("0.22")},
                "KWEMO PIERRE": {"suffrages": 493, "pourcentage": Decimal("1.31")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 359, "pourcentage": Decimal("0.96")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 261, "pourcentage": Decimal("0.70")},
                "MUNA AKERE TABENG": {"suffrages": 99, "pourcentage": Decimal("0.26")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 297, "pourcentage": Decimal("0.79")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 294, "pourcentage": Decimal("0.78")},
            },
            "Hauts-Plateaux": {
                "ATEKI SETA CAXTON": {"suffrages": 158, "pourcentage": Decimal("0.39")},
                "BELLO BOUBA MAIGARI": {"suffrages": 395, "pourcentage": Decimal("0.98")},
                "BIYA PAUL": {"suffrages": 28320, "pourcentage": Decimal("70.24")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 51, "pourcentage": Decimal("0.13")},
                "ISSA TCHIROMA": {"suffrages": 10246, "pourcentage": Decimal("25.41")},
                "IYODI HIRAM SAMUEL": {"suffrages": 45, "pourcentage": Decimal("0.11")},
                "KWEMO PIERRE": {"suffrages": 127, "pourcentage": Decimal("0.31")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 139, "pourcentage": Decimal("0.35")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 133, "pourcentage": Decimal("0.33")},
                "MUNA AKERE TABENG": {"suffrages": 44, "pourcentage": Decimal("0.11")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 403, "pourcentage": Decimal("1.00")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 258, "pourcentage": Decimal("0.64")},
            },
            "Koung-Khi": {
                "ATEKI SETA CAXTON": {"suffrages": 103, "pourcentage": Decimal("0.35")},
                "BELLO BOUBA MAIGARI": {"suffrages": 665, "pourcentage": Decimal("2.24")},
                "BIYA PAUL": {"suffrages": 17660, "pourcentage": Decimal("59.55")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 35, "pourcentage": Decimal("0.12")},
                "ISSA TCHIROMA": {"suffrages": 10315, "pourcentage": Decimal("34.78")},
                "IYODI HIRAM SAMUEL": {"suffrages": 39, "pourcentage": Decimal("0.13")},
                "KWEMO PIERRE": {"suffrages": 69, "pourcentage": Decimal("0.23")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 246, "pourcentage": Decimal("0.83")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 84, "pourcentage": Decimal("0.28")},
                "MUNA AKERE TABENG": {"suffrages": 42, "pourcentage": Decimal("0.14")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 225, "pourcentage": Decimal("0.76")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 175, "pourcentage": Decimal("0.59")},
            },
            "Menoua": {
                "ATEKI SETA CAXTON": {"suffrages": 509, "pourcentage": Decimal("0.57")},
                "BELLO BOUBA MAIGARI": {"suffrages": 1389, "pourcentage": Decimal("1.54")},
                "BIYA PAUL": {"suffrages": 39150, "pourcentage": Decimal("43.44")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 217, "pourcentage": Decimal("0.24")},
                "ISSA TCHIROMA": {"suffrages": 45057, "pourcentage": Decimal("49.99")},
                "IYODI HIRAM SAMUEL": {"suffrages": 281, "pourcentage": Decimal("0.31")},
                "KWEMO PIERRE": {"suffrages": 245, "pourcentage": Decimal("0.27")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 937, "pourcentage": Decimal("1.04")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 515, "pourcentage": Decimal("0.57")},
                "MUNA AKERE TABENG": {"suffrages": 235, "pourcentage": Decimal("0.26")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 854, "pourcentage": Decimal("0.95")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 736, "pourcentage": Decimal("0.82")},
            },
            "Mifi": {
                "ATEKI SETA CAXTON": {"suffrages": 276, "pourcentage": Decimal("0.30")},
                "BELLO BOUBA MAIGARI": {"suffrages": 1313, "pourcentage": Decimal("1.43")},
                "BIYA PAUL": {"suffrages": 12483, "pourcentage": Decimal("13.60")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 144, "pourcentage": Decimal("0.16")},
                "ISSA TCHIROMA": {"suffrages": 73220, "pourcentage": Decimal("79.79")},
                "IYODI HIRAM SAMUEL": {"suffrages": 393, "pourcentage": Decimal("0.43")},
                "KWEMO PIERRE": {"suffrages": 218, "pourcentage": Decimal("0.24")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 1159, "pourcentage": Decimal("1.26")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 360, "pourcentage": Decimal("0.39")},
                "MUNA AKERE TABENG": {"suffrages": 158, "pourcentage": Decimal("0.17")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 1509, "pourcentage": Decimal("1.65")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 535, "pourcentage": Decimal("0.58")},
            },
            "Ndé": {
                "ATEKI SETA CAXTON": {"suffrages": 146, "pourcentage": Decimal("0.29")},
                "BELLO BOUBA MAIGARI": {"suffrages": 445, "pourcentage": Decimal("0.89")},
                "BIYA PAUL": {"suffrages": 36168, "pourcentage": Decimal("72.59")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 90, "pourcentage": Decimal("0.18")},
                "ISSA TCHIROMA": {"suffrages": 11823, "pourcentage": Decimal("23.73")},
                "IYODI HIRAM SAMUEL": {"suffrages": 65, "pourcentage": Decimal("0.13")},
                "KWEMO PIERRE": {"suffrages": 171, "pourcentage": Decimal("0.34")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 247, "pourcentage": Decimal("0.50")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 147, "pourcentage": Decimal("0.30")},
                "MUNA AKERE TABENG": {"suffrages": 62, "pourcentage": Decimal("0.12")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 255, "pourcentage": Decimal("0.51")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 209, "pourcentage": Decimal("0.42")},
            },
            "Noun": {
                "ATEKI SETA CAXTON": {"suffrages": 430, "pourcentage": Decimal("0.38")},
                "BELLO BOUBA MAIGARI": {"suffrages": 1023, "pourcentage": Decimal("0.91")},
                "BIYA PAUL": {"suffrages": 36571, "pourcentage": Decimal("32.54")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 167, "pourcentage": Decimal("0.15")},
                "ISSA TCHIROMA": {"suffrages": 25519, "pourcentage": Decimal("22.71")},
                "IYODI HIRAM SAMUEL": {"suffrages": 153, "pourcentage": Decimal("0.14")},
                "KWEMO PIERRE": {"suffrages": 233, "pourcentage": Decimal("0.21")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 922, "pourcentage": Decimal("0.82")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 271, "pourcentage": Decimal("0.24")},
                "MUNA AKERE TABENG": {"suffrages": 132, "pourcentage": Decimal("0.12")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 620, "pourcentage": Decimal("0.55")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 46327, "pourcentage": Decimal("41.23")},
            },
        }
        
        self.import_region_data(election, candidates, "Ouest", data)

    def import_sud(self, election, candidates):
        """Importe les 4 départements du Sud (Pages 20-21 PDF)"""
        self.stdout.write("\n### RÉGION SUD - 4 départements ###")
        
        data = {
            "Dja-et-Lobo": {
                "ATEKI SETA CAXTON": {"suffrages": 5, "pourcentage": Decimal("0.01")},
                "BELLO BOUBA MAIGARI": {"suffrages": 29, "pourcentage": Decimal("0.03")},
                "BIYA PAUL": {"suffrages": 85774, "pourcentage": Decimal("97.72")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 10, "pourcentage": Decimal("0.01")},
                "ISSA TCHIROMA": {"suffrages": 1369, "pourcentage": Decimal("1.56")},
                "IYODI HIRAM SAMUEL": {"suffrages": 40, "pourcentage": Decimal("0.05")},
                "KWEMO PIERRE": {"suffrages": 8, "pourcentage": Decimal("0.01")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 444, "pourcentage": Decimal("0.51")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 13, "pourcentage": Decimal("0.01")},
                "MUNA AKERE TABENG": {"suffrages": 8, "pourcentage": Decimal("0.01")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 33, "pourcentage": Decimal("0.04")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 34, "pourcentage": Decimal("0.04")},
            },
            "Mvila": {
                "ATEKI SETA CAXTON": {"suffrages": 32, "pourcentage": Decimal("0.04")},
                "BELLO BOUBA MAIGARI": {"suffrages": 141, "pourcentage": Decimal("0.16")},
                "BIYA PAUL": {"suffrages": 82243, "pourcentage": Decimal("92.62")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 225, "pourcentage": Decimal("0.25")},
                "ISSA TCHIROMA": {"suffrages": 4055, "pourcentage": Decimal("4.57")},
                "IYODI HIRAM SAMUEL": {"suffrages": 113, "pourcentage": Decimal("0.13")},
                "KWEMO PIERRE": {"suffrages": 17, "pourcentage": Decimal("0.02")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 1644, "pourcentage": Decimal("1.85")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 39, "pourcentage": Decimal("0.04")},
                "MUNA AKERE TABENG": {"suffrages": 16, "pourcentage": Decimal("0.02")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 187, "pourcentage": Decimal("0.21")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 79, "pourcentage": Decimal("0.09")},
            },
            "Océan": {
                "ATEKI SETA CAXTON": {"suffrages": 112, "pourcentage": Decimal("0.14")},
                "BELLO BOUBA MAIGARI": {"suffrages": 268, "pourcentage": Decimal("0.34")},
                "BIYA PAUL": {"suffrages": 65361, "pourcentage": Decimal("81.85")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 35, "pourcentage": Decimal("0.04")},
                "ISSA TCHIROMA": {"suffrages": 9604, "pourcentage": Decimal("12.03")},
                "IYODI HIRAM SAMUEL": {"suffrages": 231, "pourcentage": Decimal("0.29")},
                "KWEMO PIERRE": {"suffrages": 32, "pourcentage": Decimal("0.04")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 3355, "pourcentage": Decimal("4.20")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 129, "pourcentage": Decimal("0.16")},
                "MUNA AKERE TABENG": {"suffrages": 58, "pourcentage": Decimal("0.07")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 493, "pourcentage": Decimal("0.62")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 178, "pourcentage": Decimal("0.22")},
            },
            "Vallée-du-Ntem": {
                "ATEKI SETA CAXTON": {"suffrages": 24, "pourcentage": Decimal("0.08")},
                "BELLO BOUBA MAIGARI": {"suffrages": 104, "pourcentage": Decimal("0.34")},
                "BIYA PAUL": {"suffrages": 27071, "pourcentage": Decimal("89.54")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 11, "pourcentage": Decimal("0.04")},
                "ISSA TCHIROMA": {"suffrages": 2179, "pourcentage": Decimal("7.21")},
                "IYODI HIRAM SAMUEL": {"suffrages": 25, "pourcentage": Decimal("0.08")},
                "KWEMO PIERRE": {"suffrages": 7, "pourcentage": Decimal("0.02")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 522, "pourcentage": Decimal("1.73")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 17, "pourcentage": Decimal("0.06")},
                "MUNA AKERE TABENG": {"suffrages": 9, "pourcentage": Decimal("0.03")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 59, "pourcentage": Decimal("0.19")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 205, "pourcentage": Decimal("0.68")},
            },
        }
        
        self.import_region_data(election, candidates, "Sud", data)

    def import_sud_ouest(self, election, candidates):
        """Importe les 6 départements du Sud-Ouest (Pages 22-23 PDF)"""
        self.stdout.write("\n### RÉGION SUD-OUEST - 6 départements ###")
        
        data = {
            "Fako": {
                "ATEKI SETA CAXTON": {"suffrages": 164, "pourcentage": Decimal("0.27")},
                "BELLO BOUBA MAIGARI": {"suffrages": 1166, "pourcentage": Decimal("1.93")},
                "BIYA PAUL": {"suffrages": 22057, "pourcentage": Decimal("36.47")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 86, "pourcentage": Decimal("0.14")},
                "ISSA TCHIROMA": {"suffrages": 30349, "pourcentage": Decimal("50.18")},
                "IYODI HIRAM SAMUEL": {"suffrages": 342, "pourcentage": Decimal("0.56")},
                "KWEMO PIERRE": {"suffrages": 84, "pourcentage": Decimal("0.14")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 1333, "pourcentage": Decimal("2.20")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 295, "pourcentage": Decimal("0.49")},
                "MUNA AKERE TABENG": {"suffrages": 302, "pourcentage": Decimal("0.50")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 4107, "pourcentage": Decimal("6.79")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 198, "pourcentage": Decimal("0.33")},
            },
            "Koupé-Manengouba": {
                "ATEKI SETA CAXTON": {"suffrages": 71, "pourcentage": Decimal("0.31")},
                "BELLO BOUBA MAIGARI": {"suffrages": 400, "pourcentage": Decimal("1.74")},
                "BIYA PAUL": {"suffrages": 17197, "pourcentage": Decimal("74.96")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 74, "pourcentage": Decimal("0.32")},
                "ISSA TCHIROMA": {"suffrages": 4365, "pourcentage": Decimal("19.03")},
                "IYODI HIRAM SAMUEL": {"suffrages": 45, "pourcentage": Decimal("0.20")},
                "KWEMO PIERRE": {"suffrages": 22, "pourcentage": Decimal("0.10")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 99, "pourcentage": Decimal("0.43")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 56, "pourcentage": Decimal("0.24")},
                "MUNA AKERE TABENG": {"suffrages": 43, "pourcentage": Decimal("0.19")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 500, "pourcentage": Decimal("2.18")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 69, "pourcentage": Decimal("0.30")},
            },
            "Lebialem": {
                "ATEKI SETA CAXTON": {"suffrages": 81, "pourcentage": Decimal("0.92")},
                "BELLO BOUBA MAIGARI": {"suffrages": 188, "pourcentage": Decimal("2.13")},
                "BIYA PAUL": {"suffrages": 6050, "pourcentage": Decimal("68.58")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 64, "pourcentage": Decimal("0.72")},
                "ISSA TCHIROMA": {"suffrages": 1811, "pourcentage": Decimal("20.53")},
                "IYODI HIRAM SAMUEL": {"suffrages": 44, "pourcentage": Decimal("0.50")},
                "KWEMO PIERRE": {"suffrages": 52, "pourcentage": Decimal("0.59")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 90, "pourcentage": Decimal("1.02")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 59, "pourcentage": Decimal("0.67")},
                "MUNA AKERE TABENG": {"suffrages": 80, "pourcentage": Decimal("0.91")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 220, "pourcentage": Decimal("2.49")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 83, "pourcentage": Decimal("0.94")},
            },
            "Manyu": {
                "ATEKI SETA CAXTON": {"suffrages": 46, "pourcentage": Decimal("0.12")},
                "BELLO BOUBA MAIGARI": {"suffrages": 98, "pourcentage": Decimal("0.26")},
                "BIYA PAUL": {"suffrages": 34186, "pourcentage": Decimal("91.70")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 22, "pourcentage": Decimal("0.06")},
                "ISSA TCHIROMA": {"suffrages": 2285, "pourcentage": Decimal("6.13")},
                "IYODI HIRAM SAMUEL": {"suffrages": 26, "pourcentage": Decimal("0.07")},
                "KWEMO PIERRE": {"suffrages": 16, "pourcentage": Decimal("0.04")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 73, "pourcentage": Decimal("0.20")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 55, "pourcentage": Decimal("0.15")},
                "MUNA AKERE TABENG": {"suffrages": 21, "pourcentage": Decimal("0.06")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 412, "pourcentage": Decimal("1.11")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 38, "pourcentage": Decimal("0.10")},
            },
            "Meme": {
                "ATEKI SETA CAXTON": {"suffrages": 66, "pourcentage": Decimal("0.19")},
                "BELLO BOUBA MAIGARI": {"suffrages": 232, "pourcentage": Decimal("0.67")},
                "BIYA PAUL": {"suffrages": 23133, "pourcentage": Decimal("67.21")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 44, "pourcentage": Decimal("0.13")},
                "ISSA TCHIROMA": {"suffrages": 6136, "pourcentage": Decimal("17.83")},
                "IYODI HIRAM SAMUEL": {"suffrages": 39, "pourcentage": Decimal("0.11")},
                "KWEMO PIERRE": {"suffrages": 36, "pourcentage": Decimal("0.11")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 82, "pourcentage": Decimal("0.24")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 77, "pourcentage": Decimal("0.22")},
                "MUNA AKERE TABENG": {"suffrages": 102, "pourcentage": Decimal("0.30")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 4400, "pourcentage": Decimal("12.78")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 73, "pourcentage": Decimal("0.21")},
            },
            "Ndian": {
                "ATEKI SETA CAXTON": {"suffrages": 0, "pourcentage": Decimal("0")},
                "BELLO BOUBA MAIGARI": {"suffrages": 34, "pourcentage": Decimal("0.10")},
                "BIYA PAUL": {"suffrages": 33352, "pourcentage": Decimal("98.90")},
                "BOUGHA HAGBE JACQUES": {"suffrages": 0, "pourcentage": Decimal("0")},
                "ISSA TCHIROMA": {"suffrages": 101, "pourcentage": Decimal("0.30")},
                "IYODI HIRAM SAMUEL": {"suffrages": 0, "pourcentage": Decimal("0")},
                "KWEMO PIERRE": {"suffrages": 0, "pourcentage": Decimal("0")},
                "LIBII LI NGUE NGUE CABRAL": {"suffrages": 0, "pourcentage": Decimal("0")},
                "MATOMBA SERGE ESPOIR": {"suffrages": 0, "pourcentage": Decimal("0")},
                "MUNA AKERE TABENG": {"suffrages": 0, "pourcentage": Decimal("0")},
                "OSIH JOSHUA NAMBANGI": {"suffrages": 236, "pourcentage": Decimal("0.70")},
                "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 0, "pourcentage": Decimal("0")},
            },
        }
        
        self.import_region_data(election, candidates, "Sud-Ouest", data)

    def import_region_data(self, election, candidates, region_name, data):
        """Helper pour importer les données d'un département"""
        for dept_name, results in data.items():
            dept = self.find_department(dept_name, region_name)
            if not dept:
                continue
            
            created_count = 0
            for candidate_name, result_data in results.items():
                candidate = candidates.get(candidate_name)
                if candidate:
                    _, created = CandidateDepartmentResult.objects.update_or_create(
                        election=election,
                        candidate=candidate,
                        department=dept,
                        defaults=result_data
                    )
                    if created:
                        created_count += 1
            
            self.stdout.write(self.style.SUCCESS(f"  ✓ {dept.name}: {len(results)} résultats importés ({created_count} créés)"))
