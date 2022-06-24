FROM pytorch/torchserve:0.5.3-cpu
COPY TransformerAppearanceClassifier.py combined.pt robertaHandler.py config.json /root
COPY roberta.base.encoder.pt roberta.vocab.pt /root/.cache/torch/hub/checkpoints/
COPY gpt2_bpe_encoder.json gpt2_bpe_vocab.bpe /root/.torchtext/cache/
COPY requirements.txt requirements.txt
USER root

RUN pip3 install -r requirements.txt

RUN torch-model-archiver \
    --model-name=getappearances \
    --version=1.0  \
    --model-file=/root/TransformerAppearanceClassifier.py \
    --serialized-file=/root/combined.pt \
    --handler=/root/robertaHandler.py \
    --extra-files="/root/config.json" \
    --export-path=/root

CMD ["torchserve", \
    "--start", \
    "--ncs", \
    "--model-store", \
     "/root", \
    "--models", \
    "classify=getappearances.mar"]

# torchserve --start --ncs --ts-config=/home/model-server/config.properties --model-store /home/model-server/model-store --models classify=getappearances.mar