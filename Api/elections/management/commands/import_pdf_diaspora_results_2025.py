"""
Commande pour extraire et importer les résultats diaspora depuis le PDF officiel.
Extrait les données des pages 24-32 et page 34 du PDF.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from candidate_results.models import CandidateDiasporaResult
from elections.models import Election
from candidates.models import Candidat
from decimal import Decimal


class Command(BaseCommand):
    help = 'Importe les résultats diaspora des candidats depuis le PDF officiel 2025'

    def add_arguments(self, parser):
        parser.add_argument(
            '--election-id',
            type=int,
            default=None,
            help='ID de l\'élection (par défaut: dernière élection active)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('IMPORT DES RÉSULTATS DIASPORA DEPUIS LE PDF'))
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

        # Données extraites du PDF - Page 34 (RÉCAPITULATIF GÉNÉRAL)
        # et pages 24-32 pour les détails par zone
        diaspora_data = {
            'BIYA PAUL': {
                'total': 4803,
                'pourcentage': 29.14,
                'afrique': 3045,      # Page 25
                'amerique': 315,      # Page 27
                'asie': 166,          # Page 28
                'europe': 1277        # Page 31
            },
            'ISSA TCHIROMA': {
                'total': 9738,
                'pourcentage': 59.09,
                'afrique': 4906,
                'amerique': 819,
                'asie': 470,
                'europe': 3543
            },
            'LIBII LI NGUE NGUE CABRAL': {
                'total': 1266,
                'pourcentage': 7.68,
                'afrique': 566,
                'amerique': 68,
                'asie': 33,
                'europe': 599
            },
            'BELLO BOUBA MAIGARI': {
                'total': 62,
                'pourcentage': 0.38,
                'afrique': 39,
                'amerique': 3,
                'asie': 4,
                'europe': 16
            },
            'TOMAINO HERMINE PATRICIA épouse NDAM NJOYA': {
                'total': 166,
                'pourcentage': 1.01,
                'afrique': 134,
                'amerique': 3,
                'asie': 3,
                'europe': 26
            },
            'OSIH JOSHUA NAMBANGI': {
                'total': 100,
                'pourcentage': 0.61,
                'afrique': 64,
                'amerique': 4,
                'asie': 5,
                'europe': 27
            },
            'ATEKI SETA CAXTON': {
                'total': 31,
                'pourcentage': 0.19,
                'afrique': 28,
                'amerique': 1,
                'asie': 1,
                'europe': 1
            },
            'IYODI HIRAM SAMUEL': {
                'total': 236,
                'pourcentage': 1.43,
                'afrique': 85,
                'amerique': 12,
                'asie': 5,
                'europe': 134
            },
            'MATOMBA SERGE ESPOIR': {
                'total': 28,
                'pourcentage': 0.17,
                'afrique': 20,
                'amerique': 1,
                'asie': 1,
                'europe': 6
            },
            'BOUGHA HAGBE JACQUES': {
                'total': 17,
                'pourcentage': 0.10,
                'afrique': 10,
                'amerique': 0,
                'asie': 1,
                'europe': 6
            },
            'KWEMO PIERRE': {
                'total': 12,
                'pourcentage': 0.07,
                'afrique': 8,
                'amerique': 1,
                'asie': 0,
                'europe': 3
            },
            'MUNA AKERE TABENG': {
                'total': 21,
                'pourcentage': 0.13,
                'afrique': 16,
                'amerique': 0,
                'asie': 0,
                'europe': 5
            }
        }

        # Mapper les noms aux candidats
        candidate_name_map = {
            'BIYA PAUL': 'BIYA PAUL',
            'ISSA TCHIROMA': 'ISSA TCHIROMA',
            'LIBII LI NGUE NGUE CABRAL': 'LIBII LI NGUE NGUE CABRAL',
            'BELLO BOUBA MAIGARI': 'BELLO BOUBA MAIGARI',
            'TOMAINO HERMINE PATRICIA épouse NDAM NJOYA': 'TOMAINO HERMINE PATRICIA épse NDAM NJOYA',
            'OSIH JOSHUA NAMBANGI': 'OSIH JOSHUA NAMBANGI',
            'ATEKI SETA CAXTON': 'ATEKI SETA CAXTON',
            'IYODI HIRAM SAMUEL': 'IYODI HIRAM SAMUEL',
            'MATOMBA SERGE ESPOIR': 'MATOMBA SERGE ESPOIR',
            'BOUGHA HAGBE JACQUES': 'BOUGHA HAGBE JACQUES',
            'KWEMO PIERRE': 'KWEMO PIERRE',
            'MUNA AKERE TABENG': 'MUNA AKERE TABENG'
        }

        created_count = 0
        updated_count = 0
        error_count = 0

        with transaction.atomic():
            for candidate_name_pdf, data in diaspora_data.items():
                try:
                    # Trouver le candidat
                    candidate_name_db = candidate_name_map.get(candidate_name_pdf)
                    candidate = Candidat.objects.filter(name__icontains=candidate_name_db.split()[0]).first()
                    
                    if not candidate:
                        self.stdout.write(self.style.WARNING(
                            f'  ⚠ Candidat non trouvé: {candidate_name_pdf}'
                        ))
                        error_count += 1
                        continue

                    self.stdout.write(f'\n{candidate.name}:')
                    
                    # Créer ou mettre à jour le résultat diaspora
                    diaspora_result, created = CandidateDiasporaResult.objects.update_or_create(
                        election=election,
                        candidate=candidate,
                        defaults={
                            'total_suffrages_diaspora': data['total'],
                            'pourcentage_diaspora': Decimal(str(data['pourcentage'])),
                            'suffrages_afrique': data['afrique'],
                            'suffrages_amerique': data['amerique'],
                            'suffrages_asie': data['asie'],
                            'suffrages_europe': data['europe'],
                        }
                    )
                    
                    if created:
                        created_count += 1
                        status = '✓ CRÉÉ'
                        style = self.style.SUCCESS
                    else:
                        updated_count += 1
                        status = '✓ MIS À JOUR'
                        style = self.style.SUCCESS
                    
                    self.stdout.write(style(f'  {status}'))
                    self.stdout.write(f'  Total diaspora: {data["total"]:,} suffrages ({data["pourcentage"]}%)')
                    self.stdout.write('  Détail par zone:')
                    self.stdout.write(f'    • Afrique:  {data["afrique"]:>5,}')
                    self.stdout.write(f'    • Amérique: {data["amerique"]:>5,}')
                    self.stdout.write(f'    • Asie:     {data["asie"]:>5,}')
                    self.stdout.write(f'    • Europe:   {data["europe"]:>5,}')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'  ✗ ERREUR pour {candidate_name_pdf}: {str(e)}'
                    ))
                    error_count += 1

        # Résumé final
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 80))
        self.stdout.write(self.style.SUCCESS('RÉSUMÉ DE L\'IMPORT'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(f'Résultats créés:     {created_count}')
        self.stdout.write(f'Résultats mis à jour: {updated_count}')
        self.stdout.write(f'Erreurs:             {error_count}')
        self.stdout.write(f'Total traité:        {created_count + updated_count}')
        
        if error_count == 0:
            self.stdout.write(self.style.SUCCESS('\n✓ Import terminé avec succès!'))
        else:
            self.stdout.write(self.style.WARNING(
                f'\n⚠ Import terminé avec {error_count} erreur(s)'
            ))
