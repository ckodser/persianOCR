import cohere

with open('cohere_apikey.txt', 'r') as file:
    cohere_key = file.read().strip()
model = "command-r-plus"
prompt = "غلط‌های نگارشی در متن زیر را اصلاح کن. مثلا اگر در متن کلمه‌ی ‘کتابها’ وجود دارد باید به ‘کتاب‌ها’ تغییر پیدا کند. فقط و فقط متن اصلاح شده را خروجی بده. متن:",

co = cohere.Client(
    api_key=cohere_key
)
chat = co.chat(
    message=prompt + "كدام یك از موارد زیر عرضهكننده مواد اولیه میباشد؟"
    , model=model
)

print(chat)
