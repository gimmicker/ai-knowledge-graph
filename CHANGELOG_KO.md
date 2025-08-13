# 변경 내역 (Korean Support)

- 한국어 파이프라인 추가: 문장 분할, 청킹, 엔터티 표준화, 관계 추론 프롬프트
- `config.toml`에 다국어 설정 추가 (`language`, `token_unit`, `sentence_splitter` 등)
- 한국어 표준 술어 스키마 `data/predicate_schema_ko.json` 및 샘플 데이터 추가
- 시각화에 Noto Sans KR 폰트 적용 및 UTF-8 보장
- CLI 옵션 `--language`, `--token-unit` 도입
- 한국어 전용 테스트 케이스 추가

