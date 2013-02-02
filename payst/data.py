import pycassa

pool = pycassa.ConnectionPool("Payst")
paste_cf = pycassa.ColumnFamily(pool, "Paste")
