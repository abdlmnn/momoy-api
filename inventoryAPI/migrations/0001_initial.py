from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productAPI', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(upload_to='products/variants/', blank=True, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('product', models.ForeignKey(related_name='variants', on_delete=django.db.models.deletion.CASCADE, to='productAPI.product')),
            ],
        ),
    ]
