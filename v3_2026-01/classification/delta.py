import json
import os
from collections import defaultdict
from data import db


def get_rule_title_map():
    """
    Loads rules from the DB and creates a mapping from hex-ID to title.
    """
    print("Loading rule titles from database...")
    hex_to_title = {}
    try:
        grouped_rules = db.getGroupedRules()
        for topic, rules in grouped_rules.items():
            for rule in rules:
                hex_id = str(rule["_id"])
                title = rule.get("name", rule.get("title", rule.get("text", "N/A")))
                if len(title) > 60:
                    title = title[:57] + "..."
                hex_to_title[hex_id] = title
        print(f"-> Loaded {len(hex_to_title)} rule titles.")
        return hex_to_title
    except Exception as e:
        print(f"ERROR: Could not load db.getGroupedRules(): {e}")
        print("Continuing with empty titles.")
        return {}


def calculate_rule_metrics(stats):
    """
    Calculates Recall, Precision, and F1 from counters (Hits, Misses, etc.).
    """
    hits = stats.get('hits', 0)
    total_violations = stats.get('total_violations', 0)
    hallucinations = stats.get('hallucinations', 0)

    recall = hits / total_violations if total_violations > 0 else 0
    precision = hits / (hits + hallucinations) if (hits + hallucinations) > 0 else 0

    if (precision + recall) == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    return {'r': recall, 'p': precision, 'f1': f1}


def analyze_rule_deltas(file_paths, rule_title_map):
    """
    Process multiple JSON files sequentially and create a delta report.
    Shows cumulative statistics first (including F1), then the individual
    rule analysis sorted by the strongest increase in hallucinations.
    """

    all_rule_data = defaultdict(dict)  # Structure: {file_path: {rule_id: {stats}}}
    all_file_summary_stats = {}
    all_rule_ids = set()

    # --- 1. Gather data from all files ---
    print("\nProcessing JSON files...")
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"WARNING: File {file_path} not found. Skipping.")
            continue

        print(f"  -> Loading: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            results = json.load(f)

        file_rule_metrics = defaultdict(lambda: defaultdict(int))

        total_hits_in_file = 0
        total_misses_in_file = 0
        total_hallucinations_in_file = 0

        for item in results:
            true_rules = set(item.get('true_hurt-rules', []))
            pred_rules = set(item.get('pred_hurt-rules', []))

            all_rule_ids.update(true_rules)
            all_rule_ids.update(pred_rules)

            hits = true_rules.intersection(pred_rules)
            misses = true_rules.difference(pred_rules)
            hallucinations = pred_rules.difference(true_rules)

            total_hits_in_file += len(hits)
            total_misses_in_file += len(misses)
            total_hallucinations_in_file += len(hallucinations)

            for rule_id in true_rules:
                file_rule_metrics[rule_id]['total_violations'] += 1
            for rule_id in hits:
                file_rule_metrics[rule_id]['hits'] += 1
            for rule_id in misses:
                file_rule_metrics[rule_id]['misses'] += 1
            for rule_id in hallucinations:
                file_rule_metrics[rule_id]['hallucinations'] += 1

        all_rule_data[file_path] = file_rule_metrics

        all_file_summary_stats[file_path] = {
            'total_hits': total_hits_in_file,
            'total_misses': total_misses_in_file,
            'total_hallucinations': total_hallucinations_in_file
        }

    if not all_rule_data:
        return "No valid files found. Aborting."

    # --- 2. Pre-calculate sorting data ---
    print("Calculating total hallucination increase for sorting...")
    sorting_data = []

    valid_file_paths = [p for p in file_paths if p in all_rule_data]

    if len(valid_file_paths) >= 2:
        first_file_path = valid_file_paths[0]
        last_file_path = valid_file_paths[-1]

        for rule_id in all_rule_ids:
            stats_first = all_rule_data[first_file_path].get(rule_id, {})
            hallucinations_first = stats_first.get('hallucinations', 0)

            stats_last = all_rule_data[last_file_path].get(rule_id, {})
            hallucinations_last = stats_last.get('hallucinations', 0)

            total_increase = hallucinations_last - hallucinations_first
            sorting_data.append({'id': rule_id, 'increase': total_increase})

        sorting_data.sort(key=lambda x: x['increase'], reverse=True)
        sorted_rule_ids = [item['id'] for item in sorting_data]

        sorting_note = (f"*(Detail tables sorted by strongest **absolute increase in hallucinations** from "
                        f"'{os.path.basename(first_file_path)}' to "
                        f"'{os.path.basename(last_file_path)}')*")
    else:
        print("Less than 2 valid files, using alphabetical sorting.")
        sorted_rule_ids = sorted(list(all_rule_ids))
        sorting_note = "*(Detail tables sorted alphabetically as there are fewer than 2 valid files)*"

    # --- 3. Generate Report ---
    print("\nGenerating Delta Report...")
    output_lines = ["# Delta Analysis of Rule Detection"]

    output_lines.append("\n## 📊 Cumulative Rule Statistics (Across All Rules)")
    output_lines.append(
        "\n| File (Model) | Total Hits | Total Misses | Total Hallucs. | Total Recall | Total Precision | Total F1 |")
    output_lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")

    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        if file_path not in all_file_summary_stats:
            output_lines.append(f"| **{file_name}** | - | - | - | *File not found* | - | - |")
            continue

        stats = all_file_summary_stats[file_path]
        h = stats['total_hits']
        m = stats['total_misses']
        hc = stats['total_hallucinations']

        recall = h / (h + m) if (h + m) > 0 else 0
        precision = h / (h + hc) if (h + hc) > 0 else 0

        if (precision + recall) == 0:
            f1 = 0.0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

        output_lines.append(
            f"| **{file_name}** | {h} | {m} | {hc} | {recall:.2%} | {precision:.2%} | {f1:.2%} |"
        )

    output_lines.append(f"\n---\n\n## 🔎 Individual Rule Analysis")
    output_lines.append(sorting_note)

    for rule_id in sorted_rule_ids:
        title = rule_title_map.get(rule_id, "N/A")

        output_lines.append(f"\n### 📜 Rule: {title}")
        output_lines.append(f"**ID:** `{rule_id}`")

        output_lines.append(
            "\n| File (Model) | Hits | Misses | Hallucs. | Recall (Delta) | Precision (Delta) | F1-Score (Delta) |")
        output_lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")

        previous_metrics = None

        for file_path in file_paths:
            if file_path not in all_rule_data:
                file_name = os.path.basename(file_path)
                output_lines.append(f"| **{file_name}** | - | - | - | *File not found* | - | - |")
                continue

            file_name = os.path.basename(file_path)
            stats = all_rule_data[file_path].get(rule_id, {})

            h = stats.get('hits', 0)
            m = stats.get('misses', 0)
            hc = stats.get('hallucinations', 0)

            metrics = calculate_rule_metrics(stats)
            r, p, f1 = metrics['r'], metrics['p'], metrics['f1']

            delta_str_r, delta_str_p, delta_str_f1 = "", "", ""
            if previous_metrics is not None:
                delta_r = r - previous_metrics['r']
                delta_p = p - previous_metrics['p']
                delta_f1 = f1 - previous_metrics['f1']

                delta_str_r = f" ({delta_r:+.2%})"
                delta_str_p = f" ({delta_p:+.2%})"
                delta_str_f1 = f" ({delta_f1:+.2%})"

            output_lines.append(
                f"| **{file_name}** | {h} | {m} | {hc} | "
                f"{r:.2%}{delta_str_r} | {p:.2%}{delta_str_p} | {f1:.2%}{delta_str_f1} |"
            )

            previous_metrics = metrics

    print("Report generation complete.")
    return "\n".join(output_lines)


def main():
    BASE_PATH = "logs/"
    FILE_PATHS = [
        os.path.join(BASE_PATH, "gpt-4.1-2025-04-14/rules_2025-11-26.json"),
        os.path.join(BASE_PATH, "gpt-5-2025-08-07-high-reasoning/rules_2025-11-26.json"),
        os.path.join(BASE_PATH, "gpt-5-2025-08-07-medium-reasoning/rules_2025-11-26.json"),
        os.path.join(BASE_PATH, "gpt-5-2025-08-07-minimal-reasoning/rules_2025-11-26.json")
    ]
    OUTPUT_FILE = "delta_rule_report_gpt.md"

    #FILE_PATHS = [
    #    "logs/gemini-2.5-flash-preview-09-2025/rules_2025-11-26.json",
    #    "logs/gemini-2.5-pro-minimal-reasoning/rules_2025-11-26.json",
    #    "logs/gemini-2.5-pro-medium-reasoning/rules_2025-11-26.json",
    #    "logs/gemini-2.5-pro-high-reasoning/rules_2025-11-26.json"
    #]
    #OUTPUT_FILE = "delta_rule_report_gemini.md"

    rule_title_map = get_rule_title_map()
    report_content = analyze_rule_deltas(FILE_PATHS, rule_title_map)

    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"\n✅ Success! Delta report saved to '{OUTPUT_FILE}'.")
    except Exception as e:
        print(f"\n❌ ERROR saving report: {e}")


if __name__ == "__main__":
    main()