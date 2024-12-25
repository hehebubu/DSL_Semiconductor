# Pattern Parser Project

## 📁 파일 구조
- `000_origin_pattern.txt` : 패턴 추출을 위한 원본 패턴 파일 (정답지로도 활용)
- `001_pattern.txt` : 패턴 생성 규칙(rule) 정의 파일
- `002_final_result.txt` : 패턴 생성 결과 파일
- `P1_converter.py` : 원본 패턴에서 rule 추출 프로그램
- `P2_pattern_parser.py` : 패턴 파서 프로그램
- `D000_code.xlsx` : 전체 코드 및 코드별 점수 분포 정리

## 💡 프로젝트 개요
본 프로젝트는 원본 패턴으로부터 규칙을 추출하고, 추출된 규칙에 따라 패턴을 생성/분석하는 파서 프로그램입니다.
원본 패턴은 `000_origin_pattern.txt`에 정의되어 있으며, `P1_converter.py`를 통해 규칙을 추출합니다.
추출된 규칙은 `001_pattern.txt`에 저장되며, 파서 프로그램(`P2_pattern_parser.py`)을 통해 
새로운 패턴을 생성합니다. 생성된 패턴의 결과는 `002_final_result.txt`에서 확인할 수 있습니다.

## 📊 성능 분석
코드별 성능 및 점수 분포는 `D000_code.xlsx` 파일에서 확인할 수 있습니다.