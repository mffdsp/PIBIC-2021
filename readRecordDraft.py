import json

import pandas as pd
import wfdb

json_test = {}

for i in range(100, 235):
    try:
        record = wfdb.rdrecord('./'+str(i))
    except:
        continue
    d_record = record.__dict__
    ft = d_record['sig_name']
    json_test[i] = {ft[0]:  list(d_record['p_signal'][:, 0]),
                    ft[1]:  list(d_record['p_signal'][:, 1])}


with open('data.json', 'w') as fp:
    json.dump(json_test, fp, indent=1)
