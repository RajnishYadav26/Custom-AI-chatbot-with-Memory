import redis
import json


class RedisClient:

    def __init__(self):

        self.client = redis.Redis(
            host="redis",
            port=6379,
            decode_responses=True
        )

    def ping(self):

        return self.client.ping()

    def set(self, key, value, expire=None):

        if isinstance(value, (dict, list)):

            value = json.dumps(value)

        self.client.set(
            key,
            value,
            ex=expire
        )

    def get(self, key):

        value = self.client.get(key)

        if value is None:
            return None

        try:

            return json.loads(value)

        except (json.JSONDecodeError, TypeError):

            return value

    def delete(self, key):

        self.client.delete(key)

    def exists(self, key):

        return self.client.exists(key)