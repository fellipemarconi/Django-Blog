# Generated by Django 5.0.1 on 2024-01-17 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0002_sitesetup_rename_new_ta_menulink_new_tab'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitesetup',
            options={'verbose_name': 'Setup', 'verbose_name_plural': 'Setup'},
        ),
    ]
