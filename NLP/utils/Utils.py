import numpy as np
import torch
from torch.utils.data import DataLoader

torch.manual_seed(376152)


class Utils():
    def __init__(self, model, data, batchsize, loss_fn, optimizer, device):
        self.model = model
        self.loss_fn = loss_fn
        self.optimzer = optimizer
        self.device = device
        self.batchsize = batchsize
        self.length = len(data)
        self.train_dataset, self.val_dataset, self.test_dataset = torch.utils.data.random_split(
            data, [int(self.length*0.8), int(self.length*0.1), int(self.length*0.1)])

    def train(self):
        train_dataloader = DataLoader(
            self.train_dataset, batch_size=self.batch_size, shuffle=True)
        size = len(train_dataloader .dataset)
        num_batches = len(train_dataloader)
        losses, correct = 0, 0
        self.model.train()
        for i_batch, sample_batched in enumerate(train_dataloader):
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

    def validate(dataloader, model, loss_fn, device):
        size = len(dataloader.dataset)
        num_batches = len(dataloader)
        loss, correct = 0, 0
        padding_token = 1
        model.eval()
        with torch.no_grad():
            for i_batch, sample_batched in enumerate(dataloader):
                pred = model(sample_batched['text'])
                loss += loss_fn(pred.permute(0, 2, 1),
                                sample_batched['appearances'].to(device)).item()
                pred = torch.argmax(pred, dim=2)
                correct += (pred == sample_batched['appearances'].to(
                    device)).type(torch.float).sum().item()
        loss /= num_batches
        correct /= size*13
        return loss, correct
        # print(f"Val Accuracy: {(100*correct):>0.1f}%, Val avg loss: {loss:>8f}")

    def test(dataloader, model, loss_fn, device, f):
        size = len(dataloader.dataset)
        num_batches = len(dataloader)
        losses, corrects = 0, np.zeros((13,), dtype=int)
        model.eval()
        with torch.no_grad():
            for i_batch, sample_batched in enumerate(dataloader):
                pred = model(sample_batched['text'])
                losses += loss_fn(pred.permute(0, 2, 1),
                                  sample_batched['appearances'].to(device)).item()

                pred = torch.argmax(pred, dim=2)
                # labels = torch.argmax(sample_batched['appearances'],dim=2)
                correct = pred == sample_batched['appearances'].to(device)
                for i in range(len(correct)):
                    for j in range(len(correct[i])):
                        if correct[i][j]:
                            corrects[j] += 1
        losses /= num_batches
        corrects = corrects/size
        if f:
            print(f"Test Accuracy:\nrace: {(100*corrects[0]):>0.1f}%, gender: {(100*corrects[1]):>0.1f}%, hair_style:{(100*corrects[2]):>0.1f}%, hair_color: {(100*corrects[3]):>0.1f}%, hair_len: {(100*corrects[4]):>0.1f}%, top: {(100*corrects[5]):>0.1f}%, top_color: {(100*corrects[6]):>0.1f}%, bottom: {(100*corrects[7]):>0.1f}%, bottom_color: {(100*corrects[8]):>0.1f}%, footwear: {(100*corrects[9]):>0.1f}%, footwear_color: {(100*corrects[10]):>0.1f}%, accessory: {(100*corrects[11]):>0.1f}%, accessory_color: {(100*corrects[12]):>0.1f}%, Test avg loss: {losses:>8f} \n")
        return corrects.mean()
