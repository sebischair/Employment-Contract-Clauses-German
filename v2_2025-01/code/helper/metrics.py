from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import numpy as np


def getMetrics(truth, pred):
    # Check that inputs are valid
    if len(truth) != len(pred):
        raise ValueError("The length of truth and pred must be the same.")

    # Define the complete set of labels
    all_labels = ["valid", "unfair", "void"]

    # Start building the output string
    output = []

    # Calculate and append accuracy
    accuracy = accuracy_score(truth, pred)
    output.append(f"Accuracy: {accuracy:.4f}")

    # Append detailed classification report (precision, recall, F1, support)
    output.append("\nClassification Report:")
    output.append(
        classification_report(
            truth,
            pred,
            labels=all_labels,
            target_names=all_labels,
            zero_division=0  # Avoid errors for missing classes
        )
    )

    # Generate confusion matrix
    cm = confusion_matrix(truth, pred, labels=all_labels)

    # Append confusion matrix in a formatted way
    output.append("\nConfusion Matrix (Formatted):")
    output.append(f"{'':<10}{'valid':<10}{'unfair':<10}{'void':<10}")
    for label, row in zip(all_labels, cm):
        output.append(f"{label:<10}{row[0]:<10}{row[1]:<10}{row[2]:<10}")

    # Combine all output into a single string
    output_text = "\n".join(output)

    # Print the output for immediate visibility
    print(output_text)

    # Return the output string for logging
    return output_text
