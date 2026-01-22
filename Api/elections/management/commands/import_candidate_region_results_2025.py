"""
Commande Django pour importer les résultats régionaux des candidats
Basé sur le PDF officiel: Resultats-Officiel-Election-Presidentiel-2025.pdf (page 34)
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from elections.models import Election
from regions.models import Region
from candidates.models import Candidat
from candidate_results.models import CandidateRegionResult


class Command(BaseCommand):
    help = "Importe les résultats régionaux des candidats de l'élection présidentielle 2025"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Supprime les résultats régionaux existants avant import',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            "Début de l'importation des résultats régionaux des candidats..."
        ))

        if options['clear']:
            self.stdout.write("Suppression des résultats régionaux existants...")
            CandidateRegionResult.objects.all().delete()

        try:
            with transaction.atomic():
                self._import_results()
            
            self.stdout.write(self.style.SUCCESS(
                "✓ Importation des résultats régionaux terminée avec succès!"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"✗ Erreur lors de l'importation: {str(e)}"
            ))
            raise

    def _import_results(self):
        """Importe les résultats régionaux depuis le PDF page 34"""
        
        # Récupérer l'élection
        try:
            election = Election.objects.get(
                title="Élection Présidentielle 2025",
                date="2025-10-12"
            )
        except Election.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "L'élection présidentielle 2025 n'existe pas."
            ))
            return

        # Mapping des noms de régions
        region_mapping = {
            'ADAMAOUA': 'Adamaoua',
            'CENTRE': 'Centre',
            'EST': 'Est',
            'EXTREME-NORD': 'Extrême-Nord',
            'LITTORAL': 'Littoral',
            'NORD': 'Nord',
            'NORD-OUEST': 'Nord-Ouest',
            'OUEST': 'Ouest',
            'SUD': 'Sud',
            'SUD-OUEST': 'Sud-Ouest',
            'TOTAL CAMEROUN': None,  # Skip
            'DIASPORA': None,  # Traiter séparément
            'TOTAL GENERAL': None,  # Skip
        }

        # Données extraites du PDF - Page 34: SUFFRAGES EN FAVEUR DE CHAQUE CANDIDAT PAR RÉGION
        results_data = {
            'ATEKI SETA CAXTON': {
                'ADAMAOUA': {'suffrages': 2997, 'pourcentage': Decimal('1.31')},
                'CENTRE': {'suffrages': 1449, 'pourcentage': Decimal('0.14')},
                'EST': {'suffrages': 1678, 'pourcentage': Decimal('0.64')},
                'EXTREME-NORD': {'suffrages': 18873, 'pourcentage': Decimal('2.63')},
                'LITTORAL': {'suffrages': 1225, 'pourcentage': Decimal('0.19')},
                'NORD': {'suffrages': 10298, 'pourcentage': Decimal('2.58')},
                'NORD-OUEST': {'suffrages': 534, 'pourcentage': Decimal('0.18')},
                'OUEST': {'suffrages': 2249, 'pourcentage': Decimal('0.43')},
                'SUD': {'suffrages': 173, 'pourcentage': Decimal('0.06')},
                'SUD-OUEST': {'suffrages': 428, 'pourcentage': Decimal('0.22')},
            },
            'BELLO BOUBA MAIGARI': {
                'ADAMAOUA': {'suffrages': 19744, 'pourcentage': Decimal('8.62')},
                'CENTRE': {'suffrages': 4331, 'pourcentage': Decimal('0.42')},
                'EST': {'suffrages': 3833, 'pourcentage': Decimal('1.47')},
                'EXTREME-NORD': {'suffrages': 28778, 'pourcentage': Decimal('4.01')},
                'LITTORAL': {'suffrages': 6757, 'pourcentage': Decimal('1.03')},
                'NORD': {'suffrages': 33876, 'pourcentage': Decimal('8.48')},
                'NORD-OUEST': {'suffrages': 5325, 'pourcentage': Decimal('1.80')},
                'OUEST': {'suffrages': 7392, 'pourcentage': Decimal('1.41')},
                'SUD': {'suffrages': 542, 'pourcentage': Decimal('0.19')},
                'SUD-OUEST': {'suffrages': 2118, 'pourcentage': Decimal('1.07')},
            },
            'BIYA PAUL': {
                'ADAMAOUA': {'suffrages': 79256, 'pourcentage': Decimal('34.61')},
                'CENTRE': {'suffrages': 722153, 'pourcentage': Decimal('70.14')},
                'EST': {'suffrages': 192543, 'pourcentage': Decimal('73.88')},
                'EXTREME-NORD': {'suffrages': 329476, 'pourcentage': Decimal('45.93')},
                'LITTORAL': {'suffrages': 137679, 'pourcentage': Decimal('20.99')},
                'NORD': {'suffrages': 154926, 'pourcentage': Decimal('38.78')},
                'NORD-OUEST': {'suffrages': 255188, 'pourcentage': Decimal('86.31')},
                'OUEST': {'suffrages': 201731, 'pourcentage': Decimal('38.61')},
                'SUD': {'suffrages': 260449, 'pourcentage': Decimal('90.86')},
                'SUD-OUEST': {'suffrages': 135975, 'pourcentage': Decimal('68.79')},
            },
            'BOUGHA HAGBE JACQUES': {
                'ADAMAOUA': {'suffrages': 1216, 'pourcentage': Decimal('0.53')},
                'CENTRE': {'suffrages': 949, 'pourcentage': Decimal('0.09')},
                'EST': {'suffrages': 744, 'pourcentage': Decimal('0.29')},
                'EXTREME-NORD': {'suffrages': 4218, 'pourcentage': Decimal('0.59')},
                'LITTORAL': {'suffrages': 907, 'pourcentage': Decimal('0.14')},
                'NORD': {'suffrages': 3750, 'pourcentage': Decimal('0.94')},
                'NORD-OUEST': {'suffrages': 222, 'pourcentage': Decimal('0.08')},
                'OUEST': {'suffrages': 1018, 'pourcentage': Decimal('0.19')},
                'SUD': {'suffrages': 281, 'pourcentage': Decimal('0.10')},
                'SUD-OUEST': {'suffrages': 290, 'pourcentage': Decimal('0.15')},
            },
            'ISSA TCHIROMA': {
                'ADAMAOUA': {'suffrages': 115258, 'pourcentage': Decimal('50.33')},
                'CENTRE': {'suffrages': 222654, 'pourcentage': Decimal('21.62')},
                'EST': {'suffrages': 51660, 'pourcentage': Decimal('19.82')},
                'EXTREME-NORD': {'suffrages': 303669, 'pourcentage': Decimal('42.34')},
                'LITTORAL': {'suffrages': 423557, 'pourcentage': Decimal('64.59')},
                'NORD': {'suffrages': 173837, 'pourcentage': Decimal('43.51')},
                'NORD-OUEST': {'suffrages': 15392, 'pourcentage': Decimal('5.21')},
                'OUEST': {'suffrages': 244315, 'pourcentage': Decimal('46.76')},
                'SUD': {'suffrages': 17207, 'pourcentage': Decimal('6.00')},
                'SUD-OUEST': {'suffrages': 45047, 'pourcentage': Decimal('22.79')},
            },
            'IYODI HIRAM SAMUEL': {
                'ADAMAOUA': {'suffrages': 704, 'pourcentage': Decimal('0.31')},
                'CENTRE': {'suffrages': 4339, 'pourcentage': Decimal('0.42')},
                'EST': {'suffrages': 665, 'pourcentage': Decimal('0.26')},
                'EXTREME-NORD': {'suffrages': 2617, 'pourcentage': Decimal('0.36')},
                'LITTORAL': {'suffrages': 5206, 'pourcentage': Decimal('0.79')},
                'NORD': {'suffrages': 2550, 'pourcentage': Decimal('0.64')},
                'NORD-OUEST': {'suffrages': 367, 'pourcentage': Decimal('0.12')},
                'OUEST': {'suffrages': 1239, 'pourcentage': Decimal('0.24')},
                'SUD': {'suffrages': 409, 'pourcentage': Decimal('0.14')},
                'SUD-OUEST': {'suffrages': 496, 'pourcentage': Decimal('0.25')},
            },
            'KWEMO PIERRE': {
                'ADAMAOUA': {'suffrages': 939, 'pourcentage': Decimal('0.41')},
                'CENTRE': {'suffrages': 880, 'pourcentage': Decimal('0.09')},
                'EST': {'suffrages': 435, 'pourcentage': Decimal('0.17')},
                'EXTREME-NORD': {'suffrages': 3732, 'pourcentage': Decimal('0.52')},
                'LITTORAL': {'suffrages': 1756, 'pourcentage': Decimal('0.27')},
                'NORD': {'suffrages': 2857, 'pourcentage': Decimal('0.72')},
                'NORD-OUEST': {'suffrages': 187, 'pourcentage': Decimal('0.06')},
                'OUEST': {'suffrages': 1801, 'pourcentage': Decimal('0.34')},
                'SUD': {'suffrages': 64, 'pourcentage': Decimal('0.02')},
                'SUD-OUEST': {'suffrages': 210, 'pourcentage': Decimal('0.11')},
            },
            'LIBII LI NGUE NGUE CABRAL': {
                'ADAMAOUA': {'suffrages': 3414, 'pourcentage': Decimal('1.49')},
                'CENTRE': {'suffrages': 62118, 'pourcentage': Decimal('6.03')},
                'EST': {'suffrages': 6214, 'pourcentage': Decimal('2.38')},
                'EXTREME-NORD': {'suffrages': 7782, 'pourcentage': Decimal('1.08')},
                'LITTORAL': {'suffrages': 59447, 'pourcentage': Decimal('9.06')},
                'NORD': {'suffrages': 4451, 'pourcentage': Decimal('1.11')},
                'NORD-OUEST': {'suffrages': 593, 'pourcentage': Decimal('0.20')},
                'OUEST': {'suffrages': 4641, 'pourcentage': Decimal('0.89')},
                'SUD': {'suffrages': 5965, 'pourcentage': Decimal('2.08')},
                'SUD-OUEST': {'suffrages': 1677, 'pourcentage': Decimal('0.85')},
            },
            'MATOMBA SERGE ESPOIR': {
                'ADAMAOUA': {'suffrages': 1020, 'pourcentage': Decimal('0.45')},
                'CENTRE': {'suffrages': 2622, 'pourcentage': Decimal('0.25')},
                'EST': {'suffrages': 687, 'pourcentage': Decimal('0.26')},
                'EXTREME-NORD': {'suffrages': 2712, 'pourcentage': Decimal('0.38')},
                'LITTORAL': {'suffrages': 3363, 'pourcentage': Decimal('0.51')},
                'NORD': {'suffrages': 2068, 'pourcentage': Decimal('0.52')},
                'NORD-OUEST': {'suffrages': 409, 'pourcentage': Decimal('0.14')},
                'OUEST': {'suffrages': 2276, 'pourcentage': Decimal('0.44')},
                'SUD': {'suffrages': 198, 'pourcentage': Decimal('0.07')},
                'SUD-OUEST': {'suffrages': 542, 'pourcentage': Decimal('0.27')},
            },
            'MUNA AKERE TABENG': {
                'ADAMAOUA': {'suffrages': 864, 'pourcentage': Decimal('0.38')},
                'CENTRE': {'suffrages': 869, 'pourcentage': Decimal('0.08')},
                'EST': {'suffrages': 355, 'pourcentage': Decimal('0.14')},
                'EXTREME-NORD': {'suffrages': 2422, 'pourcentage': Decimal('0.34')},
                'LITTORAL': {'suffrages': 946, 'pourcentage': Decimal('0.14')},
                'NORD': {'suffrages': 2524, 'pourcentage': Decimal('0.63')},
                'NORD-OUEST': {'suffrages': 656, 'pourcentage': Decimal('0.22')},
                'OUEST': {'suffrages': 956, 'pourcentage': Decimal('0.18')},
                'SUD': {'suffrages': 91, 'pourcentage': Decimal('0.03')},
                'SUD-OUEST': {'suffrages': 548, 'pourcentage': Decimal('0.28')},
            },
            'OSIH JOSHUA NAMBANGI': {
                'ADAMAOUA': {'suffrages': 1307, 'pourcentage': Decimal('0.57')},
                'CENTRE': {'suffrages': 4436, 'pourcentage': Decimal('0.43')},
                'EST': {'suffrages': 784, 'pourcentage': Decimal('0.30')},
                'EXTREME-NORD': {'suffrages': 3517, 'pourcentage': Decimal('0.49')},
                'LITTORAL': {'suffrages': 10904, 'pourcentage': Decimal('1.66')},
                'NORD': {'suffrages': 2237, 'pourcentage': Decimal('0.56')},
                'NORD-OUEST': {'suffrages': 16292, 'pourcentage': Decimal('5.51')},
                'OUEST': {'suffrages': 5617, 'pourcentage': Decimal('1.07')},
                'SUD': {'suffrages': 772, 'pourcentage': Decimal('0.27')},
                'SUD-OUEST': {'suffrages': 9875, 'pourcentage': Decimal('5.00')},
            },
            'TOMAINO HERMINE PATRICIA épouse NDAM NJOYA': {
                'ADAMAOUA': {'suffrages': 2281, 'pourcentage': Decimal('1.00')},
                'CENTRE': {'suffrages': 2829, 'pourcentage': Decimal('0.27')},
                'EST': {'suffrages': 1003, 'pourcentage': Decimal('0.38')},
                'EXTREME-NORD': {'suffrages': 9497, 'pourcentage': Decimal('1.32')},
                'LITTORAL': {'suffrages': 4047, 'pourcentage': Decimal('0.62')},
                'NORD': {'suffrages': 6145, 'pourcentage': Decimal('1.54')},
                'NORD-OUEST': {'suffrages': 500, 'pourcentage': Decimal('0.17')},
                'OUEST': {'suffrages': 49296, 'pourcentage': Decimal('9.43')},
                'SUD': {'suffrages': 496, 'pourcentage': Decimal('0.17')},
                'SUD-OUEST': {'suffrages': 461, 'pourcentage': Decimal('0.23')},
            },
        }

        results_created = 0
        results_updated = 0
        results_skipped = 0

        # Importer les résultats
        for candidat_name, regions_results in results_data.items():
            try:
                candidat = Candidat.objects.get(name=candidat_name)
            except Candidat.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"✗ Candidat '{candidat_name}' non trouvé!"
                ))
                results_skipped += len(regions_results)
                continue

            for region_name_pdf, result_data in regions_results.items():
                region_name_db = region_mapping.get(region_name_pdf)
                
                if region_name_db is None:
                    continue  # Skip totaux et diaspora
                
                try:
                    region = Region.objects.get(name=region_name_db, region_type='national')
                except Region.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"✗ Région '{region_name_db}' non trouvée!"
                    ))
                    results_skipped += 1
                    continue

                # Créer ou mettre à jour le résultat
                result, created = CandidateRegionResult.objects.update_or_create(
                    election=election,
                    candidate=candidat,
                    region=region,
                    defaults={
                        'suffrages': result_data['suffrages'],
                        'pourcentage': result_data['pourcentage']
                    }
                )

                if created:
                    results_created += 1
                else:
                    results_updated += 1

        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("Résumé de l'importation:"))
        self.stdout.write(f"  • Résultats créés: {results_created}")
        self.stdout.write(f"  • Résultats mis à jour: {results_updated}")
        self.stdout.write(f"  • Résultats ignorés: {results_skipped}")
        self.stdout.write(f"  • Total: {results_created + results_updated}")
        self.stdout.write("=" * 70)
