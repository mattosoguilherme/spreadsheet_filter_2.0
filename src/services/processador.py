# src/services/processor.py
from datetime import datetime
import math

def process_data(df):
    clientes = {}
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.upper()
    print(df.columns)

    for _, row in df.iterrows():
        if row['STATUS'] != 'NÃO RECEBIDO':
            continue

        nome = row['CLIENTE']
        # Validação do telefone e remoção de ".0", com tratamento para NaN
        telefone = str(int(row['TEL'])) if not math.isnan(row['TEL']) else '0'  # Verifica se o valor é NaN
        vendedor = row.get('VENDEDOR', 'NÃO INFORMADO')
        quantidade = row['QTD']
        produto = row['PRODUTO']
        total = row['TOTAL']
        data_pedido = row.get('DATA', 'DATA NÃO INFORMADA')
        id_produto =  row.get('ID PRODUTO')

        if isinstance(data_pedido, datetime):
            data_pedido = data_pedido.strftime('%d/%m/%Y')

        if telefone not in clientes:
            clientes[telefone] = {
                "nome": nome,
                "telefone": telefone,
                "vendedor": vendedor,
                "sended": False,
                "pedidos": [],
                "total_comanda": 0
            }

        clientes[telefone]["pedidos"].append({
            "quantidade": quantidade,
            "produto": produto,
            "total": total,
            "data": data_pedido,
            "id_produto":id_produto
        })

        clientes[telefone]["total_comanda"] += total

    return clientes
