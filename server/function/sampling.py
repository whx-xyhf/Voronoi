import random
from bns import BNS

class Sampling:
    def __init__(self, data):
        self.data = data
        pass

    def rns(self, rate):
        count = int(len(self.data) * rate)
        sampling_points = random.sample(self.data, count)
        return sampling_points

    def bns(self, rate):
        r = 0.01
        learning_rate = 0.002
        bns = BNS(self.data, R=r)
        sampling_points = bns.apply_sample()
        print(bns.rate)
        r_record = [r]
        result_record = []
        while bns.rate != rate:
            if bns.rate < rate:
                result_record.append('greater')
                if len(result_record) == 1:
                    r = r / 2
                else:
                    if result_record[len(result_record)-1] == 'greater':
                        r = r / 2
                    else:
                        r = r_record[len(r_record)]
            else:
                result_record.append('smaller')
        pass

