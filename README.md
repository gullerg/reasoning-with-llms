## Reasoning with LLMs
Repository containing the source code to test logic and linguistic reasoning abilities of LLMs.

The repository currently contains:
- A script to generate data (`construct_dataset.py`)
- A script to run the experiments (`run_experiments.py`)
- Several resrouces to generate the data (`/resources`)

### Get started
To get started, you must first clone this repository:

```
 git clone https://github.com/gullerg/reasoning-with-llms.git
 cd reasoning-with-llms
```

Once you're inside the cloned repo, install the dependencies. First create a virtual environment and activate it:

```
python -m venv env
source env/bin/activate
```

Now, install the required packages:

```
pip install -r requirements.txt
```

Finally, make sure that you set your OpenAI API key as an environment variable:


    export OPENAI_API_KEY='sk-xxxxxxxxxxxxxx'

### Generate data
To generate the data, run:

    python generate_data.py

### Run the experiments
To run the experiments, run: 
