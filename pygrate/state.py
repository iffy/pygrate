


class Column(object):
    """
    :ivar name: column name
    :ivar datatype: SQL data type
    """
    
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype