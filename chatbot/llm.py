



 

import re

from chatbot.retriever import Retriever

from chatbot.prompt_builder import PromptBuilder

from chatbot.keyword_search import KeywordSearch

from chatbot.hybrid_search import HybridSearch

from chatbot.web_trigger import WebTrigger
from chatbot.web_agent import WebAgent



from dotenv import load_dotenv

from google import genai



from chatbot.memory import MemoryManager

from chatbot.session import SessionManager

from chatbot.prompts import SYSTEM_PROMPT

from chatbot.tokenizer import TokenCounter

from chatbot.user_profile import UserProfile

from chatbot.embeddings import EmbeddingModel

from chatbot.chroma_store import ChromaStore

from chatbot.dynamic_topk import DynamicTopK

from chatbot.query_expansion import QueryExpansion

from chatbot.duplicate_remover import DuplicateRemover

from chatbot.long_term_memory import LongTermMemory
import os



print("=" * 60)

print("LOADING MY LLM.PY")

print(__file__)

print("=" * 60)





# ----------------------------------------------------

# Load Environment Variables

# ----------------------------------------------------



load_dotenv()



# ----------------------------------------------------

# Gemini Client

# ----------------------------------------------------



client = genai.Client(

    api_key=os.getenv("GEMINI_API_KEY")

)



# ----------------------------------------------------

# Managers

# ----------------------------------------------------

embedder = EmbeddingModel()



vector_store = ChromaStore()



memory = MemoryManager()

session = SessionManager()

token_counter = TokenCounter()

profile = UserProfile()

long_memory = LongTermMemory()

web_trigger = WebTrigger()
web_agent = WebAgent()



prompt_builder = PromptBuilder()



# Semantic Search

retriever = Retriever(

    embedder=embedder,

    vector_store=vector_store

)



# BM25 Search

keyword_search = KeywordSearch()



# Build BM25 Index

keyword_search.build(

    vector_store.get_all_chunks()

)



# Hybrid Search

hybrid_search = HybridSearch(

    semantic_search=retriever,

    keyword_search=keyword_search



)

dynamic_topk = DynamicTopK()

query_expansion = QueryExpansion()

duplicate_remover = DuplicateRemover()



# ----------------------------------------------------

# Configuration

# ----------------------------------------------------



MAX_TOKENS = 12000



# ----------------------------------------------------

# Load Previous Session

# ----------------------------------------------------



memory.load_history(

    session.load_session()

)



# ----------------------------------------------------

# Generate AI Response

# ----------------------------------------------------



def get_ai_response(user_message):

    # Save user message

    memory.add_user_message(user_message)



    # Update user profile

    update_user_profile(user_message)

    update_long_term_memory(user_message)



    profile_data = profile.load_profile()

    memory_data = long_memory.load()



    profile_text = ""



    if profile_data:

        profile_text = (

            "Known User Information:\n"

            f"{profile_data}\n\n"

        )



    memory_text = ""



    if memory_data:



        memory_text = (

        "Long Term Memory:\n"

        f"{memory_data}\n\n"

    )



    expanded_query = query_expansion.expand(user_message)



    print("Expanded Query:")

    print(expanded_query)



    top_k = dynamic_topk.get_top_k(expanded_query)



    retrieved_chunks = hybrid_search.search(

        expanded_query,

        top_k=top_k

    )



    retrieved_chunks = duplicate_remover.remove_duplicates(

        retrieved_chunks

    )



    print("\nAfter Duplicate Removal")

    print(f"Chunks: {len(retrieved_chunks)}")



    print("\n===== RETRIEVED CHUNKS =====")

    print(retrieved_chunks)

    print("===========================")



    if not retrieved_chunks:



        rag_prompt = user_message



    else:



        context = retriever.build_context(

            retrieved_chunks

        )



        rag_prompt = prompt_builder.build_prompt(

            context,

            user_message

        )

# -----------------------------
# Build RAG Context
# -----------------------------

    rag_context = ""

    if retrieved_chunks:

        rag_context = retriever.build_context(
        retrieved_chunks
    )

# -----------------------------
# Decide if Web Search is Needed
# -----------------------------

    web_context = ""

    if web_trigger.should_search(

        user_message,

        rag_context

):

        print("Using Web Search...")

        data = web_agent.retrieve(

            user_message

    )

        web_context = data["context"]

# -----------------------------
# Build Final Prompt
# -----------------------------

    combined_context = rag_context

    if web_context:

        combined_context += "\n\nWEB SEARCH\n\n"

        combined_context += web_context

    rag_prompt = prompt_builder.build_prompt(

        combined_context,

        user_message

)

    contents = [

        {

            "role": "user",

            "parts": [

                {

                 "text": (

                    memory_text +

                    profile_text +

                    "\n" +

                    rag_prompt

                 )        

                }

            ]

        }

    ]



    # Previous chat history

    for msg in memory.get_history()[:-1]:



        contents.append(

            {

                "role": msg["role"],

                "parts": [

                    {

                        "text": msg["text"]

                    }

                ]

            }

        )



    return stream_ai_response(contents)



    



# ----------------------------------------------------

# Update User Profile

# ----------------------------------------------------

def update_user_profile(user_message):



    profile_data = profile.load_profile()



    name = re.search(

        r"my name is (.+)",

        user_message,

        re.IGNORECASE

    )



    if name:

        profile_data["name"] = name.group(1).strip()



    language = re.search(

        r"i like (.+)",

        user_message,

        re.IGNORECASE

    )



    if language:

        profile_data["favorite"] = language.group(1).strip()



    profile.save_profile(profile_data)





# ----------------------------------------------------

# Stream AI Response

# ----------------------------------------------------

def stream_ai_response(contents):



    response = client.models.generate_content_stream(

        model="gemini-2.5-flash",

        contents=contents

    )



    full_response = ""



    for chunk in response:



        if chunk.text:



            full_response += chunk.text



            yield chunk.text



    memory.add_ai_message(full_response)



    total_tokens = token_counter.count_history(

        memory.get_history()

    )



    if total_tokens > MAX_TOKENS:

        memory.prune_history(keep_last=10)



    session.save_session(

        memory.save_history()

    )





# ----------------------------------------------------

# Token Usage

# ----------------------------------------------------

def get_token_usage():



    return token_counter.count_history(

        memory.get_history()

    )





# ----------------------------------------------------

# Clear Chat

# ----------------------------------------------------

def clear_chat():



    memory.load_history([])



    session.save_session([])



def update_long_term_memory(user_message):



    memory = long_memory.load()



    patterns = {



        "name": r"my name is (.+)",



        "occupation": r"i am (.+)",



        "goal": r"my goal is (.+)",



        "favorite_language": r"i like (.+)",



        "skill": r"i know (.+)"

    }



    for key, pattern in patterns.items():



        match = re.search(

            pattern,

            user_message,

            re.IGNORECASE

        )



        if match:



            memory[key] = match.group(1).strip()



    long_memory.save(memory)