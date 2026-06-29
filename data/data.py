def ocr_result(number, date, name, author):
    text = (f"Рационализаторское предложение зарегестрировано под номером {number}\n\n"
            
            f"Дата регистрации: {date}\n\n"

            f"Наименование: {name}\n\n"

            f"Автор: {author}\n\n"
    )
    return text

def сhecking_result(max_similarity, best_name):
     if max_similarity > 0.85:
        text = (f"Самое похожее: '{best_name}'\n"
                f"Сходство: {max_similarity:.4f}\n\n"
                f"ВНИМАНИЕ! Сходство выше порога 0.85\n"
                f"Возможно, это дубликат!"
                )
     else:
        text = (f"Самое похожее: '{best_name}'\n"
                f"Сходство: {max_similarity:.4f}\n\n"
                f"Сходство ниже порога (0.85)\n"
                f"Можно добавлять как новое предложение"
                )
     return text
         