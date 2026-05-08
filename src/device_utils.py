import torch


def get_optimal_device():
    """
    Utility function that detects available hardware for inference.
    Sets primary device to 'cuda' for NVIDIA GPUs, with an explicit fallback
    to 'cpu' so the app doesn't crash on standard laptops.
    """
    if torch.cuda.is_available():
        print("Hardware Detection: NVIDIA GPU detected. Using 'cuda'.")
        return "cuda"
    else:
        print("Hardware Detection: No GPU detected. Falling back to 'cpu'.")
        # NOTE FOR RECRUITERS/LOCAL TESTING:
        # If running on CPU, it is highly recommended to use 'GGUF' quantized versions
        # of the models (e.g., via Ollama or llama.cpp) for optimal performance.
        return "cpu"


def initialize_faiss_models():
    """
    Example initialization for SentenceTransformer and FAISS index
    using the dynamic device variable.
    """
    device = get_optimal_device()

    # Example pseudo-code for Library Swap:
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
    #
    # import faiss
    # index = faiss.IndexFlatL2(384)
    # if device == 'cuda':
    #     res = faiss.StandardGpuResources()
    #     index = faiss.index_cpu_to_gpu(res, 0, index)

    return device
