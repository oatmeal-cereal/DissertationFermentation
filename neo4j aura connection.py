from neo4j import GraphDatabase
from neo4j import Query
from typing_extensions import LiteralString
import json
import re

with open('..\\dissertation DLC content\\go away\\passwords.json', 'r') as f:
    passwords = dict(json.load(f))

neo4j_pw = passwords['neo4j']

del passwords

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", neo4j_pw)

driver = GraphDatabase.driver(URI, auth=AUTH, max_connection_lifetime=3600)

def process_entities(session):
    with open('all_entity_commands.cypher', 'r', encoding='utf-8') as f:
        entities = f.readlines()

    for entity in entities:
        session.run(entity)

def process_relations(session):
    with open('all_relation_commands.cypher', 'r', encoding='utf-8') as f:
        relations = f.readlines()
        
    for relation in relations:
        print(relation)
        ents = re.findall("\\([A-Za-z0-9]+\\)", relation)

        ent1 = ents[0][1:-1]
        ent2 = ents[1][1:-1]

        rel = re.findall("\\[:[A-Za-z0-9]+\\]", relation)[0][2:-1]

        query = f"""MATCH (a) WHERE a.customId = '{ent1}'
                    MATCH (b) WHERE b.customId = '{ent2}'
                    MERGE (a)-[:{rel}]->(b)"""

        session.run(query)

with driver.session() as session:
    process_entities(session)

    process_relations(session)