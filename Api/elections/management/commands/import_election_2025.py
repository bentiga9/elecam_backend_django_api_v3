"""
Commande Django pour importer les résultats de l'élection présidentielle 2025
Basé sur le PDF officiel: Resultats-Officiel-Election-Presidentiel-2025.pdf
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from election_types.models import ElectionType
from elections.models import Election
from regions.models import Region
from departments.models import Department
from political_parties.models import PartiePolitique
from candidates.models import Candidat
from voter_statistics.models import VoterStatistics
from department_stats.models import DepartmentStat
from candidate_results.models import (
    CandidateGlobalResult,
    CandidateRegionResult,
    CandidateDepartmentResult
)


class Command(BaseCommand):
    help = "Importe les résultats de l'élection présidentielle 2025 du Cameroun"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Supprime les données existantes avant import',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=" * 60))
        self.stdout.write(self.style.NOTICE("IMPORT ÉLECTION PRÉSIDENTIELLE 2025 - CAMEROUN"))
        self.stdout.write(self.style.NOTICE("=" * 60))

        try:
            with transaction.atomic():
                if options['clear']:
                    self.clear_existing_data()

                # 1. Créer le type d'élection
                election_type = self.create_election_type()

                # 2. Créer l'élection
                election = self.create_election(election_type)

                # 3. Créer les régions
                regions = self.create_regions()

                # 4. Créer les départements
                departments = self.create_departments(regions)

                # 5. Créer les partis politiques
                parties = self.create_political_parties()

                # 6. Créer les candidats
                candidates = self.create_candidates(election, parties)

                # 7. Créer les statistiques globales
                self.create_voter_statistics(election)

                # 8. Créer les statistiques par département
                self.create_department_stats(election, departments)

                # 9. Créer les résultats globaux des candidats
                self.create_global_results(election, candidates)

                # 10. Créer les résultats régionaux
                self.create_regional_results(election, candidates, regions)

                # 11. Créer les résultats départementaux
                self.create_department_results(election, candidates, departments)

                self.stdout.write(self.style.SUCCESS("\n" + "=" * 60))
                self.stdout.write(self.style.SUCCESS("IMPORT TERMINÉ AVEC SUCCÈS!"))
                self.stdout.write(self.style.SUCCESS("=" * 60))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de l'import: {e}"))
            raise

    def clear_existing_data(self):
        """Supprime les données existantes"""
        self.stdout.write("Suppression des données existantes...")
        CandidateDepartmentResult.objects.all().delete()
        CandidateRegionResult.objects.all().delete()
        CandidateGlobalResult.objects.all().delete()
        DepartmentStat.objects.all().delete()
        VoterStatistics.objects.all().delete()
        Candidat.objects.all().delete()
        Department.objects.all().delete()
        self.stdout.write(self.style.WARNING("Données supprimées"))

    def create_election_type(self):
        """Crée ou récupère le type d'élection présidentielle"""
        self.stdout.write("\n1. Création du type d'élection...")
        election_type, created = ElectionType.objects.get_or_create(
            name="Présidentielle",
            defaults={'name': 'Présidentielle'}
        )
        status = "créé" if created else "existant"
        self.stdout.write(self.style.SUCCESS(f"   Type '{election_type.name}' ({status})"))
        return election_type

    def create_election(self, election_type):
        """Crée l'élection présidentielle 2025"""
        self.stdout.write("\n2. Création de l'élection...")
        election, created = Election.objects.get_or_create(
            type=election_type,
            date="2025-10-12",
            defaults={
                'title': "Élection Présidentielle 2025",
                'status': 'completed',
                'is_active': True,
                'description': "Élection du Président de la République du Cameroun - 12 octobre 2025"
            }
        )
        status = "créée" if created else "existante"
        self.stdout.write(self.style.SUCCESS(f"   Élection '{election.title}' ({status})"))
        return election

    def create_regions(self):
        """Crée les 10 régions du Cameroun + 4 zones diaspora"""
        self.stdout.write("\n3. Création des régions...")
        
        regions_data = [
            # Régions nationales (10)
            {"name": "Adamaoua", "code": "AD", "region_type": "national", "chef_lieu": "Ngaoundéré"},
            {"name": "Centre", "code": "CE", "region_type": "national", "chef_lieu": "Yaoundé"},
            {"name": "Est", "code": "ES", "region_type": "national", "chef_lieu": "Bertoua"},
            {"name": "Extrême-Nord", "code": "EN", "region_type": "national", "chef_lieu": "Maroua"},
            {"name": "Littoral", "code": "LT", "region_type": "national", "chef_lieu": "Douala"},
            {"name": "Nord", "code": "NO", "region_type": "national", "chef_lieu": "Garoua"},
            {"name": "Nord-Ouest", "code": "NW", "region_type": "national", "chef_lieu": "Bamenda"},
            {"name": "Ouest", "code": "OU", "region_type": "national", "chef_lieu": "Bafoussam"},
            {"name": "Sud", "code": "SU", "region_type": "national", "chef_lieu": "Ebolowa"},
            {"name": "Sud-Ouest", "code": "SW", "region_type": "national", "chef_lieu": "Buea"},
            # Zones diaspora (4)
            {"name": "Diaspora Afrique", "code": "DA", "region_type": "diaspora", "chef_lieu": None},
            {"name": "Diaspora Amérique", "code": "DAM", "region_type": "diaspora", "chef_lieu": None},
            {"name": "Diaspora Asie", "code": "DAS", "region_type": "diaspora", "chef_lieu": None},
            {"name": "Diaspora Europe", "code": "DE", "region_type": "diaspora", "chef_lieu": None},
        ]
        
        regions = {}
        for data in regions_data:
            region, created = Region.objects.update_or_create(
                code=data["code"],
                defaults={
                    "name": data["name"],
                    "region_type": data["region_type"],
                    "chef_lieu": data["chef_lieu"],
                    "is_active": True
                }
            )
            regions[data["code"]] = region
            status = "✓" if created else "↻"
            self.stdout.write(f"   {status} {region.name}")
        
        self.stdout.write(self.style.SUCCESS(f"   {len(regions)} régions créées/mises à jour"))
        return regions

    def create_departments(self, regions):
        """Crée les 58 départements du Cameroun"""
        self.stdout.write("\n4. Création des départements...")
        
        departments_data = {
            # ADAMAOUA (5)
            "AD": [
                {"name": "Djérem", "code": "AD-DJE"},
                {"name": "Faro-et-Déo", "code": "AD-FD"},
                {"name": "Mayo-Banyo", "code": "AD-MB"},
                {"name": "Mbéré", "code": "AD-MBE"},
                {"name": "Vina", "code": "AD-VIN"},
            ],
            # CENTRE (10)
            "CE": [
                {"name": "Haute-Sanaga", "code": "CE-HS"},
                {"name": "Lékié", "code": "CE-LEK"},
                {"name": "Mbam-et-Inoubou", "code": "CE-MI"},
                {"name": "Mbam-et-Kim", "code": "CE-MK"},
                {"name": "Méfou-et-Afamba", "code": "CE-MA"},
                {"name": "Méfou-et-Akono", "code": "CE-MAK"},
                {"name": "Mfoundi", "code": "CE-MFD"},
                {"name": "Nyong-et-Kellé", "code": "CE-NK"},
                {"name": "Nyong-et-Mfoumou", "code": "CE-NM"},
                {"name": "Nyong-et-So'o", "code": "CE-NS"},
            ],
            # EST (4)
            "ES": [
                {"name": "Boumba-et-Ngoko", "code": "ES-BN"},
                {"name": "Haut-Nyong", "code": "ES-HN"},
                {"name": "Kadey", "code": "ES-KAD"},
                {"name": "Lom-et-Djérem", "code": "ES-LD"},
            ],
            # EXTRÊME-NORD (6)
            "EN": [
                {"name": "Diamaré", "code": "EN-DIA"},
                {"name": "Logone-et-Chari", "code": "EN-LC"},
                {"name": "Mayo-Danay", "code": "EN-MD"},
                {"name": "Mayo-Kani", "code": "EN-MK"},
                {"name": "Mayo-Sava", "code": "EN-MS"},
                {"name": "Mayo-Tsanaga", "code": "EN-MT"},
            ],
            # LITTORAL (4)
            "LT": [
                {"name": "Moungo", "code": "LT-MOU"},
                {"name": "Nkam", "code": "LT-NKA"},
                {"name": "Sanaga-Maritime", "code": "LT-SM"},
                {"name": "Wouri", "code": "LT-WOU"},
            ],
            # NORD (4)
            "NO": [
                {"name": "Bénoué", "code": "NO-BEN"},
                {"name": "Faro", "code": "NO-FAR"},
                {"name": "Mayo-Louti", "code": "NO-ML"},
                {"name": "Mayo-Rey", "code": "NO-MR"},
            ],
            # NORD-OUEST (7)
            "NW": [
                {"name": "Boyo", "code": "NW-BOY"},
                {"name": "Bui", "code": "NW-BUI"},
                {"name": "Donga-Mantung", "code": "NW-DM"},
                {"name": "Menchum", "code": "NW-MEN"},
                {"name": "Mezam", "code": "NW-MEZ"},
                {"name": "Momo", "code": "NW-MOM"},
                {"name": "Ngo-Ketunjia", "code": "NW-NK"},
            ],
            # OUEST (8)
            "OU": [
                {"name": "Bamboutos", "code": "OU-BAM"},
                {"name": "Haut-Nkam", "code": "OU-HN"},
                {"name": "Hauts-Plateaux", "code": "OU-HP"},
                {"name": "Koung-Khi", "code": "OU-KK"},
                {"name": "Menoua", "code": "OU-MEN"},
                {"name": "Mifi", "code": "OU-MIF"},
                {"name": "Ndé", "code": "OU-NDE"},
                {"name": "Noun", "code": "OU-NOU"},
            ],
            # SUD (4)
            "SU": [
                {"name": "Dja-et-Lobo", "code": "SU-DL"},
                {"name": "Mvila", "code": "SU-MVI"},
                {"name": "Océan", "code": "SU-OCE"},
                {"name": "Vallée-du-Ntem", "code": "SU-VN"},
            ],
            # SUD-OUEST (6)
            "SW": [
                {"name": "Fako", "code": "SW-FAK"},
                {"name": "Koupé-Manengouba", "code": "SW-KM"},
                {"name": "Lebialem", "code": "SW-LEB"},
                {"name": "Manyu", "code": "SW-MAN"},
                {"name": "Meme", "code": "SW-MEM"},
                {"name": "Ndian", "code": "SW-NDI"},
            ],
        }
        
        departments = {}
        count = 0
        for region_code, depts in departments_data.items():
            region = regions.get(region_code)
            if region:
                for dept_data in depts:
                    dept, created = Department.objects.update_or_create(
                        code=dept_data["code"],
                        defaults={
                            "name": dept_data["name"],
                            "region": region
                        }
                    )
                    departments[dept_data["code"]] = dept
                    count += 1
        
        self.stdout.write(self.style.SUCCESS(f"   {count} départements créés/mis à jour"))
        return departments

    def create_political_parties(self):
        """Crée les partis politiques des candidats 2025"""
        self.stdout.write("\n5. Création des partis politiques...")
        
        parties_data = [
            {"name": "Rassemblement Démocratique du Peuple Camerounais", "abbreviation": "RDPC", "color_hex": "#006400"},
            {"name": "Front Social National du Cameroun", "abbreviation": "FSNC", "color_hex": "#FF6600"},
            {"name": "Parti Camerounais pour la Réconciliation Nationale", "abbreviation": "PCRN", "color_hex": "#0066CC"},
            {"name": "Union Nationale pour la Démocratie et le Progrès", "abbreviation": "UNDP", "color_hex": "#FFD700"},
            {"name": "Union Démocratique du Cameroun", "abbreviation": "UDC", "color_hex": "#800080"},
            {"name": "Parti de l'Alliance Libérale", "abbreviation": "PAL", "color_hex": "#FF0000"},
            {"name": "Front Démocratique du Cameroun", "abbreviation": "FDC", "color_hex": "#00FF00"},
            {"name": "Union des Mouvements Socialistes", "abbreviation": "UMS", "color_hex": "#FF69B4"},
            {"name": "Parti Uni pour le Renouveau Social", "abbreviation": "PURS", "color_hex": "#8B4513"},
            {"name": "Mouvement Camerounais pour la Nouvelle Citoyenneté", "abbreviation": "MCNC", "color_hex": "#1E90FF"},
            {"name": "Social Democratic Front", "abbreviation": "SDF", "color_hex": "#DC143C"},
            {"name": "Univers", "abbreviation": "UNIVERS", "color_hex": "#4B0082"},
        ]
        
        parties = {}
        for data in parties_data:
            party, created = PartiePolitique.objects.update_or_create(
                abbreviation=data["abbreviation"],
                defaults={
                    "name": data["name"],
                    "color_hex": data["color_hex"]
                }
            )
            parties[data["abbreviation"]] = party
            status = "✓" if created else "↻"
            self.stdout.write(f"   {status} {party.abbreviation} - {party.name}")
        
        self.stdout.write(self.style.SUCCESS(f"   {len(parties)} partis créés/mis à jour"))
        return parties

    def create_candidates(self, election, parties):
        """Crée les 12 candidats de l'élection 2025"""
        from .election_2025_data import CANDIDATES_DATA
        
        self.stdout.write("\n6. Création des candidats...")
        
        candidates = {}
        for data in CANDIDATES_DATA:
            party = parties.get(data["party"])
            candidate, created = Candidat.objects.update_or_create(
                election=election,
                name=data["name"],
                defaults={
                    "partie_politique": party,
                    "is_active": True
                }
            )
            candidates[data["name"]] = candidate
            status = "✓" if created else "↻"
            self.stdout.write(f"   {status} {data['ballot']}. {candidate.name} ({data['party']})")
        
        # Mettre à jour le compteur de candidats
        election.candidates_count = len(candidates)
        election.save(update_fields=['candidates_count'])
        
        self.stdout.write(self.style.SUCCESS(f"   {len(candidates)} candidats créés/mis à jour"))
        return candidates

    def create_voter_statistics(self, election):
        """Crée les statistiques globales de l'élection"""
        from .election_2025_data import GLOBAL_STATS
        
        self.stdout.write("\n7. Création des statistiques globales...")
        
        stats, created = VoterStatistics.objects.update_or_create(
            election=election,
            defaults=GLOBAL_STATS
        )
        
        status = "créées" if created else "mises à jour"
        self.stdout.write(self.style.SUCCESS(f"   Statistiques {status}:"))
        self.stdout.write(f"   - Inscrits: {stats.total_inscrits:,}")
        self.stdout.write(f"   - Votants: {stats.total_votants:,}")
        self.stdout.write(f"   - Participation: {stats.taux_participation}%")
        self.stdout.write(f"   - Suffrages exprimés: {stats.total_suffrages_exprimes:,}")

    def create_department_stats(self, election, departments):
        """Crée les statistiques par département"""
        from .election_2025_data import (
            DEPARTMENT_STATS_ADAMAOUA,
            DEPARTMENT_STATS_CENTRE,
            DEPARTMENT_STATS_EST,
            DEPARTMENT_STATS_EXTREME_NORD,
            DEPARTMENT_STATS_LITTORAL,
            DEPARTMENT_STATS_NORD,
        )
        
        self.stdout.write("\n8. Création des statistiques départementales...")
        
        all_department_stats = {
            "ADAMAOUA": DEPARTMENT_STATS_ADAMAOUA,
            "CENTRE": DEPARTMENT_STATS_CENTRE,
            "EST": DEPARTMENT_STATS_EST,
            "EXTRÊME-NORD": DEPARTMENT_STATS_EXTREME_NORD,
            "LITTORAL": DEPARTMENT_STATS_LITTORAL,
            "NORD": DEPARTMENT_STATS_NORD,
        }
        
        created_count = 0
        for region_name, dept_stats in all_department_stats.items():
            self.stdout.write(f"   → Région {region_name}")
            
            for dept_name, stats_data in dept_stats.items():
                # Recherche du département par nom
                dept = None
                for d in departments.values():
                    if d.name == dept_name:
                        dept = d
                        break
                
                if not dept:
                    self.stdout.write(self.style.WARNING(f"     ⚠ Département non trouvé: {dept_name}"))
                    continue
                
                DepartmentStat.objects.update_or_create(
                    election=election,
                    department=dept,
                    defaults=stats_data
                )
                created_count += 1
                self.stdout.write(f"     ✓ {dept.name}: {stats_data['inscrits']:,} inscrits, {stats_data['taux_participation']}% participation")
        
        self.stdout.write(self.style.SUCCESS(f"   TOTAL: {created_count} statistiques départementales créées/mises à jour"))

    def create_global_results(self, election, candidates):
        """Crée les résultats globaux des candidats"""
        from .election_2025_data import CANDIDATES_DATA
        
        self.stdout.write("\n9. Création des résultats globaux...")
        
        for data in CANDIDATES_DATA:
            candidate = candidates.get(data["name"])
            if candidate:
                result, created = CandidateGlobalResult.objects.update_or_create(
                    election=election,
                    candidate=candidate,
                    defaults={
                        "rang": data["rank"],
                        "total_suffrages": data["votes"],
                        "pourcentage_national": data["percentage"],
                        "is_winner": data["winner"]
                    }
                )
                winner_str = " 🏆 ÉLU" if data["winner"] else ""
                self.stdout.write(f"   {data['rank']}. {candidate.name}: {data['votes']:,} ({data['percentage']}%){winner_str}")
        
        self.stdout.write(self.style.SUCCESS("   Résultats globaux créés"))

    def create_regional_results(self, election, candidates, regions):
        """Crée les résultats par région pour chaque candidat"""
        from .election_2025_data import REGIONAL_RESULTS
        
        self.stdout.write("\n10. Création des résultats régionaux...")
        
        count = 0
        for region_code, results in REGIONAL_RESULTS.items():
            region = regions.get(region_code)
            if region:
                for candidate_name, result_data in results.items():
                    candidate = candidates.get(candidate_name)
                    if candidate:
                        CandidateRegionResult.objects.update_or_create(
                            election=election,
                            candidate=candidate,
                            region=region,
                            defaults={
                                "suffrages": result_data["votes"],
                                "pourcentage": result_data["pct"]
                            }
                        )
                        count += 1
        
        self.stdout.write(self.style.SUCCESS(f"   {count} résultats régionaux créés"))
    
    def create_department_results(self, election, candidates, departments):
        """Crée les résultats par département pour chaque candidat"""
        from .election_2025_data import (
            DEPARTMENT_RESULTS_ADAMAOUA,
            DEPARTMENT_RESULTS_CENTRE,
            DEPARTMENT_RESULTS_EST,
            DEPARTMENT_RESULTS_EXTREME_NORD,
            DEPARTMENT_RESULTS_LITTORAL,
            DEPARTMENT_RESULTS_NORD,
        )
        
        self.stdout.write("\n11. Création des résultats départementaux...")
        
        all_department_results = {
            "ADAMAOUA": DEPARTMENT_RESULTS_ADAMAOUA,
            "CENTRE": DEPARTMENT_RESULTS_CENTRE,
            "EST": DEPARTMENT_RESULTS_EST,
            "EXTRÊME-NORD": DEPARTMENT_RESULTS_EXTREME_NORD,
            "LITTORAL": DEPARTMENT_RESULTS_LITTORAL,
            "NORD": DEPARTMENT_RESULTS_NORD,
        }
        
        created_count = 0
        for region_name, dept_results in all_department_results.items():
            self.stdout.write(f"   → Région {region_name}")
            
            for dept_name, candidates_data in dept_results.items():
                # Recherche du département par nom
                dept = None
                for d in departments.values():
                    # Normaliser les noms pour la comparaison
                    dept_name_normalized = dept_name.upper().replace(" ", "").replace("-", "").replace("'", "")
                    d_name_normalized = d.name.upper().replace(" ", "").replace("-", "").replace("'", "")
                    
                    if dept_name_normalized in d_name_normalized or d_name_normalized in dept_name_normalized:
                        dept = d
                        break
                
                if not dept:
                    self.stdout.write(self.style.WARNING(f"     ⚠ Département non trouvé: {dept_name}"))
                    continue
                
                dept_count = 0
                for candidate_name, result_data in candidates_data.items():
                    candidate = candidates.get(candidate_name)
                    if not candidate:
                        continue
                    
                    CandidateDepartmentResult.objects.update_or_create(
                        election=election,
                        candidate=candidate,
                        department=dept,
                        defaults={
                            'suffrages': result_data['votes'],
                            'pourcentage': result_data['percentage']
                        }
                    )
                    dept_count += 1
                    created_count += 1
                
                self.stdout.write(f"     ✓ {dept.name}: {dept_count} résultats")
        
        self.stdout.write(self.style.SUCCESS(f"   TOTAL: {created_count} résultats départementaux créés/mis à jour"))
