# Generated by Django 4.0.10 on 2023-06-27 23:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('region', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='username')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(blank=True, max_length=32, null=True, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='Email for signin')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Phone number')),
                ('is_staff', models.BooleanField(default=False)),
                ('gender', models.CharField(blank=True, max_length=16, null=True, verbose_name='User Gender')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='date of birth')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/user/profile/', verbose_name='User Profile Photo')),
                ('id_card_photo', models.ImageField(blank=True, null=True, upload_to='images/user/id_card/', verbose_name='User Id Card Photo')),
                ('biography', models.CharField(blank=True, max_length=8192, null=True, verbose_name='User biography')),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('invite_code', models.CharField(blank=True, max_length=256, null=True)),
                ('bank_account_number', models.CharField(blank=True, max_length=128, null=True)),
                ('count_coin', models.IntegerField(blank=True, null=True)),
                ('is_premium', models.BooleanField(blank=True, default=False, null=True)),
                ('deactive', models.BooleanField(blank=True, default=False, null=True)),
                ('otp', models.CharField(default=0, max_length=32, verbose_name='OTP')),
                ('otp_expiry', models.DateTimeField(blank=True, null=True, verbose_name='OTP Expiry Date')),
                ('max_otp_try', models.CharField(default=3, max_length=2)),
                ('otp_max_out', models.DateTimeField(blank=True, null=True)),
                ('otp_accept', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='region.city', verbose_name='City')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.CharField(max_length=255, verbose_name='Interest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'User Interests',
            },
        ),
        migrations.CreateModel(
            name='LoginActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('success', models.BooleanField(blank=True, default=True, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=255, null=True)),
                ('device_type', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blocked_date', models.DateTimeField(auto_now_add=True)),
                ('blocked_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_who_is_blocked', to=settings.AUTH_USER_MODEL, verbose_name='blocked_user')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_who_blocked', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'unique_together': {('user', 'blocked_user')},
            },
        ),
    ]
