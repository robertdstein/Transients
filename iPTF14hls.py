import numpy as np
import os
import ConfigParser
import argparse
import sys

sys.path.append(
    "/afs/ifh.de/user/s/steinrob/Desktop/python/The-Flux-Evaluator/")

import MergeFiles as MF
import RunCluster as RC

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--submit", action="store_true")
cfg = parser.parse_args()

user_dir = "/afs/ifh.de/user/s/steinrob/Desktop/python/The-Flux-Evaluator/"
file_name = "analysis_config/iPTF14hls.ini"
pickle_name = "iPTF14hls/result"

test_configs_file = user_dir + file_name

Config = ConfigParser.ConfigParser()

name = pickle_name

with open(test_configs_file, "w") as f:
    Config.add_section(name)
    Config.set(name, "UseEnergy", True)
    Config.set(name, "FitGamma", True)
    Config.set(name, "FixedGamma", 2)
    Config.set(name, "UseTime", True)
    Config.set(name, "SimTimeModel", "Decay")
    Config.set(name, "SimTimeParameters",
               {"t0": 300, "length": 100, "t_pp": 1.0})
    Config.set(name, "ReconTimeModel", "Box")
    Config.set(name, "ReconTimeParameters", {"t0": -50, "length": 1000})
    Config.set(name, "FitWeights", True)
    Config.set(name, "UseBox", True)
    Config.set(name, "CatName",
               "/afs/ifh.de/user/s/steinrob/scratch/PS_Data/" +
               "Catalogue/iPTF14hls.npy")
    Config.set(name, "DataConfig", "IC86.ini")
    Config.set(name, "MaxK", 1)
    Config.write(f)

# os.system("rm " + user_dir + "logs/*")

if cfg.submit:
    for section in Config.sections():
        os.system(
            "python " + user_dir + "RunLocal.py" +
            " -c " + section + " -f " + file_name + " -n 100 -s 10")
    #
    #     RC.submit_to_cluster(10, section, file_name, ntrials=200, steps=20)
    # RC.wait_for_cluster()

name = pickle_name
fits = MF.run(name, user_dir)

print fits
