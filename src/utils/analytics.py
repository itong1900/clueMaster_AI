import datetime
import pandas as pd
import os

# import sys
# sys.path.append("../utils/")

def export_csv_helper(playersHashmap, nameOfGame):
    ct = str(datetime.datetime.now()).split()[0]
    path = "../../log/" + ct + "-" + nameOfGame + "/"
    for player in playersHashmap.keys():
        if not os.path.exists(path):
            os.mkdir(path)
        full_path = path + player + ".csv"
        playersHashmap[player].score_table.to_csv(full_path)
