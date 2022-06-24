import torch
import torch.nn as nn
import torchtext
from torchtext.functional import to_tensor


class TransformerAppearanceClassifier(nn.Module):
    def __init__(self, num_of_appearance_catagories, num_of_catagory_classes, device):
        super().__init__()
        self.device = device
        self.hidden_vector_size = 768
        self.num_of_appearance_catagories = num_of_appearance_catagories
        self.num_of_catagory_classes = num_of_catagory_classes
        roberta_model_bundle = torchtext.models.ROBERTA_BASE_ENCODER
        self.text_tokenizer = roberta_model_bundle.transform()
        self.encoder_transformer = roberta_model_bundle.get_model()
        # Turn gradients off to freeze the encoder and prevent it from changing during training
        self.encoder_transformer.requires_grad_(False)
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=self.hidden_vector_size, nhead=8, batch_first=True)
        self.decoder_transformer = nn.TransformerDecoder(
            decoder_layer, num_layers=6)
        self.learnable_queries = nn.Parameter(torch.randn(
            (self.num_of_appearance_catagories, self.hidden_vector_size)))
        self.readout_layer = nn.Conv1d(
            in_channels=self.num_of_appearance_catagories * self.hidden_vector_size,
            out_channels=self.num_of_appearance_catagories * self.num_of_catagory_classes,
            kernel_size=1,
            groups=self.num_of_appearance_catagories,
        )

    def forward(self, list_of_input_text):
        tokenized_input_list = self.text_tokenizer(list_of_input_text)
        padding_token = 1
        tokenized_input_tensor = to_tensor(
            tokenized_input_list, padding_value=padding_token).to(self.device)
        batch_size, sequence_length = tokenized_input_tensor.shape
        encoded_feature_tensor = self.encoder_transformer(
            tokenized_input_tensor)
        batch_of_learnable_queries = self.learnable_queries.repeat(
            batch_size, 1, 1)
        query_response_tensor = self.decoder_transformer(
            batch_of_learnable_queries, encoded_feature_tensor)
        query_response_tensor = query_response_tensor.reshape(
            batch_size, self.num_of_appearance_catagories * self.hidden_vector_size, 1)
        prediction_tensor = self.readout_layer(query_response_tensor)
        prediction_tensor = prediction_tensor.reshape(
            batch_size, self.num_of_appearance_catagories, self.num_of_catagory_classes)
        return prediction_tensor
