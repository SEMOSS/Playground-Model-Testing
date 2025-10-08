# Playground-Model-Testing
![README Image](test-images/readme-image.png "Description of the image")
## Project Overview

This is a Python testing framework for validating AI model responses across different providers through the SEMOSS API. The framework runs standardized tests against multiple models and uses OpenAI models to confirm response quality.

## Environment Setup

This project uses `uv` for dependency management.

**Required Environment Variables (in `.env`):**
- `SEMOSS_ACCESS_KEY` - Access key for SEMOSS API
- `SEMOSS_SECRET_KEY` - Secret key for SEMOSS API
- `SEMOSS_BASE_URL` - Base URL for SEMOSS instance (e.g., `http://localhost:9090/Monolith/api`)
- `OPENAI_API_KEY` - OpenAI API key for confirmation testing

**Install dependencies:**
```bash
uv sync
```
**OR**
```bash
pip install -r pyproject.toml
```


## Running Application
**To run the application, use the following command:**
```bash
streamlit run main.py
```

**Proceed to http://localhost:8501 in your web browser.**

## Project Structure
- `main.py`: Entry point for the Streamlit application.
- `src/`: Contains all source code.
    - `runners/`: Logic for executing tests against selected models.
    - `tests/`: Standardized test cases and response models.
    - `utils/`: Utility functions and model definitions.
    - `confirmations/`: Logic for confirming test responses using OpenAI models.
    - `pixels/`: Pixel factory class for creating pixel calls

## Adding New Models
To add a new model, update the `models` list in `src/utils/models.py` with the new model's details.

## Adding New Tests
1. Create a new method in `src/tests/standard_tests.py` or create a new file/class with the method.
2. (If required) Update the Pixel Maker class to include any new parameters needed for the test.
3. Then update the `TestSelections` class in `src/runners/runners.py` to include the new test option.
4. Update the `run_selected_tests` function in `src/runners/runners.py` to execute the new test when selected.
5. Update the Streamlit UI in `main.py`

## Test to Add
- [ ] **Basic Param Values**: Test model's ability to handle basic param values like temperature, max tokens, etc.
```bash
AskPlayground(
engine=["b0d18f4b-ff2c-4563-8f9d-57efbff53d60"],
roomId=["9431b571-b8d0-4502-80a5-52b3cc50cb18"],
command=["<encode>Tell me a story about World War 2.</encode>"],
mcpToolID=[],
paramValues=[{"temperature": 0.7, "max_tokens": 2000, "top_p": 0.9}]
);
```

- [ ] **Prompt with Base64 Images**: Test model's ability to handle prompts containing base64-encoded images.
```bash
AskPlayground(
engine=["b0d18f4b-ff2c-4563-8f9d-57efbff53d60"],
roomId=["9431b571-b8d0-4502-80a5-52b3cc50cb18"],
command=["<encode>What is this image?</encode>"],
context=[],
image=["\\Harry-Maguire-Victor-Lindelof-Man-Utd-F365.jpg"],
mcpToolID=[],
paramValues=[]
);
```

- [ ] **Structured JSON Ouputs**: Test model's ability to return structured JSON responses.
```bash
AskPlayground(roomId=["5828f90f-22b4-4299-ad75-96e93085bdba"], engine=["4acbe913-df40-4ac0-b28a-daa5ad91b172"], command=["Name a few Manchester United players you know with their positions, countries, and skill ratings."], paramValues=[{'schema': {'type': 'object', 'properties': {'players': {'type': 'array', 'items': {'type': 'object', 'properties': {'name': {'type': 'string'}, 'position': {'type': 'string'}, 'country': {'type': 'string'}, 'skill': {'type': 'integer'}}, 'required': ['name', 'position', 'country', 'skill']}}}, 'required': ['players']}}]);
```

- [ ] **Tool Calling**: Test the full tool calling script (ie. sending a prompt with tool IDs, getting a response with tool calls, executing the tool calls, sending the tool results back to the model, and getting a final response).
```bash 
AskPlayground(
engine=["b0d18f4b-ff2c-4563-8f9d-57efbff53d60"],
roomId=["8d8cf868-6d61-4cc6-a092-39e528d0775a"],
command=["<encode>What is the price of META?</encode>"],
context=[],
images=[],
mcpToolID=["29e9e371-9243-4293-ad3b-4be08ef95ab5"],

paramValues=[]
);
```

- [ ] **Tool Calling with Tool Choice**: Test the model's ability to handle tool choice selections such as AUTO, FORCED, NONE, REQUIRED
```bash 
AskPlayground(
engine=["b0d18f4b-ff2c-4563-8f9d-57efbff53d60"],
roomId=["8d8cf868-6d61-4cc6-a092-39e528d0775a"],
command=["<encode>What is the price of META?</encode>"],
context=[],
images=[],
mcpToolID=["29e9e371-9243-4293-ad3b-4be08ef95ab5"],

paramValues=[{"tool_choice": "AUTO"}]
);
```

- [ ] **Streaming**: Test model's ability to handle streaming responses. This will be easier when we flip the current LLM reactor to LLM2 and we can use the SDK's built-in streaming functionality.


## Features to Add

- [ ] **Ability to export results as JSON**: Allow users to download test results in JSON format that can be easily shared.

- [ ] **Ability to add models through UI**: Update the code to read models from a JSON file so that we can add models through the UI instead of hardcoding them in `models.py`

- [ ] **Ability to update env variables through UI**: Allow users to update environment variables like SEMOSS API keys and OpenAI API key through the UI.

- [ ] **Full Capabilities Test**: Eventually when we have more tests built, I want the ability to add a model, run the full test suite and return a table of the capabilities of the model

- [ ] **Docker Support**: Ability to run the application in a Docker container for easier deployment (preferably with Docker Compose)