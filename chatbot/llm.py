import re
import ollama

from chatbot.memory import MemoryManager
from chatbot.session import SessionManager
from chatbot.user_profile import UserProfile
from chatbot.long_term_memory import LongTermMemory

from chatbot.embeddings import EmbeddingModel
from chatbot.chroma_store import ChromaStore
from chatbot.retriever import Retriever

from chatbot.keyword_search import KeywordSearch
from chatbot.hybrid_search import HybridSearch

from chatbot.query_expansion import QueryExpansion
from chatbot.dynamic_topk import DynamicTopK
from chatbot.duplicate_remover import DuplicateRemover

from chatbot.prompt_builder import PromptBuilder

from chatbot.web_trigger import WebTrigger
from chatbot.web_agent import WebAgent

from chatbot.tokenizer import TokenCounter
from chatbot.router_agent import RouterAgent

router = RouterAgent()

embedder = EmbeddingModel()

vector_store = ChromaStore()

memory = MemoryManager()
session = SessionManager()
profile = UserProfile()
long_memory = LongTermMemory()

token_counter = TokenCounter()

prompt_builder = PromptBuilder()

web_trigger = WebTrigger()
web_agent = WebAgent()
router = RouterAgent()

retriever = Retriever(
    embedder=embedder,
    vector_store=vector_store
)

keyword_search = KeywordSearch()

keyword_search.build(
    vector_store.get_all_chunks()
)

hybrid_search = HybridSearch(
    semantic_search=retriever,
    keyword_search=keyword_search
)

query_expansion = QueryExpansion()

dynamic_topk = DynamicTopK()

duplicate_remover = DuplicateRemover()

MAX_TOKENS = 12000

memory.load_history(
    session.load_session()
)


def build_rag_context(user_message):

    expanded_query = query_expansion.expand(user_message)

    top_k = dynamic_topk.get_top_k(expanded_query)

    chunks = hybrid_search.search(
        expanded_query,
        top_k=top_k
    )

    chunks = duplicate_remover.remove_duplicates(
        chunks
    )

    if not chunks:
        return "", []

    context = retriever.build_context(
        chunks
    )

    return context, chunks

def get_ai_response(user_message):

    # -----------------------------------
    # Save User Message
    # -----------------------------------

    memory.add_user_message(user_message)

    print("Conversation History:")
    print(memory.get_history())

    update_user_profile(user_message)


    update_long_term_memory(user_message)

        # -----------------------------------
    # Load Stored Memory
    # -----------------------------------

    profile_data = profile.load_profile()

    long_memory_data = long_memory.load()

    profile_text = ""

    if profile_data:

        profile_text = (
            "USER PROFILE\n"
            "---------------------\n"
            f"{profile_data}\n\n"
        )

    memory_text = ""

    if long_memory_data:

        memory_text = (
            "LONG TERM MEMORY\n"
            "---------------------\n"
            f"{long_memory_data}\n\n"
        )

    # -----------------------------------
    # Retrieve PDF Context
    # -----------------------------------

            # -----------------------------------
    # Route the Query
    # -----------------------------------

    route = router.route(user_message)

    print("=" * 60)
    print(f"Route Selected: {route}")
    print("=" * 60)

    rag_context = ""
    retrieved_chunks = []
    web_context = ""

    # -----------------------------------
    # Execute Selected Route
    # -----------------------------------

    if route == "pdf":

        rag_context, retrieved_chunks = build_rag_context(
            user_message
        )

        print(f"Retrieved Chunks: {len(retrieved_chunks)}")

    elif route == "research":

        print("Using Research/Web Agent...")

        web_data = web_agent.retrieve(
            user_message
        )

        web_context = web_data["context"]

    elif route == "memory":

        print("Memory Agent Selected")

        # Future implementation
        pass

    elif route == "code":

        print("Code Agent Selected")

        # Future implementation
        pass

    else:

        print("General LLM Response")

    # -----------------------------------
    # Build Prompt
    # -----------------------------------

    prompt = prompt_builder.build_prompt(

        context=rag_context,

        question=user_message,

        web_context=web_context

    )

    # -----------------------------------
    # Final Prompt
    # -----------------------------------

    final_prompt = (

        profile_text +

        memory_text +

        prompt

    )

    print("=" * 60)
    print("FINAL PROMPT")
    print(final_prompt)
    print("=" * 60)

    contents = [

        {

            "role": "user",

            "parts": [

                {

                    "text": final_prompt

                }

            ]

        }

    ]

    return stream_ai_response(contents)

def stream_ai_response(contents):

    # ------------------------------------
    # Extract Prompt
    # ------------------------------------

    prompt = contents[0]["parts"][0]["text"]

    print("=" * 60)
    print("Sending Prompt to Ollama...")
    print("=" * 60)

    print("=" * 80)
    print("FINAL PROMPT SENT TO LLM")
    print(prompt)
    print("=" * 80)

    full_response = ""

    try:

        response = ollama.chat(

            model="llama3.2",

            messages=[

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            stream=True

        )

        for chunk in response:

            text = chunk["message"]["content"]

            full_response += text

            yield text

    except Exception as e:

        error_message = f"\nOllama Error:\n{str(e)}"

        print(error_message)

        yield error_message

        return

    # ------------------------------------
    # Save AI Response
    # ------------------------------------

    memory.add_ai_message(full_response)

    # ------------------------------------
    # Token Count
    # ------------------------------------

    total_tokens = token_counter.count_history(

        memory.get_history()

    )

    print(f"Conversation Tokens: {total_tokens}")

    # ------------------------------------
    # Memory Pruning
    # ------------------------------------

    if total_tokens > MAX_TOKENS:

        print("Pruning Conversation History...")

        memory.prune_history(

            keep_last=10

        )

    # ------------------------------------
    # Save Session
    # ------------------------------------

    session.save_session(

        memory.save_history()

    )

    print("Session Saved Successfully.")

def update_user_profile(user_message):

    profile_data = profile.load_profile()

    patterns = {

        "name": r"my name is (.+)",

        "favorite_language": r"i like (.+)",

        "occupation": r"i am (.+)",

        "goal": r"my goal is (.+)"

    }

    for key, pattern in patterns.items():

        match = re.search(

            pattern,

            user_message,

            re.IGNORECASE

        )

        if match:

            profile_data[key] = match.group(1).strip()

    profile.save_profile(profile_data)


def update_long_term_memory(user_message):

    memory_data = long_memory.load()

    patterns = {

        "name": r"my name is (.+)",

        "occupation": r"i am (.+)",

        "goal": r"my goal is (.+)",

        "favorite_language": r"i like (.+)",

        "skill": r"i know (.+)"

    }

    updated = False

    for key, pattern in patterns.items():

        match = re.search(

            pattern,

            user_message,

            re.IGNORECASE

        )

        if match:

            memory_data[key] = match.group(1).strip()

            updated = True

    if updated:

        long_memory.save(memory_data)

def get_token_usage():

    return token_counter.count_history(

        memory.get_history()

    )

def clear_chat():

    memory.load_history([])

    session.save_session([])

    print("Conversation Cleared.")


def debug_pipeline():

    print("=" * 60)

    print("Conversation Length")

    print(len(memory.get_history()))

    print("=" * 60)

    print("Profile")

    print(profile.load_profile())

    print("=" * 60)

    print("Long-Term Memory")

    print(long_memory.load())

    print("=" * 60)   
    



