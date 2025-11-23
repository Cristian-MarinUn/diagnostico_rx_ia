from django.core.management.base import BaseCommand
from authentication.tasks import InactivityMonitor

class Command(BaseCommand):
    help = 'Verifica y cierra sesiones inactivas'
    
    def handle(self, *args, **options):
        count = InactivityMonitor.check_inactive_sessions()
        self.stdout.write(
            self.style.SUCCESS(
                f'Se cerraron {count} sesiones inactivas'
            )
        )