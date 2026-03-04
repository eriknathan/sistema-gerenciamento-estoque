import argparse
import re
import sys
from pathlib import Path


def fix_content(content):
    """
    Procura por tags {{ }}, {% %} e {# #} que se espalham por várias linhas
    e remove as quebras de linha contidas nelas.
    """

    def format_match(match):
        # Pega a tag inteira (que pode estar quebrada em várias linhas)
        text = match.group(0)
        # Substitui quebras de linha e retornos de carro por um espaço simples
        text = text.replace("\n", " ").replace("\r", "")
        # Removemos espaços em branco excessivos criados pela formatação da tag
        text = re.sub(r"\s+", " ", text)

        # Formata '==' para ter espaços apenas DENTRO das tags do Django
        # Procura por '==' sem os espaços adequados (ex: var==val)
        text = re.sub(r"(?<=[^\s])==|==(?=[^\s])", " == ", text)
        # Remove espaços duplos criados caso houvesse apenas um espaço
        text = re.sub(r" \s+==\s+ ", " == ", text)
        text = re.sub(r"\s+==\s+", " == ", text)

        return text

    # re.DOTALL permite que o '.' também coincida com quebras de linha ('\n')
    new_content = re.sub(r"\{\{.*?\}\}", format_match, content, flags=re.DOTALL)
    new_content = re.sub(r"\{%.*?%\}", format_match, new_content,
                         flags=re.DOTALL)
    new_content = re.sub(r"\{#.*?#\}", format_match, new_content,
                         flags=re.DOTALL)

    return new_content


def validate_templates(templates_dir, auto_fix=False):
    """
    Percorre a pasta de templates e verifica (ou corrige) se há tags do Django
    mal formatadas ou que não fecham na mesma linha.
    """
    templates_path = Path(templates_dir)
    if not templates_path.exists() or not templates_path.is_dir():
        print(f"Erro: O diretório '{templates_dir}' não foi encontrado.")
        sys.exit(1)

    # Regex para encontrar tags perfeitamente formadas NA MESMA LINHA
    regex_variavel_ok = re.compile(r"\{\{.*?\}\}")
    regex_bloco_ok = re.compile(r"\{%.*?%\}")
    regex_comentario_ok = re.compile(r"\{#.*?#\}")

    # Expressão regular para detectar abertura ou fechamento órfão
    regex_quebrada = re.compile(r"(\{\{|\}\}|\{%|%\}|\{#|#\})")

    # Expressão regular para encontrar locais com '==' sem espaços
    regex_espaco_igual = re.compile(
        r"(\{%|\{\{)[^}%]*?[^\s]==[^}%]*?(%\}|\}\})|"
        r"(\{%|\{\{)[^}%]*?==[^\s][^}%]*?(%\}|\}\})"
    )

    erros_encontrados = False
    arquivos_verificados = 0
    arquivos_corrigidos = 0

    print(f"Iniciando {'CORREÇÃO' if auto_fix else 'VALIDAÇÃO'} de templates "
          f"no diretório: {templates_path.resolve()}")

    for ext in ["*.html", "*.txt", "*.email"]:
        for filepath in templates_path.rglob(ext):
            arquivos_verificados += 1
            try:
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()

                # Se auto_fix estiver ativado, aplicamos a correção
                if auto_fix:
                    novo_conteudo = fix_content(content)
                    if novo_conteudo != content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(novo_conteudo)
                        print(f"✅ Arquivo corrigido: {filepath}")
                        arquivos_corrigidos += 1
                    continue

                # Modo de validação (linha por linha, estrito)
                lines = content.splitlines()
                for line_number, line in enumerate(lines, start=1):
                    clean_line = line
                    # Remove as tags que estão perfeitamente contidas
                    clean_line = regex_variavel_ok.sub("", clean_line)
                    clean_line = regex_bloco_ok.sub("", clean_line)
                    clean_line = regex_comentario_ok.sub("", clean_line)

                    # Se restou algo como {{, }}, {% etc., há sintaxe irregular
                    if regex_quebrada.search(clean_line):
                        erros_encontrados = True
                        print(f"❌ Erro encontrado no arquivo: {filepath}")
                        print(f"   Linha {line_number}: Tag mal formatada.")
                        print(f"   Conteúdo: {line.strip()}")
                        print("-" * 60)

                    # Checagem de falta de espaço no '=='
                    if regex_espaco_igual.search(line):
                        erros_encontrados = True
                        print(f"❌ Erro encontrado no arquivo: {filepath}")
                        print(f"   Linha {line_number}: '==' sem espaços.")
                        print(f"   Conteúdo: {line.strip()}")
                        print("-" * 60)
            except Exception as e:
                print(f"Erro ao processar o arquivo {filepath}: {e}")
                erros_encontrados = True

    print(f"\nResumo da {'Correção' if auto_fix else 'Validação'}:")
    print(f"Arquivos verificados: {arquivos_verificados}")

    if auto_fix:
        print(f"Arquivos corrigidos: {arquivos_corrigidos}")
        print("✅ Correção finalizada!")
        sys.exit(0)
    else:
        if erros_encontrados:
            print("❌ Validação falhou! Corrija os erros ou use --fix.")
            sys.exit(1)
        else:
            print("✅ Nenhum erro encontrado. Tudo pronto!")
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validador de tags Django.")
    parser.add_argument("--fix", action="store_true", help="Corrige tags.")
    args = parser.parse_args()

    # templates_dir = "templates"
    validate_templates("templates", auto_fix=args.fix)
