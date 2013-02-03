from pycassa.system_manager import *

def prepare_database(address="localhost:9160"):
    sys = SystemManager(address)
    sys.create_keyspace("Payst", SIMPLE_STRATEGY, {'replication_factor': '1'})
    sys.create_column_family("Payst", "Paste")
    sys.close()

if __name__ == "__main__":
    prepare_database()
