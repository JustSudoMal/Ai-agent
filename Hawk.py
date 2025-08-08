import tkinter as tk
from tkinter import scrolledtext, font, filedialog
from PIL import Image, ImageTk
from llama_cpp import Llama

class SmartAI:
    def __init__(self, model_path, persona="", max_tokens=256, n_threads=4):
        try:
            self.llm = Llama(model_path=model_path, n_ctx=2048, n_threads=n_threads)
            print(f"[+] Model loaded: {model_path}")
        except Exception as e:
            print(f"[!] Failed to load model: {e}")
            raise

        self.persona = persona
        self.max_tokens = max_tokens
        self.history = ""

    def chat(self, user_input):
        prompt = f"""### SYSTEM:
You are {self.persona}

{self.history}
### USER:
{user_input}

### ASSISTANT:
"""
        try:
            response = self.llm(prompt, max_tokens=self.max_tokens, stop=["###"])
            reply = response["choices"][0]["text"].strip()
            self.history += f"\n### USER:\n{user_input}\n### ASSISTANT:\n{reply}"
            return reply
        except Exception as e:
            print(f"[!] Error generating response: {e}")
            return "[Error generating response]"

class ChatWindow:
    def __init__(self, ai):
        self.ai = ai
        self.root = tk.Tk()
        self.root.title("Hawk AI Chat")
        self.root.geometry("700x600")

        self.font_chat = font.Font(family="Segoe UI", size=12)
        self.font_input = font.Font(family="Segoe UI", size=14)

        # Canvas for background + widgets
        self.canvas = tk.Canvas(self.root, width=700, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Ask for background image
        bg_path = filedialog.askopenfilename(
            title="Select Background Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        self.bg_image = None
        if bg_path:
            img = Image.open(bg_path)
            img = img.resize((700, 600), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        else:
            # fallback bg color
            self.canvas.configure(bg="#1e1e2f")

        # Create chat_area
        self.chat_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state='disabled', height=25,
            bg="#2e2e44", fg="#e0e0e0", font=self.font_chat,
            relief=tk.FLAT, padx=10, pady=10
        )
        self.chat_window = self.canvas.create_window(15, 15, window=self.chat_area, anchor="nw", width=670, height=400)

        # Input frame
        self.input_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.input_window = self.canvas.create_window(15, 420, window=self.input_frame, anchor="nw", width=670, height=50)

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            self.input_frame, textvariable=self.input_var,
            bg="#3a3a55", fg="#ffffff", insertbackground="#ffffff",
            font=self.font_input, relief=tk.FLAT
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.input_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.input_frame, text="Send",
            bg="#5656a6", fg="#ffffff", font=self.font_input,
            relief=tk.FLAT, activebackground="#7070c0",
            command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=(10, 0), ipady=8, ipadx=15)

        self.input_entry.focus_set()

    def send_message(self, event=None):
        user_msg = self.input_var.get().strip()
        if not user_msg:
            return
        print(f"[User] {user_msg}")  # debug print
        self.input_var.set("")

        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, "You: ", "user_tag")
        self.chat_area.insert(tk.END, f"{user_msg}\n", "user_msg")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

        ai_response = self.ai.chat(user_msg)
        print(f"[Hawk] {ai_response}")  # debug print

        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, "Hawk: ", "ai_tag")
        self.chat_area.insert(tk.END, f"{ai_response}\n\n", "ai_msg")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def run(self):
        self.chat_area.tag_config("user_tag", foreground="#6ec1ff", font=("Segoe UI", 12, "bold"))
        self.chat_area.tag_config("ai_tag", foreground="#ff9e64", font=("Segoe UI", 12, "bold"))
        self.chat_area.tag_config("user_msg", foreground="#c0d9ff")
        self.chat_area.tag_config("ai_msg", foreground="#ffd9b3")

        self.root.mainloop()

if __name__ == "__main__":
    model_path = "/home/mal/Downloads/capybarahermes-2.5-mistral-7b.Q2_K.gguf"  # Adjust as needed
    persona = "Hawk, a clever comedian who is really good at jokes"

    try:
        ai = SmartAI(model_path=model_path, persona=persona, n_threads=8)
    except Exception as e:
        print(f"Failed to initialize AI: {e}")
        exit(1)

    window = ChatWindow(ai)
    window.run()
