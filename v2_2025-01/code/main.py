import os
import json
from datetime import datetime

from helper import db
from helper import llm
from helper import metrics

from variants import minimal
from variants import rules
from variants import sources

from sanity import doSanityChecks

retrievers = [minimal, rules, sources]

# sanity checks
if not doSanityChecks():
    print("Sanity Check Failed")
    quit()

# Retrieve clauses and LLM model name
clauses = db.getClauses()
print("Model", llm.model)
print("Compact Clauses:", len(clauses))

# Iterate over retrievers
for retriever in retrievers:
    # Prepare log file name and directory
    retriever_name = retriever.__name__.split('.')[-1]
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_dir = f"logs/{llm.model}/"

    # Ensure the directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Initialize results array and tracking lists
    results = []
    truth = []
    pred = []

    print(f"\n## Testing Retriever: {retriever_name}")
    for clause in clauses:
        # Use the current retriever to get the answer
        answer = retriever.addAnswer(json.loads(json.dumps(clause, ensure_ascii=False)))

        # Extract classification
        truth.append(answer["true_label"])
        pred.append(answer["pred_label"])

        results.append(answer)

        # Print progress
        print(f"-> {answer["pred_label"]} Truth: {clause['true_label']} ({len(pred)}/{len(clauses)})")

    # Compute metrics and add to the output
    metrics_output = metrics.getMetrics(truth, pred)

    with open(os.path.join(log_dir, f"{retriever_name}_{date_str}.json"), 'w', encoding='utf-8') as log:
        json.dump(results, log, indent=4, ensure_ascii=False)
    with open(os.path.join(log_dir, f"{retriever_name}_{date_str}.metrics"), 'w', encoding='utf-8') as met:
        met.write(metrics_output)
