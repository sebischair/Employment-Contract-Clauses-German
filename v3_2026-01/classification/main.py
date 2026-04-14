import os
import json
from datetime import datetime
from data import db
import metrics

from retriever import rules

retrievers = [rules]

# Retrieve clauses and LLM model name
model = "gpt-5-2025-08-07"
clauses = db.getClauses()
print("Model", model)
print("Total Clauses:", len(clauses))

# Iterate over retrievers
for retriever in retrievers:
    # Prepare log file name and directory
    retriever_name = retriever.__name__.split('.')[-1]
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_dir = f"logs/{model}/"

    # Ensure the directory exists
    os.makedirs(log_dir, exist_ok=True)

    log_file_path = os.path.join(log_dir, f"{retriever_name}_{date_str}.json")
    metrics_file_path = os.path.join(log_dir, f"{retriever_name}_{date_str}.metrics")

    # Initialize results array and tracking set
    results = []
    processed_clause_contents = set()

    # Load existing results if file exists
    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
                # Use 'content' from the clause, assuming it's present in the 'answer' object
                processed_clause_contents = {entry.get("content") for entry in results}
            print(f"Loaded {len(results)} already processed results from {log_file_path}.")
        except json.JSONDecodeError:
            print(f"Warning: Could not parse existing log file {log_file_path}. Starting fresh.")
            results = []
            processed_clause_contents = set()
        except Exception as e:
            print(f"Error loading log file: {e}. Starting fresh.")
            results = []
            processed_clause_contents = set()

    # Populate truth and pred from loaded results
    truth = [entry.get("true_label") for entry in results]
    pred = [entry.get("pred_label") for entry in results]

    print(f"\n## Testing Retriever: {retriever_name}")
    processed_count = len(results)

    for i, clause in enumerate(clauses):
        clause_content = clause.get("content")  # Use content as unique identifier

        # Skip if already processed
        if clause_content in processed_clause_contents:
            # Shorten content for cleaner logging
            print(f"skipping clause: {clause_content[:70]}...")
            continue

        # Use the current retriever to get the answer
        # Pass a copy to avoid modifying the original 'clause' object in memory
        answer = retriever.addAnswer(model, json.loads(json.dumps(clause, ensure_ascii=False)))

        # Handle None response from retriever (all retries failed)
        if answer is None:
            print(f"  -> Retriever failed for clause after retries. Skipping.")
            continue

        # Extract classification
        truth.append(answer["true_label"])
        pred.append(answer["pred_label"])

        results.append(answer)
        processed_count += 1

        # Print progress
        print(f"-> {answer['pred_label']} Truth: {clause['true_label']} ({processed_count}/{len(clauses)})")

        # Save progress after each clause
        try:
            with open(log_file_path, 'w', encoding='utf-8') as log:
                json.dump(results, log, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving progress to {log_file_path}: {e}")

    # Compute final metrics and add to the output
    print(f"\nCalculating final metrics for {retriever_name}...")
    metrics_output = metrics.getMetrics(truth, pred)

    # Save final results and metrics
    with open(log_file_path, 'w', encoding='utf-8') as log:
        json.dump(results, log, indent=4, ensure_ascii=False)
    print(f"Final results saved to {log_file_path}")

    with open(metrics_file_path, 'w', encoding='utf-8') as met:
        met.write(metrics_output)
    print(f"Metrics saved to {metrics_file_path}")

print("\nBenchmark complete.")
