"""
Commande Django pour importer les statistiques régionales de l'élection présidentielle 2025
Basé sur le PDF officiel: Resultats-Officiel-Election-Presidentiel-2025.pdf (page 33)
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from elections.models import Election
from regions.models import Region
from region_stats.models import RegionStat


class Command(BaseCommand):
    help = "Importe les statistiques régionales de l'élection présidentielle 2025"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Supprime les statistiques régionales existantes avant import',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            "Début de l'importation des statistiques régionales..."
        ))

        if options['clear']:
            self.stdout.write("Suppression des statistiques régionales existantes...")
            RegionStat.objects.all().delete()

        try:
            with transaction.atomic():
                self._import_region_stats()
            
            self.stdout.write(self.style.SUCCESS(
                "✓ Importation des statistiques régionales terminée avec succès!"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"✗ Erreur lors de l'importation: {str(e)}"
            ))
            raise

    def _import_region_stats(self):
        """Importe les statistiques régionales depuis les données du PDF (page 33)"""
        
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

        # Données extraites du PDF - Page 33: RECAPITULATIF GENERAL
        regions_data = [
            {
                'name': 'ADAMAOUA',
                'code': 'AD',
                'inscrits': 511932,
                'votants': 232096,
                'taux_participation': Decimal('45.34'),
                'taux_abstention': Decimal('54.66'),
                'bulletins_nuls': 3096,
                'suffrages_exprimes': 229000
            },
            {
                'name': 'CENTRE',
                'code': 'CE',
                'inscrits': 1484347,
                'votants': 1036887,
                'taux_participation': Decimal('69.85'),
                'taux_abstention': Decimal('30.15'),
                'bulletins_nuls': 7258,
                'suffrages_exprimes': 1029629
            },
            {
                'name': 'EST',
                'code': 'ES',
                'inscrits': 394359,
                'votants': 263325,
                'taux_participation': Decimal('66.77'),
                'taux_abstention': Decimal('33.23'),
                'bulletins_nuls': 2724,
                'suffrages_exprimes': 260601
            },
            {
                'name': 'EXTREME-NORD',
                'code': 'EN',
                'inscrits': 1261595,
                'votants': 734662,
                'taux_participation': Decimal('58.23'),
                'taux_abstention': Decimal('41.77'),
                'bulletins_nuls': 17369,
                'suffrages_exprimes': 717293
            },
            {
                'name': 'LITTORAL',
                'code': 'LT',
                'inscrits': 1340024,
                'votants': 661382,
                'taux_participation': Decimal('49.36'),
                'taux_abstention': Decimal('50.64'),
                'bulletins_nuls': 5588,
                'suffrages_exprimes': 655794
            },
            {
                'name': 'NORD',
                'code': 'NO',
                'inscrits': 793505,
                'votants': 408917,
                'taux_participation': Decimal('51.53'),
                'taux_abstention': Decimal('48.47'),
                'bulletins_nuls': 9398,
                'suffrages_exprimes': 399519
            },
            {
                'name': 'NORD-OUEST',
                'code': 'NW',
                'inscrits': 628096,
                'votants': 297875,
                'taux_participation': Decimal('47.43'),
                'taux_abstention': Decimal('52.57'),
                'bulletins_nuls': 2210,
                'suffrages_exprimes': 295665
            },
            {
                'name': 'OUEST',
                'code': 'OU',
                'inscrits': 877580,
                'votants': 528969,
                'taux_participation': Decimal('60.28'),
                'taux_abstention': Decimal('39.72'),
                'bulletins_nuls': 6438,
                'suffrages_exprimes': 522531
            },
            {
                'name': 'SUD',
                'code': 'SU',
                'inscrits': 326329,
                'votants': 288098,
                'taux_participation': Decimal('88.28'),
                'taux_abstention': Decimal('11.72'),
                'bulletins_nuls': 1451,
                'suffrages_exprimes': 286647
            },
            {
                'name': 'SUD-OUEST',
                'code': 'SW',
                'inscrits': 430706,
                'votants': 199459,
                'taux_participation': Decimal('46.31'),
                'taux_abstention': Decimal('53.69'),
                'bulletins_nuls': 1792,
                'suffrages_exprimes': 197667
            },
        ]

        # Total Cameroun (national)
        total_cameroun = {
            'inscrits': 8048473,
            'votants': 4651670,
            'taux_participation': Decimal('57.80'),
            'taux_abstention': Decimal('42.20'),
            'bulletins_nuls': 57324,
            'suffrages_exprimes': 4594346
        }

        # Diaspora
        diaspora_data = {
            'name': 'DIASPORA',
            'code': 'DI',
            'inscrits': 34219,
            'votants': 16776,
            'taux_participation': Decimal('49.03'),
            'taux_abstention': Decimal('50.97'),
            'bulletins_nuls': 296,
            'suffrages_exprimes': 16480
        }

        stats_created = 0
        stats_updated = 0

        # Mapping des noms de régions (PDF -> Base de données)
        region_name_mapping = {
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
        }

        # Importer les statistiques des 10 régions nationales
        for region_data in regions_data:
            region_name_pdf = region_data['name']
            region_name_db = region_name_mapping.get(region_name_pdf, region_name_pdf)
            
            try:
                region = Region.objects.get(name=region_name_db, region_type='national')
            except Region.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"✗ Région '{region_name_db}' non trouvée dans la base de données!"
                ))
                continue

            # Créer ou mettre à jour les statistiques
            region_stat, created = RegionStat.objects.update_or_create(
                election=election,
                region=region,
                defaults={
                    'inscrits': region_data['inscrits'],
                    'votants': region_data['votants'],
                    'taux_participation': region_data['taux_participation'],
                    'taux_abstention': region_data['taux_abstention'],
                    'bulletins_nuls': region_data['bulletins_nuls'],
                    'suffrages_exprimes': region_data['suffrages_exprimes']
                }
            )

            if created:
                stats_created += 1
                self.stdout.write(self.style.SUCCESS(
                    f"  ✓ Créé: {region.name} - "
                    f"{region_data['inscrits']:,} inscrits, "
                    f"{region_data['votants']:,} votants ({region_data['taux_participation']}%)"
                ))
            else:
                stats_updated += 1
                self.stdout.write(self.style.SUCCESS(
                    f"  ↻ Mis à jour: {region.name}"
                ))

        # Importer les statistiques de la Diaspora (agrégées de toutes les zones)
        # Note: Dans la base, il y a 4 zones diaspora distinctes
        # Ici on va créer un total "Diaspora" si nécessaire ou ignorer
        self.stdout.write("\n" + self.style.WARNING(
            "Note: Les statistiques diaspora sont agrégées dans le PDF."
        ))
        self.stdout.write(self.style.WARNING(
            f"  Total Diaspora: {diaspora_data['inscrits']:,} inscrits, "
            f"{diaspora_data['votants']:,} votants ({diaspora_data['taux_participation']}%)"
        ))
        
        # On peut créer les stats pour chaque zone diaspora en répartissant proportionnellement
        # ou simplement ignorer pour le moment
        # Pour l'instant, on va juste afficher l'information
        diaspora_zones = Region.objects.filter(region_type='diaspora')
        self.stdout.write(f"  Zones diaspora dans la base: {diaspora_zones.count()}")
        for zone in diaspora_zones:
            self.stdout.write(f"    - {zone.name} ({zone.code})")
        
        # Skip diaspora individual region stats for now since PDF only has aggregate
        # The individual diaspora zone stats would need to be extracted from other pages

        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS(
            f"Résumé de l'importation:"
        ))
        self.stdout.write(f"  • Statistiques créées: {stats_created}")
        self.stdout.write(f"  • Statistiques mises à jour: {stats_updated}")
        self.stdout.write(f"  • Total: {stats_created + stats_updated} régions")
        self.stdout.write("\n" + f"TOTAL GÉNÉRAL (Cameroun + Diaspora):")
        self.stdout.write(f"  • Inscrits: {8082692:,}")
        self.stdout.write(f"  • Votants: {4668446:,}")
        self.stdout.write(f"  • Taux de participation: 57.76%")
        self.stdout.write(f"  • Bulletins nuls: {57620:,}")
        self.stdout.write(f"  • Suffrages exprimés: {4610826:,}")
        self.stdout.write("=" * 70)
