from flask import Flask, request, jsonify
from flasgger import Swagger
import pandas as pd
import os
from src.services.processador import process_data
from src.services.file_handler import load_excel, save_json

app = Flask(__name__)
Swagger(app)  # Inicializa o Swagger

@app.route('/filter', methods=['POST'])
def filter_spreadsheet():
    """
    Endpoint para filtrar dados de um arquivo Excel.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: false  # Não obrigatório
        description: O arquivo Excel contendo os dados. Caso não seja enviado, será utilizado o arquivo fixo no servidor.
      - name: sheet_name
        in: query
        type: string
        required: false
        description: Nome da aba do Excel que será lida. Se não especificado, a aba padrão 'ABRIL 2025' será usada.
    responses:
      200:
        description: Lista de clientes filtrados
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID do cliente
              nome:
                type: string
                description: Nome do cliente
              email:
                type: string
                description: Email do cliente
      400:
        description: Erro, nenhum arquivo enviado (caso você precise processar um arquivo).
    """
    file_path = os.path.join("c:/arkg.solutions/solutions/agentes/maju/spreadsheet_filter_2.0/data/", 'controle.xlsm')
    output_file = os.path.join("c:/arkg.solutions/solutions/agentes/maju/spreadsheet_filter_2.0/out/", 'clientes.json')

    # Verifica se o parâmetro 'sheet_name' foi enviado na URL, se não, usa "ABRIL 2025"
    sheet_name = request.args.get('sheet_name', 'ABRIL 2025')

    # Se um arquivo for enviado, usaremos ele. Caso contrário, usaremos o arquivo fixo
    if 'file' in request.files:
        file = request.files['file']
        df = pd.read_excel(file, sheet_name=sheet_name)
    else:
        # Caso nenhum arquivo seja enviado, usa o arquivo fixo no servidor
        df = load_excel(file_path, sheet_name=sheet_name)

    # Processa os dados
    clientes = process_data(df)
    save_json(list(clientes.values()), output_file)   

    # Retorna a lista de clientes como JSON
    return jsonify(list(clientes.values()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    print("Acesse http://localhost:5000/apidocs para ver a documentação do Swagger")
