from guardrails.hub import ToxicLanguage
from guardrails import Guard, ValidationOutcome
from typing import Dict, List, Tuple, Any

import json
from datetime import datetime
import re

from datasets import Dataset

from common.metrics import EvaluationMetrics

def evaluate_toxicity(dataset: Dataset, threshold: float) -> EvaluationMetrics:
    """
    Evaluate Guardrails's Toxicity detection capabilities against a ground truth dataset.
    
    Args:
        dataset: Dataset containing the prompt and ground truth toxicity label
        threshold: Threshold for toxicity detection
        sample_size: Optional number of samples to evaluate (defaults to entire dataset)
        
    Returns:
        An EvaluationMetrics object with the evaluation results
    """
    # Initialize components
    metrics = EvaluationMetrics("guardrails_toxicity")
    guard = Guard().use(
        ToxicLanguage, threshold=0.5, validation_method="sentence", on_fail="exception"
    )

    total_samples = len(dataset)
    
    # Process each example in the dataset
    for idx, example in enumerate(dataset):
        if idx % 100 == 0:
            print(f"Processing {idx}/{total_samples} samples ({int(idx/total_samples*100)}%)")
        
        text = example["text"]
        ground_truth_toxic = example["toxicity"]  # Assuming this is a boolean or threshold value

        metrics.increment_evaluated_prompts()
        guardrails_detected_toxic = False
        try:
            guard.validate(text)
        except Exception as e:
            guardrails_detected_toxic = True
        
        if ground_truth_toxic and guardrails_detected_toxic:
            # True Positive: Text is toxic and detected as toxic
            metrics.increment_statistic("tp", details={
                "text": text
            })
        elif ground_truth_toxic and not guardrails_detected_toxic:
            # False Negative: Text is toxic but not detected as toxic
            metrics.increment_statistic("fn", details={
                "text": text
            })
        elif not ground_truth_toxic and guardrails_detected_toxic:
            # False Positive: Text is not toxic but detected as toxic
            metrics.increment_statistic("fp", details={
                "text": text
            })
        else:  # not ground_truth_toxic and not guardrails_detected_toxic
            # True Negative: Text is not toxic and not detected as toxic
            metrics.increment_statistic("tn", details={
                "text": text
            })
    
    # Set end time for evaluation duration calculation
    metrics.end_date = datetime.now()
    
    return metrics