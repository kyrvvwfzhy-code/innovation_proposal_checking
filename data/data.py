def ocr_result(registered, name, description):
    text = (f"Рационализаторское предложение: {registered}\n\n"

            f"Наименование: {name}\n\n"

            f"Описание: {description}"
    )
    return text
         
def base_prompt_text(result, new_name):
    if not result:
        return f"""РЕШЕНИЕ: МОЖНО ДОБАВЛЯТЬ
ПРИЧИНА: Похожих нет
СТАТУС: УНИКАЛЕН
НАЗВАНИЯ: Нет"""
    
    # Формируем список документов для промпта
    docs_text = ""
    for i, item in enumerate(result[:5], 1):
        name = item.get('name', 'Неизвестно')
        similarity = item.get('similarity', 0)
        docs_text += f"{i}. {name} - {similarity:.2%}\n"
    
    names = ", ".join([item['name'] for item in result[:3]])
    max_sim = result[0]['similarity']
    
    # Логика по правилам
    if max_sim > 0.85:
        decision = "НЕЛЬЗЯ ДОБАВЛЯТЬ"
        status = "ДУБЛИКАТ"
        reason = f"Сходство {max_sim:.2%} > 85%"
        names = ""  # Пусто, если дубликат
    elif max_sim > 0.70:
        decision = "ТРЕБУЕТСЯ ПРОВЕРКА"
        status = "ОЧЕНЬ ПОХОЖ"
        reason = f"Сходство {max_sim:.2%} > 70%"
    else:
        decision = "МОЖНО ДОБАВЛЯТЬ"
        status = "УНИКАЛЕН"
        reason = f"Сходство {max_sim:.2%} < 70%"
    
    prompt = f"""Ты ИИ-помощник по поиску ДУБЛИКАТОВ рационализаторских предложений.

Пользователь ищет рационализаторское предложение под названием: {new_name}

Найденные похожие документы (топ-5):
{docs_text}

Максимальное сходство: {max_sim:.2%}

Правила принятия решения:
- Сходство > 85% → НЕЛЬЗЯ ДОБАВЛЯТЬ (ДУБЛИКАТ)
- Сходство 70-85% → ТРЕБУЕТСЯ ПРОВЕРКА (ОЧЕНЬ ПОХОЖ)
- Сходство < 70% → МОЖНО ДОБАВЛЯТЬ (УНИКАЛЕН)

ОТВЕТЬ РОВНО 4 СТРОКАМИ. БЕЗ ЛИШНИХ СЛОВ. НЕ ВЫДУМЫВАЙ.

РЕШЕНИЕ: {decision}
ПРИЧИНА: {reason}
СТАТУС: {status}
НАЗВАНИЯ: {names}"""
    
    return prompt