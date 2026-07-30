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

                    ОТВЕТЬ КРАТКО (1 предложение):
                    - НА КАКОЕ ОНО ПОХОЖЕ БЛИЖЕ ВСЕГО ПО СМЫЛУ ИЗ 📌 ТОП-5 ПОХОЖИХ ДОКУМЕНТОВ

                    ТЫ ДОЛЖЕН ДАТЬ ОТВЕТ ОДНИМ ПРЕДЛОЖЕНИЕ!
                    НЕ ВЫДУМЫВАЙ. НЕ ВРИ, ТОЛЬКО ПО ФАКТАМ ЗАКЛЮЧЕНИЯ.
                    """
    return response_text, prompt

def general_text(response_text, base_prompt_text):
    general = (f"{response_text}"
               f"АНАЛИЗ НЕЙРОСЕТИ:\n\n{base_prompt_text}")
    
    return general

def make_response_text(result, new_name):
    name_max_sim = f' - {result[0]["name"]}'
    max_sim = result[0]["similarity"]

    # name_list = []
    # for item in result:         
    #     name_list.append(item['name'])

    # sum_list = []
    # for item in result:         
    #     sum_list.append(item['similarity'])

    if max_sim > 0.99:
        status = "🔴 ПОЛНОЕ СХОДСТВО (ДУБЛИКАТ)"
    elif max_sim > 0.95:
        status = "🟠 ВЫСОКИЙ УРОВЕНЬ СХОДСТВА"
    elif max_sim > 0.85:
        status = "🟡 ВОЗМОЖНОЕ СХОДСТВО"
    elif max_sim > 0.8:
        status = "🔵 СЛАБОЕ СХОДСТВО"
        name_max_sim = ""
    else:
        status = "✅ УНИКАЛЬНОЕ РЕШЕНИЕ"
        name_max_sim = ""

    names_text =  names_text_process(result)

    
    text = (f"ПРОВЕРКА УНИКАЛЬНОСТИ РАЦИОНАЛИЗАТОРСКОГО ПРЕДЛОЖЕНИЯ\n"
            "----------------------------------------------------------\n\n"

            f"{new_name}\n\n"

            "----------------------------------------------------------\n\n"

            f"ТОП ПОХОЖИХ ДОКУМЕНТОВ:\n{names_text}\n\n"

            "----------------------------------------------------------\n\n"

            f"Сходство: = {max_sim:.2%}{name_max_sim}\n\n"
            "----------------------------------------------------------\n\n"

            f"Результат: {status}\n\n"

            )

    return text

def names_text_process(result):
    similarity_list = []
    for i, v  in enumerate(result):
        name = v["name"]
        similarity = v["similarity"]
        
        if similarity > 0.85:
            similarity_list.append(f"{i+1}. {name} - {similarity:.2%}")
    
    return "\n".join(similarity_list)



