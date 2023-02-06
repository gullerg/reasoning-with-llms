import argparse
import json
import os
from datetime import datetime
from helpers import test_model

models = {
    "1": "text-davinci-001",
    "2": "text-davinci-002",
    "3": "text-davinci-003"
}


def validate_mode(mode):
    if mode not in ['all', '1', '2', '3']:
        raise argparse.ArgumentTypeError(
            "%s is an invalid value, must be in ['all', '1', '2', '3']" % mode)
    return mode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-mode", help="Determines which models to test. Either 'all', '1', '2', or '3", default='3', type=validate_mode)
    parser.add_argument(
        "-path_to_data_dir", help="The relative path to the directory containing the experiment data")
    args = parser.parse_args()

    mode = args.mode
    path_to_data_dir = args.path_to_data_dir

    results = []

    if mode == "all":
        for model in models.values():
            for filename in os.scandir(path_to_data_dir):
                if filename.is_file():
                    result = test_model(filename.path, model)
                    results.append(result)
    else:
        for filename in os.scandir(path_to_data_dir):
            if filename.is_file():
                result = test_model(filename.path, models[mode])
                results.append(result)


    output_dir = os.path.join(path_to_data_dir, "results")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, "results_{0}.json".format(datetime.timestamp(datetime.now())))
    with open(output_path, "w") as outfile:
        outfile.write(json.dumps(results))


if __name__ == "__main__":
    main()
