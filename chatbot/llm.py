import re
import time
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


# =========================================================
# OLLAMA
# =========================================================

# IMPORTANT FOR DOCKER
#
# Ollama is running in another Docker container
# named "ollama".
#
# Therefore we connect to:
#
# http://ollama:11434
#
# NOT:
#
# http://localhost:11434
#

ollama_client = ollama.Client(
    host="http://ollama:11434"
)


# =========================================================
# INITIALIZE COMPONENTS
# =========================================================

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


# =========================================================
# RETRIEVER
# =========================================================

retriever = Retriever(
    embedder=embedder,
    vector_store=vector_store
)


# =========================================================
# KEYWORD SEARCH
# =========================================================

keyword_search = KeywordSearch()


# Get documents from Chroma
all_chunks = vector_store.get_all_chunks()

print("=" * 60)
print("DOCUMENT DATABASE")
print("=" * 60)

print("Total chunks:", len(all_chunks))


# IMPORTANT:
# BM25 crashes when there are zero documents.
#
# Therefore only build it if documents exist.

if all_chunks:

    keyword_search.build(
        all_chunks
    )

    print("BM25 index created.")

else:

    print(
        "No documents found."
    )

    print(
        "Skipping BM25 index."
    )


# =========================================================
# HYBRID SEARCH
# =========================================================

hybrid_search = HybridSearch(

    semantic_search=retriever,

    keyword_search=keyword_search

)


# =========================================================
# OTHER COMPONENTS
# =========================================================

query_expansion = QueryExpansion()

dynamic_topk = DynamicTopK()

duplicate_remover = DuplicateRemover()


# =========================================================
# CONFIGURATION
# =========================================================

MAX_TOKENS = 12000


# =========================================================
# LOAD PREVIOUS SESSION
# =========================================================

memory.load_history(

    session.load_session()

)


# =========================================================
# BUILD RAG CONTEXT
# =========================================================

def build_rag_context(user_message):

    print("=" * 60)
    print("BUILDING PDF CONTEXT")
    print("=" * 60)

    # -----------------------------------------
    # Query Expansion
    # -----------------------------------------

    expanded_query = query_expansion.expand(
        user_message
    )

    print("Expanded Query:")
    print(expanded_query)

    # -----------------------------------------
    # Dynamic Top K
    # -----------------------------------------

    top_k = dynamic_topk.get_top_k(
        expanded_query
    )

    print("Top K:", top_k)

    # -----------------------------------------
    # Hybrid Search
    # -----------------------------------------

    chunks = hybrid_search.search(

        expanded_query,

        top_k=top_k

    )

    # -----------------------------------------
    # Remove duplicates
    # -----------------------------------------

    chunks = duplicate_remover.remove_duplicates(
        chunks
    )

    print(
        "Retrieved chunks:",
        len(chunks)
    )

    # -----------------------------------------
    # No results
    # -----------------------------------------

    if not chunks:

        print(
            "No PDF chunks found."
        )

        return "", []

    # -----------------------------------------
    # Build context
    # -----------------------------------------

    context = retriever.build_context(
        chunks
    )

    return context, chunks


# =========================================================
# GET AI RESPONSE
# =========================================================

def get_ai_response(user_message):

    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    memory.add_user_message(
        user_message
    )

    print("=" * 60)
    print("QUESTION")
    print("=" * 60)

    print(user_message)


    # =====================================================
    # UPDATE USER MEMORY
    # =====================================================

    update_user_profile(
        user_message
    )

    update_long_term_memory(
        user_message
    )


    # =====================================================
    # LOAD USER PROFILE
    # =====================================================

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


    # =====================================================
    # ROUTE QUERY
    # =====================================================

    route = router.route(
        user_message
    )

    print("=" * 60)
    print("ROUTE SELECTED:", route)
    print("=" * 60)


    # =====================================================
    # EMPTY CONTEXT
    # =====================================================

    rag_context = ""

    retrieved_chunks = []

    web_context = ""


    # =====================================================
    # PDF ROUTE
    # =====================================================

    if route == "pdf":

        print(
            "Using PDF / Resume Search..."
        )

        rag_context, retrieved_chunks = (
            build_rag_context(
                user_message
            )
        )


        print("=" * 60)
        print(
            "Retrieved Chunks:",
            len(retrieved_chunks)
        )
        print("=" * 60)


        # Show retrieved documents
        for chunk in retrieved_chunks:

            print(
                "Document:",
                chunk.get(
                    "document",
                    "unknown"
                )
            )

            print(
                "Page:",
                chunk.get(
                    "page",
                    "unknown"
                )
            )

            print(
                chunk.get(
                    "text",
                    ""
                )[:300]
            )

            print("-" * 50)


    # =====================================================
    # RESEARCH ROUTE
    # =====================================================

    elif route == "research":

        print(
            "Using Research / Web..."
        )

        web_data = web_agent.retrieve(
            user_message
        )

        web_context = web_data.get(
            "context",
            ""
        )


    # =====================================================
    # MEMORY ROUTE
    # =====================================================

    elif route == "memory":

        print(
            "Using Memory..."
        )

        # For now, allow the LLM to answer
        # using stored user information.

        final_prompt = f"""
You are a helpful AI assistant.

Answer ONLY the current question.

Use the stored user information only when
the question is actually about the user.

USER INFORMATION:
{profile_text}

LONG TERM MEMORY:
{memory_text}

CURRENT QUESTION:
{user_message}

Answer clearly and directly.
"""


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

        return stream_ai_response(
            contents
        )


    # =====================================================
    # CODE ROUTE
    # =====================================================

    elif route == "code":

        print(
            "Using Code / General LLM..."
        )


    # =====================================================
    # GENERAL ROUTE
    # =====================================================

    else:

        print(
            "Using General LLM..."
        )


    # =====================================================
    # BUILD FINAL PROMPT
    # =====================================================

    if route == "pdf":

        # -------------------------------------------------
        # PDF QUESTION
        # -------------------------------------------------

        if rag_context:

            final_prompt = prompt_builder.build_prompt(

                context=rag_context,

                question=user_message,

                web_context=""

            )

        else:

            # IMPORTANT:
            #
            # Do NOT let the model invent resume information.
            #

            final_prompt = f"""
You are an AI assistant.

The user is asking about their uploaded resume.

However, no relevant information was found
in the uploaded resume.

Do NOT invent resume information.

Tell the user that the requested information
could not be found in the uploaded resume.

CURRENT QUESTION:
{user_message}

Answer:
"""


    elif route == "research":

        final_prompt = prompt_builder.build_prompt(

            context="",

            question=user_message,

            web_context=web_context

        )


    else:

        # -------------------------------------------------
        # GENERAL QUESTION
        # -------------------------------------------------

        # Do NOT include resume context.
        # Do NOT include long-term memory.
        # Do NOT include profile.
        #
        # This prevents:
        #
        # "What is Gen AI?"
        #
        # from becoming a resume answer.

        final_prompt = user_message


    # =====================================================
    # DEBUG
    # =====================================================

    print("=" * 60)
    print("FINAL PROMPT")
    print("=" * 60)

    print(final_prompt)

    print("=" * 60)


    # =====================================================
    # CREATE CONTENTS
    # =====================================================

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


    # =====================================================
    # SEND TO OLLAMA
    # =====================================================

    return stream_ai_response(
        contents
    )


# =========================================================
# STREAM AI RESPONSE
# =========================================================

def stream_ai_response(contents):

    prompt = contents[0]["parts"][0]["text"]


    print("=" * 60)
    print("SENDING PROMPT TO OLLAMA")
    print("=" * 60)

    print(prompt)

    print("=" * 60)


    full_response = ""


    try:

        # IMPORTANT:
        #
        # Use ollama_client instead of ollama.chat()
        #
        # because Ollama is running in another
        # Docker container.

        response = ollama_client.chat(

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

        error_message = (
            f"\nOllama Error: {str(e)}"
        )

        print(
            error_message
        )

        yield error_message

        return


    # =====================================================
    # SAVE AI RESPONSE
    # =====================================================

    memory.add_ai_message(
        full_response
    )


    # =====================================================
    # TOKEN COUNT
    # =====================================================

    total_tokens = (
        token_counter.count_history(
            memory.get_history()
        )
    )

    print(
        "Conversation Tokens:",
        total_tokens
    )


    # =====================================================
    # PRUNE MEMORY
    # =====================================================

    if total_tokens > MAX_TOKENS:

        print(
            "Pruning Conversation History..."
        )

        memory.prune_history(
            keep_last=10
        )


    # =====================================================
    # SAVE SESSION
    # =====================================================

    session.save_session(

        memory.save_history()

    )

    print(
        "Session Saved Successfully."
    )


# =========================================================
# UPDATE USER PROFILE
# =========================================================

def update_user_profile(
    user_message
):

    profile_data = (
        profile.load_profile()
    )


    patterns = {

        "name":
        r"my name is (.+)",

        "favorite_language":
        r"i like (.+)",

        "occupation":
        r"i am (.+)",

        "goal":
        r"my goal is (.+)"

    }


    for key, pattern in patterns.items():

        match = re.search(

            pattern,

            user_message,

            re.IGNORECASE

        )


        if match:

            profile_data[key] = (
                match.group(1).strip()
            )


    profile.save_profile(
        profile_data
    )


# =========================================================
# UPDATE LONG TERM MEMORY
# =========================================================

def update_long_term_memory(
    user_message
):

    memory_data = (
        long_memory.load()
    )


    patterns = {

        "name":
        r"my name is (.+)",

        "occupation":
        r"i am (.+)",

        "goal":
        r"my goal is (.+)",

        "favorite_language":
        r"i like (.+)",

        "skill":
        r"i know (.+)"

    }


    updated = False


    for key, pattern in patterns.items():

        match = re.search(

            pattern,

            user_message,

            re.IGNORECASE

        )


        if match:

            memory_data[key] = (
                match.group(1).strip()
            )

            updated = True


    if updated:

        long_memory.save(
            memory_data
        )


# =========================================================
# TOKEN USAGE
# =========================================================

def get_token_usage():

    return token_counter.count_history(

        memory.get_history()

    )


# =========================================================
# CLEAR CHAT
# =========================================================

def clear_chat():

    memory.load_history([])

    session.save_session([])

    print(
        "Conversation Cleared."
    )


# =========================================================
# DEBUG PIPELINE
# =========================================================

def debug_pipeline():

    print("=" * 60)

    print("CONVERSATION LENGTH")

    print(
        len(
            memory.get_history()
        )
    )

    print("=" * 60)

    print("PROFILE")

    print(
        profile.load_profile()
    )

    print("=" * 60)

    print("LONG TERM MEMORY")

    print(
        long_memory.load()
    )

    print("=" * 60)

    print("CHROMA DOCUMENTS")

    chunks = (
        vector_store.get_all_chunks()
    )

    print(
        "Total chunks:",
        len(chunks)
    )

    for chunk in chunks[:5]:

        print(
            chunk.get(
                "document",
                "unknown"
            )
        )

        print(
            chunk.get(
                "page",
                "unknown"
            )
        )

    print("=" * 60)
    
