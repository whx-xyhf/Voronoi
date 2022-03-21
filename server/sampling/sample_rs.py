import json
import random
if __name__ == "__main__":
    for i in range(1):
        filename_origin = "Occupation"
        for rate in [0.05]:
            with open(f'../data/{filename_origin}.json', 'r') as fr:
                data = json.load(fr)
            count = int(len(data) * rate)
            data_processed = random.sample(data, count)
            with open(f'../data/rs_{filename_origin}$rate={round(rate,2)}$count={i}.json', 'w') as fw:
                json.dump(data_processed, fw)
