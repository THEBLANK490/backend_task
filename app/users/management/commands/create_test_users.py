from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from app.users.models import User


class Command(BaseCommand):
    help = "Create test users with locations and vector lines"

    def handle(self, *args, **options):
        users_data = [
            {
                "username": "ram",
                "password": "Test@321",
                "home_address": Point(85.324, 27.7172),
                "office_address": Point(85.3235, 27.7075),
            },
            {
                "username": "hari",
                "password": "Test@321",
                "home_address": Point(85.321, 27.7180),
                "office_address": Point(85.325, 27.7020),
            },
            {
                "username": "shyam",
                "password": "Test@321",
                "home_address": Point(83.9856, 28.2096),
                "office_address": Point(83.9956, 28.2046),
            },
        ]

        for udata in users_data:
            user, created = User.objects.get_or_create(
                username=udata["username"],
                defaults={
                    "home_address": udata["home_address"],
                    "office_address": udata["office_address"],
                },
            )
            if created:
                user.set_password(udata["password"])
                user.save()
                self.stdout.write(f"Created user {user.username}")
            else:
                self.stdout.write(f"User {user.username} already exists")

            self.stdout.write(f"UserVectorLine updated for {user.username}")
