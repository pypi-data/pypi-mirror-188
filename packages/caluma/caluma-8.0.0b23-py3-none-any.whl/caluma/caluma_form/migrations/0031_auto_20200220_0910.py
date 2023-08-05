# Generated by Django 2.2.10 on 2020-02-20 09:10

import logging

import django.db.models.deletion
from django.db import migrations, models


def cleanup_invalid_family_pointers(apps, schema_editor):
    Document = apps.get_model("caluma_form.Document")
    invalid_family_pointers = Document.objects.exclude(
        family__in=Document.objects.all().values("pk")
    )
    for doc in invalid_family_pointers:
        logging.warning(
            f"Document pk={doc.pk} (form={doc.form_id}) missing it's family={doc.family}. Resetting to itself"
        )
        doc.family = doc.pk
        doc.save()


class Migration(migrations.Migration):

    dependencies = [("caluma_form", "0030_auto_20200219_1359")]

    operations = [
        migrations.RunPython(
            cleanup_invalid_family_pointers, migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name="document",
            name="family",
            field=models.ForeignKey(
                help_text="Family id which document belongs too.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="caluma_form.Document",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldocument",
            name="family",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                help_text="Family id which document belongs too.",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="caluma_form.Document",
            ),
        ),
    ]
