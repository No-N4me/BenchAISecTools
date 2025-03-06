from llm_guard.vault import Vault
from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.base import Scanner
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
from llm_guard.util import configure_logger

import json
from typing import Dict, List, Any
from datetime import datetime
import re

from datasets import Dataset

from common.metrics import EvaluationMetrics
from utils.datasets import get_ai4privacy_to_presidio_mapping

configure_logger(log_level="ERROR", render_json=True)

def evaluate_pii_detection(dataset: Dataset, entities: list[str], sample_size: int = None) -> EvaluationMetrics:
    """
    Evaluate LLMGuard's PII detection capabilities against a ground truth dataset.
    
    Args:
        dataset: The ai4privacy/pii-masking-200k dataset
        entities: List of Presidio entity types to evaluate
        
    Returns:
        An EvaluationMetrics object with the evaluation results
    """
    # Initialize components
    vault = Vault()
    metrics = EvaluationMetrics("llmguard_pii")
    scanner = Anonymize(
        vault, 
        recognizer_conf=BERT_LARGE_NER_CONF, 
        language="en", 
        entity_types=entities
    )
    
    # Get mapping from ai4privacy to Presidio entity types
    entity_mapping = get_ai4privacy_to_presidio_mapping(entities)
    ai4privacy_entities = list(entity_mapping.keys())
    
    # Limit the number of examples to process if sample_size is specified
    dataset_to_process = dataset
    if sample_size is not None and sample_size < len(dataset):
        dataset_to_process = dataset.select(range(sample_size))

    total_samples = len(dataset_to_process)
    # Process each example in the dataset
    for idx, example in enumerate(dataset_to_process):

        if idx % 100 == 0:
            print(f"Processing {idx}/{total_samples} samples ({int(idx/total_samples*100)}%)")
        
        source_text = example["source_text"]
        
        # Parse ground truth privacy masks
        try:
            privacy_masks = json.loads(example["privacy_mask"]) if isinstance(example["privacy_mask"], str) else example["privacy_mask"]
        except (json.JSONDecodeError, TypeError):
            # Skip examples with invalid privacy_mask format
            continue
        
        # Filter for entity types we're evaluating
        relevant_masks = [
            mask for mask in privacy_masks 
            if mask["label"] in ai4privacy_entities
        ]
        
        # If no relevant entities in this example, count as True Negative if nothing detected
        if not relevant_masks:
            sanitized_text, is_valid, risk_score = scanner.scan(source_text)
            metrics.increment_evaluated_prompts()
            # True Negative: No PII expected, none detected
            if sanitized_text == source_text:
                metrics.increment_statistic("tn")
            # False Positive: No PII expected, but something detected
            else:
                metrics.increment_statistic("fp", details={
                    "text": source_text,
                    "sanitized": sanitized_text,
                    "privacy_mask": privacy_masks,
                    "expected": "No PII"
                })
            continue
        
        # Process example with expected PII
        sanitized_text, is_valid, risk_score = scanner.scan(source_text)
        metrics.increment_evaluated_prompts()
        
        # Check if all expected PII was found
        all_pii_detected = sanitized_text != source_text
        
        # For detailed analysis, extract the redacted entities from sanitized text
        redacted_entities = []
        if all_pii_detected:
            # Extract [REDACTED_ENTITY_TYPE_N] patterns from sanitized text
            redaction_pattern = re.compile(r"\[REDACTED_([A-Z_]+)_\d+\]")
            redacted_entities = redaction_pattern.findall(sanitized_text)
        
        # Evaluate each expected PII entity
        for mask in relevant_masks:
            pii_value = mask["value"]
            pii_type = mask["label"]
            presidio_type = entity_mapping.get(pii_type)
            
            # Skip if we don't have a mapping for this entity type
            if not presidio_type:
                continue
            
            # Check if this specific PII value was detected
            pii_detected = False
            for entity_type in redacted_entities:
                # FIX: Compare the full entity type (not split) against LLMGuard output
                if entity_type == presidio_type:
                    pii_detected = True
                    break
            
            if pii_detected:
                # True Positive: Expected PII and detected
                metrics.increment_statistic("tp", details={
                    "entity_type": pii_type,
                    "value": pii_value
                })
            else:
                # False Negative: Expected PII but not detected
                metrics.increment_statistic("fn", details={
                    "entity_type": pii_type,
                    "privacy_mask": privacy_masks,
                    "value": pii_value,
                    "text": source_text,
                    "sanitized": sanitized_text
                })
        
        # Create a set to track which entity types have been accounted for
        accounted_entity_types = set()
        
        # Add all entity types that we've already processed in the true positives check
        for mask in relevant_masks:
            pii_type = mask["label"]
            if pii_type in ai4privacy_entities:
                presidio_type = entity_mapping.get(pii_type)
                if presidio_type:
                    # Add the full Presidio type to accounted types
                    accounted_entity_types.add(presidio_type)
        
        # Check for entities in the redacted output that weren't accounted for
        for detected_type in redacted_entities:
            if detected_type not in accounted_entity_types:
                # Only count as false positive if we're evaluating this entity type
                # This prevents counting entities we're not testing for
                is_evaluated_entity = detected_type in entities
                
                if is_evaluated_entity:
                    metrics.increment_statistic("fp", details={
                        "entity_type": detected_type,
                        "text": source_text,
                        "privacy_mask": privacy_masks,
                        "sanitized": sanitized_text
                    })
    
    # Set end time for evaluation duration calculation
    metrics.end_date = datetime.now()
    
    return metrics