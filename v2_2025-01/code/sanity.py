import os
from helper import db

def doSanityChecks():
    clauses = db.getClauses()
    topics = db.getTopics()
    rules = db.getRules()

    issues_found = False

    topic_names = [t['title'] for t in topics]
    for clause in clauses:
        if clause['topic'] not in topic_names:
            print(f"Clause topic {clause['topic']} does not exist in topics list.")
            issues_found = True

    topic_ids = [t['_id'] for t in topics]
    for rule in rules:
        if rule['topic'] not in topic_ids:
            print(f"Rule topic {rule['topic']} does not exist in topics list.")
            issues_found = True

    for rule in rules:
        for reference in rule['references']:
            filename = reference.replace('.', '_').replace('/', '+')+".md"
            filepath = os.path.join("../data/sources", filename)
            if not os.path.isfile(filepath):
                print(f"File for reference {reference} does not exist at: {filepath}")
                issues_found = True

    return not issues_found

if __name__ == "__main__":
    result = doSanityChecks()
    print("Sanity Check Result:", "Passed" if result else "Failed")
