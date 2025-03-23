from llama_cpp import Llama
import threading
import time

# Global variables for models
llm = None
llm2 = None
model_lock = threading.Lock()


def load_models():
    global llm, llm2
    with model_lock:
        if llm is None and llm2 is None:
            print("🔄 Loading AI models into memory...")
            llm = Llama(
                model_path="/root/AISim-Game-server/models/DeepSeek-R1-Distill-Llama-8B-Q6_K.gguf",
                n_gpu_layers=32,
                n_ctx=4096,
                top_k=0,
                verbose=False,
            )

            llm2 = Llama(
                model_path="/root/AISim-Game-server/models/Llama-3.2-3B-Instruct2-Q8_0.gguf",
                n_gpu_layers=32,
                n_ctx=4096,
                top_k=0,
                verbose=False,
            )
            
        response = llm2.create_chat_completion(messages=[{"role": "user", "content" : "tell me a story"}], max_tokens=500, seed=int(time.time()))
        response_text = response["choices"][0]["message"]["content"].strip()

        print(f"🗣️ {response_text}\n")
        print("✅ AI models loaded successfully.")


def unload_models():
    global llm, llm2
    with model_lock:
        if llm or llm2:
            print("🛑 Unloading AI models from memory...")
            llm = None
            llm2 = None
            print("✅ AI models unloaded.")
