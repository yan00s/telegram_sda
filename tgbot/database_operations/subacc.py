from .database_connector import execute_query

def add_dbsub(peeridsub, access_code):
    req = "INSERT INTO subaccs (peerid, access) VALUES (?, ?)"
    execute_query(req, [peeridsub,access_code])
    
    
def dell_dbsub(peeridsub):
    req = "DELETE FROM subaccs WHERE peerid = ?"
    execute_query(req, [peeridsub])