import os
from openai import OpenAI
from gptcache.processor.pre import get_prompt
from gptcache import cache
from gptcache.adapter.api import put as cache_put, get as cache_get, init_similar_cache
from gptcache.embedding import Onnx
from gptcache.manager import CacheBase, VectorBase, get_data_manager
from datetime import datetime
from gptcache.manager import CacheBase, manager_factory

onnx = Onnx()
# postgres_url = os.environ.get("DATABASE_URL")

# if postgres_url and postgres_url.startswith("postgres://"):
#     postgres_url = postgres_url.replace("postgres://", "postgresql://", 1)

# print(postgres_url)

# cache_base = CacheBase("postgresql", sql_url=postgres_url)

cache_base = CacheBase('redis',
    redis_host="localhost",
    redis_port=6381,
    global_key_prefix="gptcache",
)

# # vector_base = RedisVectorStore()
vector_base = VectorBase("faiss", dimension=onnx.dimension)
# # vector_base = VectorBase("redis", host="127.0.0.1", port="6379", dimension=8)

data_manager = get_data_manager(cache_base, vector_base)


# data_manager = manager_factory("redis,faiss", data_dir="./workspace",
#     scalar_params={
#         "redis_host": "localhost",
#         "redis_port": 6381,
#         "global_key_prefix": "gptcache",
#     },
#     vector_params={"dimension": 128},
# )

cache.init(pre_embedding_func=get_prompt, data_manager=data_manager)
init_similar_cache()


def get_response_from_cache(query):
    return cache_get(query)


def set_question_and_response_in_cache(query, response):
    return cache_put(query, response)

