import zipfile

nome_novo_arquivo_zip = "novo_arquivo.zip"

with zipfile.ZipFile(nome_novo_arquivo_zip, 'w') as zip_ref:
    zip_ref.write('data_file.json')
    zip_ref.write('functional_programming.py')
    zip_ref.write('json_serialize.py')
