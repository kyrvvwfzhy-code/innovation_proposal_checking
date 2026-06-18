import re

class Extraction:
    def extrection(self, registered_text):
        number_pattern_1 = r'№ (\d+/\d+-\d+)'
        number_pattern_2 = r'№ — (\d+/\d+-\d+)'
        number_pattern_3 = r'№ (\d+-\d+)'
        number_pattern_4 = r'№ _ (\d+/\d+-\d+)'
        number_pattern_5 = r'№ —(\d+/\d+-\d+)'
        number_pattern = [number_pattern_1, number_pattern_2, number_pattern_3, number_pattern_4, number_pattern_5]

        date_pattern_1 = r'«(\d+)»\s+(\d+)\s+(\d+)' 
        date_pattern_2 = r'« (\d+)»\s+(\d+)\s+(\d+)'
        date_pattern_3 = r'«\s*(\d+)»\s*__\s*(\d+)\s+(\d+)'
        date_pattern_4 = r'«([a-zA-Z]+)\s*»\s*(\d+)\s+(\d+)'
        date_pattern_5 = r'«([a-zA-Z]+)»\s*(\d+)\s+(\d+)'
        date_pattern_6 = r'«(\d+)\s*»\s+(\d+)\s+(\d+)' 
        date_pattern_7 = r'«(\d+)»\s*_\s+(\d+)\s+(\d+)'
        date_pattern_8 = r'«(\d+)\s*»\s*_\s+(\d+)\s+(\d+)'
        date_pattern_9 = r'«\s*(\d+)\s*»\s+(\d+)\s+(\d+)'
        date_pattern_10 = r'«([а-яА-я]+)»\s*(\d+)\s+(\d+)'

        date_pattern = [date_pattern_1, date_pattern_2, date_pattern_3, date_pattern_4, date_pattern_5, date_pattern_6, 
                        date_pattern_7, date_pattern_8, date_pattern_9, date_pattern_10]

        for i in number_pattern:
            number_match = re.search(i, registered_text)
            if number_match:
                number = f"№ — {number_match.group(1)}"

        for i in date_pattern:
            date_match = re.search(i, registered_text)
            if date_match:
                day = date_match.group(1)
                mounth = date_match.group(2)
                year = date_match.group(3)
                date = f"{day}.{mounth}.{year}"

        return number, date
                

if __name__ == "__main__":
    
    text = "Зарегистрировано № 122/13-23 от«Ш» 05 2023 г."
    start = Extraction()
    result1, result2 = start.extrection(text)
    print(result1, result2)