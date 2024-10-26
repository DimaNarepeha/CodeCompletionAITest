import json
import statistics
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sacrebleu.metrics import CHRF
from sklearn.metrics import accuracy_score
from difflib import SequenceMatcher

with open('completed_code_dataset_fim.json', 'r') as f:
    data = json.load(f)

chrf_metric = CHRF()
scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

exact_matches = []
bleu_scores = []
chrf_scores = []
rouge_scores = []
similarity_scores = []
length_differences = []
incorrect_completions = []

def compute_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


for entry in data:
    middle = entry["middle"]
    model_completion = entry["model_completion"]

    #Exact Match
    exact_match = int(middle == model_completion)
    exact_matches.append(exact_match)

    #BLEU Score
    bleu_score = sentence_bleu(
        [middle.split()],
        model_completion.split(),
        smoothing_function=SmoothingFunction().method1
    )
    bleu_scores.append(bleu_score)

    #chrF Score
    chrf_score = chrf_metric.sentence_score(model_completion, [middle]).score
    chrf_scores.append(chrf_score)

    #ROUGE-L Score
    rouge_score = scorer.score(middle, model_completion)['rougeL'].fmeasure
    rouge_scores.append(rouge_score)

    #Similarity Score
    similarity_score = compute_similarity(middle, model_completion)
    similarity_scores.append(similarity_score)

    #Length Difference
    length_diff = abs(len(middle) - len(model_completion))
    length_differences.append(length_diff)

    #incorrect completions
    if similarity_score < 0.5:
        incorrect_completions.append(entry)


average_exact_match = sum(exact_matches) / len(exact_matches)
average_bleu = statistics.mean(bleu_scores)
average_chrf = statistics.mean(chrf_scores)
average_rouge = statistics.mean(rouge_scores)
average_similarity = statistics.mean(similarity_scores)
average_length_diff = statistics.mean(length_differences)
percent_incorrect = (len(incorrect_completions) / len(data)) * 100


print(f"Exact Match Rate: {average_exact_match:.2f}")
print(f"Average BLEU Score: {average_bleu:.4f}")
print(f"Average chrF Score: {average_chrf:.4f}")
print(f"Average ROUGE-L Score: {average_rouge:.4f}")
print(f"Average Similarity Score: {average_similarity:.4f}")
print(f"Average Length Difference: {average_length_diff:.2f} characters")
print(f"Percentage of Incorrect Completions: {percent_incorrect:.2f}%")

with open('incorrect_completions.json', 'w') as f:
    json.dump(incorrect_completions, f, indent=4)

print("Done")
