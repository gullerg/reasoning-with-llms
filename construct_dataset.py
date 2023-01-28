import json
import os
import random
from datetime import datetime

random.seed(10)

resources_directory = "./resources"
data_directory = "./data"
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

samples_logic = []
samples_linguistic = []

n_samples = 100

argument_templates_file = open(os.path.join(resources_directory, "argument_templates.json"))

argument_templates = json.load(argument_templates_file)
argument_templates_logic = argument_templates["logic"]
argument_templates_linguistic = argument_templates["linguistic"]

propositions_file = open(os.path.join(resources_directory, "propositions.json"))
propositions = json.load(propositions_file)

noun_phrases_file = open(os.path.join(resources_directory, "noun_phrases.json"))
noun_phrases = json.load(noun_phrases_file)

#TODO: add a check to ensure that all samples are unique

while len(samples_logic) < n_samples:
    proposition_type = "normal" if random.random() < 0.5 else "nonce"

    template = random.sample(argument_templates_logic, 1)[0]
    argument_propositions = random.sample(propositions[proposition_type], 3)

    X = argument_propositions[0]
    Y = argument_propositions[1]
    Z = argument_propositions[2]

    sample = {}
    sample["type"] = "logic"
    sample["premise"] = template["premise"].replace("X", X).replace("Y", Y).replace("Z", Z)
    sample["conclusion"] = template["conclusion"].replace("X", X).replace("Y", Y).replace("Z", Z)
    sample["valid"] = template["valid"]

    samples_logic.append(sample)

while len(samples_linguistic) < n_samples:
    template = random.sample(argument_templates_linguistic, 1)[0]

    #X will always either be an object or a statement
    X = random.sample(propositions["normal"], 1)[0] if template["object"] == "statement" else random.sample(noun_phrases["objects"], 1)[0]

    #Y and Z will always be people
    people = random.sample(noun_phrases["people"], 2)
    
    Y = people[0]
    Z = people[1]

    sample = {}
    sample["type"] = "linguistic"
    sample["premise"] = template["premise"].replace("X", X).replace("Y", Y).replace("Z", Z)
    sample["conclusion"] = template["conclusion"].replace("X", X).replace("Y", Y).replace("Z", Z)
    sample["valid"] = template["valid"]

    samples_linguistic.append(sample)

samples = samples_logic + samples_linguistic

data_file_name = "data_{0}.json".format(datetime.timestamp(datetime.now()))
output_path = os.path.join(data_directory, data_file_name)

with open(output_path, "w") as outfile:
    outfile.write(json.dumps(samples))
