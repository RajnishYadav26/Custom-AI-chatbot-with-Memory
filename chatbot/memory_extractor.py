import re


class MemoryExtractor:

    def extract(self, text):

        memories = []

        text = text.strip()

        # ----------------------------
        # Name
        # ----------------------------

        m = re.search(
            r"my name is (.+)",
            text,
            re.IGNORECASE
        )

        if m:

            memories.append({

                "type": "name",

                "value": m.group(1).strip(),

                "importance": 1.0

            })

        # ----------------------------
        # Favourite Language
        # ----------------------------

        m = re.search(

            r"my favorite language is (.+)",

            text,

            re.IGNORECASE

        )

        if m:

            memories.append({

                "type": "favorite_language",

                "value": m.group(1).strip(),

                "importance": 0.95

            })

        # ----------------------------
        # Profession
        # ----------------------------

        m = re.search(

            r"i am (?:a|an) (.+)",

            text,

            re.IGNORECASE

        )

        if m:

            memories.append({

                "type": "profession",

                "value": m.group(1).strip(),

                "importance": 0.90

            })

        return memories