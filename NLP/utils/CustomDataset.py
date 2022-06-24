import pandas as pd
import json
import torch
class CustomDataset():
    def __init__(self, path):
        df = pd.DataFrame(json.load(open(path))) 
        categories = df.columns.values.tolist()[1:]
        df[categories] = df[categories].astype('category')
        indexes = [df[category].cat.categories.to_list() for category in categories]
        for category in categories:
            df[category] = df[category].cat.codes
        self.appearance_catagories = dict(zip(categories, indexes))
        self.text_frame = df
        
    def __len__(self):
        return len(self.text_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        text = self.text_frame.iloc[idx, 0]
        appearances = self.text_frame.iloc[idx, 1:].to_list()
        appearances = torch.tensor(appearances).type(torch.LongTensor)
        sample = {'text': text, 'appearances': appearances}
        return sample