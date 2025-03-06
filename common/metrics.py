from datetime import datetime
from typing import Any, Dict, List

class EvaluationMetrics:
    def __init__(self, label: str, start_date: datetime = None, end_date: datetime = None):
        """
        Initialize the EvaluationMetrics class.
        
        :param label: Label for the classification model
        :param start_date: Optional start date of evaluation
        :param end_date: Optional end date of evaluation
        """
        self.label = label
        self.start_date = start_date or datetime.now()
        self.end_date = end_date
        self.evaluated_prompts = 0
        
        # Initialize statistics dictionary with default values
        self.statistics: Dict[str, int] = {
            "tp": 0,  # True Positives
            "fp": 0,  # False Positives
            "tn": 0,  # True Negatives
            "fn": 0   # False Negatives
        }
        
        # Initialize errors dictionary
        self.errors: Dict[str, List[Any]] = {
            "tp": [],
            "fp": [],
            "tn": [],
            "fn": []
        }
    
    def increment_statistic(self, stat_type: str, value: int = 1, details: Any = None):
        """
        Increment a specific statistic and optionally add error details.
        
        :param stat_type: Type of statistic to increment (tp, fp, tn, fn)
        :param value: Amount to increment (default 1)
        :param error_details: Optional details
        """
        if stat_type not in self.statistics:
            raise ValueError(f"Invalid statistic type: {stat_type}")
        
        self.statistics[stat_type] += value
        
        # Add error details if provided
        if details is not None:
            self.errors[stat_type].append(details)

    def increment_evaluated_prompts(self):
        self.evaluated_prompts += 1
    
    def calculate_metrics(self):
        """
        Calculate performance metrics.
        
        :return: Dictionary of calculated metrics
        """
        total_samples = sum(self.statistics.values())
        metrics = {}
        
        if total_samples > 0:
            # Accuracy
            metrics['accuracy'] = (self.statistics['tp'] + self.statistics['tn']) / total_samples
            
            # Precision (handling division by zero)
            metrics['precision'] = (self.statistics['tp'] / (self.statistics['tp'] + self.statistics['fp'])) \
                if (self.statistics['tp'] + self.statistics['fp']) > 0 else 0
            
            # Recall (handling division by zero)
            metrics['recall'] = (self.statistics['tp'] / (self.statistics['tp'] + self.statistics['fn'])) \
                if (self.statistics['tp'] + self.statistics['fn']) > 0 else 0
            
            # F1 Score (harmonic mean of precision and recall)
            # Use 0 if precision and recall are both 0 to avoid division by zero
            if metrics['precision'] + metrics['recall'] > 0:
                metrics['f1_score'] = 2 * (metrics['precision'] * metrics['recall']) / \
                    (metrics['precision'] + metrics['recall'])
            else:
                metrics['f1_score'] = 0
        
        return metrics
    
    def display_results(self):
        """
        Display a formatted summary of evaluation metrics.
        """
        print(f"Evaluation Metrics for {self.label}")
        print("=" * 40)
        
        # Print basic statistics
        print("\nConfusion Matrix Statistics:")
        for stat, value in self.statistics.items():
            print(f"{stat.upper()}: {value}")
        
        # Calculate and print performance metrics
        metrics = self.calculate_metrics()
        
        print("\nPerformance Metrics:")
        if metrics:
            print(f"Accuracy:   {metrics['accuracy']:.4f}")
            print(f"Precision: {metrics['precision']:.4f}")
            print(f"Recall:    {metrics['recall']:.4f}")
            print(f"F1 Score:  {metrics['f1_score']:.4f}")
        
        # Print error details if available
        print("\nError Details:")
        for error_type, error_list in self.errors.items():
            print(f"{error_type.upper()} Details ({len(error_list)} entries):")
            for idx, error in enumerate(error_list[:5]):  # Display up to 5 error details
                print(f"\n[====<{idx}>====] ")
                for key, value in error.items():
                    print(f" [{key}] - {value}")
            if len(error_list) > 5:
                print(f"  ... and {len(error_list) - 5} more\n\n")
        
        # Print evaluation time
        if self.end_date:
            eval_duration = self.end_date - self.start_date
            print(f"\nEvaluated prompts: {self.evaluated_prompts}")
            print(f"\nEvaluation Duration: {eval_duration}")
            print(f"\nMean processing time: {eval_duration/self.evaluated_prompts}")
    
    def save_to_file(self, filename: str):
        """
        Save evaluation metrics to a file.
        
        :param filename: Path to the output file
        """
        metrics = self.calculate_metrics()
        
        with open(filename, 'w') as f:
            f.write(f"Evaluation Metrics for {self.label}\n")
            f.write("=" * 40 + "\n\n")
            
            f.write("Confusion Matrix Statistics:\n")
            for stat, value in self.statistics.items():
                f.write(f"{stat.upper()}: {value}\n")
            
            f.write("\nPerformance Metrics:\n")
            if metrics:
                f.write(f"Accuracy:   {metrics['accuracy']:.4f}\n")
                f.write(f"Precision: {metrics['precision']:.4f}\n")
                f.write(f"Recall:    {metrics['recall']:.4f}\n")
                f.write(f"F1 Score:  {metrics['f1_score']:.4f}\n")
            
            f.write("\nError Details:\n")
            for error_type, error_list in self.errors.items():
                f.write(f"{error_type.upper()} Errors ({len(error_list)} entries):\n")
                for error in error_list:
                    f.write(f"  - {error}\n")
            
            if self.end_date:
                eval_duration = self.end_date - self.start_date
                f.write(f"\nEvaluated prompts: {self.evaluated_prompts}")
                f.write(f"\nEvaluation Duration: {eval_duration}")
                f.write(f"\nMean processing time: {eval_duration/self.evaluated_prompts}")