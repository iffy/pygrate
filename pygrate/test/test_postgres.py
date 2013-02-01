from twisted.trial.unittest import TestCase
from zope.interface.verify import verifyObject


from pygrate.state import Column
from pygrate import action
from pygrate.postgres import IPostgresAction, CreateTable, dataType


import os

skip_postgres = ''

try:
    import psycopg2
except ImportError:
    skip_postgres = 'psycopg2 not installed'


connkw = {}
def connect():
    return psycopg2.connect(connkw)


if os.environ.get('PG_DB', ''):
    from urlparse import urlparse
    r = urlparse(os.environ['PG_DB'])
    connkw.update({
        'database': r.path.lstrip('/'),
        'user': r.username,
        'host': r.hostname,
        'port': r.port,
    })
else:
    skip_postgres = 'No PG_DB env set'



class dataTypeTest(TestCase):


    def test_int(self):
        self.assertEqual(dataType('int'), 'integer')
        self.assertEqual(dataType('integer'), 'integer')


    def test_text(self):
        self.assertEqual(dataType('text'), 'text')


    def test_blob(self):
        self.assertEqual(dataType('rawstr'), 'blob')




class CreateTableTest(TestCase):


    skip = skip_postgres


    def test_IPostgresAction(self):
        verifyObject(IPostgresAction, CreateTable(None))


    def test_basic_functional(self):
        """
        You should be able to make an sqlite table with normal fields
        """
        s = IPostgresAction(action.CreateTable('foo', [
            Column('a', 'integer'),
            Column('b', 'integer'),
        ]))
        
        db = sqlite.connect(':memory:')
        s.run(db)
        
        c = db.cursor()
        c.execute('insert into foo (a, b) values (?, ?)', (1, 2))
        c.execute('select * from foo')
        rows = c.fetchall()
        self.assertEqual(rows, [
            (1, 2),
        ])


    def test_autoincrement(self):
        """
        A single autoincrementing integer should work
        """
        s = IPostgresAction(action.CreateTable('foo', [
            Column('a', 'integer', primary=True, autoincrement=True),
        ]))
        
        db = sqlite.connect(':memory:')
        s.run(db)
        
        c = db.cursor()
        c.execute('insert into foo default values')
        c.execute('insert into foo default values')
        c.execute('select * from foo order by a')
        rows = c.fetchall()
        self.assertEqual(rows, [
            (1,),
            (2,),
        ])


        