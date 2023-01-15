# Kakaotalk Chat Analysis
카카오톡 대화 내용을 분석하는 프로그램이다. 프로그램을 실행하면 대화한 메시지를 공백 문자 기준으로 나눠, 각 단어가 해당 대화방에서 얼만큼 나왔는지 확인할 수 있다. (현재 이모티콘과 사진, 동영상 등은 대화 내용을 추출할 때 해당 텍스트로 변환돼서 대화 내용의 완벽한 분석 결과를 알아내기 어렵다)

## Updated Date
2023-01-15

## Language & Library
- Python 3.9.16
- Pandas 1.5.2 (`pip install pandas`)
``` Bash
$ python --version     
Python 3.9.16

$ pip list
Package         Version
--------------- --------
numpy           1.24.1
pandas          1.5.2
...
```

## Usage
1. 대화 내용을 분석하고 싶은 카카오톡 대화방에 들어가 `대화 내용 내보내기`를 클릭
    - `텍스트 메시지만 보내기` 클릭
    - 이메일을 통해 파일 다운로드 진행
2. 대화 파일을 `chat` 폴더에 넣음
    - 텍스트(`txt`) 파일만 인식할 수 있으므로, 대화 파일이 텍스트 파일인지 확인
3. `python analysis.py` 실행
    - 프로그램 실행이 완료되면, `result` 폴더에 `word_count.txt` 파일이 생김
    - 해당 파일에서 `{단어} : {나온 횟수}` 확인 (내림차순으로 정렬)

## Reference
- 정규표현식 작성: https://regexr.com/
- 카카오톡 메시지 파싱: https://wikidocs.net/162786
