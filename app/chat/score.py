from app.chat.redis.redis_client import redis_client


def score_conversation(
        conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    print("Generating the scores using OpenAI {}", llm)
    score = min(max(score, 0), 1)

    redis_client.hincrby("llm_score_values", llm, score)
    redis_client.hincrby("retriever_score_values", retriever, score)
    redis_client.hincrby("memory_score_values", memory, score)

    redis_client.hincrby("llm_score_counts", llm, 1)
    redis_client.hincrby("retriever_score_counts", retriever, 1)
    redis_client.hincrby("memory_score_counts", memory, 1)


def get_scores():
    """
        Example:

        {
            'llm': {
                'chatopenai-3.5-turbo': [score1, score2],
                'chatopenai-4': [score3, score4]
            },
            'retriever': { 'pinecone_store': [score5, score6] },
            'memory': { 'persist_memory': [score7, score8] }
        }
    """

    aggregate_scores = {"llm": {}, "retriever": {}, "memory": {}}
    for component_type in aggregate_scores.keys():

        score_values = redis_client.hgetall(f"{component_type}_score_values")
        score_counts = redis_client.hgetall(f"{component_type}_score_counts")

        component_names = score_values.keys()

        for component_name in component_names:
            score = int(score_values.get(component_name, 1))
            count = int(score_counts.get(component_name, 1))

            average_score = score/count
            aggregate_scores[component_type][component_name] = [average_score]

    return aggregate_scores
