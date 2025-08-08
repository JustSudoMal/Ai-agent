

A sleek, customizable desktop chat interface for local LLMs using `llama-cpp-python`, built with Python’s `tkinter`. Includes background image support, styled chat history, and persona customization.




-  Local LLM chat powered by [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
-  Custom background image support (any `.png`, `.jpg`, `.gif`, etc.)
-  Clean, styled chat interface with color-coded messages
-  Persona injection (e.g. “Hawk, a clever comedian…”)
-  Threaded model inference with adjustable token limits



## 📦 Requirements

- Python 3.8+
- [llama-cpp-python](https://pypi.org/project/llama-cpp-python/)
- Pillow (`PIL`)
- tkinter (pre-installed with most Python installations)

Install all dependencies:

```bash
pip install -r requirements.txt
📂 Model Setup

    Download a compatible .gguf model (e.g., Capybara Hermes, Mistral, etc.)

    Save the model to a path like:

    /home/mal/Downloads/capybarahermes-2.5-mistral-7b.Q2_K.gguf

    Update the model_path in __main__ at the bottom of the Python script to match.

🖼️ Background Image

On first launch, a file picker lets you select any image for the chat window background. Optional but makes the UI ✨shine✨.
🧑‍💻 Usage

python your_script.py

    Type into the input field and hit Enter or click Send

    All chat history is styled and scrollable

    AI persona is injected via the prompt system section

🛠️ Customization

    Change the AI’s persona in the __main__ section.

    Edit window dimensions, fonts, or colors in the ChatWindow class.

    Add logging or output saving if desired.

🤓 Example Persona

persona = "Hawk, a clever comedian who is really good at jokes"

Make it wild, informative, serious, whatever suits your use-case.
