from unittest import TestCase
from zope.interface.verify import verifyObject

try:
    from pysqlite2 import dbapi2 as sqlite
except ImportError:
    import sqlite3 as sqlite


from pygrate.state import Column
from pygrate import action
from pygrate.sqlite import ISqliteAction, CreateTable, dataType



class dataTypeTest(TestCase):


    def test_int(self):
        self.assertEqual(dataType('int'), 'integer')
        self.assertEqual(dataType('integer'), 'integer')


    def test_text(self):
        self.assertEqual(dataType('text'), 'text')


    def test_blob(self):
        self.assertEqual(dataType('rawstr'), 'blob')




class CreateTableTest(TestCase):


    def test_ISqliteAction(self):
        verifyObject(ISqliteAction, CreateTable(None))


    def test_basic_functional(self):
        """
        You should be able to make an sqlite table with normal fields
        """
        s = ISqliteAction(action.CreateTable('foo', [
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
        s = ISqliteAction(action.CreateTable('foo', [
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


        