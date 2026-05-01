from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicBlog', '0004_review_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('friend_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friended_by', to='musicBlog.profile')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships', to='musicBlog.profile')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('profile', 'friend_profile'), name='unique_musicblog_friendship')],
            },
        ),
    ]