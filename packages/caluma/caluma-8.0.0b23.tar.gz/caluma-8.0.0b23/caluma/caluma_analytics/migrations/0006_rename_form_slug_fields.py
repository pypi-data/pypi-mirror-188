# Generated by Django 3.2.15 on 2022-11-25 16:22

from django.db import migrations


def rename_form_slug_fields(apps, schema_editor):
    AnalyticsField = apps.get_model("caluma_analytics.AnalyticsField")
    for field in AnalyticsField.objects.filter(data_source__endswith="form_id"):
        field.data_source = field.data_source.replace("form_id", "caluma_form.slug")
        field.save()


class Migration(migrations.Migration):

    dependencies = [
        ("caluma_analytics", "0005_analytics_field_ordering"),
    ]

    operations = [
        migrations.RunPython(rename_form_slug_fields, migrations.RunPython.noop)
    ]
