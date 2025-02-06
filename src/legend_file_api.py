import re

# from py_rpautom.python_utils import criar_arquivo_texto

# criar_arquivo_texto(caminho='', dado='', em_bytes='', encoding='utf-8')


def extract_text_from_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    text_lines = []
    for line in content:
        if not re.match(r'^\d+$', line.strip()) and not '-->' in line:
            text_lines.append(line.strip())

    return '\n'.join(text_lines)


# Exemplo de uso
texto_extraido = extract_text_from_srt('captiona.srt')
print(texto_extraido)
