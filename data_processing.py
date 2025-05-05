import os
import pandas as pd
import matplotlib.pyplot as plt

# Create output folder
os.makedirs('plots', exist_ok=True)

# Academic style settings
plt.style.use('seaborn-v0_8-colorblind')
plt.rcParams.update({
    'font.size': 12,
    # 'font.family': 'serif',
    'figure.dpi': 300,
    'axes.titlesize': 12,
    'axes.labelsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
})

# Load data
df = pd.read_csv('nt2_ai.csv')

# Preprocess correctness
df['is_correct'] = df['correct'] == 'correct'

# Overall accuracy
accuracy_overall = df['is_correct'].mean()
print(f"Overall accuracy: {accuracy_overall:.4%}")

# Accuracy breakdowns
acc_by_deel = df.groupby('deel')['is_correct'].mean().reset_index()
acc_by_taak = df.groupby('taak')['is_correct'].mean().reset_index()
acc_by_type = df.groupby('exercise_type')['is_correct'].mean().reset_index()
acc_by_options = df.groupby('options_num')['is_correct'].mean().reset_index()

# Top 10 topics
top_topics = df['topic'].value_counts().nlargest(10).index
def acc_by_topic():
    filtered = df[df['topic'].isin(top_topics)]
    return filtered.groupby('topic')['is_correct'].mean().reset_index()
acc_topic = acc_by_topic()

# Print detailed results
print("\nAccuracy by deel:")
print(acc_by_deel.to_string(index=False, formatters={'is_correct': '{:.4%}'.format}))

print("\nAccuracy by taak:")
print(acc_by_taak.to_string(index=False, formatters={'is_correct': '{:.4%}'.format}))

print("\nAccuracy by exercise type:")
print(acc_by_type.to_string(index=False, formatters={'is_correct': '{:.4%}'.format}))

print("\nAccuracy by number of options:")
print(acc_by_options.to_string(index=False, formatters={'is_correct': '{:.4%}'.format}))

print("\nAccuracy for top 10 topics:")
print(acc_topic.to_string(index=False, formatters={'is_correct': '{:.4%}'.format}))

# Plot helper for academic figures

def save_barplot(data, x, y, title, filename, rotate_x=False, horizontal=False):
    fig, ax = plt.subplots(figsize=(8, 6))
    if horizontal:
        ax.barh(data[x], data[y])
        ax.set_xlabel('Accuracy')
        ax.set_ylabel(x.capitalize())
    else:
        ax.bar(data[x], data[y])
        ax.set_xlabel(x.capitalize())
        ax.set_ylabel('Accuracy')
    ax.set_title(title)
    if rotate_x:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    fig.savefig(os.path.join('plots', f"{filename}.pdf"))
    plt.close(fig)

# Generate and save plots
tables = [
    (acc_by_deel, 'deel', 'is_correct', 'Accuracy by Deel', 'accuracy_by_deel', False, False),
    (acc_by_taak, 'taak', 'is_correct', 'Accuracy by Taak', 'accuracy_by_taak', True, False),
    (acc_by_type, 'exercise_type', 'is_correct', 'Accuracy by Exercise Type', 'accuracy_by_exercise_type', True, False),
    (acc_by_options, 'options_num', 'is_correct', 'Accuracy by Number of Options', 'accuracy_by_options', False, False),
    (acc_topic.sort_values('is_correct', ascending=False), 'topic', 'is_correct', 'Accuracy for Top 10 Topics', 'accuracy_by_top_topics', True, True),
]

for data, x, y, title, fname, rot, horiz in tables:
    save_barplot(data, x, y, title, fname, rotate_x=rot, horizontal=horiz)

print("\nPlots saved in 'plots/' directory as PDF files.")