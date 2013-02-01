


class Column(object):
    """
    :ivar name: column name
    :ivar datatype: SQL data type
    """
    
    def __init__(self, name, datatype, primary=False, autoincrement=False):
        self.name = name
        self.datatype = datatype
        self.primary = primary
        self.autoincrement = autoincrement