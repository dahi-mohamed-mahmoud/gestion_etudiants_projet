from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'
    verbose_name = 'Gestion des étudiants'

    def ready(self):
        from django.db.models.signals import post_migrate

        def seed_filieres(sender, **kwargs):
            if sender.name != 'students':
                return

            from .models import Filiere

            defaults = [
                ("INFO", "Informatique", "Filière Informatique"),
                ("GEST", "Gestion", "Filière Gestion"),
                ("ELEC", "Électronique", "Filière Électronique"),
            ]

            for code, nom, description in defaults:
                Filiere.objects.get_or_create(
                    code=code,
                    defaults={"nom": nom, "description": description},
                )

        post_migrate.connect(
            seed_filieres,
            sender=self,
            dispatch_uid='students.seed_filieres',
            weak=False,
        )
