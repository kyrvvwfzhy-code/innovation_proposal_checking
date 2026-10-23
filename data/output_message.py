# DOWNLOAD
def text_recognition_output(registered, name, description):
    text = f"""Рационализаторское предложение: {registered}\n\n
Наименование: {name}\n\n
Описание: {description}"""
    return text

# DOWNLOAD AND SEARCH
def conclution_output(new_name, top5, max_sim, name_max_sim, status):
    text = f"""<p><b>ОЦЕНКА УНИКАЛЬНОСТИ РАЦИОНАЛИЗАТОРСКОГО ПРЕДЛОЖЕНИЯ</b></p>
    <p>{new_name}</p>
    <p>{top5}</p>
    <p><b>Сходство:</b> {max_sim:.2%} {name_max_sim}</p>
    <p><b>Результат:</b> {status}</p>"""
    return text

def conclusion_AI_output(response_text, conclusion_with_AI_analys):
    text = f"""<p>{response_text}</p>
    <p><b>АНАЛИЗ НЕЙРОСЕТИ:</b></p>
    {conclusion_with_AI_analys}"""
    return text

def image_conclusion_output(name, similarity):
    text = f"""<p><b>ОЦЕНКА УНИКАЛЬНОСТИ РАЦИОНАЛИЗАТОРСКОГО ПРЕДЛОЖЕНИЯ</b></p>
    <p><b>ПО ИЗОБРАЖЕНИЮ</b></p>
    <p><b>ПОХОЖИЙ ДОКУМЕНТ:</b></p>
    <p>{name}</p>
    <p><b>Сходство:</b> {similarity:.2%}</p>"""
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
        url = v["url"]
        name = v["name"]
        similarity = v["similarity"]   
        if similarity > 0.75:
            similarity_list.append(f"""{i+1}. <a href="{url}">{name}</a> - {color(f"{similarity:.2%}", "red")}""")
    if len(similarity_list) == 0:
        return ""
    else:
        text_el = "\n\n".join(similarity_list)
        return f"""<p><b>ТОП ПОХОЖИХ ДОКУМЕНТОВ:</b></p>
        <p>{text_el}</p>"""

def color(text, c):
    return f'<span style="color:{c};">{text}</span>'