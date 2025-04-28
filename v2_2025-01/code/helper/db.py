from helper import files

# File paths
topics_file = "../data/topics.json"
rules_file = "../data/rules.json"
clauses_file = "../data/clauses.json"

# Load data from disk
_topics_cache = files.readJson(topics_file)
_rules_cache = files.readJson(rules_file)
_clauses_cache = files.readJson(clauses_file)

def getClauses():
    return _clauses_cache

def getTopics():
    return _topics_cache

def getRules():
    return _rules_cache

def getGroupedRules():
    # Create a map of topic IDs to topic titles
    topic_map = {str(topic["_id"]): topic.get("title", "Unknown Topic") for topic in _topics_cache}

    # Group rules by topic titles
    grouped_rules = {}
    for rule in _rules_cache:
        topic_id = str(rule["topic"])  # Convert ObjectId to string
        topic_title = topic_map.get(topic_id, "Unknown Topic")

        if topic_title not in grouped_rules:
            grouped_rules[topic_title] = []
        grouped_rules[topic_title].append(rule)

    return grouped_rules
