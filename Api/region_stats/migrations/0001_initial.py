# Generated migration to use existing department_stats_regionstat table

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('elections', '0015_alter_election_candidates_count'),
        ('regions', '0003_alter_region_options_region_chef_lieu_and_more'),
        ('department_stats', '0003_regionstat_and_more'),  # La table existe déjà ici
    ]

    operations = [
        # Pas d'opération - la table existe déjà dans department_stats
        # Le modèle RegionStat pointe maintenant vers department_stats_regionstat via db_table
    ]
