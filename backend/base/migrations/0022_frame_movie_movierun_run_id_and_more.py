# Replays operations from 0020 that were not applied to the DB.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_rename_run_id_movierun_run'),
    ]

    operations = [
        migrations.AddField(
            model_name='frame',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.movie'),
        ),
        migrations.DeleteModel(
            name='Slide',
        ),
        migrations.DeleteModel(
            name='SlideRun',
        ),
        migrations.DeleteModel(
            name='SlideImage',
        ),
    ]
