from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+s://9864518a.databases.neo4j.io"
AUTH = ("neo4j", "BlRJIZ4R-eyomKYVOObJSQ8fYZZiH-sZ7E74FJF5xg4")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    
    with open('tiny_example.cypher', 'r', encoding='utf-8') as f:
        queries = f.readlines()
        
    for query in queries:
        driver.execute_query(query)