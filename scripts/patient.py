from gqlalchemy import Memgraph

MEMGRAPH_HOST = '3.145.26.159'
MEMGRAPH_PORT = 7687
MEMGRAPH_USERNAME = 'rishinpandit98@gmail.com'
MEMGRAPH_PASSWORD = 'Healthcare@123'

def query_memgraph():
    connection = Memgraph(
        host=MEMGRAPH_HOST,
        port=MEMGRAPH_PORT,
        username=MEMGRAPH_USERNAME,
        password=MEMGRAPH_PASSWORD,
        encrypted=True
    )
    results = connection.execute_and_fetch(
        'MATCH (n:Patient) RETURN n'
    )
    print(results)
    for result in results:
        print(result)

if __name__ == "__main__":
    query_memgraph()
