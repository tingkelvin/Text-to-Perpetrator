from flask import Flask, request, jsonify
from TransformerAppearanceClassifier import TransformerAppearanceClassifier
import json
import torch
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None
appearance_catagories = None

with open('config.json') as fp:
    config = json.load(fp)
    num_of_appearance_catagories = config['num_of_appearance_catagories']
    num_of_catagory_classes = config['num_of_catagory_classes']
    appearance_catagories = dict(config['appearance_catagories'])
    # serialized_file = self.manifest['model']['serializedFile']
    # model_pt_path = os.path.join(model_dir, serialized_file)
    model = TransformerAppearanceClassifier(
        num_of_appearance_catagories=num_of_appearance_catagories,
        num_of_catagory_classes=num_of_catagory_classes,
        device=device
    )

    checkpoint = torch.load('combined.pt', map_location=torch.device(device))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/predict')
def predict():
    input = request.args.get("text")
    # print("input", input)
    pred = model([input])
    pred = torch.squeeze(pred)
    pred = torch.argmax(pred, dim=1)
    pred_appearances = dict.fromkeys(appearance_catagories.keys(), 0)
    # print(pred)
    for i, key in enumerate(appearance_catagories.keys()):
        if len(appearance_catagories[key]) > pred[i]:
            # print(key, self.appearance_catagories[key][pred[i]])
            pred_appearances[key] = appearance_catagories[key][pred[i]]
        else:
            pred_appearances[key] = "NA"

    # print(json.dumps(pred_appearances))
    response = jsonify(pred_appearances)
    return response


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
