# Lang Learn - Language Tutor
Virtual language tutor that uses AI to help users pratice their language skills. The idea behind the tool is to emulate behavior between student and tutor, which is different from group oriented studying. Those who prefere one-on-one interactions can benifit a lot from this.

# Features
1. Currently suppored languages: Dutch
2. Take notes and store them locally with the help of sqlite
3. The application is hosted using Flask with browser Web UI so it is easily modifiable

# AI Behind the Tutor
The model is accessed with [Ollama Python API](https://github.com/ollama/ollama-python), and the model used for Dutch tutor is [GEITje](https://github.com/Rijgersberg/GEITje). The model is run locally, so all your converstions with the tutor are private. However, that means that Ollam and the desired model needs to be installed and run on a local machine or AI Server.
