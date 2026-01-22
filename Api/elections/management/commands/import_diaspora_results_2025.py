"""
Commande pour importer les résultats diaspora des candidats pour l'élection présidentielle 2025.
Calcule automatiquement les résultats agrégés à partir des résultats régionaux des zones diaspora.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from candidate_results.models import CandidateRegionResult, CandidateDiasporaResult
from regions.models import Region
from elections.models import Election
from candidates.models import Candidat


class Command(BaseCommand):
    help = 'Importe les résultats diaspora des candidats pour l\'élection présidentielle 2025'

    def add_arguments(self, parser):
        parser.add_argument(
            '--election-id',
            type=int,
            default=None,
            help='ID de l\'élection (par défaut: dernière élection active)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('IMPORT DES RÉSULTATS DIASPORA - ÉLECTION PRÉSIDENTIELLE 2025'))
        self.stdout.write(self.style.SUCCESS('=' * 70))

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

        # Récupérer les zones diaspora
        diaspora_zones = Region.objects.filter(region_type='diaspora', is_active=True)
        self.stdout.write(f'\nZones diaspora trouvées: {diaspora_zones.count()}')
        for zone in diaspora_zones:
            self.stdout.write(f'  - {zone.name} ({zone.code})')

        if diaspora_zones.count() != 4:
            self.stdout.write(self.style.WARNING(
                f'Attention: {diaspora_zones.count()} zones diaspora trouvées au lieu de 4'
            ))

        # Récupérer tous les candidats
        candidates = Candidat.objects.filter(is_active=True).order_by('id')
        self.stdout.write(f'\nCandidats actifs: {candidates.count()}')

        # Calculer et créer les résultats diaspora
        with transaction.atomic():
            created_count = 0
            updated_count = 0
            
            for candidate in candidates:
                self.stdout.write(f'\nTraitement: {candidate.name}')
                
                # Récupérer les résultats régionaux pour les zones diaspora
                regional_results = CandidateRegionResult.objects.filter(
                    election=election,
                    candidate=candidate,
                    region__region_type='diaspora'
                )
                
                if not regional_results.exists():
                    self.stdout.write(self.style.WARNING(
                        f'  Aucun résultat régional diaspora trouvé pour {candidate.name}'
                    ))
                    continue
                
                # Calculer les totaux
                total_suffrages = sum(r.suffrages for r in regional_results)
                
                # Récupérer les suffrages par zone
                suffrages_by_zone = {}
                for result in regional_results:
                    zone_code = result.region.code
                    suffrages_by_zone[zone_code] = result.suffrages
                
                # Calculer le pourcentage (par rapport au total diaspora)
                # Note: Pour un pourcentage précis, il faudrait les suffrages exprimés totaux diaspora
                # Pour l'instant, on utilise le pourcentage moyen des zones
                avg_percentage = sum(r.pourcentage for r in regional_results) / regional_results.count() if regional_results.count() > 0 else 0
                
                # Créer ou mettre à jour le résultat diaspora
                diaspora_result, created = CandidateDiasporaResult.objects.update_or_create(
                    election=election,
                    candidate=candidate,
                    defaults={
                        'total_suffrages_diaspora': total_suffrages,
                        'pourcentage_diaspora': round(avg_percentage, 2),
                        'suffrages_afrique': suffrages_by_zone.get('DA', 0),
                        'suffrages_amerique': suffrages_by_zone.get('DAM', 0),
                        'suffrages_asie': suffrages_by_zone.get('DAS', 0),
                        'suffrages_europe': suffrages_by_zone.get('DE', 0),
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Créé: {total_suffrages:,} suffrages ({avg_percentage:.2f}%)'
                    ))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Mis à jour: {total_suffrages:,} suffrages ({avg_percentage:.2f}%)'
                    ))
                
                # Afficher le détail par zone
                self.stdout.write('    Détail par zone:')
                self.stdout.write(f'      - Afrique:  {suffrages_by_zone.get("DA", 0):,}')
                self.stdout.write(f'      - Amérique: {suffrages_by_zone.get("DAM", 0):,}')
                self.stdout.write(f'      - Asie:     {suffrages_by_zone.get("DAS", 0):,}')
                self.stdout.write(f'      - Europe:   {suffrages_by_zone.get("DE", 0):,}')

        # Résumé final
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('RÉSUMÉ DE L\'IMPORT'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f'Résultats créés: {created_count}')
        self.stdout.write(f'Résultats mis à jour: {updated_count}')
        self.stdout.write(f'Total: {created_count + updated_count}')
        self.stdout.write(self.style.SUCCESS('\n✓ Import terminé avec succès!'))
