from datetime import datetime, timedelta


class MemoryExpiration:

    def __init__(self):

        self.rules = {

            "name": None,

            "profession": None,

            "favorite_language": None,

            "temporary": 1,

            "event": 7,

            "weather": 1,

            "travel": 30

        }

    def add_expiration(self, metadata):

        memory_type = metadata.get("type")

        days = self.rules.get(memory_type)

        if days is None:

            metadata["expires_at"] = None

        else:

            metadata["expires_at"] = (

                datetime.now() +

                timedelta(days=days)

            ).isoformat()

        return metadata

    def is_expired(self, metadata):

        expires = metadata.get("expires_at")

        if expires is None:

            return False

        return datetime.now() > datetime.fromisoformat(expires)