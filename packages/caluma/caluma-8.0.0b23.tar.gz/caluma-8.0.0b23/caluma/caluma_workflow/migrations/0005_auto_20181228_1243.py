# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-28 12:43
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.indexes
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("caluma_workflow", "0004_auto_20181218_1352")]

    operations = [
        migrations.AddField(
            model_name="task",
            name="address_groups",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="workitem",
            name="addressed_groups",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=150),
                default=list,
                help_text="Offer work item to be processed by a group of users, such are not committed to process it though.",
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="workitem",
            name="assigned_users",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=150),
                default=list,
                help_text="Users responsible to undertake given work item.",
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="created_by_group",
            field=models.CharField(
                blank=True, db_index=True, max_length=150, null=True
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="meta",
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name="flow",
            name="created_by_group",
            field=models.CharField(
                blank=True, db_index=True, max_length=150, null=True
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="created_by_group",
            field=models.CharField(
                blank=True, db_index=True, max_length=150, null=True
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="meta",
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name="taskflow",
            name="created_by_group",
            field=models.CharField(
                blank=True, db_index=True, max_length=150, null=True
            ),
        ),
        migrations.AlterField(
            model_name="workflow",
            name="created_by_group",
            field=models.CharField(
                blank=True, db_index=True, max_length=150, null=True
            ),
        ),
        migrations.AlterField(
            model_name="workflow",
            name="meta",
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name="workitem",
            name="child_case",
            field=models.OneToOneField(
                blank=True,
                help_text="Defines case of a sub-workflow",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="parent_work_item",
                to="caluma_workflow.Case",
            ),
        ),
        migrations.AlterField(
            model_name="workitem",
            name="created_by_group",
            field=models.CharField(
                blank=True, db_index=True, max_length=150, null=True
            ),
        ),
        migrations.AlterField(
            model_name="workitem",
            name="meta",
            field=models.JSONField(default=dict),
        ),
        migrations.AddIndex(
            model_name="workitem",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["addressed_groups"], name="workflow_wo_address_679262_gin"
            ),
        ),
        migrations.AddIndex(
            model_name="workitem",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["assigned_users"], name="workflow_wo_assigne_76d859_gin"
            ),
        ),
    ]
