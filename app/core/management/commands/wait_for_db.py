"""
Django command to wait for the database to be available 
"""
# for sleep 
import time
# the error from psycopg2 when the db isn't ready 
from psycopg2 import OperationalError as Psycopg2OpError
# the error django throws when database is not ready 
from django.db.utils import OperationalError


from django.core.management.base import BaseCommand

# basic empty stab for creating a command 
class Command(BaseCommand):
    """Django command to wait for database."""
    #minimum code need for adding Django command 
    def handle(self, *args, **options):
         
         
        
        # standad output
        self.stdout.write('Waiting for database...')
        # in the first we assume the databse is not up till we know 
        db_up = False
        while db_up is False:
            try:
                # the check method we mock inside out tests 
                    # if we call this and the databse is not ready => thros an exception
                    # which will raise the operational error or
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
