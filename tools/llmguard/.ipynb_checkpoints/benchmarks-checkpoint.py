from common.metrics import EvaluationMetrics
from utils.datasets import load_dataset, get_ai4privacy_to_presidio_mapping

from .input_scanners.pii import evaluate_pii_detection

def bench_pii(dataset: str, split: str, max_split_size: int, preferred_language: str, entities: list[str]) -> EvaluationMetrics:
    print(f"Preparing dataset for PII Evaluation...")
    dataset = load_dataset(dataset, split)
    if preferred_language != "":
        dataset = dataset.filter(lambda example: example["language"] == preferred_language)
    
    dataset = dataset.select(range(min(len(dataset), max_split_size)))
    print(f"Running LLMGuard PII Evaluation...")
    
    metrics: EvaluationMetrics = evaluate_pii_detection(dataset, entities)
    print(f"Finished LLMGuard PII Evaluation!")
    return metrics


def bench_toxicity(dataset: str, split: str, max_split_size: int) -> EvaluationMetrics:
    print(f"Preparing dataset for PII Evaluation...")
    dataset = load_dataset(dataset, split)
    print(f"Running LLMGuard PII Evaluation...")
    
    metrics: EvaluationMetrics = evaluate_pii_detection(dataset, entities)
    print(f"Finished LLMGuard PII Evaluation!")
    return metrics