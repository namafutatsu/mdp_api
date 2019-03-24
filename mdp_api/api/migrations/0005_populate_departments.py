from django.db import migrations


def clean_dpt_code(raw_dpt_code):
    try:
        dpt_code = '%0.2d' % int(raw_dpt_code)
    except (ValueError, TypeError):
        dpt_code = raw_dpt_code.upper()  # corsica 21/2B.
    return dpt_code


def populate_shops(apps, schema_editor):
    FrenchDepartment = apps.get_model('mdp_api_api', 'FrenchDepartment')
    Shop = apps.get_model('mdp_api_api', 'Shop')
    for shop in Shop.objects.all():
        try:
            dpt = FrenchDepartment.objects.get(code=clean_dpt_code(shop.state))
        except Exception:
            print('>>>>>>>>>>>>> department=%s could not be found for shop=%s' % (
                shop.state.upper(), shop.name
            ))
            continue
        dpt.region = shop.region
        dpt.save(update_fields=('region',))
        shop.department = dpt
        shop.save(update_fields=('department',))


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_api_api', '0004_make_department_a_foreignkey'),
    ]

    operations = [
        migrations.RunPython(populate_shops,),
    ]
