# AzOpenAIEvals

This repo contains a completionfunction for using azure openai chat completions api for running evals.

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

   oaieval azure_openai test-match --registry_path registry

   ```
