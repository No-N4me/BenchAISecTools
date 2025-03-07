from llm_guard.input_scanners import Toxicity
from llm_guard.input_scanners.base import Scanner
from llm_guard.input_scanners.toxicity import MatchType
from llm_guard.util import configure_logger

from datasets import Dataset
from datetime import datetime
import json
from typing import Dict, List, Any

from common.metrics import EvaluationMetrics

configure_logger(log_level="ERROR", render_json=True)

def evaluate_toxicity(dataset: Dataset, threshold: float) -> EvaluationMetrics:
    """
    Evaluate LLMGuard's Toxicity detection capabilities against a ground truth dataset.
    
    Args:
        dataset: Dataset containing the prompt and ground truth toxicity label
        threshold: Threshold for toxicity detection
        sample_size: Optional number of samples to evaluate (defaults to entire dataset)
        
    Returns:
        An EvaluationMetrics object with the evaluation results
    """
    # Initialize components
    metrics = EvaluationMetrics("llmguard_toxicity")
    scanner = Toxicity(threshold=threshold, match_type=MatchType.SENTENCE)

    total_samples = len(dataset)
    
    # Process each example in the dataset
    for idx, example in enumerate(dataset):
        if idx % 100 == 0:
            print(f"Processing {idx}/{total_samples} samples ({int(idx/total_samples*100)}%)")
        
        text = example["text"]
        ground_truth_toxic = example["toxicity"]  # Assuming this is a boolean or threshold value
        
        # Process example with LLM Guard scanner
        sanitized_text, is_valid, risk_score = scanner.scan(text)
        metrics.increment_evaluated_prompts()
        
        # Determine if LLM Guard detected toxicity (not valid or sanitized)
        llm_guard_detected_toxic = not is_valid or sanitized_text != text
        
        # Compare LLM Guard detection with ground truth
        if ground_truth_toxic and llm_guard_detected_toxic:
            # True Positive: Text is toxic and detected as toxic
            metrics.increment_statistic("tp", details={
                "text": text,
                "risk_score": risk_score,
                "sanitized": sanitized_text
            })
        elif ground_truth_toxic and not llm_guard_detected_toxic:
            # False Negative: Text is toxic but not detected as toxic
            metrics.increment_statistic("fn", details={
                "text": text,
                "risk_score": risk_score,
                "sanitized": sanitized_text
            })
        elif not ground_truth_toxic and llm_guard_detected_toxic:
            # False Positive: Text is not toxic but detected as toxic
            metrics.increment_statistic("fp", details={
                "text": text,
                "risk_score": risk_score,
                "sanitized": sanitized_text
            })
        else:  # not ground_truth_toxic and not llm_guard_detected_toxic
            # True Negative: Text is not toxic and not detected as toxic
            metrics.increment_statistic("tn", details={
                "text": text,
                "risk_score": risk_score
            })
    
    # Set end time for evaluation duration calculation
    metrics.end_date = datetime.now()
    
    return metrics