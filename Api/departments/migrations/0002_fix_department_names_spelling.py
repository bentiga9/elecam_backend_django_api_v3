# Generated manually to fix department name spelling errors
# Compares database names with official PDF data

from django.db import migrations


def fix_department_names(apps, schema_editor):
    """
    Corrige les erreurs d'orthographe dans les noms de départements
    pour correspondre exactement aux données du PDF officiel.
    """
    Department = apps.get_model('departments', 'Department')
    Region = apps.get_model('regions', 'Region')
    
    # Liste des corrections à appliquer
    corrections = [
        {
            'region_name': 'Centre',
            'old_name': 'Nyong-et-Kellé',
            'new_name': 'Nyong-et-Kéllé',
            'description': 'Ajout accent aigu sur le é final'
        },
        {
            'region_name': 'Centre',
            'old_name': "Nyong-et-So'o",
            'new_name': 'Nyong-et-Soo',
            'description': 'Suppression de l\'apostrophe'
        },
        {
            'region_name': 'Est',
            'old_name': 'Lom-et-Djérem',
            'new_name': 'Lom-et-Djerem',
            'description': 'Suppression accent aigu sur le é'
        },
    ]
    
    print("\n" + "=" * 80)
    print("CORRECTION DES NOMS DE DÉPARTEMENTS")
    print("=" * 80)
    
    for correction in corrections:
        try:
            region = Region.objects.get(name=correction['region_name'])
            department = Department.objects.filter(
                region=region,
                name=correction['old_name']
            ).first()
            
            if department:
                old_name = department.name
                department.name = correction['new_name']
                department.save()
                print(f"\n✓ Corrigé: {correction['region_name']}/{old_name}")
                print(f"  → Nouveau nom: {correction['new_name']}")
                print(f"  → Raison: {correction['description']}")
            else:
                print(f"\n⚠ Département '{correction['old_name']}' non trouvé dans {correction['region_name']}")
                
        except Region.DoesNotExist:
            print(f"\n❌ Région '{correction['region_name']}' introuvable")
        except Exception as e:
            print(f"\n❌ Erreur lors de la correction de '{correction['old_name']}': {str(e)}")
    
    print("\n" + "=" * 80)
    print("FIN DES CORRECTIONS")
    print("=" * 80 + "\n")


def reverse_fix_department_names(apps, schema_editor):
    """
    Annule les corrections en restaurant les anciens noms.
    """
    Department = apps.get_model('departments', 'Department')
    Region = apps.get_model('regions', 'Region')
    
    # Liste des corrections inversées
    corrections = [
        {
            'region_name': 'Centre',
            'old_name': 'Nyong-et-Kéllé',
            'new_name': 'Nyong-et-Kellé',
        },
        {
            'region_name': 'Centre',
            'old_name': 'Nyong-et-Soo',
            'new_name': "Nyong-et-So'o",
        },
        {
            'region_name': 'Est',
            'old_name': 'Lom-et-Djerem',
            'new_name': 'Lom-et-Djérem',
        },
    ]
    
    print("\n" + "=" * 80)
    print("ANNULATION DES CORRECTIONS (ROLLBACK)")
    print("=" * 80)
    
    for correction in corrections:
        try:
            region = Region.objects.get(name=correction['region_name'])
            department = Department.objects.filter(
                region=region,
                name=correction['old_name']
            ).first()
            
            if department:
                old_name = department.name
                department.name = correction['new_name']
                department.save()
                print(f"\n✓ Restauré: {correction['region_name']}/{old_name}")
                print(f"  → Ancien nom: {correction['new_name']}")
                
        except Region.DoesNotExist:
            print(f"\n❌ Région '{correction['region_name']}' introuvable")
        except Exception as e:
            print(f"\n❌ Erreur lors de la restauration: {str(e)}")
    
    print("\n" + "=" * 80)
    print("FIN DE L'ANNULATION")
    print("=" * 80 + "\n")


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            fix_department_names,
            reverse_code=reverse_fix_department_names
        ),
    ]
