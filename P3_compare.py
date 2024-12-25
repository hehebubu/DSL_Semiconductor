import re

def normalize_pattern(text: str) -> str:
    """
    패턴 텍스트를 정규화하는 함수
    - 모든 공백 문자를 제거
    - '#' 기호 제거
    - 대소문자 구분 없애기
    """
    # 모든 공백 문자 제거
    text = re.sub(r'\s+', '', text)
    # '#' 기호 제거
    text = text.replace('#', '')
    # 대소문자 통일
    text = text.upper()
    return text

def compare_patterns(file1: str, file2: str) -> tuple[bool, float, list[str]]:
    """
    두 패턴 파일을 비교하는 함수
    
    Returns:
        tuple[bool, float, list[str]]: 
            - 완전 일치 여부 (True/False)
            - 일치율 (0.0 ~ 1.0)
            - 차이점 목록
    """
    try:
        # 파일 읽기
        with open(file1, 'r') as f:
            pattern1 = f.read()
        with open(file2, 'r') as f:
            pattern2 = f.read()

        # 패턴 정규화
        norm_pattern1 = normalize_pattern(pattern1)
        norm_pattern2 = normalize_pattern(pattern2)

        # 완전 일치 검사
        exact_match = norm_pattern1 == norm_pattern2

        # 차이점 찾기
        differences = []
        
        # 원본 패턴을 라인 단위로 분리
        lines1 = [line.strip() for line in pattern1.split('\n') if line.strip()]
        lines2 = [line.strip() for line in pattern2.split('\n') if line.strip()]

        # 각 라인 정규화 후 비교
        norm_lines1 = [normalize_pattern(line) for line in lines1]
        norm_lines2 = [normalize_pattern(line) for line in lines2]

        # 라인 단위 비교
        for i, (line1, norm1) in enumerate(zip(lines1, norm_lines1), 1):
            if i <= len(norm_lines2):
                if norm1 != norm_lines2[i-1]:
                    differences.append(f"Line {i} differs:")
                    differences.append(f"  File1: {line1}")
                    differences.append(f"  File2: {lines2[i-1]}")

        # 라인 수가 다른 경우
        if len(lines1) != len(lines2):
            differences.append(f"Number of lines differs: {len(lines1)} vs {len(lines2)}")

        # 일치율 계산 (문자 단위)
        total_chars = max(len(norm_pattern1), len(norm_pattern2))
        if total_chars == 0:
            similarity = 1.0
        else:
            # Levenshtein 거리 계산
            import difflib
            matcher = difflib.SequenceMatcher(None, norm_pattern1, norm_pattern2)
            similarity = matcher.ratio()

        return exact_match, similarity, differences

    except Exception as e:
        return False, 0.0, [f"Error comparing patterns: {str(e)}"]

def main():
    file1 = "000_origin_pattern.txt"
    file2 = "002_final_result.txt"
    exact_match, similarity, differences = compare_patterns(file1, file2)
    
    # Similarity 값을 results.txt 파일에 누적해서 저장
    with open('results.txt', 'a') as f:
        f.write(f"{similarity:.4f}\n")
    
    # 기존 출력은 유지
    print(f"Patterns {'match exactly' if exact_match else 'do not match exactly'}")
    print(f"Similarity: {similarity:.2%}")
    if differences:
        print("\nDifferences found:")
        for diff in differences:
            print(diff)

if __name__ == "__main__":
    main()