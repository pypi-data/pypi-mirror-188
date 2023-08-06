import numpy as np
import torch
import autumn8
from sentence_transformers import SentenceTransformer, util

query = "How many people live in London?"
docs = [
    "Around 9 Million people live in London",
    "London is known for its financial district",
]

# Load the model
model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")


# Encode query and documents
query_emb = model.encode(query)
doc_emb = model.encode(docs)

test = torch.tensor([[1, 2, 3]])
test2 = torch.tensor([[1, 1, 1]])
model({"input_ids": test, "attention_mask": test2})

# Compute dot score between query and all document embeddings
scores = util.dot_score(query_emb, doc_emb)[0].cpu().tolist()

# Combine docs & scores
doc_score_pairs = list(zip(docs, scores))

# Sort by decreasing score
doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

# Output passages & scores
for doc, score in doc_score_pairs:
    print(score, doc)

autumn8.lib.attach_model(
    model,
    query,
    interns=[],
    externs=[
        "torch",
        "torchvision",
        "sentence_transformers",
        "jinja",
        "huggingface_hub",
        "yaml",
        "transformers.models.mpnet.modeling_mpnet",
        "tensorflow",
        "transformers.activations",
        "transformers.models.mpnet.configuration_mpnet",
        "transformers.models.mpnet.tokenization_mpnet_fast",
        "tokenizers",
        "tokenizers.models",
        "requests",
        "numpy",
        "transformers",
        "tqdm.autonotebook",
        "sys",
        "packaging.version",
        "requests.exceptions",
        "filelock",
        "tqdm",
        "tqdm.auto",
        "_io",
        "requests.auth",
        "tensorboard.summary._tf.summary",
    ],
)
