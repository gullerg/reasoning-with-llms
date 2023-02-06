import os
import json
import random
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

resources_directory = "./resources"

argument_templates_file = open(os.path.join(
    resources_directory, "argument_templates.json"))

argument_templates = json.load(argument_templates_file)
argument_templates_logic = argument_templates["logic"]
argument_templates_linguistic = argument_templates["linguistic"]

propositions_file = open(os.path.join(
    resources_directory, "propositions.json"))
propositions = json.load(propositions_file)

noun_phrases_file = open(os.path.join(
    resources_directory, "noun_phrases.json"))
noun_phrases = json.load(noun_phrases_file)


def get_samples(task, data_type="normal", n_samples=100):
    # TODO: add a check to ensure that all samples are unique
    samples = []
    if task == "logic":
        while len(samples) < n_samples:
            # proposition_type = "normal" if random.random() < 0.5 else "nonce"
            proposition_type = data_type

            template = random.sample(argument_templates_logic, 1)[0]
            argument_propositions = random.sample(
                propositions[proposition_type], 3)

            X = argument_propositions[0]
            Y = argument_propositions[1]
            Z = argument_propositions[2]

            sample = {}
            sample["premise"] = template["premise"].replace(
                "X", X).replace("Y", Y).replace("Z", Z)
            sample["conclusion"] = template["conclusion"].replace(
                "X", X).replace("Y", Y).replace("Z", Z)
            sample["valid"] = template["valid"]

            samples.append(sample)
    else:
        while len(samples) < n_samples:
            template = random.sample(argument_templates_linguistic, 1)[0]

            # X will always either be an object or a statement
            X = random.sample(propositions[data_type], 1)[
                0] if template["object"] == "statement" else random.sample(noun_phrases["objects"][data_type], 1)[0]

            # Y and Z will always be people
            people = random.sample(noun_phrases["people"][data_type], 2)

            Y = people[0]
            Z = people[1]

            sample = {}
            sample["premise"] = template["premise"].replace(
                "X", X).replace("Y", Y).replace("Z", Z)
            sample["conclusion"] = template["conclusion"].replace(
                "X", X).replace("Y", Y).replace("Z", Z)
            sample["valid"] = template["valid"]

            samples.append(sample)
    return samples


def get_prompt(sample):
    return (
        "You are a large language model tasked to determine whether certain conclusions can be inferred from certain premises. " +
        "You will be presented with a premise and a conclusion, and you will have to determine whether the conclusion can be inferred from the premise. " +
        "If the conclusion can be inferred from the premise, reply with 'yes'; otherwise, reply with 'no'. " +
        "You're only allowed to reply with 'yes' or 'no'.\n" +
        "Premise:\n{0}\n".format(sample["premise"]) +
        "Conclusion:\n{0}\n".format(sample["conclusion"]) +
        "Conclusion can be inferred from premise:"
    )


def test_model(path_to_data, model):
    print(path_to_data)
    data_file = open(path_to_data)
    data_file_content = json.load(data_file)
    data = data_file_content["data"]

    task = data_file_content["meta_data"]["task"]
    data_type = data_file_content["meta_data"]["type"]

    print("Model:", model)
    print("Task:", task)
    print("Type:", data_type)

    correct = 0

    for sample in data:
        completion = openai.Completion.create(
            model=model,
            prompt=get_prompt(sample),
            max_tokens=4
        )
        answer = completion.choices[0].text.lower(
        ).strip().replace('.', '')
        if (answer == "yes") and sample["valid"]:
            correct += 1
        elif (answer == "no") and not sample["valid"]:
            correct += 1

    print("Accuracy:", correct / len(data))

    return {
        "task": data_file_content["meta_data"]["task"],
        "type": data_file_content["meta_data"]["type"],
        "accuracy": correct / len(data),
        "model": model
    }
