"""
Correction des données incorrectes pour Djérem (Adamaoua) et Faro-et-Déo
Ces départements avaient reçu les mauvaises données lors de l'import
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from elections.models import Election
from departments.models import Department
from candidates.models import Candidat
from candidate_results.models import CandidateDepartmentResult


class Command(BaseCommand):
    help = "Corrige les données incorrectes de Djérem et Faro-et-Déo (Adamaoua)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("=" * 80))
        self.stdout.write(self.style.WARNING("CORRECTION DES DONNEES DJEREM ET FARO-ET-DEO"))
        self.stdout.write(self.style.WARNING("=" * 80))

        try:
            with transaction.atomic():
                election = Election.objects.get(date="2025-10-12")
                candidates = {c.name: c for c in Candidat.objects.filter(election=election)}
                
                self.fix_djerem(election, candidates)
                self.fix_faro_deo(election, candidates)
                
                self.stdout.write(self.style.SUCCESS("\n" + "=" * 80))
                self.stdout.write(self.style.SUCCESS("CORRECTION TERMINÉE!"))
                self.stdout.write(self.style.SUCCESS("=" * 80))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur: {e}"))
            raise

    def fix_djerem(self, election, candidates):
        """Corrige les données de Djérem (Adamaoua) - Page 4 PDF"""
        self.stdout.write("\n### CORRECTION DJEREM (Adamaoua) ###")
        
        # Données correctes du PDF page 4
        correct_data = {
            "ATEKI SETA CAXTON": {"suffrages": 304, "pourcentage": Decimal("1.12")},
            "BELLO BOUBA MAIGARI": {"suffrages": 2462, "pourcentage": Decimal("9.09")},
            "BIYA PAUL": {"suffrages": 9033, "pourcentage": Decimal("33.35")},
            "BOUGHA HAGBE JACQUES": {"suffrages": 111, "pourcentage": Decimal("0.41")},
            "ISSA TCHIROMA": {"suffrages": 13925, "pourcentage": Decimal("51.42")},
            "IYODI HIRAM SAMUEL": {"suffrages": 71, "pourcentage": Decimal("0.26")},
            "KWEMO PIERRE": {"suffrages": 132, "pourcentage": Decimal("0.49")},
            "LIBII LI NGUE NGUE CABRAL": {"suffrages": 391, "pourcentage": Decimal("1.44")},
            "MATOMBA SERGE ESPOIR": {"suffrages": 122, "pourcentage": Decimal("0.45")},
            "MUNA AKERE TABENG": {"suffrages": 126, "pourcentage": Decimal("0.47")},
            "OSIH JOSHUA NAMBANGI": {"suffrages": 155, "pourcentage": Decimal("0.57")},
            "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 252, "pourcentage": Decimal("0.93")},
        }
        
        dept = Department.objects.get(name="Djérem", region__name="Adamaoua")
        
        updated_count = 0
        for candidate_name, result_data in correct_data.items():
            candidate = candidates.get(candidate_name)
            if candidate:
                obj, created = CandidateDepartmentResult.objects.update_or_create(
                    election=election,
                    candidate=candidate,
                    department=dept,
                    defaults=result_data
                )
                if not created:
                    updated_count += 1
        
        total = sum([r["suffrages"] for r in correct_data.values()])
        self.stdout.write(self.style.SUCCESS(f"  ✓ Djérem corrigé: {updated_count} résultats mis à jour"))
        self.stdout.write(f"  Total: {total:,} suffrages (PDF: 27,084)")

    def fix_faro_deo(self, election, candidates):
        """Corrige les données de Faro-et-Déo (Adamaoua) - Page 4 PDF"""
        self.stdout.write("\n### CORRECTION FARO-ET-DEO (Adamaoua) ###")
        
        # Données correctes du PDF page 4
        correct_data = {
            "ATEKI SETA CAXTON": {"suffrages": 438, "pourcentage": Decimal("1.98")},
            "BELLO BOUBA MAIGARI": {"suffrages": 3706, "pourcentage": Decimal("16.71")},
            "BIYA PAUL": {"suffrages": 7330, "pourcentage": Decimal("33.06")},
            "BOUGHA HAGBE JACQUES": {"suffrages": 187, "pourcentage": Decimal("0.84")},
            "ISSA TCHIROMA": {"suffrages": 9551, "pourcentage": Decimal("43.07")},
            "IYODI HIRAM SAMUEL": {"suffrages": 84, "pourcentage": Decimal("0.38")},
            "KWEMO PIERRE": {"suffrages": 135, "pourcentage": Decimal("0.61")},
            "LIBII LI NGUE NGUE CABRAL": {"suffrages": 142, "pourcentage": Decimal("0.64")},
            "MATOMBA SERGE ESPOIR": {"suffrages": 114, "pourcentage": Decimal("0.51")},
            "MUNA AKERE TABENG": {"suffrages": 118, "pourcentage": Decimal("0.53")},
            "OSIH JOSHUA NAMBANGI": {"suffrages": 93, "pourcentage": Decimal("0.42")},
            "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"suffrages": 277, "pourcentage": Decimal("1.25")},
        }
        
        dept = Department.objects.get(name="Faro-et-Déo", region__name="Adamaoua")
        
        updated_count = 0
        for candidate_name, result_data in correct_data.items():
            candidate = candidates.get(candidate_name)
            if candidate:
                obj, created = CandidateDepartmentResult.objects.update_or_create(
                    election=election,
                    candidate=candidate,
                    department=dept,
                    defaults=result_data
                )
                if not created:
                    updated_count += 1
        
        total = sum([r["suffrages"] for r in correct_data.values()])
        self.stdout.write(self.style.SUCCESS(f"  ✓ Faro-et-Déo corrigé: {updated_count} résultats mis à jour"))
        self.stdout.write(f"  Total: {total:,} suffrages (PDF: 22,175)")
