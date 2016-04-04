from datetime import timedelta

from chirps.models import Chirp
from django.core.management import BaseCommand
from django.utils import timezone


class Command(BaseCommand):



    def add_arguments(self, parser):
        parser.add_argument("--dry_run", action='store_true', help="Don't Commit Changes")
        parser.add_argument("--limit", type=int, help="Limit the results",
                            default=1)

    def handle(self, *args, **options):

        three_months_ago = timezone.now() - timedelta(days=90)
        qs = Chirp.objects.filter(archived=False) \
            .filter(created_at__lt=three_months_ago)

        if options["dry_run"]:
            rows = qs.count()
            self.stdout.write("Update would affect {} rows".format(rows))
        else:
            rows = qs.update(archived=True)
            self.stdout.write("Update affected {} rows".format(rows))

