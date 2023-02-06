import json
import os
import random
from datetime import datetime
import argparse

from helpers import get_samples

random.seed(10)


def validate_mode(mode):
    if mode not in ['all', 'normal', 'nonce', 'random']:
        raise argparse.ArgumentTypeError(
            "%s is an invalid value, must be in ['all', 'normal', 'nonce', 'random']" % mode)
    return mode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-mode", help="Determines what data to generate. Either 'all', 'normal', 'nonce', or 'random'", default='all', type=validate_mode)
    args = parser.parse_args()

    mode = args.mode

    data_directory = "./data"
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    current_data_directory = os.path.join(
        data_directory, "run_{0}".format(datetime.timestamp(datetime.now())))
    if not os.path.exists(current_data_directory):
        os.makedirs(current_data_directory)

    n_samples = 100

    tasks = ["logic", "linguistic"]
    data_types = ["normal", "nonce", "random"]

    if mode == "all":
        for task in tasks:
            for data_type in data_types:
                samples = get_samples(
                    task=task, data_type=data_type, n_samples=n_samples)

                data_file_content = {
                    "meta_data": {
                        "task": task,
                        "type": data_type
                    },
                    "data": samples
                }

                data_file_name = "data_{0}_{1}_{2}.json".format(
                    task, data_type, datetime.timestamp(datetime.now()))
                output_path = os.path.join(
                    current_data_directory, data_file_name)

                with open(output_path, "w") as outfile:
                    outfile.write(json.dumps(data_file_content))

    else:
        for task in tasks:
            samples = get_samples(
                task=task, data_type=mode, n_samples=n_samples)

            data_file_content = {
                "meta_data": {
                    "task": task,
                    "type": mode
                },
                "data": samples
            }

            data_file_name = "data_{0}_{1}_{2}.json".format(
                task, mode, datetime.timestamp(datetime.now()))
            output_path = os.path.join(current_data_directory, data_file_name)

            with open(output_path, "w") as outfile:
                outfile.write(json.dumps(data_file_content))

    print("-------")
    print("Data generated")
    print("-------")
    print("To run experiments, execute:")
    print("python run_experiments.py -path_to_data_dir {0}".format(current_data_directory))


if __name__ == "__main__":
    main()
