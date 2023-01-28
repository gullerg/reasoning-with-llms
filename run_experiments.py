import argparse
import json
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

models = {
    "ada": "text-ada-001",
    "babbage": "text-babbage-001",
    "curie": "text-curie-001",
    "davinci": "text-davinci-003"
}


def validate_mode(mode):
    if mode not in ['ada', 'babbage', 'curie', 'davinci']:
        raise argparse.ArgumentTypeError(
            "%s is an invalid value, must be in ['all', 'ada', 'babbage', 'curie', 'davinci']" % mode)
    return mode


def get_prompt(sample):
    return (
        "You are a large language model tasked to determine whether certain conclusions can be inferred from certain premises. " +
        "You will b presented with a premise and a conclusion, and you will have to determine whether the conclusion can be inferred from the premise. " +
        "If the conclusion can be inferred from the premise, reply with 'yes'; otherwise, reply with 'no'. If you don't know, reply with 'cannot be decided'. " +
        "You're only allowed to reply with 'yes', 'no', or 'cannot be decided'. \n" +
        "Premise:\n{0}\n".format(sample["premise"]) +
        "Conclusion:\n{0}\n".format(sample["conclusion"]) +
        "Conclusion can be inferred from premise:"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-mode", help="Determines which models to test. Either 'all', 'ada', 'curie', or 'davinci", default='ada', type=validate_mode)
    parser.add_argument(
        "-path_to_data", help="The relative path to the file containing the experiment data")
    args = parser.parse_args()

    mode = args.mode
    path_to_data = args.path_to_data

    data_file = open(path_to_data)
    data = json.load(data_file)

    for sample in data:
        completion = openai.Completion.create(
            model=models[mode],
            prompt=get_prompt(sample),
            max_tokens=4
        )
        print(completion.choices[0].text.strip(), sample["valid"], sample["type"])


if __name__ == "__main__":
    main()
