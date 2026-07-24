class MemoryCategories:

    CATEGORY_RULES = {

        "Personal": [

            "name",
            "age",
            "gender"
        ],

        "Education": [

            "university",
            "degree",
            "student",
            "college"
        ],

        "Career": [

            "job",
            "company",
            "profession",
            "internship"
        ],

        "Preference": [

            "favorite",
            "prefer",
            "like"
        ],

        "Skill": [

            "skill",
            "python",
            "react",
            "sql"
        ],

        "Project": [

            "project",
            "application",
            "system"
        ],

        "Goal": [

            "goal",
            "dream",
            "want"
        ],

        "Programming": [

            "python",
            "java",
            "javascript",
            "c++"
        ],

        "AI": [

            "machine learning",
            "deep learning",
            "llm",
            "genai"
        ],

        "Cybersecurity": [

            "security",
            "cyber",
            "penetration",
            "network"
        ],

        "Location": [

            "nepal",
            "kathmandu",
            "pokhara"
        ],

        "Hobby": [

            "music",
            "movie",
            "football"
        ]

    }

    def classify(self, memory_type, value):

        text = (memory_type + " " + value).lower()

        for category, keywords in self.CATEGORY_RULES.items():

            for keyword in keywords:

                if keyword in text:

                    return category

        return "Other"

    def detect_category_from_query(self, query):

        query = query.lower()

        for category, keywords in self.CATEGORY_RULES.items():

            for keyword in keywords:

                if keyword in query:

                    return category

        return None