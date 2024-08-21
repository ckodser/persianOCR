import os
import time

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
    fixed_options = []
    for index, row in df.iterrows():
        try:
            result = co.chat(
                message=prompt + row['question'], model=model
            ).text
            fixed_questions.append(result)
            print("----->", result)

        except Exception as e:
            print(row)
            print(e)
            raise ValueError

        options_row=[]
        for option in row['options']:
            try:
                result = co.chat(
                    message=prompt + option, model=model
                ).text
                options_row.append(result)
                print("----->", result)

            except Exception as e:
                print(row)
                print(e)
                raise ValueError
        fixed_options.append(options_row)
        if index%7==6:
            time.sleep(60)

    df['question'] = pd.Series(fixed_questions, index=df.index)
    df['options'] = pd.Series(fixed_options, index=df.index)

    df.to_json(join( f"csvs/fixed_{filename}"), orient="records")

    time.sleep(60)


