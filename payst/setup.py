def setup_database(address):
    from pycassa.system_manager import *
    sys = SystemManager(address)
    sys.create_keyspace("Payst", SIMPLE_STRATEGY, {'replication_factor': '1'})
    sys.create_column_family("Payst", "Paste")
    sys.close()
