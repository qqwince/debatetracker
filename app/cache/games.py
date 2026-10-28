
from pydantic import TypeAdapter
from redis import Redis

from app.config import settings
from app.schemas.games import GameResponse


def form_cache_key(current_user, game_id):
    return f"game:{current_user.id}:{game_id}"

async def set_game_cache(redis: Redis, current_user, game_id, cached_info):
    cache_key = form_cache_key(current_user, game_id)
    cache_ttl_game_seconds = settings.CACHE_TTL_GAME_SECONDS

    adapter = TypeAdapter(GameResponse)
    game_json = adapter.dump_json(cached_info).decode("utf-8")

    await redis.set(cache_key, game_json, ex=cache_ttl_game_seconds)

async def delete_game_cache(redis: Redis, current_user, game_id):
    cache_key = form_cache_key(current_user, game_id)
    await redis.delete(cache_key)
    
async def get_game_cache(redis: Redis, current_user, game_id):
    cache_key = form_cache_key(current_user, game_id)
    cached_data = await redis.get(cache_key)
    return cached_data