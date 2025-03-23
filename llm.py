from llama_cpp import Llama
import threading
import time
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
    BitsAndBytesConfig,
)

deepseek = None
llama = None
model_lock = threading.Lock()


def load_llama_model():
    """
    Loads the 4-bit quantized LLaMA model using HuggingFace Transformers and BitsAndBytes.
    Stores the pipeline in the global `llama` variable.
    """
    global llama
    if llama is None:
        with model_lock:
            try:
                bnb_config = BitsAndBytesConfig(
                    load_in_8bit=True,
                    llm_int8_threshold=6.0,
                )

                tokenizer = AutoTokenizer.from_pretrained(
                    "meta-llama/Llama-3.2-3B-Instruct"
                )
                model = AutoModelForCausalLM.from_pretrained(
                    "meta-llama/Llama-3.2-3B-Instruct",
                    quantization_config=bnb_config,
                    device_map="auto",
                    trust_remote_code=True,
                )

                llama = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    return_full_text=False,
                )

                print("✅ Quantized LLaMA model loaded successfully.")
                return True
            except Exception as e:
                print(f"❌ Failed to load LLaMA model: {str(e)}")
                return False
    else:
        print("ℹ️ LLaMA model is already loaded.")
    return False


def unload_llama_model():
    """
    Unloads the LLaMA model and clears GPU memory cache if applicable.
    """
    global llama
    with model_lock:
        llama = None
        print("🗑️ LLaMA model unloaded.")

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("🧹 GPU memory cache cleared.")


def call_llama(messages: list, max_tokens: int = 1000) -> str:
    """
    Sends a prompt to the HuggingFace-based LLaMA pipeline and returns the generated response.
    """
    global llama
    if llama is None:
        raise RuntimeError("LLaMA model not loaded. Call load_llama_model() first.")

    outputs = llama(messages, max_new_tokens=max_tokens, pad_token_id=50256)
    return outputs[0]["generated_text"].strip()


def load_deepseek_model():
    """
    Loads the DeepSeek quantized model using llama-cpp and stores it in `deepseek`.
    """
    global deepseek
    with model_lock:
        if deepseek is None:
            print("🔄 Loading DeepSeek model...")
            deepseek = Llama(
                model_path="/root/AISim-Game-server/models/DeepSeek-R1-Distill-Llama-8B-Q6_K.gguf",
                n_gpu_layers=32,
                n_ctx=4096,
                top_k=0,
                verbose=False,
            )
            print("✅ DeepSeek model loaded successfully.")
        else:
            print("ℹ️ DeepSeek model is already loaded.")


def unload_deepseek_model():
    """
    Unloads the DeepSeek model and resets the reference.
    """
    global deepseek
    with model_lock:
        if deepseek:
            print("🛑 Unloading DeepSeek model...")
            deepseek = None
            print("✅ DeepSeek model unloaded.")


def call_deepseek(messages: list, max_tokens: int = 1000) -> str:
    """
    Sends a prompt to the llama-cpp-based DeepSeek model and returns the generated response.
    """
    global deepseek
    if deepseek is None:
        raise RuntimeError(
            "DeepSeek model not loaded. Call load_deepseek_model() first."
        )

    # Convert chat messages to a formatted prompt
    prompt = ""
    for m in messages:
        if m["role"] == "system":
            prompt += f"<|system|>\n{m['content']}\n"
        elif m["role"] == "user":
            prompt += f"<|user|>\n{m['content']}\n"
        elif m["role"] == "assistant":
            prompt += f"<|assistant|>\n{m['content']}\n"
    prompt += "<|assistant|>\n"

    response = deepseek(prompt, max_tokens=max_tokens)
    return response["choices"][0]["text"].strip()
