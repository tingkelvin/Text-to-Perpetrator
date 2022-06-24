from os.path import join
from turtle import home
from utils import DataUtils, Model
import argparse
import os
import json
from torch.utils.tensorboard import SummaryWriter


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_args():
    '''
    Usual pythonic way of parsing command line arguments
    :return: all command line arguments read
    '''
    args = argparse.ArgumentParser("walk")
    args.add_argument('-ip', '--input', default='dataset/',
                      help='Dataset filename')
    args.add_argument('-d', '--dataset', type=str, default='',
                      help='Name of the dataset')
    args.add_argument('-e', '--epoches', default=50, type=int,
                      help='Number of epochs (for GRU)')
    args.add_argument('-lr', '--learning_rate', default=5e-4, type=float,
                      help='Learning rate')
    args.add_argument('-b', '--batch_size', default=256, type=int,
                      help='Learning rate')
    args.add_argument('-t', '--train', nargs='?', const=True, default=True, type=str2bool,
                      help='Is training?')
    args.add_argument('-tb', '--tensorboard', nargs='?', const=True, default=True, type=str2bool,
                      help='Tensorboard?')
    args.add_argument('-o', '--output', type=str, default='save/',
                      help='Output file for the model')
    args.add_argument('-g', '--google_colab', nargs='?', const=True, default=False, type=str2bool,
                      help='running on google colab?')

    return args.parse_args()

    # print(f"Val Accuracy: {(100*correct):>0.1f}%, Val avg loss: {loss:>8f}")


if __name__ == "__main__":
  args = parse_args()

  if args.google_colab:
      home_dir = "/content/mnt/MyDrive/Team-15/NLP/"
  else:
      home_dir = os.getcwd()
  data_dir = join(home_dir, args.input, args.dataset)
  saved_path = home_dir + 'save/' + args.dataset + '.pt'
  dataset_name = args.dataset + ".json"
  dataset = DataUtils(join(data_dir, dataset_name))

  configs = json.load(open(home_dir + "config.json", "r"))
  if args.dataset not in configs.keys():
    configs[args.dataset] = {"acc":0, 
    "num_of_appearance_catagories": dataset.num_of_appearance_catagories, 
    "num_of_catagory_classes": dataset.num_of_catagory_classes, 
    "appearance_catagories": dataset.appearance_catagories}

  config = configs[args.dataset]

  model = Model(config["num_of_appearance_catagories"], config["num_of_catagory_classes"], args)
  if args.train:
    print(
        f"Training Dataset: {args.dataset}, batch size: {args.batch_size}, epochs: {args.epoches}, learning rate: {args.learning_rate}")
    if args.tensorboard:
        writer = SummaryWriter(
            f'{home_dir}tensorboard/{args.dataset}/BatchSize {args.batch_size} LR {args.learning_rate} ')

    max_acc = config['acc']
    model.split_dataset(dataset)
    for epoch in range(args.epoches):
        tr_loss = model.train()
        val_loss, val_acc = model.validate()

        print(
            f"Epoch {epoch+1}: Train loss: {tr_loss:>8f}, Val loss: {val_loss:>8f}, Val acc: {(100*val_acc):>0.1f}%")
        if val_acc > max_acc:
            model.save(saved_path)
            max_acc = val_acc

        if args.tensorboard:
            writer.add_scalar("loss/train", tr_loss, epoch)
            writer.add_scalar("loss/val", val_loss, epoch)
            writer.add_scalar("acc/val", val_acc, epoch)
            writer.add_hparams({'lr': args.learning_rate, 'bsize': args.batch_size}, {
                                "accuracy": val_acc, "loss": val_loss})
    config['acc'] = max_acc
    jsonFile = open(home_dir + "config.json", "w+")
    jsonFile.write(json.dumps(configs, indent=4))    
  else:
    # if not trained then just load the model from save
    if os.path.exists(saved_path):
        print(f"Loading trained model on dataset {args.dataset}...")
        model.load(saved_path)
    else:
        raise FileNotFoundError(
            f'Trained model on dataset {args.dataset_name} is not found.')
    model.split_dataset(dataset)    
    model.test()
