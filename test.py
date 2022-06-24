from os.path import join
from utils import Model
import json
import argparse
import os
from model.TransformerAppearanceClassifier import TransformerAppearanceClassifier
import torch
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
  args.add_argument('-m', '--model', type=str, default='',
                    help='Name of the model')
  args.add_argument('-t', '--text', type=str, default='',
                    help='text?')                
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

  configs = json.load(open(home_dir + "config.json", "r"))
  if not configs[args.model]:
    raise FileNotFoundError(
    f'Config on model ${args.model} is not found.')
  config = configs[args.model]
  saved_path = home_dir + 'save/' + args.model + '.pt'

  max_acc = 0
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  model = TransformerAppearanceClassifier(config["num_of_appearance_catagories"], config["num_of_catagory_classes"], device)
  model.to(device)
  model.eval()
  checkpoint = torch.load(saved_path, map_location=torch.device(device))
  model.load_state_dict(checkpoint['model_state_dict'])
  appearance_catagories = config["appearance_catagories"]
  pred = model([args.text])
  pred = torch.squeeze(pred)
  pred = torch.argmax(pred, dim=1)
  for i, key in enumerate(appearance_catagories.keys()):
      print(key, appearance_catagories[key][pred[i]])
  
