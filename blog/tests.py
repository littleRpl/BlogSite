from django.test import TestCase

# Create your tests here.

import sqlite3

con = sqlite3.connect('db')
cursor = con.cursor()