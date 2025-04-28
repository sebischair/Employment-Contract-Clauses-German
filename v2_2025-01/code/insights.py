import json
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import defaultdict


def analyze_rules(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        rules = json.load(f)

    word_counts = []
    all_references = set()

    for rule in rules:
        text = rule.get("text", "")  # Handle missing "text" fields
        words = text.split()
        word_counts.append(len(words))

        references = rule.get("references", [])
        for ref in references:
            all_references.add(ref)

    num_rules = len(rules)
    num_unique_references = len(all_references)

    print(f"Total number of rules: {num_rules}")
    print(f"Total number of unique references: {num_unique_references}")

    print("\nStats for Rules:") # Added stats output
    if word_counts:
        print(f"Min: {min(word_counts)}")
        print(f"Max: {max(word_counts)}")
        print(f"Avg: {np.mean(word_counts):.2f}")
    else:
        print("No rule texts found.")


    # Plotting the histogram
    if word_counts: # Check if word_counts is not empty before plotting
        plt.figure(figsize=(10, 6))  # Adjust figure size for better readability
        plt.hist(word_counts, bins=np.arange(min(word_counts)-0.5, max(word_counts)+1.5, 1), edgecolor='black') # Integer bins
        plt.title('Distribution of Word Counts in Rule Texts')
        plt.xlabel('Word Count')
        plt.ylabel('Number of Rules')
        plt.xticks(range(min(word_counts), max(word_counts)+1)) # Integer ticks
        plt.grid(axis='y', alpha=0.75) # Add a grid for better readability
        plt.tight_layout() # Adjust layout to prevent labels from overlapping
        plt.show()
    else:
        print("No data to plot for rules.")


def analyze_texts(data_dir):
    law_word_counts = []
    ruling_word_counts = []
    law_count = 0
    ruling_count = 0

    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                    words = text.split()
                    word_count = len(words)

                    if filename.endswith(".md"):
                        law_word_counts.append(word_count)
                        law_count += 1
                    else:
                        ruling_word_counts.append(word_count)
                        ruling_count += 1
            except UnicodeDecodeError:
                print(f"Skipping file {filename} due to decoding error.")
                continue # Skip file if there is an encoding error.
            except Exception as e:
                print(f"An error occurred while reading {filename}: {e}")
                continue

    print(f"Number of laws: {law_count}")
    print(f"Number of court rulings: {ruling_count}")

    def plot_and_print_stats(word_counts, title):
        if not word_counts: # Check if list is empty, avoid errors
            print(f"No data to plot for {title}.")
            return

        print(f"\nStats for {title}:")
        print(f"Min: {min(word_counts)}")
        print(f"Max: {max(word_counts)}")
        print(f"Avg: {np.mean(word_counts):.2f}")

        plt.figure(figsize=(10, 6))
        plt.hist(word_counts, bins=20, edgecolor='black') # Fixed bin count
        plt.title(f'Distribution of Word Counts in {title}')
        plt.xlabel('Word Count')
        plt.ylabel('Number of Documents')
        plt.grid(axis='y', alpha=0.75)
        plt.tight_layout()
        plt.show()

    plot_and_print_stats(law_word_counts, "Laws")
    plot_and_print_stats(ruling_word_counts, "Court Rulings")


def confusionMatrix():
    import matplotlib.pyplot as plt
    import numpy as np

    # Data for the confusion matrix
    labels = ['valid', 'unfair', 'void']
    confusion_matrix = np.array([
        [581, 88, 28],
        [40, 25, 17],
        [10, 12, 90]
    ])

    # Normalize the confusion matrix by rows (true labels)
    row_sums = confusion_matrix.sum(axis=1, keepdims=True)
    normalized_matrix = (confusion_matrix / row_sums) * 100

    # Plotting the normalized confusion matrix
    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.matshow(normalized_matrix, cmap='Blues')

    # Adding labels and ticks
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel('Predicted Labels', fontsize=12)
    ax.set_ylabel('True Labels', fontsize=12)

    # Annotating each cell with its percentage value
    for (i, j), val in np.ndenumerate(normalized_matrix):
        ax.text(j, i, f'{val:.1f}%', ha='center', va='center', color='black', fontsize=10)

    plt.tight_layout()
    plt.savefig('confusion_matrix.svg', format='svg', dpi=300)
    plt.show()


def clauseStats():
    from collections import Counter
    with open("../data/clauses.json", 'r', encoding='utf-8') as f:
        clauses = json.load(f)

    # Initialize a dictionary to store statistics
    stats = defaultdict(lambda: {"valid": 0, "unfair": 0, "void": 0, "sum": 0})

    # Calculate counts for each category
    for item in clauses:
        topic = item["topic"]
        label = item["true_label"]
        stats[topic][label] += 1
        stats[topic]["sum"] += 1

    # Prepare the final statistics
    final_stats = []
    overall = {"valid": 0, "unfair": 0, "void": 0, "sum": 0}

    for topic, values in stats.items():
        row = {
            "Category": topic,
            "Valid": values["valid"],
            "Unfair": values["unfair"],
            "Void": values["void"],
            "Sum": values["sum"],
            "Valid %": f"{(values['valid'] / values['sum'] * 100):.1f}%" if values["sum"] > 0 else "0%",
            "Unfair %": f"{(values['unfair'] / values['sum'] * 100):.1f}%" if values["sum"] > 0 else "0%",
            "Void %": f"{(values['void'] / values['sum'] * 100):.1f}%" if values["sum"] > 0 else "0%",
        }
        final_stats.append(row)
        for key in ["valid", "unfair", "void", "sum"]:
            overall[key] += values[key]

    # Add overall row
    overall_row = {
        "Category": "SUM",
        "Valid": overall["valid"],
        "Unfair": overall["unfair"],
        "Void": overall["void"],
        "Sum": overall["sum"],
        "Valid %": f"{(overall['valid'] / overall['sum'] * 100):.1f}%" if overall["sum"] > 0 else "0%",
        "Unfair %": f"{(overall['unfair'] / overall['sum'] * 100):.1f}%" if overall["sum"] > 0 else "0%",
        "Void %": f"{(overall['void'] / overall['sum'] * 100):.1f}%" if overall["sum"] > 0 else "0%",
    }
    final_stats.append(overall_row)

    # Output the statistics
    for row in final_stats:
        print(row)


if __name__ == "__main__":
    #analyze_rules("../data/rules.json")
    #analyze_texts("../data/sources/")
    #confusionMatrix()
    clauseStats()
