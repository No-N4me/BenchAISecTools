# Import Guard and Validator
from guardrails.hub import FinancialTone
from guardrails import Guard
from datasets import load_dataset



def categorize_sentiment(dataset):
    Label = []
    for idx, example in enumerate(dataset):
        print(idx)
        vader_score = example["Sentiment Vader Text"]
        if vader_score > 0.05:
            Label += ["positive"] 
            print('positive')
        elif vader_score < -0.05:
            Label += ["negative"] 
            print('negative')
        else:
            Label += ["negative"] 
            print('neutral')
    return Label
        #new_column = ["foo"] * len(ds)
#
ds = load_dataset("FrancophonIA/french_financial_news","default")['train']
Label = categorize_sentiment(ds)
ds = ds.add_column("Label", Label)

ds.save_to_disk("./labeled_finance_tone_dataset")
print("### END ###")
e = int(input())

            