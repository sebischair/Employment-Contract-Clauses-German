import json
import textstat  # Requires: pip install textstat
from collections import defaultdict


def calculate_metrics(results, rule_title_map=None):
    """
    Calculates granular metrics focused on Robo Judge output,
    linguistic quality, and rule-specific performance.

    Includes an "Overall" quality table, symmetrical metrics
    for TP/FP/FN, and a rule-performance table sorted by F1-Score.
    """
    total_clauses = len(results)
    if total_clauses == 0:
        return "No results to analyze."

    if rule_title_map is None:
        rule_title_map = {}

    # --- 1. Classification Counters ---
    tp, fp, fn, tn = 0, 0, 0, 0
    truly_void, truly_valid = 0, 0

    # --- 2. Robo Judge Aggregates (Overall) ---
    total_missed_problems = 0
    total_unnecessary_changes = 0

    # --- 3. Granular Judge Metrics (TP/FP/FN) ---
    tp_perfect, tp_good_sloppy, tp_partial_clean, tp_partial_sloppy = 0, 0, 0, 0
    tp_total_missed, tp_total_unnecessary = 0, 0
    fp_total_missed, fp_total_unnecessary = 0, 0
    fn_total_missed, fn_total_unnecessary = 0, 0
    fp_with_changes = 0

    # --- 4. Linguistic Quality Aggregates ---
    total_readability_delta = 0.0
    total_word_count_delta = 0
    total_corrections_for_linguistics = 0  # Counts both TPs and FPs

    # --- 5. Rule-Specific Metrics ---
    rule_metrics = defaultdict(lambda: {
        'total_violations': 0, 'hits': 0, 'misses': 0, 'hallucinations': 0
    })
    all_rule_ids = set()

    for r in results:
        is_true_void = r.get('true_label') == 'void'
        is_pred_void = r.get('pred_label') == 'void'

        original_clause = r['content']

        # --- 1. Populate Classification ---
        if is_true_void:
            truly_void += 1
            if is_pred_void:
                tp += 1
            else:
                fn += 1
        else:
            truly_valid += 1
            if is_pred_void:
                fp += 1
            else:
                tn += 1

        # --- 2. Populate Judge Metrics ---
        if 'robo_judge' in r and isinstance(r['robo_judge'], dict):
            judge = r['robo_judge']
            missed = judge.get('missed_problems', 0)
            unnecessary = judge.get('unnecessary_changes', 0)

            total_missed_problems += missed
            total_unnecessary_changes += unnecessary

            if is_true_void and is_pred_void:  # --- TRUE POSITIVE ---
                tp_total_missed += missed
                tp_total_unnecessary += unnecessary
                if missed == 0 and unnecessary == 0:
                    tp_perfect += 1
                elif missed == 0 and unnecessary > 0:
                    tp_good_sloppy += 1
                elif missed > 0 and unnecessary == 0:
                    tp_partial_clean += 1
                elif missed > 0 and unnecessary > 0:
                    tp_partial_sloppy += 1

            elif not is_true_void and is_pred_void:  # --- FALSE POSITIVE ---
                fp_total_missed += missed
                fp_total_unnecessary += unnecessary
                if unnecessary > 0:
                    fp_with_changes += 1

            elif is_true_void and not is_pred_void:  # --- FALSE NEGATIVE ---
                fn_total_missed += missed
                fn_total_unnecessary += unnecessary

        # --- 4. Populate Linguistic Metrics ---
        if is_pred_void:  # A correction was attempted (TP or FP)
            correction_text = r.get('pred_correction')
            if correction_text:
                try:
                    original_grade = textstat.flesch_kincaid_grade(original_clause)
                    correction_grade = textstat.flesch_kincaid_grade(correction_text)

                    original_words = len(original_clause.split())
                    correction_words = len(correction_text.split())

                    total_readability_delta += (correction_grade - original_grade)
                    total_word_count_delta += (correction_words - original_words)
                    total_corrections_for_linguistics += 1
                except Exception as e:
                    print(f"Warning: textstat failed for clause. Error: {e}")

        # --- 5. Populate Rule-Specific Metrics ---
        true_rules = set(r.get('true_hurt-rules', []))
        pred_rules = set(r.get('pred_hurt-rules', []))

        all_rule_ids.update(true_rules)
        all_rule_ids.update(pred_rules)

        for rule_id in true_rules:
            rule_metrics[rule_id]['total_violations'] += 1
        for rule_id in true_rules.intersection(pred_rules):
            rule_metrics[rule_id]['hits'] += 1
        for rule_id in true_rules.difference(pred_rules):
            rule_metrics[rule_id]['misses'] += 1
        for rule_id in pred_rules.difference(true_rules):
            rule_metrics[rule_id]['hallucinations'] += 1

    # --- Calculations for Tables ---
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (tp + tn) / total_clauses if total_clauses > 0 else 0

    avg_missed_per_clause = total_missed_problems / total_clauses if total_clauses > 0 else 0
    avg_unnecessary_per_clause = total_unnecessary_changes / total_clauses if total_clauses > 0 else 0
    avg_readability_delta = total_readability_delta / total_corrections_for_linguistics if total_corrections_for_linguistics > 0 else 0
    avg_word_count_delta = total_word_count_delta / total_corrections_for_linguistics if total_corrections_for_linguistics > 0 else 0
    avg_missed_per_tp = tp_total_missed / tp if tp > 0 else 0
    avg_unnecessary_per_tp = tp_total_unnecessary / tp if tp > 0 else 0
    avg_missed_per_fp = fp_total_missed / fp if fp > 0 else 0
    avg_unnecessary_per_fp = fp_total_unnecessary / fp if fp > 0 else 0
    avg_missed_per_fn = fn_total_missed / fn if fn > 0 else 0
    avg_unnecessary_per_fn = fn_total_unnecessary / fn if fn > 0 else 0

    # --- Format Output ---
    output_lines = [
        "**Benchmark Summary**",
        f"* **Total Clauses:** {total_clauses}",
        f"* **Truly Void:** {truly_void}",
        f"* **Truly Valid:** {truly_valid}",
        "\n---",
        "**1. Classification Metrics (The \"Funnel\")**",
        "\n| Metric | Score |",
        "| :--- | :--- |",
        f"| Accuracy | {accuracy:.2%} |",
        f"| Precision | {precision:.2%} |",
        f"| Recall | {recall:.2%} |",
        f"| F1-Score | {f1:.2f} |",
        "\n| | **Predicted: Void** | **Predicted: Valid** |",
        "| :--- | :--- | :--- |",
        f"| **Actual: Void** | {tp} (TP) | {fn} (FN) |",
        f"| **Actual: Valid** | {fp} (FP) | {tn} (TN) |",
        "\n---",
        "**2. Linguistic Quality of Corrections**",
        f"*(n = {total_corrections_for_linguistics} attempted corrections)*",
        "\n| Linguistic Metric | Avg. Delta |",
        "| :--- | :--- |",
        f"| Readability (Flesch-Kincaid Grade) | {avg_readability_delta:+.2f} grades |",
        f"| Verbosity (Word Count) | {avg_word_count_delta:+.2f} words |",
        "\n---",
        "**3. Overall Correction Quality (All Clauses)**",
        f"*(n = {total_clauses} clauses)*",
        "\n| Metric | Total | Avg. per Clause |",
        "| :--- | :--- | :--- |",
        f"| **Total Problems Missed** | {total_missed_problems} | {avg_missed_per_clause:.2f} |",
        f"| **Total Unnecessary Changes** | {total_unnecessary_changes} | {avg_unnecessary_per_clause:.2f} |",
        "\n---",
        f"**4. Correction Quality Analysis: True Positives (TPs)**\n*(n = {tp} clauses)*",
        "\n| Correction Quality | Count | % of TPs |",
        "| :--- | :--- | :--- |",
        f"| **Perfect** (Fixed all, 0 junk) | {tp_perfect} | {tp_perfect / tp:.2%}" if tp > 0 else "| **Perfect** (Fixed all, 0 junk) | 0 | 0.00% |",
        f"| **Good, but Sloppy** (Fixed all, >0 junk) | {tp_good_sloppy} | {tp_good_sloppy / tp:.2%}" if tp > 0 else "| **Good, but Sloppy** (Fixed all, >0 junk) | 0 | 0.00% |",
        f"| **Partial, but Clean** (Missed some, 0 junk) | {tp_partial_clean} | {tp_partial_clean / tp:.2%}" if tp > 0 else "| **Partial, but Clean** (Missed some, 0 junk) | 0 | 0.00% |",
        f"| **Partial & Sloppy** (Missed some, >0 junk) | {tp_partial_sloppy} | {tp_partial_sloppy / tp:.2%}" if tp > 0 else "| **Partial & Sloppy** (Missed some, >0 junk) | 0 | 0.00% |",
        "\n| TP Error Averages | Total | Avg. per TP |",
        "| :--- | :--- | :--- |",
        f"| Missed Problems | {tp_total_missed} | {avg_missed_per_tp:.2f} |",
        f"| Unnecessary Changes | {tp_total_unnecessary} | {avg_unnecessary_per_tp:.2f} |",
        "\n---",
        f"**5. Correction Quality Analysis: False Positives (FPs)**\n*(n = {fp} clauses)*",
        "\n| FP Error Averages | Total | Avg. per FP |",
        "| :--- | :--- | :--- |",
        f"| Missed Problems | {fp_total_missed} | {avg_missed_per_fp:.2f} |",
        f"| Unnecessary Changes | {fp_total_unnecessary} | {avg_unnecessary_per_fp:.2f} |",
        "\n---",
        f"**6. Correction Quality Analysis: False Negatives (FNs)**\n*(n = {fn} clauses)*",
        "\n| FN Error Averages | Total | Avg. per FN |",
        "| :--- | :--- | :--- |",
        f"| Missed Problems | {fn_total_missed} | {avg_missed_per_fn:.2f} |",
        f"| Unnecessary Changes | {fn_total_unnecessary} | {avg_unnecessary_per_fn:.2f} |",
        "\n---",
        "**7. Rule-Specific Performance**",
        "\n| Rule ID | Title | Total Violations | Hits | Misses | Hallucinations | Rule Recall | Rule Precision | F1-Score |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    # --- Build, Sort, and Print Rule Table ---

    # 1. Build a list of dicts with all rule data
    rule_table_data = []
    for rule_id in all_rule_ids:
        stats = rule_metrics[rule_id]
        total_violations = stats['total_violations']
        hits = stats['hits']
        misses = stats['misses']
        hallucinations = stats['hallucinations']

        rule_recall = hits / total_violations if total_violations > 0 else 0
        rule_precision = hits / (hits + hallucinations) if (hits + hallucinations) > 0 else 0

        if (rule_precision + rule_recall) == 0:
            rule_f1 = 0.0
        else:
            rule_f1 = 2 * (rule_precision * rule_recall) / (rule_precision + rule_recall)

        rule_table_data.append({
            "id": rule_id,
            "title": rule_title_map.get(str(rule_id), "N/A"),
            "violations": total_violations,
            "hits": hits,
            "misses": misses,
            "hallucinations": hallucinations,
            "recall": rule_recall,
            "precision": rule_precision,
            "f1": rule_f1
        })

    # 2. Sort the list by F1-Score, descending
    sorted_rule_data = sorted(rule_table_data, key=lambda x: x['f1'], reverse=True)

    # 3. Add the sorted rows to the output
    for row in sorted_rule_data:
        title = row['title']
        if len(title) > 40:
            title = title[:37] + "..."

        output_lines.append(
            f"| {row['id']} | {title} | {row['violations']} | "
            f"{row['hits']} | {row['misses']} | {row['hallucinations']} | "
            f"{row['recall']:.2%} | {row['precision']:.2%} | {row['f1']:.2%} |"
        )

    # Final cleanup for edge cases
    final_output = "\n".join(output_lines)
    final_output = final_output.replace("nan%", "0.00%").replace("inf%", "0.00%")

    return final_output.strip()