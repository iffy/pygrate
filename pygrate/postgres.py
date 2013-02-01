from zope.interface import implements, Interface
from twisted.python.components import registerAdapter

from pygrate import action



def dataType(general_type):
    return {
        'int': 'integer',
        'integer': 'integer',
        'rawstr': 'blob',
        'text': 'text',
    }[general_type]



class IPostgresAction(Interface):


    def run(db):
        """
        Apply an action to an SQLite database.
        
        :param db: a database connection from which a cursor may be obtained
        """



class CreateTable(object):

    implements(IPostgresAction)
    
    
    def __init__(self, original):
        self.original = original


    def run(self, db):
        c = db.cursor()
        columns = []
        for column in self.original.columns:
            if column.autoincrement:
                columns.append('%s integer primary key' % (column.name,))
            else:
                columns.append('%s %s' % (column.name, dataType(column.datatype)))
        sql = 'CREATE TABLE %(name)s (%(columns)s)' % {
            'name': self.original.name,
            'columns': ', '.join(columns),
        }
        c.execute(sql)



registerAdapter(CreateTable, action.CreateTable, IPostgresAction)