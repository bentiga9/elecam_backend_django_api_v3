"""
Commande Django pour importer les statistiques diaspora de l'élection présidentielle 2025
Basé sur les données extraites du PDF officiel et calculées à partir des résultats par zone
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from elections.models import Election
from diaspora_stats.models import DiasporaStat
from candidate_results.models import CandidateRegionResult
from regions.models import Region


class Command(BaseCommand):
    help = 'Importe les statistiques diaspora pour l\'élection présidentielle 2025'

    def add_arguments(self, parser):
        parser.add_argument(
            '--election-id',
            type=int,
            default=None,
            help='ID de l\'élection (par défaut: dernière élection active)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('IMPORT DES STATISTIQUES DIASPORA - ÉLECTION PRÉSIDENTIELLE 2025'))
        self.stdout.write(self.style.SUCCESS('=' * 80))

        # Récupérer l'élection
        election_id = options.get('election_id')
        if election_id:
            try:
                election = Election.objects.get(id=election_id)
            except Election.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Élection avec ID {election_id} introuvable'))
                return
        else:
            election = Election.objects.filter(is_active=True).order_by('-date').first()
            if not election:
                self.stdout.write(self.style.ERROR('Aucune élection active trouvée'))
                return

        self.stdout.write(f'\nÉlection: {election.title} ({election.date})')

        # Données agrégées diaspora extraites du PDF (page 33)
        total_diaspora = {
            'inscrits': 34219,
            'votants': 16776,
            'taux_participation': Decimal('49.03'),
            'taux_abstention': Decimal('50.97'),
            'bulletins_nuls': 296,
            'suffrages_exprimes': 16480
        }

        self.stdout.write(f'\nTotal Diaspora (PDF):')
        self.stdout.write(f'  • Inscrits: {total_diaspora["inscrits"]:,}')
        self.stdout.write(f'  • Votants: {total_diaspora["votants"]:,}')
        self.stdout.write(f'  • Taux participation: {total_diaspora["taux_participation"]}%')
        self.stdout.write(f'  • Bulletins nuls: {total_diaspora["bulletins_nuls"]:,}')
        self.stdout.write(f'  • Suffrages exprimés: {total_diaspora["suffrages_exprimes"]:,}')

        # Récupérer les zones diaspora
        diaspora_zones = Region.objects.filter(region_type='diaspora', is_active=True).order_by('code')
        
        if diaspora_zones.count() != 4:
            self.stdout.write(self.style.WARNING(
                f'\nAttention: {diaspora_zones.count()} zones diaspora trouvées au lieu de 4'
            ))

        self.stdout.write(f'\nZones diaspora trouvées: {diaspora_zones.count()}')
        for zone in diaspora_zones:
            self.stdout.write(f'  - {zone.name} ({zone.code})')

        # Mapping des codes de zone pour les statistiques
        zone_code_mapping = {
            'DA': 'AFRIQUE',
            'DAM': 'AMERIQUE',
            'DAS': 'ASIE',
            'DE': 'EUROPE'
        }

        # Calculer les suffrages exprimés par zone à partir des résultats des candidats
        self.stdout.write(f'\n{self.style.WARNING("Calcul des statistiques par zone à partir des résultats...")}')
        
        zone_suffrages = {}
        for zone in diaspora_zones:
            # Calculer le total des suffrages pour cette zone
            results = CandidateRegionResult.objects.filter(
                election=election,
                region=zone
            )
            
            total_suffrages = sum(r.suffrages for r in results)
            zone_suffrages[zone.code] = total_suffrages
            
            self.stdout.write(f'  • {zone.name} ({zone.code}): {total_suffrages:,} suffrages')

        # Total des suffrages calculés
        total_suffrages_calc = sum(zone_suffrages.values())
        self.stdout.write(f'\n  Total suffrages calculé: {total_suffrages_calc:,}')
        self.stdout.write(f'  Total suffrages PDF: {total_diaspora["suffrages_exprimes"]:,}')
        
        if total_suffrages_calc != total_diaspora['suffrages_exprimes']:
            self.stdout.write(self.style.WARNING(
                f'  ⚠ Différence: {abs(total_suffrages_calc - total_diaspora["suffrages_exprimes"]):,}'
            ))

        # Répartir proportionnellement les inscrits, votants et bulletins nuls
        self.stdout.write(f'\n{self.style.WARNING("Répartition proportionnelle des statistiques par zone...")}')
        
        stats_created = 0
        stats_updated = 0

        with transaction.atomic():
            for zone in diaspora_zones:
                zone_suffrages_count = zone_suffrages.get(zone.code, 0)
                
                if total_suffrages_calc > 0:
                    proportion = Decimal(str(zone_suffrages_count / total_suffrages_calc))
                else:
                    proportion = Decimal('0.25')  # Répartition égale si pas de données
                
                # Calculer les statistiques pour cette zone
                inscrits = int(total_diaspora['inscrits'] * proportion)
                votants = int(total_diaspora['votants'] * proportion)
                bulletins_nuls = int(total_diaspora['bulletins_nuls'] * proportion)
                suffrages_exprimes = zone_suffrages_count
                
                # Calculer le taux de participation
                if inscrits > 0:
                    taux_participation = Decimal(str((votants / inscrits) * 100)).quantize(Decimal('0.01'))
                    taux_abstention = Decimal('100.00') - taux_participation
                else:
                    taux_participation = Decimal('0.00')
                    taux_abstention = Decimal('0.00')

                # Mapper le code de zone au nom utilisé dans DiasporaStat
                zone_name_for_model = zone_code_mapping.get(zone.code, zone.code)

                # Créer ou mettre à jour les statistiques
                diaspora_stat, created = DiasporaStat.objects.update_or_create(
                    election=election,
                    zone=zone_name_for_model,
                    defaults={
                        'inscrits': inscrits,
                        'votants': votants,
                        'taux_participation': taux_participation,
                        'taux_abstention': taux_abstention,
                        'bulletins_nuls': bulletins_nuls,
                        'suffrages_exprimes': suffrages_exprimes
                    }
                )

                if created:
                    stats_created += 1
                    status = '✓ CRÉÉ'
                    style = self.style.SUCCESS
                else:
                    stats_updated += 1
                    status = '↻ MIS À JOUR'
                    style = self.style.SUCCESS

                self.stdout.write(style(f'\n{status}: {zone.name} ({zone_name_for_model})'))
                self.stdout.write(f'  • Inscrits: {inscrits:,} ({proportion * 100:.2f}%)')
                self.stdout.write(f'  • Votants: {votants:,}')
                self.stdout.write(f'  • Taux participation: {taux_participation}%')
                self.stdout.write(f'  • Bulletins nuls: {bulletins_nuls:,}')
                self.stdout.write(f'  • Suffrages exprimés: {suffrages_exprimes:,}')

        # Résumé final
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 80))
        self.stdout.write(self.style.SUCCESS('RÉSUMÉ DE L\'IMPORT'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(f'Statistiques créées:     {stats_created}')
        self.stdout.write(f'Statistiques mises à jour: {stats_updated}')
        self.stdout.write(f'Total:                   {stats_created + stats_updated} zones')
        
        # Vérification des totaux
        from django.db.models import Sum
        self.stdout.write(f'\nVérification des totaux:')
        total_inscrits = DiasporaStat.objects.filter(election=election).aggregate(
            total=Sum('inscrits')
        )['total'] or 0
        total_votants = DiasporaStat.objects.filter(election=election).aggregate(
            total=Sum('votants')
        )['total'] or 0
        
        self.stdout.write(f'  • Inscrits (somme zones): {total_inscrits:,}')
        self.stdout.write(f'  • Inscrits (PDF):         {total_diaspora["inscrits"]:,}')
        self.stdout.write(f'  • Votants (somme zones):  {total_votants:,}')
        self.stdout.write(f'  • Votants (PDF):          {total_diaspora["votants"]:,}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Import terminé avec succès!'))
