from guardrails.hub import DetectJailbreak
from guardrails import Guard, ValidationOutcome

from datetime import datetime

from datasets import Dataset

from common.metrics import EvaluationMetrics


def evaluate_jailbreak(dataset: Dataset) -> EvaluationMetrics:
    """
    Evaluate Guardrails's Jailbreak detection capabilities against a ground truth dataset.
    
    Args:
        dataset: The dataset
        
    Returns:
        An EvaluationMetrics object with the evaluation results
    """
    # Initialize components
    metrics = EvaluationMetrics("guardrails_jailbreak")
    guard = Guard().use(
        DetectJailbreak
    )

    total_samples = len(dataset)
    # Process each example in the dataset
    for idx, example in enumerate(dataset):

        if idx % 100 == 0:
            print(f"Processing {idx}/{total_samples} samples ({int(idx/total_samples*100)}%)")
        
        source_text = example["prompt"]
        ground_truth_jailbreak = example["type"] == "jailbreak"

        guardrails_detected_jailbreak = False
        try:
            guard.validate(source_text)
        except Exception as e:
            # An exception indicates a potential jailbreak attempt
            guardrails_detected_jailbreak = True
        
        metrics.increment_evaluated_prompts()
        
        
        # Compare GuardrailsAI detection with ground truth
        if ground_truth_jailbreak and guardrails_detected_jailbreak:
            # True Positive: Text is a jailbreak and detected as a jailbreak
            metrics.increment_statistic("tp", details={
                "text": source_text
            })
        elif ground_truth_jailbreak and not guardrails_detected_jailbreak:
            # False Negative: Text is a jailbreak but not detected as a jailbreak
            metrics.increment_statistic("fn", details={
                "text": source_text
            })
        elif not ground_truth_jailbreak and guardrails_detected_jailbreak:
            # False Positive: Text is not a jailbreak but detected as a jailbreak
            metrics.increment_statistic("fp", details={
                "text": source_text
            })
        else:  # not ground_truth_jailbreak and not guardrails_detected_jailbreak
            # True Negative: Text is not a jailbreak and not detected as a jailbreak
            metrics.increment_statistic("tn", details={
                "text": source_text
            })
    
    # Set end time for evaluation duration calculation
    metrics.end_date = datetime.now()
    
    return metrics