"""Tests for Korean entity standardisation utilities."""

from src.knowledge_graph.entity_standardization import standardize_entities


def test_particle_stripping():
    triples = [{"subject": "세종대왕이", "predicate": "창제", "object": "한글을"}]
    config = {
        "general": {"language": "ko", "strip_particles": True},
        "standardization": {"enabled": True, "use_llm_for_entities": False},
    }
    result = standardize_entities(triples, config)
    assert result[0]["subject"] == "세종대왕"
    assert result[0]["object"] == "한글"

