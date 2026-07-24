from chatbot.code_agent import CodeAgent

agent = CodeAgent()

print("=" * 60)
print("Generate Code")
print("=" * 60)

print(

    agent.generate_code(

        "Build FastAPI CRUD API"

    )

)

print("=" * 60)

print("Language Detection")

print("=" * 60)

print(

    agent.detect_language(

"""
def add(a,b):

    return a+b

"""
)

)

print("=" * 60)

print("Explain Code")

print("=" * 60)

print(

    agent.explain_code(

"""
def add(a,b):

    return a+b

"""

)

)

print("=" * 60)

print("Debug Code")

print("=" * 60)

print(

    agent.debug_code(

"""
def add(a,b)

    return a+b

"""

)

)