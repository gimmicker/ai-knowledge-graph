"""Centralised repository for LLM prompts.

The module exposes helper functions that return prompts according to the
requested language. English prompts mirror the original project while
Korean prompts implement guidance for subject–predicate–object extraction,
entity standardisation and relationship inference.
"""

from __future__ import annotations

from typing import Callable, Dict, Tuple


# ---------------------------------------------------------------------------
# Main extraction prompts
# ---------------------------------------------------------------------------


def _en_main_prompts() -> Tuple[str, str]:
    system = (
        "You are an advanced AI system specialised in knowledge extraction "
        "and knowledge graph generation.\n"
        "CRITICAL INSTRUCTION: predicates must be 3 words or fewer."
    )

    user = (
        "Your task: Read the text below (delimited by triple backticks) "
        "and identify all Subject-Predicate-Object relationships.\n"
        "Return a JSON array only."
        "\n\nText to analyse:\n``\n"
    )
    return system, user


def _ko_main_prompts() -> Tuple[str, str]:
    system = (
        "당신은 한국어 지문에서 지식 그래프 삼중항을 추출하는 전문가입니다."\
        " 문장 속 주어, 술어, 목적어를 정확히 찾아 JSON 형태로 제시하세요."
    )

    user = (
        "다음 한국어 문단을 읽고 모든 주어-술어-목적어(S-P-O) 관계를 "
        "JSON 배열로 추출하십시오.\n"
        "지침:\n"
        "- 출력은 JSON 배열만 사용합니다. 각 항목은 {\"subject\":\"...\","
        " \"predicate\":\"...\", \"object\":\"...\"}\n"
        "- 조사와 어미를 제거하고 가능한 한 표제어로 기록합니다.\n"
        "- \"이다\", \"있다\", \"했다\" 등 의미가 빈약한 술어는 제외합니다.\n"
        "- 필요하면 time, source_span 필드를 추가할 수 있습니다.\n"
        "\n한국어 텍스트:\n``\n"
    )
    return system, user


MAIN_PROMPTS: Dict[str, Tuple[str, str]] = {
    "en": _en_main_prompts(),
    "ko": _ko_main_prompts(),
}


def get_main_prompts(language: str = "en") -> Tuple[str, str]:
    return MAIN_PROMPTS.get(language, MAIN_PROMPTS["en"])


# Backwards compatibility constants
MAIN_SYSTEM_PROMPT, MAIN_USER_PROMPT = get_main_prompts("en")


# ---------------------------------------------------------------------------
# Entity resolution prompts
# ---------------------------------------------------------------------------


def _en_entity_prompts() -> Tuple[str, Callable[[str], str]]:
    system = (
        "You are an expert in entity resolution and knowledge representation."
    )

    def user(entity_list: str) -> str:
        return (
            "Below is a list of entity names extracted from a knowledge graph.\n"
            "Standardise variants and return JSON mapping.\n\n" f"Entity list:\n{entity_list}\n"
        )

    return system, user


def _ko_entity_prompts() -> Tuple[str, Callable[[str], str]]:
    system = "당신은 지식 그래프 엔터티 표준화를 담당하는 한국어 전문가입니다."

    def user(entity_list: str) -> str:
        return (
            "다음은 추출된 엔터티 목록입니다.\n"
            "각 항목을 표준 형태와 별칭으로 정리하세요.\n"
            "출력 형식: [{\"canonical\":\"...\", \"aliases\":[...]}]\n\n"
            f"엔터티:\n{entity_list}\n"
        )

    return system, user


ENTITY_PROMPTS: Dict[str, Tuple[str, Callable[[str], str]]] = {
    "en": _en_entity_prompts(),
    "ko": _ko_entity_prompts(),
}


def get_entity_resolution_prompts(
    language: str = "en",
) -> Tuple[str, Callable[[str], str]]:
    return ENTITY_PROMPTS.get(language, ENTITY_PROMPTS["en"])


# Backwards compatibility
ENTITY_RESOLUTION_SYSTEM_PROMPT, _entity_user_en = _en_entity_prompts()


def get_entity_resolution_user_prompt(entity_list: str, language: str = "en") -> str:
    _, user_fn = get_entity_resolution_prompts(language)
    return user_fn(entity_list)


# ---------------------------------------------------------------------------
# Relationship inference prompts
# ---------------------------------------------------------------------------


def _en_relation_prompts() -> Tuple[str, Callable[[str, str, str], str]]:
    system = (
        "You are an expert in knowledge representation and inference."
    )

    def user(entities1: str, entities2: str, triples_text: str) -> str:
        return (
            "I have a knowledge graph with two disconnected communities of entities.\n"
            f"Community 1 entities: {entities1}\n"
            f"Community 2 entities: {entities2}\n"
            f"Existing relationships:\n{triples_text}\n"
            "Infer 2-3 plausible relationships and return JSON array with "
            "subject, predicate, object."
        )

    return system, user


def _ko_relation_prompts() -> Tuple[str, Callable[[str, str, str], str]]:
    system = "당신은 표준 술어 집합을 사용해 신뢰할 수 있는 관계만 제안하는 한국어 전문가입니다."

    def user(entities1: str, entities2: str, triples_text: str) -> str:
        return (
            "다음은 두 개의 엔터티 집합입니다.\n"
            f"커뮤니티1: {entities1}\n"
            f"커뮤니티2: {entities2}\n"
            f"기존 관계:\n{triples_text}\n"
            "표준 술어만 사용해 새로운 관계를 JSON 배열로 제시하세요.\n"
            "각 항목은 {\"subject\":..., \"predicate\":..., \"object\":..., \"confidence\":\"high|medium|low\", \"rationale\":\"...\"} 형태입니다."
        )

    return system, user


RELATION_PROMPTS: Dict[str, Tuple[str, Callable[[str, str, str], str]]] = {
    "en": _en_relation_prompts(),
    "ko": _ko_relation_prompts(),
}


def get_relationship_inference_user_prompt(
    entities1: str, entities2: str, triples_text: str, language: str = "en"
) -> str:
    _, user_fn = RELATION_PROMPTS.get(language, RELATION_PROMPTS["en"])
    return user_fn(entities1, entities2, triples_text)


def get_within_community_inference_user_prompt(
    pairs_text: str, triples_text: str, language: str = "en"
) -> str:
    # For simplicity use the same structure as cross-community prompt
    return (
        "다음 엔터티 쌍에 대해 신뢰 가능한 관계를 추론하여 JSON 배열로 제시하세요.\n"
        if language == "ko"
        else "Infer plausible relationships between these entity pairs and return JSON array.\n"
    ) + f"Pairs:\n{pairs_text}\nExisting:\n{triples_text}\n"


RELATIONSHIP_INFERENCE_SYSTEM_PROMPT, _relation_user_en = _en_relation_prompts()
WITHIN_COMMUNITY_INFERENCE_SYSTEM_PROMPT = RELATIONSHIP_INFERENCE_SYSTEM_PROMPT

