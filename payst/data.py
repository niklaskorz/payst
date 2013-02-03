from __future__ import absolute_import, print_function
from pycassa import NotFoundException
import pycassa

pool = pycassa.ConnectionPool("Payst")
paste_cf = pycassa.ColumnFamily(pool, "Paste")
