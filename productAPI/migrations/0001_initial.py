from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('product_type', models.CharField(blank=True, max_length=20, null=True, choices=[
                    ('dry_food', 'Dry Food'),
                    ('wet_food', 'Wet Food'),
                    ('pet_care', 'Pet Care'),
                    ('pet_treats', 'Pet Treats'),
                    ('pet_milk', 'Pet Milk'),
                    ('cat_litter', 'Cat Litter'),
                    ('other_essentials', 'Other Essentials'),
                    ('merch', 'Merch'),
                ])),
                ('brand', models.CharField(blank=True, max_length=255, null=True)),
                ('is_new', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='categoryAPI.category')),
            ],
        ),
    ]
