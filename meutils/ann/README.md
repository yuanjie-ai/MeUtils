# 集成Faiss/Milvus


```
from docarray import Document, DocumentArray
import numpy as np

n_dim = 3
metric = 'Euclidean'

# initialize a DocumentArray with ANNLiter Document Store
da = DocumentArray(
    storage='annlite',
    config={'n_dim': n_dim, 'columns': [('price', 'float'), ('cat', 'str')], 'metric': metric},
)
da
# add Documents to the DocumentArray
with da:
    da.extend(
        [
            Document(
                id=f'r{i}',
                embedding=i * np.ones(n_dim),
                tags={'price': i, 'cat': f'cat_{i}'}
            )
            for i in range(100000)
        ]
    )
da
# perform vector search
np_query = np.ones(n_dim) * 8
da.find(np_query, filter={"cat": {'$in': ['cat_1', 'cat_5']}})[:, ('id', 'tags', 'scores__euclidean__value')]
```