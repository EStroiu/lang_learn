import json
import time
import numpy as np
from sentence_transformers import SentenceTransformer, util
import ollama
from nltk.translate.bleu_score import corpus_bleu
from collections import defaultdict
import language_tool_python
from bert_score import score as bert_score
from nltk import word_tokenize
import nltk

nltk.download('punkt_tab')

# Configuration: model and test files
MODEL = 'bramvanroy/fietje-2b-chat:f16'
EMBED_MODEL = 'paraphrase-multilingual-MiniLM-L12-v2'
PARAPHRASE_THRESHOLD = 0.9

# Load embedding model once
tap = SentenceTransformer(EMBED_MODEL)
# Initialize grammar checker
lang_tool = language_tool_python.LanguageTool('nl')

# 1. Accuracy: BLEU on translation/paraphrase tasks
def eval_accuracy(test_pairs):
    references, hypotheses = [], []
    for item in test_pairs:
        src, ref = item['source'], item['reference']
        resp = ollama.chat(model=MODEL, messages=[{'role':'user','content':src}])
        hyp_tokens = resp['message']['content'].split()
        hypotheses.append(hyp_tokens)
        references.append([ref.split()])
    return corpus_bleu(references, hypotheses) * 100

# 2. Consistency: paraphrase-based stability
def eval_consistency(questions):
    paraphrase_templates = [lambda q: q,
                             lambda q: f"Kun je uitleggen: {q}",
                             lambda q: f"Hoe zou je dit zeggen in het Nederlands: {q}"]
    scores = []
    for q in questions:
        pars = [t(q) for t in paraphrase_templates]
        emb_answers = []
        for p in pars:
            ans = ollama.chat(model=MODEL, messages=[{'role':'user','content':p}])['message']['content']
            emb_answers.append(ans)
        embs = tap.encode(emb_answers, convert_to_tensor=True)
        sims = util.cos_sim(embs, embs).cpu().numpy()
        n = len(emb_answers)
        hits = np.sum((sims > PARAPHRASE_THRESHOLD)) - n
        scores.append(hits/(n*(n-1)) if n > 1 else 1.0)
    return float(np.mean(scores))

# 3. Fairness: subgroup accuracy disparity
def eval_fairness(test_flemish, test_netherlandic):
    def acc(items):
        return np.mean([
            ollama.chat(model=MODEL, messages=[{'role':'user','content':x['source']}])['message']['content'] == x['reference']
            for x in items
        ])
    a_f, a_n = acc(test_flemish), acc(test_netherlandic)
    return abs(a_f - a_n), a_f, a_n

# 4. Calibration: placeholder
def eval_calibration(responses, confidences):
    return None

# 5. BERTScore: semantic similarity metric
def eval_bertscore(test_pairs):
    refs = [x['reference'] for x in test_pairs]
    hyps = []
    for x in test_pairs:
        resp = ollama.chat(model=MODEL, messages=[{'role':'user','content':x['source']}])['message']['content']
        hyps.append(resp)
    P, R, F1 = bert_score(hyps, refs, lang='nl', rescale_with_baseline=True)
    return float(F1.mean() * 100)

# 6. Lexical Diversity: Type-Token Ratio (TTR)
def eval_lexical_diversity(questions):
    ttr_scores = []
    for q in questions:
        resp = ollama.chat(model=MODEL, messages=[{'role':'user','content':q}])['message']['content']
        tokens = word_tokenize(resp.lower())
        if tokens:
            ttr_scores.append(len(set(tokens)) / len(tokens))
    return float(np.mean(ttr_scores) * 100)

# 7. Grammar Errors: number of issues per response
def eval_grammar_errors(questions):
    error_counts = []
    for q in questions:
        resp = ollama.chat(model=MODEL, messages=[{'role':'user','content':q}])['message']['content']
        matches = lang_tool.check(resp)
        error_counts.append(len(matches))
    return float(np.mean(error_counts))

if __name__ == '__main__':
    # Load test sets
    translation_set = json.load(open('data/translation_eval.json', encoding='utf-8'))
    grammar_set = json.load(open('data/grammar_eval.json', encoding='utf-8'))
    flemish_set = json.load(open('data/flemish_eval.json', encoding='utf-8'))
    nether_set = json.load(open('data/netherlandic_eval.json', encoding='utf-8'))

    results = {}
    start = time.time()
    results['bleu_translation'] = eval_accuracy(translation_set)
    results['bleu_grammar'] = eval_accuracy(grammar_set)
    results['consistency'] = eval_consistency([i['source'] for i in translation_set[:50]])
    fairness_delta, a_f, a_n = eval_fairness(flemish_set, nether_set)
    results['fairness_delta'] = fairness_delta
    results['acc_flemish'] = a_f
    results['acc_netherlandic'] = a_n
    results['bertscore_translation'] = eval_bertscore(translation_set)
    results['lexical_diversity'] = eval_lexical_diversity([i['source'] for i in translation_set[:50]])
    results['grammar_errors_avg'] = eval_grammar_errors([i['source'] for i in grammar_set[:50]])
    results['total_time_s'] = time.time() - start

    print(json.dumps(results, indent=2, ensure_ascii=False))
