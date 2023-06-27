import json

data = {
        "Aluno1": {"name": "Ramon", "idade": "20"},
        "Aluno2": {"name": "Stephanie", "idade": "19"},
        "Aluno3": {"name": "Romulo", "idade": "18"}
}

#Transform em formato json e serializa os dados no arquivo
with open("data_file.json", "w") as arquivo:
    json.dump(data, arquivo)

#Transforma em formato json e coloca numa variável
#json_serializado = json.dumps(data)
#print(json_serializado)
