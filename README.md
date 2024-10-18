# COSEVITO Chatbot

Specialized chatbot in preparation for COSEVI driving test

## Instalation

- Create the environment
```
$ python -m venv venv
```

- Activate the virtual environment

    On Windows:
```
$ .\venv\Scripts\Activate.ps1
```

    On MacOS and Linux:

```
$ source venv/Scripts/activate
```

- Install all dependencies

```
$ pip install -r requirements.txt
```

## Inserting your API_KEY

- Insert your own API key in the following path "\LlamaChat\ConfLlama\.env"
    
    Note: To get said KEY, you need to go to "https://console.groq.com/keys"

```
GROQ_API_KEY = "YOUR_API_KEY"   
```

## Usage

- Run the program in the virtual environment

```
$ python manage.py runserver
```

- Ask the bot your question

```
    query_engine = index.as_query_engine(llm=llm)

    result = query_engine.query(message)

    return str(result)

result = query("How much is the parking ticket in Costa Rica?")
print(result)
```

## Aditional info

- This program it's still in its early development stages, so bugs and wrong responses are expected.
- You must insert your API_KEY in the correct .env file, if not, the program might not run.