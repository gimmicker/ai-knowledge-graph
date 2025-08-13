"""Tests for the Korean pipeline utilities."""

from pathlib import Path

from src.knowledge_graph.text_utils import split_sentences_ko, chunk_text
from src.knowledge_graph.llm import extract_json_from_text
from src.knowledge_graph.visualization import visualize_knowledge_graph


def test_kss_sentence_split():
    text = "세종대왕이 한글을 만들었다. 이는 백성을 위한 것이다."
    sentences = split_sentences_ko(text)
    assert sentences == ["세종대왕이 한글을 만들었다.", "이는 백성을 위한 것이다."]


def test_chunk_by_chars_and_sentences(tmp_path):
    text = "가나다라마바사아자차카타파하. 두번째 문장입니다. 세번째 문장입니다."
    char_chunks = chunk_text(text, chunk_size=10, overlap=2, token_unit="chars", language="ko")
    assert len(char_chunks) > 1
    sent_chunks = chunk_text(text, chunk_size=1, overlap=0, token_unit="sentences", language="ko", sentence_splitter="kss")
    assert len(sent_chunks) == 3


def test_extract_json_schema():
    response = '[{"subject":"세종","predicate":"창제","object":"한글"}]'
    triples = extract_json_from_text(response)
    assert isinstance(triples, list)
    assert set(triples[0].keys()) == {"subject", "predicate", "object"}


def test_visualization_font(tmp_path):
    triples = [{"subject": "세종", "predicate": "창제", "object": "한글"}]
    output = tmp_path / "graph.html"
    visualize_knowledge_graph(triples, output_file=str(output), config={"visualization": {"font_family": "Noto Sans KR"}})
    html = output.read_text(encoding="utf-8")
    assert "Noto Sans KR" in html

