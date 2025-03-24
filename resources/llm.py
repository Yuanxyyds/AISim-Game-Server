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

# Global model references
reasoning = None
chat = None
summarizer = None
model_lock = threading.Lock()


def _load_llama_model(target_name: str):
    """
    Loads a quantized LLaMA model using HuggingFace Transformers and BitsAndBytes.
    Stores the pipeline in the specified global variable.
    """
    global chat, summarizer

    with model_lock:
        target = {"chat": chat, "summarizer": summarizer}.get(target_name)
        if target is not None:
            print(f"ℹ️ LLaMA ({target_name}) model is already loaded.")
            return

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

            pipeline_model = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                return_full_text=False,
            )

            if target_name == "chat":
                chat = pipeline_model
            elif target_name == "summarizer":
                summarizer = pipeline_model

            print(f"✅ LLaMA ({target_name}) model loaded successfully.")
        except Exception as e:
            print(f"❌ Failed to load LLaMA ({target_name}): {str(e)}")


def _call_llama(model: any, messages: list, max_tokens: int = 1000) -> str:
    outputs = model(messages, max_new_tokens=max_tokens, pad_token_id=50256)
    return outputs[0]["generated_text"].strip()


def _load_deepseek_model():
    """
    Loads the DeepSeek quantized model using llama-cpp.
    """
    global reasoning
    with model_lock:
        if reasoning is not None:
            print("ℹ️ DeepSeek model is already loaded.")
            return

        print("🔄 Loading DeepSeek model...")
        reasoning = Llama(
            model_path="/root/AISim-Game-server/models/DeepSeek-R1-Distill-Llama-8B-Q6_K.gguf",
            n_gpu_layers=32,
            n_ctx=4096,
            top_k=0,
            verbose=False,
        )
        print("✅ DeepSeek model loaded successfully.")


def _call_deepseek(model: any, messages: list, max_tokens: int = 1000) -> str:
    prompt = ""
    for m in messages:
        if m["role"] == "system":
            prompt += f"<|system|>\n{m['content']}\n"
        elif m["role"] == "user":
            prompt += f"<|user|>\n{m['content']}\n"
        elif m["role"] == "assistant":
            prompt += f"<|assistant|>\n{m['content']}\n"
    prompt += "<|assistant|>\n"

    response = model(prompt, max_tokens=max_tokens)
    return response["choices"][0]["text"].strip()


# Public API
def call_chat(messages: list, max_tokens: int = 1000) -> str:
    if chat is None:
        raise RuntimeError("LLaMA chat model not loaded. Call init_models() first.")
    return _call_llama(chat, messages, max_tokens)


def call_summarizer(messages: list, max_tokens: int = 1000) -> str:
    if summarizer is None:
        raise RuntimeError("LLaMA summarizer model not loaded. Call init_models() first.")
    return _call_llama(summarizer, messages, max_tokens)


def call_reasoning(messages: list, max_tokens: int = 1000) -> str:
    if reasoning is None:
        raise RuntimeError("DeepSeek model not loaded. Call init_models() first.")
    return _call_deepseek(reasoning, messages, max_tokens)


def unload_all_models():
    """
    Unloads all models and resets the references.
    """
    global reasoning, chat, summarizer
    with model_lock:
        print("🛑 Unloading all models...")
        reasoning = None
        chat = None
        summarizer = None
        print("✅ All models unloaded.")


def init_models(load_summarizer: bool = True):
    """
    Initializes the LLaMA chat model and optionally the summarizer model.
    Also loads the DeepSeek model for reasoning tasks.
    """
    _load_llama_model("chat")
    if load_summarizer:
        _load_llama_model("summarizer")
    _load_deepseek_model()
