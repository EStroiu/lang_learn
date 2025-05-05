# NT2 Web Tutor

Virtual language tutor that uses AI to help users practice their language skills. The idea behind the tool is to emulate a one-on-one conversation between student and tutor, which differs from group‑oriented studying. Those who prefer individual interaction can benefit greatly from this approach.

## Features

1. Currently supported languages: Dutch
2. Take notes and store them locally using SQLite
3. Web application hosted with Flask for easy customization
4. Rich text editing for notes powered by Quill.js

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.8 or newer
- Node.js and npm
- GNU Make

## Setup

From the project root, run:

```bash
make          # Installs both web dependencies and Python environment
```

This invokes the `Makefile` to:

1. Install web dependencies (`npm install`)
2. Create and activate a Python virtual environment (`.venv`)
3. Upgrade pip and install Python packages from `requirements.txt`

## Running the Application

After setup, start the web app:

```bash
# Activate virtual environment
source .venv/bin/activate   # on Windows use `.venv\\Scripts\\activate`

# Run the Flask app directly
python app.py           # serves API on http://127.0.0.1:5000 by default
```


## Configuration

The AI model is accessed through the Ollama Python API and can be swapped out or configured by pointing to your locally running model instance. By default, the application looks for the Ollama endpoint at `http://localhost:11434`.

To change the model or its settings, update the relevant variables in the configuration file or environment variables before launching the application.

## Data Storage

All user notes and session data are stored in a local SQLite database file (`notes.db` by default). You can find this file in the project root. To reset your data, delete or rename this file before starting the application.

## Cleaning Up

To remove installed dependencies and start fresh:

```bash
make clean   # removes virtualenv and node_modules, package-lock.json
```

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open a pull request or submit an issue on the repository.

---

*Happy language learning!*

