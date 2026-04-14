import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, precision_score

# ==========================================
# 1. KONFIGURATION & PFADE
# ==========================================
BASE_PATH = "logs/"

# Zuordnung der Dateipfade zu den Modellen und Settings
gpt_files = {
    "None": os.path.join(BASE_PATH, "gpt-4.1-2025-04-14/rules_2025-11-26.json"),
    "Minimal": os.path.join(BASE_PATH, "gpt-5-2025-08-07-minimal-reasoning/rules_2025-11-26.json"),
    "Medium": os.path.join(BASE_PATH, "gpt-5-2025-08-07-medium-reasoning/rules_2025-11-26.json"),
    "High": os.path.join(BASE_PATH, "gpt-5-2025-08-07-high-reasoning/rules_2025-11-26.json")
}

gemini_files = {
    "None": os.path.join(BASE_PATH, "gemini-2.5-flash-preview-09-2025/rules_2025-11-26.json"),
    "Minimal": os.path.join(BASE_PATH, "gemini-2.5-pro-minimal-reasoning/rules_2025-11-26.json"),
    "Medium": os.path.join(BASE_PATH, "gemini-2.5-pro-medium-reasoning/rules_2025-11-26.json"),
    "High": os.path.join(BASE_PATH, "gemini-2.5-pro-high-reasoning/rules_2025-11-26.json")
}

ALL_LABELS = ["valid", "unfair", "void"]
N_BOOTSTRAP = 10000


# ==========================================
# 2. HILFSFUNKTIONEN FÜR METRIKEN
# ==========================================
def get_macro_f1(y_true, y_pred):
    return f1_score(y_true, y_pred, labels=ALL_LABELS, average='macro', zero_division=0)


def get_void_precision(y_true, y_pred):
    # Binarisieren für Void-Klasse (1 wenn 'void', sonst 0)
    yt = [1 if y == 'void' else 0 for y in y_true]
    yp = [1 if y == 'void' else 0 for y in y_pred]
    return precision_score(yt, yp, zero_division=0)


def load_predictions(filepath):
    """Lädt true_label und pred_label aus einer JSON Log-Datei."""
    if not os.path.exists(filepath):
        print(f"WARNUNG: Datei nicht gefunden: {filepath}")
        return [], []
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    y_true = [entry.get("true_label") for entry in data]
    y_pred = [entry.get("pred_label") for entry in data]
    return y_true, y_pred


def compute_bootstrap(y_true, y_pred, n_iterations=N_BOOTSTRAP):
    """Berechnet Punktschätzer und 95% CI per Bootstrap Resampling."""
    if not y_true or not y_pred:
        return 0, (0, 0), 0, (0, 0)

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    n_size = len(y_true)

    f1_scores = np.empty(n_iterations)
    prec_scores = np.empty(n_iterations)

    # Bootstrap Loop
    for i in range(n_iterations):
        # Ziehen MIT Zurücklegen
        indices = np.random.choice(n_size, size=n_size, replace=True)
        y_true_sample = y_true[indices]
        y_pred_sample = y_pred[indices]

        f1_scores[i] = get_macro_f1(y_true_sample, y_pred_sample)
        prec_scores[i] = get_void_precision(y_true_sample, y_pred_sample)

    # Punkt-Schätzer berechnen (auf dem Original-Datensatz)
    base_f1 = get_macro_f1(y_true, y_pred)
    base_prec = get_void_precision(y_true, y_pred)

    # 95% Konfidenzintervalle (2.5% und 97.5% Quantile)
    f1_ci = (np.percentile(f1_scores, 2.5), np.percentile(f1_scores, 97.5))
    prec_ci = (np.percentile(prec_scores, 2.5), np.percentile(prec_scores, 97.5))

    return base_f1, f1_ci, base_prec, prec_ci


# ==========================================
# 3. DATEN VERARBEITEN & BOOTSTRAPPING
# ==========================================
print(f"Starte Bootstrap Resampling mit {N_BOOTSTRAP} Iterationen...\n")

settings = ["None", "Minimal", "Medium", "High"]
results = {"GPT": {}, "Gemini": {}}

for family_name, file_dict in [("GPT", gpt_files), ("Gemini", gemini_files)]:
    print(f"--- {family_name} Family ---")
    for setting in settings:
        filepath = file_dict[setting]
        y_true, y_pred = load_predictions(filepath)

        base_f1, f1_ci, base_prec, prec_ci = compute_bootstrap(y_true, y_pred)

        results[family_name][setting] = {
            "f1": base_f1, "f1_ci": f1_ci,
            "prec": base_prec, "prec_ci": prec_ci
        }

        print(f"{setting:<10} | F1: {base_f1:.3f} (95% CI: {f1_ci[0]:.3f} - {f1_ci[1]:.3f}) "
              f"| Void Prec: {base_prec:.3f} (95% CI: {prec_ci[0]:.3f} - {prec_ci[1]:.3f})")
    print()

# ==========================================
# 4. PLOTTING (mit Offset für Fehlerbalken)
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

x_pos = np.arange(len(settings))
colors = {"GPT": "#0047AB", "Gemini": "#D48100"}

# Wir definieren einen minimalen Offset (Verschiebung auf der X-Achse)
offset_width = 0.08

for family_name in ["GPT", "Gemini"]:
    color = colors[family_name]

    # Verschiebung: GPT leicht nach links (-), Gemini leicht nach rechts (+)
    current_offset = -offset_width if family_name == "GPT" else offset_width
    x_current = x_pos + current_offset

    # F1 Daten extrahieren
    f1_means = [results[family_name][s]["f1"] for s in settings]
    f1_ci_lower = [results[family_name][s]["f1_ci"][0] for s in settings]
    f1_ci_upper = [results[family_name][s]["f1_ci"][1] for s in settings]

    # Fehler berechnen
    f1_err = [[m - l for m, l in zip(f1_means, f1_ci_lower)],
              [u - m for m, u in zip(f1_means, f1_ci_upper)]]

    # Precision Daten extrahieren
    prec_means = [results[family_name][s]["prec"] for s in settings]
    prec_ci_lower = [results[family_name][s]["prec_ci"][0] for s in settings]
    prec_ci_upper = [results[family_name][s]["prec_ci"][1] for s in settings]

    prec_err = [[m - l for m, l in zip(prec_means, prec_ci_lower)],
                [u - m for m, u in zip(prec_means, prec_ci_upper)]]

    # Plot ax1 (mit den verschobenen X-Koordinaten 'x_current')
    ax1.errorbar(x_current, f1_means, yerr=f1_err, fmt='-o', color=color,
                 capsize=4, elinewidth=1.5, markersize=6, label=f"{family_name} Family")

    # Plot ax2 (mit den verschobenen X-Koordinaten 'x_current')
    ax2.errorbar(x_current, prec_means, yerr=prec_err, fmt='-o', color=color,
                 capsize=4, elinewidth=1.5, markersize=6, label=f"{family_name} Family")

# Styling für beide Achsen
for ax in (ax1, ax2):
    # Die Ticks (Beschriftungen) bleiben in der exakten Mitte
    ax.set_xticks(x_pos)
    ax.set_xticklabels(settings, fontsize=11)
    ax.set_xlabel("Reasoning Effort", fontsize=12)
    ax.tick_params(axis='y', labelsize=11)
    ax.grid(True, linestyle='--', alpha=0.6)

ax1.set_ylabel("Macro Avg F1", fontsize=12)
ax2.set_ylabel("Precision (Void Class)", fontsize=12)
ax2.legend(fontsize=11)

plt.tight_layout()
plt.savefig("figure_1_bootstrapped_offset.png", bbox_inches='tight')
print("Grafik erfolgreich generiert und als 'figure_1_bootstrapped_offset.png' gespeichert.")
plt.show()