# AI 지식 그래프 생성기 (한국어)

이 프로젝트는 한국어 문서를 입력받아 주어-술어-목적어(SPO) 삼중항을 추출하고, 시각적 지식 그래프로 변환합니다.

## 빠른 시작

1. 의존성 설치

```bash
pip install -r requirements.txt
```

2. `config.toml`의 `[general]` 섹션에서 `language = "ko"`가 설정되어 있는지 확인합니다.

3. 실행 예시

```bash
uv run generate-graph.py --input data/sample_ko.txt --output sample_ko.html --language ko
```

## 주요 설정

- `general.language`: `ko` 또는 `en`
- `general.token_unit`: `chars`, `words`, `sentences`
- `predicates.predicates_path`: 표준 술어 JSON 경로
- `visualization.font_family`: HTML 시각화 폰트 (기본 `Noto Sans KR`)

## 한글 폰트

시각화 HTML은 기본적으로 구글 웹폰트 **Noto Sans KR**을 사용합니다. 인터넷에 연결된 환경이라면 추가 설치 없이 한글이 올바르게 렌더링됩니다.

## 모델 선택

한국어 처리를 위해서는 다국어 성능이 좋은 LLM을 사용하는 것이 좋습니다. 예: `gemma3`, `GPT-4o`, `Claude 3.5 Sonnet`, `Llama 3.1 Instruct` 등.

