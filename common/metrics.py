from datetime import datetime
from typing import Any, Dict, List
import matplotlib.pyplot as plt
import numpy as np
import json
import os

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
                
            # Calculate specificity (true negative rate)
            metrics['specificity'] = (self.statistics['tn'] / (self.statistics['tn'] + self.statistics['fp'])) \
                if (self.statistics['tn'] + self.statistics['fp']) > 0 else 0
        
        return metrics
    
    def plot_confusion_matrix(self):
        """
        Plot the confusion matrix as a heatmap.
        """
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Create the confusion matrix
        cm = np.array([
            [self.statistics['tp'], self.statistics['fn']],
            [self.statistics['fp'], self.statistics['tn']]
        ])
        
        # Create a heatmap
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        
        # Add colorbar
        plt.colorbar(im)
        
        # Add labels and title
        classes = ['Positive', 'Negative']
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)
        
        # Add text annotations in the cells
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], 'd'),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        
        # Add axis labels and title
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.title(f'Confusion Matrix for {self.label}')
        
        # Ensure layout is tight
        plt.tight_layout()
        
        return fig
    
    def plot_metrics_bar(self, metrics):
        """
        Plot the performance metrics as a bar chart.
        """
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extract metrics for plotting
        metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1_score', 'specificity']
        values = [metrics.get(metric, 0) for metric in metrics_to_plot]
        
        # Create a bar chart
        bars = ax.bar(metrics_to_plot, values, color='skyblue')
        
        # Add value annotations on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.4f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Set y-axis limit to 1.0 (or slightly higher for annotations)
        ax.set_ylim(0, 1.1)
        
        # Add labels and title
        plt.xlabel('Metrics')
        plt.ylabel('Value')
        plt.title(f'Performance Metrics for {self.label}')
        
        # Ensure layout is tight
        plt.tight_layout()
        
        return fig
    
    def plot_distribution_pie(self):
        """
        Plot the distribution of TP, FP, TN, FN as a pie chart.
        """
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Extract values for plotting
        labels = ['True Positives', 'False Positives', 'True Negatives', 'False Negatives']
        values = [self.statistics['tp'], self.statistics['fp'], self.statistics['tn'], self.statistics['fn']]
        
        # Create color map
        colors = ['#4CAF50', '#FF9800', '#2196F3', '#F44336']
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', 
                                         startangle=90, colors=colors)
        
        # Add a title
        ax.set_title(f'Distribution of Prediction Results for {self.label}')
        
        # Ensure layout is tight
        plt.tight_layout()
        
        return fig
    
    def display_results(self, save_path=None):
        """
        Display a formatted summary of evaluation metrics with visualizations.
        
        :param save_path: Optional path to save the visualizations
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
            print(f"Accuracy:    {metrics['accuracy']:.4f}")
            print(f"Precision:   {metrics['precision']:.4f}")
            print(f"Recall:      {metrics['recall']:.4f}")
            print(f"F1 Score:    {metrics['f1_score']:.4f}")
            print(f"Specificity: {metrics.get('specificity', 0):.4f}")
        
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
        
        # Create and display visualizations
        try:
            # Generate plots
            confusion_matrix_fig = self.plot_confusion_matrix()
            metrics_bar_fig = self.plot_metrics_bar(metrics)
            distribution_pie_fig = self.plot_distribution_pie()
            
            # Show plots
            plt.show()
            
            # Save visualizations if a path is provided
            if save_path:
                # Create directory if it doesn't exist
                os.makedirs(save_path, exist_ok=True)
                
                # Save plots
                confusion_matrix_fig.savefig(os.path.join(save_path, f"{self.label}_confusion_matrix.png"))
                metrics_bar_fig.savefig(os.path.join(save_path, f"{self.label}_metrics.png"))
                distribution_pie_fig.savefig(os.path.join(save_path, f"{self.label}_distribution.png"))
                
                print(f"\nVisualizations saved to {save_path}")
        
        except Exception as e:
            print(f"Error generating visualizations: {e}")
    
    def save_to_file(self, output_dir: str):
        """
        Save evaluation metrics and visualizations to files.
        
        :param output_dir: Path to the output directory
        """
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Base filename using the label
        base_filename = os.path.join(output_dir, f"{self.label.replace(' ', '_')}")
        
        # Calculate metrics
        metrics = self.calculate_metrics()
        
        # Create data structure for JSON export
        data = {
            "label": self.label,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "evaluated_prompts": self.evaluated_prompts,
            "statistics": self.statistics,
            "metrics": metrics,
            "errors": {
                # Convert complex objects to string representations if needed
                k: [str(e) if not isinstance(e, (dict, str, int, float, bool, type(None))) else e 
                    for e in v] for k, v in self.errors.items()
            }
        }
        
        # Save metrics as JSON
        with open(f"{base_filename}_metrics.json", 'w') as f:
            json.dump(data, f, indent=4)
        
        # Save human-readable report
        with open(f"{base_filename}_report.txt", 'w') as f:
            f.write(f"Evaluation Metrics for {self.label}\n")
            f.write("=" * 40 + "\n\n")
            
            f.write("Confusion Matrix Statistics:\n")
            for stat, value in self.statistics.items():
                f.write(f"{stat.upper()}: {value}\n")
            
            f.write("\nPerformance Metrics:\n")
            if metrics:
                f.write(f"Accuracy:    {metrics['accuracy']:.4f}\n")
                f.write(f"Precision:   {metrics['precision']:.4f}\n")
                f.write(f"Recall:      {metrics['recall']:.4f}\n")
                f.write(f"F1 Score:    {metrics['f1_score']:.4f}\n")
                f.write(f"Specificity: {metrics.get('specificity', 0):.4f}\n")
            
            f.write("\nError Details:\n")
            for error_type, error_list in self.errors.items():
                f.write(f"{error_type.upper()} Errors ({len(error_list)} entries):\n")
                for error in error_list:
                    f.write(f"  - {error}\n")
            
            if self.end_date:
                eval_duration = self.end_date - self.start_date
                f.write(f"\nEvaluated prompts: {self.evaluated_prompts}\n")
                f.write(f"Evaluation Duration: {eval_duration}\n")
                f.write(f"Mean processing time: {eval_duration/self.evaluated_prompts if self.evaluated_prompts else 0}\n")
        
        # Save visualizations
        try:
            # Generate and save confusion matrix
            confusion_fig = self.plot_confusion_matrix()
            confusion_fig.savefig(f"{base_filename}_confusion_matrix.png", dpi=300, bbox_inches='tight')
            plt.close(confusion_fig)
            
            # Generate and save metrics bar chart
            metrics_fig = self.plot_metrics_bar(metrics)
            metrics_fig.savefig(f"{base_filename}_metrics_bar.png", dpi=300, bbox_inches='tight')
            plt.close(metrics_fig)
            
            # Generate and save distribution pie chart
            pie_fig = self.plot_distribution_pie()
            pie_fig.savefig(f"{base_filename}_distribution_pie.png", dpi=300, bbox_inches='tight')
            plt.close(pie_fig)
            
        except Exception as e:
            print(f"Error saving visualizations: {e}")
        
        print(f"All metrics and visualizations saved to {output_dir}")