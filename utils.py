import pandas as pd
import torch
from torch.utils import tensorboard
from torch.utils.data import DataLoader
import torch.nn as nn
import string
import json
from model.TransformerAppearanceClassifier import TransformerAppearanceClassifier

import numpy as np

torch.manual_seed(376152)

class DataUtils():
    def __init__(self, path):
        df = pd.DataFrame(json.load(open(path)))
        categories = df.columns.values.tolist()[1:]
        df[categories] = df[categories].astype('category')
        indexes = [df[category].cat.categories.to_list()
                   for category in categories]
        for category in categories:
            df[category] = df[category].cat.codes
        self.appearance_catagories = dict(zip(categories, indexes))
        self.num_of_appearance_catagories = len(self.appearance_catagories)
        self.num_of_catagory_classes = max([
            len(self.appearance_catagories[cat]) for cat in self.appearance_catagories])
        self.text_frame = df

    def __len__(self):
        return len(self.text_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        text = self.text_frame.iloc[idx, 0]
        appearances = self.text_frame.iloc[idx, 1:].to_list()
        appearances = torch.tensor(appearances).type(torch.LongTensor)
        sample = {'text': text.translate(str.maketrans(
            '', '', string.punctuation)), 'appearances': appearances}
        return sample


class Model():
    def __init__(self, num_of_appearance_catagories,num_of_catagory_classes,args):
      self.device = torch.device(
          "cuda" if torch.cuda.is_available() else "cpu")
      self.model = TransformerAppearanceClassifier(num_of_appearance_catagories=num_of_appearance_catagories,
                                                    num_of_catagory_classes=num_of_catagory_classes,
                                                    device=self.device)
      
      self.loss_fn = nn.CrossEntropyLoss()
      self.optimizer = torch.optim.Adam(
          self.model.parameters(), lr=args.learning_rate)
      self.batch_size = args.batch_size
      self.num_of_appearance_catagories = num_of_appearance_catagories
      self.num_of_catagory_classes = num_of_catagory_classes
      self.model.to(self.device)
      print(f"Running GPU: {torch.cuda.get_device_name(0)}")

    def split_dataset(self, dataset):
      self.length = len(dataset)
      self.train_dataset, self.val_dataset, self.test_dataset = torch.utils.data.random_split(
          dataset, [int(self.length*0.8), int(self.length*0.1), int(self.length*0.1)])
      self.train_dataloader = DataLoader(
          self.train_dataset, batch_size=self.batch_size, shuffle=True)
      self.val_dataloader = DataLoader(
          self.val_dataset, batch_size=self.batch_size, shuffle=True)
      self.test_dataloader = DataLoader(
          self.test_dataset, batch_size=self.batch_size, shuffle=True)
        

    def train(self):
        num_batches = len(self.train_dataloader)
        losses, correct = 0, 0
        self.model.train()
        for i_batch, sample_batched in enumerate(self.train_dataloader):
            pred = self.model(sample_batched['text'])
            loss = self.loss_fn(pred.permute(0, 2, 1),
                                sample_batched['appearances'].to(self.device))
            losses += loss
            # Backpropagation
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            # if i_batch % 10 == 0:
            #     loss, current = loss.item(), i_batch * len(sample_batched['text'])
            #     print(f"loss: {loss:>7f}  [{current:>5d}/{4000:>5d}]")
          
        losses /= num_batches
        # print(f"Train avg loss: {losses:>8f}")
        return losses

    def validate(self):
      size = len(self.val_dataloader.dataset)

      num_batches = len(self.val_dataloader)
      losses, correct = 0, 0
      self.model.eval()
      with torch.no_grad():
          for i_batch, sample_batched in enumerate(self.val_dataloader):
              pred = self.model(sample_batched['text'])
              losses += self.loss_fn(pred.permute(0, 2, 1),
                                      sample_batched['appearances'].to(self.device)).item()
              pred = torch.argmax(pred, dim=2)
              correct += (pred == sample_batched['appearances'].to(
                  self.device)).type(torch.float).sum().item()
      losses /= num_batches
      correct /= size*self.num_of_appearance_catagories
      return losses, correct
        # print(f"Val Accuracy: {(100*correct):>0.1f}%, Val avg loss: {loss:>8f}")

    def test(self):
        size = len(self.test_dataloader.dataset)
        num_batches = len(self.test_dataloader)
        losses, corrects = 0, np.zeros(
            (self.num_of_appearance_catagories,), dtype=int)
        self.model.eval()
        with torch.no_grad():
            for i_batch, sample_batched in enumerate(self.test_dataloader):
                pred = self.model(sample_batched['text'])
                losses += self.loss_fn(pred.permute(0, 2, 1),
                                       sample_batched['appearances'].to(self.device)).item()

                pred = torch.argmax(pred, dim=2)
                # labels = torch.argmax(sample_batched['appearances'],dim=2)
                correct = pred == sample_batched['appearances'].to(self.device)
                for i in range(len(correct)):
                    for j in range(len(correct[i])):
                        if correct[i][j]:
                            corrects[j] += 1
        losses /= num_batches
        corrects = corrects/size
        # for i in range(10):
        #   test_data = next(iter(self.test_dataloader))
        #   print(test_data['text'][0])
        #   print("class", "predicted", "grantruth")
        #   getAppearances(test_data['text'][0], test_data['appearances'][0])
        #   print("-------------------------------------------------------------")
        print(f"Test Accuracy:\nrace: {(100*corrects[0]):>0.1f}%, gender: {(100*corrects[1]):>0.1f}%, hair_style:{(100*corrects[2]):>0.1f}%, hair_color: {(100*corrects[3]):>0.1f}%, hair_len: {(100*corrects[4]):>0.1f}%, top: {(100*corrects[5]):>0.1f}%, top_color: {(100*corrects[6]):>0.1f}%, bottom: {(100*corrects[7]):>0.1f}%, bottom_color: {(100*corrects[8]):>0.1f}%, footwear: {(100*corrects[9]):>0.1f}%, footwear_color: {(100*corrects[10]):>0.1f}%, accessory: {(100*corrects[11]):>0.1f}%, accessory_color: {(100*corrects[12]):>0.1f}%, Test avg loss: {losses:>8f} \n")
        return corrects.mean()

    def save(self, path):
      torch.save({
      'model_state_dict': self.model.state_dict(),
      'optimizer_state_dict': self.optimizer.state_dict(),
      }, path)
      print("Model saved.")
    
    def load(self, path):
      checkpoint = torch.load(path, map_location=torch.device(self.device))
      self.model.load_state_dict(checkpoint['model_state_dict'])


