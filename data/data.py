from db.database import DataBase

db = DataBase()

def ocr_result(registered, name, description):
    text = (f"Рационализаторское предложение: {registered}\n\n"

            f"Наименование: {name}\n\n"

            f"Описание: {description}"
    )
    return text

def default_prompt(conclusion=None):
    prompt = f"""
            Ты — ИИ-ассистент, специализирующийся на анализе заключений по проверке рационализаторских предложений на уникальность.

            На вход подаётся текст заключения:
            {conclusion}

            Задача: на основе заключения выдели 2–3 предложения, которые наиболее точно описывают суть нового решения из списка похожих документов.

            Требования:
            - Не копируй и не пересказывай текст заключения дословно.
            - Не добавляй домыслов и лишней информации.
            - Опирайся исключительно на факты из заключения.
            - Избегай повторов и шаблонных формулировок.

            Ответ дай на русском языке.
            """
    return prompt

def conclution(new_name, top5, max_sim, name_max_sim, status):
    text = (f"ПРОВЕРКА УНИКАЛЬНОСТИ РАЦИОНАЛИЗАТОРСКОГО ПРЕДЛОЖЕНИЯ\n"
            "----------------------------------------------------------\n\n"

            f"{new_name}\n\n"

            "----------------------------------------------------------\n\n"

            f"ТОП ПОХОЖИХ ДОКУМЕНТОВ:\n{top5}\n\n"

            "----------------------------------------------------------\n\n"

            f"Сходство: {max_sim:.2%}{name_max_sim}\n\n"
            "----------------------------------------------------------\n\n"

            f"Результат: {status}\n\n"

            )

    return text

def conclusion_with_AI_analys(result, new_name):
    if result is None and new_name is None:
        response_text = "None"
    else:
        response_text = conclusion_forming(result, new_name)

    template = db.get_innovation_proposal_prompt()
    prompt = template.replace('{conclution}', response_text)
    
    return response_text, prompt

def transformer_result(response_text, conclusion_with_AI_analys):
    text = (f"{response_text}"
               f"АНАЛИЗ НЕЙРОСЕТИ:\n\n{conclusion_with_AI_analys}")
    
    return text

def conclusion_forming(result, new_name):
    name_max_sim = f' - {result[0]["name"]}'
    max_sim = result[0]["similarity"]

    if max_sim > 0.99:
        status = "🔴 ПОЛНОЕ СХОДСТВО (ДУБЛИКАТ)"
    elif max_sim > 0.85:
        status = "🟠 ВЫСОКИЙ УРОВЕНЬ СХОДСТВА"
    elif max_sim > 0.75:
        status = "🟡 ВОЗМОЖНОЕ СХОДСТВО"
    elif max_sim > 0.6:
        status = "🔵 СЛАБОЕ СХОДСТВО"
        name_max_sim = ""
    else:
        status = "✅ УНИКАЛЬНОЕ РЕШЕНИЕ"
        name_max_sim = ""

    top5 =  top5_rules_process(result)

    text = conclution(new_name, top5, max_sim, name_max_sim, status)
    return text

def top5_rules_process(result):
    similarity_list = []
    for i, v  in enumerate(result):
        name = v["name"]
        similarity = v["similarity"]
        
        if similarity > 0.75:
            similarity_list.append(f"{i+1}. {name} - {similarity:.2%}")
    
    return "\n".join(similarity_list)



