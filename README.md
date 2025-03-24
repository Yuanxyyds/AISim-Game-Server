### Installation:

Note to install the llama-cpp-python

```
CMAKE_ARGS="-DGGML_CUDA=ON" pip install --no-cache-dir llama-cpp-python --force-reinstall --no-binary llama-cpp-python
```

```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```