"""
Commande Django pour importer les statistiques départementales de l'élection présidentielle 2025
Basé sur le PDF officiel: Resultats-Officiel-Election-Presidentiel-2025.pdf (pages 4-23)
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from elections.models import Election
from regions.models import Region
from departments.models import Department
from department_stats.models import DepartmentStat


class Command(BaseCommand):
    help = "Importe les statistiques départementales de l'élection présidentielle 2025"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Supprime les statistiques départementales existantes avant import',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            "Début de l'importation des statistiques départementales..."
        ))

        if options['clear']:
            self.stdout.write("Suppression des statistiques départementales existantes...")
            DepartmentStat.objects.all().delete()

        try:
            with transaction.atomic():
                self._import_department_stats()
            
            self.stdout.write(self.style.SUCCESS(
                "✓ Importation des statistiques départementales terminée avec succès!"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"✗ Erreur lors de l'importation: {str(e)}"
            ))
            raise

    def _import_department_stats(self):
        """Importe les statistiques départementales depuis les données du PDF"""
        
        # Récupérer l'élection présidentielle 2025
        try:
            election = Election.objects.get(
                title="Élection Présidentielle 2025",
                date="2025-10-12"
            )
        except Election.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "L'élection présidentielle 2025 n'existe pas. "
                "Veuillez d'abord exécuter: python manage.py import_election_2025"
            ))
            return

        # Données extraites du PDF - Toutes les régions
        departments_data = []
        
        # RÉGION ADAMAOUA (Page 4)
        departments_data.extend([
            {'region': 'Adamaoua', 'name': 'Djérem', 'inscrits': 63683, 'votants': 27426, 'taux_participation': Decimal('43.07'), 'taux_abstention': Decimal('56.93'), 'bulletins_nuls': 342, 'suffrages_exprimes': 27084},
            {'region': 'Adamaoua', 'name': 'Faro-et-Déo', 'inscrits': 45265, 'votants': 22460, 'taux_participation': Decimal('49.62'), 'taux_abstention': Decimal('50.38'), 'bulletins_nuls': 285, 'suffrages_exprimes': 22175},
            {'region': 'Adamaoua', 'name': 'Mayo-Banyo', 'inscrits': 82424, 'votants': 36690, 'taux_participation': Decimal('44.51'), 'taux_abstention': Decimal('55.49'), 'bulletins_nuls': 631, 'suffrages_exprimes': 36059},
            {'region': 'Adamaoua', 'name': 'Mbéré', 'inscrits': 81656, 'votants': 38866, 'taux_participation': Decimal('47.60'), 'taux_abstention': Decimal('52.40'), 'bulletins_nuls': 541, 'suffrages_exprimes': 38325},
            {'region': 'Adamaoua', 'name': 'Vina', 'inscrits': 238904, 'votants': 106654, 'taux_participation': Decimal('44.64'), 'taux_abstention': Decimal('55.36'), 'bulletins_nuls': 1297, 'suffrages_exprimes': 105357},
        ])
        
        # RÉGION CENTRE (Page 6)
        departments_data.extend([
            {'region': 'Centre', 'name': 'Haute-Sanaga', 'inscrits': 60701, 'votants': 57560, 'taux_participation': Decimal('94.83'), 'taux_abstention': Decimal('5.17'), 'bulletins_nuls': 272, 'suffrages_exprimes': 57288},
            {'region': 'Centre', 'name': 'Lékié', 'inscrits': 160527, 'votants': 148985, 'taux_participation': Decimal('92.81'), 'taux_abstention': Decimal('7.19'), 'bulletins_nuls': 1014, 'suffrages_exprimes': 147971},
            {'region': 'Centre', 'name': 'Mbam-et-Inoubou', 'inscrits': 94177, 'votants': 85872, 'taux_participation': Decimal('91.18'), 'taux_abstention': Decimal('8.82'), 'bulletins_nuls': 785, 'suffrages_exprimes': 85087},
            {'region': 'Centre', 'name': 'Mbam-et-Kim', 'inscrits': 65022, 'votants': 60333, 'taux_participation': Decimal('92.79'), 'taux_abstention': Decimal('7.21'), 'bulletins_nuls': 473, 'suffrages_exprimes': 59860},
            {'region': 'Centre', 'name': 'Méfou-et-Afamba', 'inscrits': 112313, 'votants': 105425, 'taux_participation': Decimal('93.87'), 'taux_abstention': Decimal('6.13'), 'bulletins_nuls': 663, 'suffrages_exprimes': 104762},
            {'region': 'Centre', 'name': 'Méfou-et-Akono', 'inscrits': 46103, 'votants': 31173, 'taux_participation': Decimal('67.62'), 'taux_abstention': Decimal('32.38'), 'bulletins_nuls': 294, 'suffrages_exprimes': 30879},
            {'region': 'Centre', 'name': 'Mfoundi', 'inscrits': 771503, 'votants': 393708, 'taux_participation': Decimal('51.03'), 'taux_abstention': Decimal('48.97'), 'bulletins_nuls': 3068, 'suffrages_exprimes': 390640},
            {'region': 'Centre', 'name': 'Nyong-et-Kellé', 'inscrits': 62917, 'votants': 57255, 'taux_participation': Decimal('91.00'), 'taux_abstention': Decimal('9.00'), 'bulletins_nuls': 231, 'suffrages_exprimes': 57024},
            {'region': 'Centre', 'name': 'Nyong-et-Mfoumou', 'inscrits': 50190, 'votants': 39955, 'taux_participation': Decimal('79.61'), 'taux_abstention': Decimal('20.39'), 'bulletins_nuls': 134, 'suffrages_exprimes': 39821},
            {'region': 'Centre', 'name': "Nyong-et-So'o", 'inscrits': 60894, 'votants': 56621, 'taux_participation': Decimal('92.98'), 'taux_abstention': Decimal('7.02'), 'bulletins_nuls': 324, 'suffrages_exprimes': 56297},
        ])
        
        # RÉGION EST (Page 9)
        departments_data.extend([
            {'region': 'Est', 'name': 'Boumba-et-Ngoko', 'inscrits': 44931, 'votants': 27423, 'taux_participation': Decimal('61.03'), 'taux_abstention': Decimal('38.97'), 'bulletins_nuls': 319, 'suffrages_exprimes': 27104},
            {'region': 'Est', 'name': 'Haut-Nyong', 'inscrits': 93665, 'votants': 73840, 'taux_participation': Decimal('78.83'), 'taux_abstention': Decimal('21.17'), 'bulletins_nuls': 454, 'suffrages_exprimes': 73386},
            {'region': 'Est', 'name': 'Kadey', 'inscrits': 76540, 'votants': 74647, 'taux_participation': Decimal('97.53'), 'taux_abstention': Decimal('2.47'), 'bulletins_nuls': 658, 'suffrages_exprimes': 73989},
            {'region': 'Est', 'name': 'Lom-et-Djérem', 'inscrits': 179223, 'votants': 87415, 'taux_participation': Decimal('48.77'), 'taux_abstention': Decimal('51.23'), 'bulletins_nuls': 1293, 'suffrages_exprimes': 86122},
        ])
        
        # RÉGION EXTRÊME-NORD (Page 11)
        departments_data.extend([
            {'region': 'Extrême-Nord', 'name': 'Diamaré', 'inscrits': 305771, 'votants': 169046, 'taux_participation': Decimal('55.29'), 'taux_abstention': Decimal('44.71'), 'bulletins_nuls': 3479, 'suffrages_exprimes': 165567},
            {'region': 'Extrême-Nord', 'name': 'Logone-et-Chari', 'inscrits': 215294, 'votants': 122890, 'taux_participation': Decimal('57.08'), 'taux_abstention': Decimal('42.92'), 'bulletins_nuls': 2983, 'suffrages_exprimes': 119907},
            {'region': 'Extrême-Nord', 'name': 'Mayo-Danay', 'inscrits': 218740, 'votants': 142416, 'taux_participation': Decimal('65.11'), 'taux_abstention': Decimal('34.89'), 'bulletins_nuls': 3058, 'suffrages_exprimes': 139358},
            {'region': 'Extrême-Nord', 'name': 'Mayo-Kani', 'inscrits': 158265, 'votants': 98313, 'taux_participation': Decimal('62.12'), 'taux_abstention': Decimal('37.88'), 'bulletins_nuls': 2348, 'suffrages_exprimes': 95965},
            {'region': 'Extrême-Nord', 'name': 'Mayo-Sava', 'inscrits': 146095, 'votants': 88373, 'taux_participation': Decimal('60.49'), 'taux_abstention': Decimal('39.51'), 'bulletins_nuls': 2169, 'suffrages_exprimes': 86204},
            {'region': 'Extrême-Nord', 'name': 'Mayo-Tsanaga', 'inscrits': 217430, 'votants': 113624, 'taux_participation': Decimal('52.26'), 'taux_abstention': Decimal('47.74'), 'bulletins_nuls': 3332, 'suffrages_exprimes': 110292},
        ])
        
        # RÉGION LITTORAL (Page 13)
        departments_data.extend([
            {'region': 'Littoral', 'name': 'Moungo', 'inscrits': 234020, 'votants': 121101, 'taux_participation': Decimal('51.75'), 'taux_abstention': Decimal('48.25'), 'bulletins_nuls': 1240, 'suffrages_exprimes': 119861},
            {'region': 'Littoral', 'name': 'Nkam', 'inscrits': 27339, 'votants': 14846, 'taux_participation': Decimal('54.30'), 'taux_abstention': Decimal('45.70'), 'bulletins_nuls': 220, 'suffrages_exprimes': 14626},
            {'region': 'Littoral', 'name': 'Sanaga-Maritime', 'inscrits': 100710, 'votants': 50734, 'taux_participation': Decimal('50.38'), 'taux_abstention': Decimal('49.62'), 'bulletins_nuls': 546, 'suffrages_exprimes': 50188},
            {'region': 'Littoral', 'name': 'Wouri', 'inscrits': 977955, 'votants': 474701, 'taux_participation': Decimal('48.54'), 'taux_abstention': Decimal('51.46'), 'bulletins_nuls': 3582, 'suffrages_exprimes': 471119},
        ])
        
        # RÉGION NORD (Page 15)
        departments_data.extend([
            {'region': 'Nord', 'name': 'Bénoué', 'inscrits': 423422, 'votants': 198943, 'taux_participation': Decimal('46.98'), 'taux_abstention': Decimal('53.02'), 'bulletins_nuls': 4685, 'suffrages_exprimes': 194258},
            {'region': 'Nord', 'name': 'Faro', 'inscrits': 39057, 'votants': 25026, 'taux_participation': Decimal('64.08'), 'taux_abstention': Decimal('35.92'), 'bulletins_nuls': 476, 'suffrages_exprimes': 24550},
            {'region': 'Nord', 'name': 'Mayo-Louti', 'inscrits': 173359, 'votants': 90404, 'taux_participation': Decimal('52.15'), 'taux_abstention': Decimal('47.85'), 'bulletins_nuls': 1982, 'suffrages_exprimes': 88422},
            {'region': 'Nord', 'name': 'Mayo-Rey', 'inscrits': 157667, 'votants': 94544, 'taux_participation': Decimal('59.96'), 'taux_abstention': Decimal('40.04'), 'bulletins_nuls': 2255, 'suffrages_exprimes': 92289},
        ])
        
        # RÉGION NORD-OUEST (Page 16)
        departments_data.extend([
            {'region': 'Nord-Ouest', 'name': 'Boyo', 'inscrits': 56828, 'votants': 9775, 'taux_participation': Decimal('17.20'), 'taux_abstention': Decimal('82.80'), 'bulletins_nuls': 60, 'suffrages_exprimes': 9715},
            {'region': 'Nord-Ouest', 'name': 'Bui', 'inscrits': 104230, 'votants': 16364, 'taux_participation': Decimal('15.70'), 'taux_abstention': Decimal('84.30'), 'bulletins_nuls': 71, 'suffrages_exprimes': 16293},
            {'region': 'Nord-Ouest', 'name': 'Donga-Mantung', 'inscrits': 96778, 'votants': 40630, 'taux_participation': Decimal('41.98'), 'taux_abstention': Decimal('58.02'), 'bulletins_nuls': 508, 'suffrages_exprimes': 40122},
            {'region': 'Nord-Ouest', 'name': 'Menchum', 'inscrits': 52568, 'votants': 10520, 'taux_participation': Decimal('20.01'), 'taux_abstention': Decimal('79.99'), 'bulletins_nuls': 158, 'suffrages_exprimes': 10362},
            {'region': 'Nord-Ouest', 'name': 'Mezam', 'inscrits': 208476, 'votants': 169952, 'taux_participation': Decimal('81.52'), 'taux_abstention': Decimal('18.48'), 'bulletins_nuls': 731, 'suffrages_exprimes': 169221},
            {'region': 'Nord-Ouest', 'name': 'Momo', 'inscrits': 57183, 'votants': 26317, 'taux_participation': Decimal('46.02'), 'taux_abstention': Decimal('53.98'), 'bulletins_nuls': 154, 'suffrages_exprimes': 26163},
            {'region': 'Nord-Ouest', 'name': 'Ngo-Ketunjia', 'inscrits': 52033, 'votants': 24317, 'taux_participation': Decimal('46.73'), 'taux_abstention': Decimal('53.27'), 'bulletins_nuls': 528, 'suffrages_exprimes': 23789},
        ])
        
        # RÉGION OUEST (Page 18)
        departments_data.extend([
            {'region': 'Ouest', 'name': 'Bamboutos', 'inscrits': 118275, 'votants': 71802, 'taux_participation': Decimal('60.71'), 'taux_abstention': Decimal('39.29'), 'bulletins_nuls': 826, 'suffrages_exprimes': 70976},
            {'region': 'Ouest', 'name': 'Haut-Nkam', 'inscrits': 57244, 'votants': 37858, 'taux_participation': Decimal('66.13'), 'taux_abstention': Decimal('33.87'), 'bulletins_nuls': 369, 'suffrages_exprimes': 37489},
            {'region': 'Ouest', 'name': 'Hauts-Plateaux', 'inscrits': 44765, 'votants': 41023, 'taux_participation': Decimal('91.64'), 'taux_abstention': Decimal('8.36'), 'bulletins_nuls': 704, 'suffrages_exprimes': 40319},
            {'region': 'Ouest', 'name': 'Koung-Khi', 'inscrits': 41549, 'votants': 30050, 'taux_participation': Decimal('72.32'), 'taux_abstention': Decimal('27.68'), 'bulletins_nuls': 392, 'suffrages_exprimes': 29658},
            {'region': 'Ouest', 'name': 'Menoua', 'inscrits': 145128, 'votants': 90951, 'taux_participation': Decimal('62.67'), 'taux_abstention': Decimal('37.33'), 'bulletins_nuls': 826, 'suffrages_exprimes': 90125},
            {'region': 'Ouest', 'name': 'Mifi', 'inscrits': 178163, 'votants': 92697, 'taux_participation': Decimal('52.03'), 'taux_abstention': Decimal('47.97'), 'bulletins_nuls': 929, 'suffrages_exprimes': 91768},
            {'region': 'Ouest', 'name': 'Ndé', 'inscrits': 71160, 'votants': 50388, 'taux_participation': Decimal('70.81'), 'taux_abstention': Decimal('29.19'), 'bulletins_nuls': 560, 'suffrages_exprimes': 49828},
            {'region': 'Ouest', 'name': 'Noun', 'inscrits': 221296, 'votants': 114200, 'taux_participation': Decimal('51.61'), 'taux_abstention': Decimal('48.39'), 'bulletins_nuls': 1832, 'suffrages_exprimes': 112368},
        ])
        
        # RÉGION SUD (Page 20)
        departments_data.extend([
            {'region': 'Sud', 'name': 'Dja-et-Lobo', 'inscrits': 98288, 'votants': 87939, 'taux_participation': Decimal('89.47'), 'taux_abstention': Decimal('10.53'), 'bulletins_nuls': 172, 'suffrages_exprimes': 87767},
            {'region': 'Sud', 'name': 'Mvila', 'inscrits': 93788, 'votants': 89117, 'taux_participation': Decimal('95.02'), 'taux_abstention': Decimal('4.98'), 'bulletins_nuls': 326, 'suffrages_exprimes': 88791},
            {'region': 'Sud', 'name': 'Océan', 'inscrits': 93177, 'votants': 80641, 'taux_participation': Decimal('86.55'), 'taux_abstention': Decimal('13.45'), 'bulletins_nuls': 785, 'suffrages_exprimes': 79856},
            {'region': 'Sud', 'name': 'Vallée-du-Ntem', 'inscrits': 41076, 'votants': 30401, 'taux_participation': Decimal('74.01'), 'taux_abstention': Decimal('25.99'), 'bulletins_nuls': 168, 'suffrages_exprimes': 30233},
        ])
        
        # RÉGION SUD-OUEST (Page 22)
        departments_data.extend([
            {'region': 'Sud-Ouest', 'name': 'Fako', 'inscrits': 182746, 'votants': 61489, 'taux_participation': Decimal('33.65'), 'taux_abstention': Decimal('66.35'), 'bulletins_nuls': 1006, 'suffrages_exprimes': 60483},
            {'region': 'Sud-Ouest', 'name': 'Koupé-Manengouba', 'inscrits': 38420, 'votants': 23036, 'taux_participation': Decimal('59.96'), 'taux_abstention': Decimal('40.04'), 'bulletins_nuls': 95, 'suffrages_exprimes': 22941},
            {'region': 'Sud-Ouest', 'name': 'Lebialem', 'inscrits': 22499, 'votants': 8976, 'taux_participation': Decimal('39.90'), 'taux_abstention': Decimal('60.10'), 'bulletins_nuls': 154, 'suffrages_exprimes': 8822},
            {'region': 'Sud-Ouest', 'name': 'Manyu', 'inscrits': 55228, 'votants': 37444, 'taux_participation': Decimal('67.80'), 'taux_abstention': Decimal('32.20'), 'bulletins_nuls': 166, 'suffrages_exprimes': 37278},
            {'region': 'Sud-Ouest', 'name': 'Meme', 'inscrits': 95082, 'votants': 34658, 'taux_participation': Decimal('36.45'), 'taux_abstention': Decimal('63.55'), 'bulletins_nuls': 238, 'suffrages_exprimes': 34420},
            {'region': 'Sud-Ouest', 'name': 'Ndian', 'inscrits': 36731, 'votants': 33856, 'taux_participation': Decimal('92.17'), 'taux_abstention': Decimal('7.83'), 'bulletins_nuls': 133, 'suffrages_exprimes': 33723},
        ])

        stats_created = 0
        stats_updated = 0
        stats_skipped = 0

        # Mapping des noms de régions
        region_name_mapping = {
            'Adamaoua': 'Adamaoua',
            'Centre': 'Centre',
            'Est': 'Est',
            'Extrême-Nord': 'Extrême-Nord',
            'Littoral': 'Littoral',
            'Nord': 'Nord',
            'Nord-Ouest': 'Nord-Ouest',
            'Ouest': 'Ouest',
            'Sud': 'Sud',
            'Sud-Ouest': 'Sud-Ouest',
        }

        # Importer les statistiques
        for dept_data in departments_data:
            region_name = region_name_mapping.get(dept_data['region'], dept_data['region'])
            dept_name = dept_data['name']
            
            try:
                department = Department.objects.get(name=dept_name)
            except Department.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"✗ Département '{dept_name}' non trouvé dans la base de données!"
                ))
                stats_skipped += 1
                continue

            # Créer ou mettre à jour les statistiques
            dept_stat, created = DepartmentStat.objects.update_or_create(
                election=election,
                department=department,
                defaults={
                    'inscrits': dept_data['inscrits'],
                    'votants': dept_data['votants'],
                    'taux_participation': dept_data['taux_participation'],
                    'taux_abstention': dept_data['taux_abstention'],
                    'bulletins_nuls': dept_data['bulletins_nuls'],
                    'suffrages_exprimes': dept_data['suffrages_exprimes']
                }
            )

            if created:
                stats_created += 1
                self.stdout.write(self.style.SUCCESS(
                    f"  ✓ Créé: {department.name} ({region_name}) - "
                    f"{dept_data['inscrits']:,} inscrits, {dept_data['votants']:,} votants ({dept_data['taux_participation']}%)"
                ))
            else:
                stats_updated += 1
                self.stdout.write(self.style.SUCCESS(
                    f"  ↻ Mis à jour: {department.name} ({region_name})"
                ))

        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS(
            f"Résumé de l'importation:"
        ))
        self.stdout.write(f"  • Statistiques créées: {stats_created}")
        self.stdout.write(f"  • Statistiques mises à jour: {stats_updated}")
        self.stdout.write(f"  • Départements ignorés: {stats_skipped}")
        self.stdout.write(f"  • Total: {stats_created + stats_updated} départements")
        self.stdout.write("=" * 70)
