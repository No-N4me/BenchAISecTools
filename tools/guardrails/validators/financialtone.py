from guardrails.hub import FinancialTone
from guardrails import Guard, ValidationOutcome
import io
import sys
from datetime import datetime

from datasets import Dataset

from common.metrics import EvaluationMetrics

def evaluate_financial_tone(dataset: Dataset) -> EvaluationMetrics:
    """
    Evaluate Guardrails's Financial Tone detection capabilities against a french news dataset.
    
    Args:
        dataset: The dataset
        
    Returns:
        An EvaluationMetrics object with the evaluation results
    """
    # Initialize components
    metrics = EvaluationMetrics("guardrails_financial_tone")
    guard = Guard().use(
        FinancialTone, on_fail="exception"
    )
    print("Metrics start",metrics)
    total_samples = len(dataset)
    # Process each example in the dataset
    for idx, example in enumerate(dataset):
        if idx % 100 == 0:
            print(f"Processing {idx}/{total_samples} samples ({int(idx/total_samples*100)}%)")
        source_text = example["Contenu"]
        
        ground_truth = example["Label"]
        

        #guardrails_detected_emotion = False
        try:
            # Validate the text using Guardrails
            
            
            # Extract predicted label and confidence (if available)
            print("Metrics BEFORE: ",metrics)
            print("Contenu: ",source_text)
            print("Truth: ",ground_truth)

            # since guard.validate only puts the prediction in a print statement, we are forcing stdout
            # Redirect stdout to capture print output
            # captured_output = io.StringIO()
            # sys.stdout = captured_output
            
            # # Call the validator (output)
            prediction = guard.validate(source_text, metadata={"financial_tone": ground_truth})
            
            # # Reset stdout to its original state
            # sys.stdout = sys.__stdout__
            
            # # Get the printed output
            # prediction = captured_output.getvalue().strip().split()[2]
            
            print(prediction)
            print("Predicted label:", prediction)
            ### problème d'extraction de la prediction
            metrics.increment_evaluated_prompts()
            
            # Compare GuardrailsAI detection with ground truth
            if ground_truth == prediction:
                # True Positive: Text matches the ground truth and is correctly detected
                metrics.increment_statistic("tp", details={
                "text": source_text
                })
                print("Metrics changed: ",metrics)
            elif ground_truth != prediction and ground_truth == "positive":
                # False Negative: Text is positive but not detected as positive
                metrics.increment_statistic("fn", details={
                "text": source_text
                })
                print("Metrics changed: ",metrics)
            elif ground_truth != prediction and ground_truth == "negative":
                # False Positive: Text is negative but detected as positive
                metrics.increment_statistic("fp", details={
                "text": source_text
                })
                print("Metrics changed: ",metrics)
            else:
                # True Negative: Text matches the ground truth and is correctly not detected as positive
                metrics.increment_statistic("tn", details={
                "text": source_text
                })
            print("Metrics : ",metrics)


        except Exception as e:
            # Handle exceptions 
            print("Error",e)

        
        #a=input(">")
        
        print(metrics)


    # Set end time for evaluation duration calculation
    metrics.end_date = datetime.now()
    
    return metrics
