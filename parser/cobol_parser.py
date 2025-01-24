from .parser import Parser
import re

class CobolParser(Parser):

    def clean_cobol_code(self, cobol_code):
        cleaned_lines = []
        for line in cobol_code.splitlines():
            # Remove line numbers (first 6 columns)
            if len(line) > 6 and line[:6].strip().isdigit():
                line = line[6:]
            # Remove comments (lines starting with '*' in column 7)
            if len(line) > 6 and line[0] == '*':
                continue
            # Remove any text past column 66
            if len(line) > 66:
                line = line[:66]
            cleaned_lines.append(line.rstrip())
        return "\n".join(cleaned_lines)

    def parse_cobol_paragraphs(self, cobol_code):
        paragraph_pattern = re.compile(r'(?m)^\s*([A-Z0-9-]+)\.\s*$')
        
        paragraphs = {}
        current_paragraph = None
        lines = cobol_code.splitlines()

        for line in lines:
            paragraph_match = paragraph_pattern.match(line)

            if paragraph_match:
                current_paragraph = paragraph_match.group(1)
                paragraphs[current_paragraph] = [f"{current_paragraph}."]
            elif current_paragraph:
                paragraphs[current_paragraph].append(line.strip())

        # Convert list of lines back to string for each paragraph and remove empty or EXIT paragraphs
        cleaned_paragraphs = {}
        for key, content in paragraphs.items():
            content_str = "\n".join(content).strip()
            if not re.search(r'\bEXIT\b', content_str, re.IGNORECASE):
                cleaned_paragraphs[key] = content_str

        return cleaned_paragraphs

    def __init__(self, code_data):
        self.code_data = code_data

    def who_am_i(self):
        super().who_am_i()
        print("I will be used to parse COBOL programs")

    def dump_info(self):
        super().dump_info()

    def return_function_text(self, paragraphs):
        return  self.parse_cobol_paragraphs(paragraphs)


    def parse_functions(self):
        return self.clean_cobol_code(self.code_data)

   