import json
import concurrent.futures
import requests


# dispatch requests in parallel
url = f'https://mci-7qq6nbfcxq-km.a.run.app/predict'
paraphrase = {'text': "RP states male is out front of his address, throwing glass bottles at passing cars/pedestrians. Appears drug affected. Male described as cauc, wearing a grey hoodie, black track pants, addidas sneakers, red cap."}
        # we'll send half the requests as not_paraphrase examples for sanity
data = paraphrase 
response = requests.post(url, data=paraphrase)
print(requests.post(url, data=paraphrase))
print(response)

