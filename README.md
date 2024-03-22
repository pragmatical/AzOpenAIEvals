# AzOpenAIEvals

This repo contains a completionfunction for using azure openai chat completions api for running evals.

NOTE: this requires an Azure OpenAI resource and credentials for that resource, even though we will be running evaluations against that Azure OpenAI API resource, there is still a need to provide a key for OpenAI API as the oaieval CLI requires it.

## Usage

1. Install project required packages by runing the following command

   ``` bash

   pip install -r requirements.txt

   ```

2. Create a .env file in the top level directory to hold your azure openai configurations and secrets, example file is found [here](sampledotenv)
3. Run the following command to set environment variables from your newly created .env file

   ``` bash

   source setenv.sh

   ```

4. Add current directory to  python envrironment to be able to use modules and packages

   ``` bash

   pip install -e .

   ```

5. Test evals against your Azure OpenAI API

   ``` bash

   # Since some of the evaluation sets are quite large, we add the max_samples parameter to avoid overwhelming your Azure OpneAI resource

   oaieval azure_openai test-match --registry_path registry --max_samples 5

   ```
