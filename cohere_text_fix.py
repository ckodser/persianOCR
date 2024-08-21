import os
import pandas as pd
import os
from os.path import isfile, join

import cohere

with open('cohere_apikey.txt', 'r') as file:
    cohere_key = file.read().strip()
model = "command-r-plus"
prompt = "غلط‌های نگارشی در متن زیر را اصلاح کن. مثلا اگر در متن کلمه‌ی ‘کتابها’ وجود دارد باید به ‘کتاب‌ها’ تغییر پیدا کند. فقط و فقط متن اصلاح شده را خروجی بده. متن:"

co = cohere.Client(
    api_key=cohere_key
)
files = [file for file in os.listdir("csvs") if file.endswith(".json") and "fixed" not in file]

for filename in files:
    df = pd.read_json(join("csvs", f"{filename}"))

    fixed_questions = []

    for index, row in df.iterrows():
        try:
            result = co.chat(
                message=prompt + row['question'], model=model
            )
            fixed_questions.append(result)

        except Exception as e:
            print(row)
            raise ValueError

    df['fix_questions'] = pd.Series(fixed_questions, index=df.index)

    df.to_json(join( f"csvs/fixed_{filename}.json"), orient="records")


