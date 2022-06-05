"""
Test custom Django management commands 
unit test for django command    
"""
# import patch the mock behavior 
# simulate when db is returing or respone or not 
from unittest.mock import patch
# the possibilities of the errors might get 
# when we try and connect to the db
from psycopg2 import OperationalError as Psycopg2OpError

# helper function provide by Django 
# to actually call the command by the name 
from django.core.management import call_command
# 
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# mock the behavior of the database 
# the command we're goint to mock 
# core.management.commands.wait_for_db => path 
# Command.check provide by the base command 
# which allows us to check the status of the database 
@patch('core.management.commands.wait_for_db.Command.check')

class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True
        call_command('wait_for_db')
        # check the method has been called 
        # make sure the check command in our patch which called with "databases=['default']" this parameters 
        # calling the right ring for our weight for db 
        patched_check.assert_called_once_with(databases=['default'])
    #mock the sleep 
    @patch('time.sleep')
    # test for the database should happend and should not happend 
    # if the database isn't ready 
    # the database return some exception or the check return some exception 
    # that indicate the databse is'nt ready yet 
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        
        """Test waiting for database when getting OperationalError."""
        # how the mocking work when we want to  raise the exception
        # it will rasie if the database wasn't ready 
        # raise the exception instead of the return useing => side effect
        # side effect allows you to pass in carious different items that 
        # get handdled differently depending of th type 
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
