import random

from app.chat.chains.streaming_conversational_retrieval_chain import StreamingConversationalRetrievalChain
from app.chat.language_models.chatopenai import build_condense_question_chain_llm
from app.chat.memory import memory_map
from app.chat.models import ChatArgs
from app.chat.language_models import llm_map
from app.chat.vector_store import retriever_map
from app.chat.redis.redis_client import redis_client
from app.web.api import (set_conversation_components, get_conversation_components)

def random_component_by_score(component_type, component_builder_map):

    # Make sure component_type is 'llm', 'retriever', or 'memory'
    if component_type not in ['llm', 'retriever', 'memory']:
        raise ValueError(f"component_type must be 'llm', 'retriever', or 'memory', not {component_type}")

    # From redis, get the hash containing the sum total scores for the component_type
    # For example, if component_type is 'llm', then get the hash 'llm_score_values'
    score_values = redis_client.hgetall(f"{component_type}_score_values")

    # From redis, get the hash containing the number of times each component_type has been used
    # For example, if component_type is 'llm', then get the hash 'llm_score_counts'
    score_counts = redis_client.hgetall(f"{component_type}_score_counts")

    # Get all the valid component names for the component_type
    component_names = component_builder_map.keys()

    # Loop over those valid component names and use them to calculate the average score for each component
    # Add average scores to a dictionary
    average_scores = {}
    for component_name in component_names:
        # Get the total score for the component_name
        total_score = int(score_values.get(component_name, 1))

        # Get the number of times the component_name has been used
        count = int(score_counts.get(component_name, 1))

        # Calculate the average score for the component_name
        average_score = total_score / count if count > 0 else 0

        # Add the average score to the dictionary
        average_scores[component_name] = max(average_score, 0.1)

    # Do a weighted random choice of the component_name based on the average scores
    sum_scores = sum(average_scores.values())
    random_val = random.uniform(0, sum_scores)
    cumulative = 0
    for name, score in average_scores.items():
        cumulative += score
        if random_val <= cumulative:
            return name


def select_component(component_type, component_builder_map, chat_args):
    components = get_conversation_components(chat_args.conversation_id)
    previous_component_name = components[component_type]

    if previous_component_name:
        builder = component_builder_map[previous_component_name]
        return previous_component_name, builder(chat_args)
    else:
        random_name = random_component_by_score(component_type, component_builder_map)
        builder = component_builder_map[random_name]
        return random_name, builder(chat_args)


def build_chat(chat_args: ChatArgs):
    # Instantiate components based on whether one's linked to a conversation or not
    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)
    llm_name, llm = select_component("llm", llm_map, chat_args)
    set_conversation_components(chat_args.conversation_id, llm=llm_name, retriever=retriever_name, memory=memory_name)
    print(f"Running chain with llm: {llm_name}, retriever: {retriever_name}, memory: {memory_name}")
    condense_question_chain_llm = build_condense_question_chain_llm(chat_args)

    return StreamingConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory,
                                                          condense_question_llm=condense_question_chain_llm,
                                                          metadata=chat_args.metadata,
                                                          verbose=True)
