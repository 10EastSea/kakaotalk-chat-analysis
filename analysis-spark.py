import os
import pandas as pd
import re
import shutil

"""
pyspark
    - version: 3.3.1
    - install: pip install pyspark
    - execute: python analysis-spark.py
"""
from pyspark.sql import SparkSession
import pyspark.sql.functions as f

CHAT_PATH = os.path.join(os.path.dirname(__file__), 'chat')
RESULT_PATH = os.path.join(os.path.dirname(__file__), 'result')

FILE_HEADER_1 = r'Talk_\d{4}\.\d{1,2}\.\d{1,2} .*.txt'
FILE_HEADER_2 = r'저장한 날짜 : \d{4}\. \d{1,2}\. \d{1,2}\. (오전|오후) \d{1,2}:\d{1,2}'
DATE_INFO     = r'\d{4}년 \d{1,2}월 \d{1,2}일 (일|월|화|수|목|금|토)요일'
JOIN_INFO     = r'\d{4}\. \d{1,2}\. \d{1,2}\. (오전|오후) \d{1,2}:\d{1,2}: .*'
KAKAOTALK_MSG = r'\d{4}\. \d{1,2}\. \d{1,2}\. (오전|오후) \d{1,2}:\d{1,2}, .* :'


def kakaotalk_msg_parse(file_path: str):
    """
    카카오톡 대화 내용 파일(txt)을 읽어드려, 메시지만을 파싱한다.
        Args:
            file_path (str): 파일 경로
        Returns:
            ['date', 'user', 'text'] 컬럼 값을 가지는 DataFrame 반환
    """
    msg_list = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if re.match(FILE_HEADER_1, line) or re.match(FILE_HEADER_2, line): continue
            elif re.match(DATE_INFO, line) or re.match(JOIN_INFO, line): continue
            elif line == '\n': continue

            elif re.match(KAKAOTALK_MSG, line):
                date_user_text = line.split(',')
                user_text = date_user_text[1].split(':', maxsplit=1)

                date = date_user_text[0]
                user = user_text[0].strip()
                text = user_text[1].strip()
                msg_list.append({'date': date, 'user': user, 'text': text})
            
            elif len(msg_list) != 0:
                msg_list[-1]['text'] += '\n' + line.strip()

    msg_df = pd.DataFrame(msg_list)
    return msg_df


def main(spark: SparkSession):
    msg_df = pd.DataFrame()

    ## File -Parse Message-> DataFrame
    file_list = [file for file in os.listdir(CHAT_PATH) if file.endswith('.txt')]
    for file in file_list:
        file_path = os.path.join(CHAT_PATH, file)
        msg_df = pd.concat([msg_df, kakaotalk_msg_parse(file_path)])

    ## Spark Job
    spark_df = spark.createDataFrame(msg_df)
    word_count_df = spark_df.withColumn('word', f.explode(f.split(f.col('text'), r'[\s|\n]'))) \
        .groupBy('word') \
        .count() \
        .sort('count', ascending=False)
    # word_count_df.show()

    ## Write File
    if os.path.exists(os.path.join(RESULT_PATH, 'word_count_spark')): shutil.rmtree(os.path.join(RESULT_PATH, 'word_count_spark'))  
    word_count_df.write.options(header=True, delimiter=',').csv(os.path.join(RESULT_PATH, 'word_count_spark'))


if __name__ == "__main__":
    ## Create Spark
    spark = SparkSession.builder \
        .appName("analysis_spark") \
        .getOrCreate()

    main(spark)

    ## Stop Spark
    spark.stop()