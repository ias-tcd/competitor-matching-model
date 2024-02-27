import importlib

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs a script in django context."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("model")

    def handle(self, *args, **options):
        model = options.get("model")
        main = importlib.import_module(f"ml.models.{model}.main")
        main.main()
