import ollama

def beautiful_verdict(text_a, text_b, similarity_score, model="llama3.2:3b"):
    prompt = f"""
Ты — эксперт по семантическому анализу текстов.

Текст А: "{text_a}"
Текст Б: "{text_b}"

Косинусное сходство между их эмбеддингами = {similarity_score:.4f}
(где 1.0 — полная идентичность, 0.0 — полная непохожесть).

Напиши красивое, литературное заключение на русском языке:
- Что общего в этих текстах?
- Насколько они похожи по смыслу (в процентах)?
- Если похожи — выдели общую тему.
- Если не похожи — объясни, в чем ключевое различие.

Ответ должен быть связным, как у филолога или литературного критика.
"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.7,
            "max_tokens": 300
        }
    )
    return response["message"]["content"]




if __name__ == "__main__":
    text1 = "Кошка спит на диване"
    text2 = "Пушистый кот отдыхает на кушетке"
    cosine = 0.87

    answer = beautiful_verdict(text1, text2, cosine)
    print(answer)