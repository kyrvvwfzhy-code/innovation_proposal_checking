# DOWNLOAD
def text_recognition_output(registered, name, description):
    text = f"""Рационализаторское предложение: {registered}\n
Наименование: {name}\n
Описание: {description}
            """
    return text

# DOWNLOAD AND SEARCH
def conclution_output(new_name, top5, max_sim, name_max_sim, status):
    text = f"""ПРОВЕРКА УНИКАЛЬНОСТИ РАЦИОНАЛИЗАТОРСКОГО ПРЕДЛОЖЕНИЯ\n
----------------------------------------------------------\n
{new_name}\n
----------------------------------------------------------\n
ТОП ПОХОЖИХ ДОКУМЕНТОВ:\n
{top5}\n
----------------------------------------------------------\n
Сходство: {max_sim:.2%}{name_max_sim}\n
----------------------------------------------------------\n
Результат: {status}"""
    return text

def conclusion_AI_output(response_text, conclusion_with_AI_analys):
    text = f"""{response_text}\n
АНАЛИЗ НЕЙРОСЕТИ:\n
{conclusion_with_AI_analys}
            """
    return text

def image_conclusion_output(name, similarity):
    text = f"""ПРОВЕРКА УНИКАЛЬНОСТИ РАЦИОНАЛИЗАТОРСКОГО ПРЕДЛОЖЕНИЯ\n
----------------------------------------------------------\n
ПО ИЗОБРАЖЕНИЮ\n
----------------------------------------------------------\n
ПОХЖИЙ ДОКУМЕНТ:\n
{name}\n
----------------------------------------------------------\n
Сходство: {similarity:.2%}
            """
    return text

# internal functions
def conclusion_AI_forming(prompt, result, new_name):
    if result is None and new_name is None:
        response_text = "None"
    else:
        response_text = conclusion_rules_forming(result, new_name)
    prompt_text = prompt.replace('{conclution}', response_text)
    return response_text, prompt_text

def conclusion_rules_forming(result, new_name):
    name_max_sim = f' - {result[0]["name"]}'
    max_sim = result[0]["similarity"]
    if max_sim > 0.99:
        status = "ПОЛНОЕ СХОДСТВО (ДУБЛИКАТ)"
    elif max_sim > 0.85:
        status = "ВЫСОКИЙ УРОВЕНЬ СХОДСТВА"
    elif max_sim > 0.75:
        status = "ВОЗМОЖНОЕ СХОДСТВО"
    elif max_sim > 0.6:
        status = "СЛАБОЕ СХОДСТВО"
        name_max_sim = ""
    else:
        status = "УНИКАЛЬНОЕ РЕШЕНИЕ"
        name_max_sim = ""
    top5 =  top5_rules_forming(result)
    text = conclution_output(new_name, top5, max_sim, name_max_sim, status)
    return text

def top5_rules_forming(result):
    similarity_list = []
    for i, v  in enumerate(result):
        name = v["name"]
        similarity = v["similarity"]   
        if similarity > 0.75:
            similarity_list.append(f"{i+1}. {name} - {similarity:.2%}")
    return "\n".join(similarity_list)