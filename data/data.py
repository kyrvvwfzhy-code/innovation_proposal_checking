def ocr_result(registered, name, description):
    text = (f"Рационализаторское предложение: {registered}\n\n"

            f"Наименование: {name}\n\n"

            f"Описание: {description}"
    )
    return text

def base_prompt_text(result, new_name):
    response_text = make_response_text(result, new_name)
    prompt = f"""Ты ИИ-помощник анализа сходства рационализаторских предложений.

                    У тебя на входе текст с заключением:
                    {response_text}

                    ОТВЕТЬ КРАТКО (2 предложения):
                    - Что показал анализ?

                    НЕ ВЫДУМЫВАЙ. ТОЛЬКО ПО ФАКТАМ.
                    """
    return response_text, prompt

def general_text(response_text, base_prompt_text):
    general = (f"{response_text}"
               f"АНАЛИЗ НЕЙРОСЕТИ:\n\n{base_prompt_text}")
    
    return general

def make_response_text(result, new_name):
    name_max_sim = f' - {result[0]["name"]}'
    max_sim = result[0]["similarity"]

    name_list = []
    for item in result:         
        name_list.append(item['name'])

    if max_sim > 0.99:
        status = "ПОЛНОЕ СХОДСТВО"
    elif max_sim > 0.95:
        status = "ВЫСОКИЙ УРОВЕНЬ СХОДСТВА"
    elif max_sim > 0.85:
        status = "ВОЗМОЖНОЕ СХОДСТВО"
    elif max_sim > 0.8 and max_sim < 0.85:
        status = "CХОДСТВО НЕ НАЙДЕНО"
        name_max_sim = ""
    elif max_sim < 0.8:
        status = "CХОДСТВО НЕ НАЙДЕНО"
        name_max_sim = ""
    
    text = (f"ПРОВЕРКА УНИКАЛЬНОСТИ РАЦИОНАЛИЗАТОРСКОГО ПРЕДЛОЖЕНИЯ\n\n"
            f"{new_name}\n\n"
            f"ТОП-5 - {name_list}\n\n"
            f"Максимальное сходство = {max_sim:.2f}{name_max_sim}\n\n"
            f"РЕЗУЛЬТАТ: {status}\n\n"

            )

    return text
