# core/tests/utils.py

"""
Created on 23 de jul. de 2025

@author: masterdev

@summary: 📦 Função: debug_view_html(response, name="debug")
            ✅ Benefícios:
            Gera um arquivo .html no diretório local (/tmp/ no Linux/Mac ou tempfile.gettempdir() multiplataforma);

            Abre automaticamente no navegador (opcional);

            Ideal para rodar testes e ver o resultado como um usuário real.

@note: ✅ Resultado esperado:
            Ao rodar o teste, você verá algo assim no console:
            🧪 HTML salvo em: /tmp/raffle_draw_test.html
            E o navegador será aberto automaticamente com o conteúdo da página testada.
            Se quiser posso adaptar para Windows (sem abrir o navegador), ou enviar para uma pasta de projeto (media/test_htmls/).
            Quer customizar esse comportamento?
            Posso também incluir um flag open_browser=False para evitar abrir automaticamente.
"""

import os
import tempfile
import webbrowser


def debug_view_html(response, name="debug_view"):
    """
    Salva a resposta HTML em disco para inspeção manual.
    """
    html = response.content.decode("utf-8", errors="ignore")
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"{name}.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n🧪 HTML salvo em: {file_path}")
    try:
        webbrowser.open(f"file://{file_path}")
    except Exception as e:
        print(f"Erro ao abrir no navegador: {e}")
