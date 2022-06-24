from TransformerAppearanceClassifier import TransformerAppearanceClassifier
import os
import json
import sys
import logging

import torch
from ts.torch_handler.base_handler import BaseHandler
logger = logging.getLogger(__name__)

class robertaHandler(BaseHandler):
    def __init__(self):
        super(robertaHandler, self).__init__()
        self.initialized = False

    def initialize(self, context):
        # self.manifest = context.manifest
        # properties = context.system_properties
        # model_dir = properties.get("model_dir")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        with open('config.json') as fp:
            config = json.load(fp)
        self.num_of_appearance_catagories = config['num_of_appearance_catagories']
        self.num_of_catagory_classes = config['num_of_catagory_classes']
        self.appearance_catagories = dict(config['appearance_catagories'])
        # serialized_file = self.manifest['model']['serializedFile']
        # model_pt_path = os.path.join(model_dir, serialized_file)
        self.model = TransformerAppearanceClassifier(
            num_of_appearance_catagories=self.num_of_appearance_catagories,
            num_of_catagory_classes=self.num_of_catagory_classes,
            device=self.device
        )

        self.checkpoint = torch.load('combined.pt', map_location=torch.device(self.device))
        self.model.load_state_dict(self.checkpoint['model_state_dict'])
        self.model.to(self.device)
        self.model.eval()
        self.initialized = True

    def preprocess(self, input_data):
        """
        Tokenization pre-processing
        """
        print("data_input", input_data[0]['text'].decode('utf-8'))
        # input_ids = []
        # attention_masks = []
        # token_type_ids = []
        # for row in input_data:
        #     seq_0 = row['seq_0'].decode('utf-8')
        #     seq_1 = row['seq_1'].decode('utf-8')
        #     logger.debug(f'Received text: "{seq_0}", "{seq_1}"')

        #     inputs = self.tokenizer.encode_plus(
        #             seq_0,
        #             seq_1,
        #             max_length=self.max_length,
        #             padding='max_length',
        #             truncation=True,
        #             return_tensors='pt'
        #             )

        #     input_ids.append(inputs['input_ids'])
        #     attention_masks.append(inputs['attention_mask'])
        #     token_type_ids.append(inputs['token_type_ids'])

        # batch = (torch.cat(input_ids, 0),
        #         torch.cat(attention_masks, 0),
        #         torch.cat(token_type_ids, 0))
        return input_data[0]['text'].decode('utf-8')

    def inference(self, input):
        print("input", input)
        logger.debug(f'Received text: {input}')
        pred = self.model([input])
        pred = torch.squeeze(pred)
        pred = torch.argmax(pred, dim=1)
        pred_appearances = dict.fromkeys(self.appearance_catagories.keys(), 0)
        # print(pred)
        for i, key in enumerate(self.appearance_catagories.keys()):
            if len(self.appearance_catagories[key]) > pred[i]:
                # print(key, self.appearance_catagories[key][pred[i]])
                pred_appearances[key] = self.appearance_catagories[key][pred[i]]
            else:
                pred_appearances[key] = "NA"

        print(json.dumps(pred_appearances))
        return [json.dumps(pred_appearances)]

    def postprocess(self, inference_output):
        return inference_output


# test = robertaHandler()
# test.initialize("test")
# test.preprocess("hi")
# test.inference("black, red hat")
# torch-model-archiver \
#     --model-name "roberta" \
#     --version 1.0 \
#     --serialized-file ./combined.pt \
#     --handler "./robertaHandler.py" \
#     --export-path model_store\
#     --extra-files "./config.json,./TransformerAppearanceClassifier.py"

# torch-model-archiver \
#     --model-name my_text_classifier \
#     --version 1.0 \
#     --model-file TransformerAppearanceClassifier.py \
#     --serialized-file combined.pt  \
#     --export-path model_store\
#     --handler "./robertaHandler.py" \
#     --extra-files "./config.json"
