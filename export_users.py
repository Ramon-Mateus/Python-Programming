import os
import json
import zipfile
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from solicitacao.models import Solicitacao, DocumentoExigido, Documento


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return model_to_dict(o)
        return super().default(o)


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        # solicitacoes = Solicitacao.objects.all()
        
        # for solicitacao in solicitacoes:
            
        #     data = self.dumpSolicitacao(solicitacao)
        #     documentos = Documento.objects.filter(solicitacao=solicitacao)
        #     self.create_zip_file(data, documentos, solicitacao.selecionado.chamada.edital.identificacao, solicitacao.selecionado.cpf)
        
        solicitacao = Solicitacao.objects.first()
        data = self.dumpSolicitacao(solicitacao)
        documentos = Documento.objects.filter(solicitacao=solicitacao)
        edital = solicitacao.selecionado.chamada.edital.identificacao
        selecionado_cpf = solicitacao.selecionado.cpf
        self.create_zip_file(data, documentos, edital, selecionado_cpf)

    def dumpSolicitacao(self, solicitacao):
        data = model_to_dict(solicitacao)

        documentos_exigidos = DocumentoExigido.objects.filter(edital=solicitacao.selecionado.chamada.edital)
        exigidos = []
        for documento_exigido in documentos_exigidos:
            documento = {
                'documentacao': model_to_dict(documento_exigido.documentacao),
                'lista': documento_exigido.lista
            }
            exigidos.append(documento)

        documentos = Documento.objects.filter(solicitacao=solicitacao)

        documentos_data = []
        for documento in documentos:
            documento_data = model_to_dict(documento)
            documento_data['arquivo'] = documento.arquivo.path
            documentos_data.append(documento_data)
        
        data['selecionado'] = model_to_dict(solicitacao.selecionado)
        data['selecionado']['chamada'] = model_to_dict(solicitacao.selecionado.chamada)
        data['selecionado']['chamada']['edital'] = model_to_dict(solicitacao.selecionado.chamada.edital)
        data['selecionado']['chamada']['edital']['documentos_exigidos'] = exigidos
        data['selecionado']['matriz_curso'] = model_to_dict(solicitacao.selecionado.matriz_curso)
        data['selecionado']['ano_letivo'] = model_to_dict(solicitacao.selecionado.ano_letivo)
        data['selecionado']['periodo_letivo'] = model_to_dict(solicitacao.selecionado.periodo_letivo)
        data['selecionado']['turno'] = model_to_dict(solicitacao.selecionado.turno)
        data['selecionado']['forma_ingresso'] = model_to_dict(solicitacao.selecionado.forma_ingresso)
        data['selecionado']['polo'] = model_to_dict(solicitacao.selecionado.polo) if solicitacao.selecionado.polo is not None else None
        data['selecionado']['convenio'] = model_to_dict(solicitacao.selecionado.convenio) if solicitacao.selecionado.convenio is not None else None
        data['selecionado']['cota_sistec'] = model_to_dict(solicitacao.selecionado.cota_sistec) if solicitacao.selecionado.cota_sistec is not None else None
        data['selecionado']['cota_mec'] = model_to_dict(solicitacao.selecionado.cota_mec) if solicitacao.selecionado.cota_mec is not None else None
        data['selecionado']['nacionalidade'] = model_to_dict(solicitacao.selecionado.nacionalidade)
        data['linha_pesquisa'] = model_to_dict(solicitacao.linha_pesquisa) if solicitacao.linha_pesquisa is not None else None
        data['estado_civil_pai'] = model_to_dict(solicitacao.estado_civil_pai) if solicitacao.estado_civil_pai is not None else None
        data['tipo_necessidade_especial'] = model_to_dict(solicitacao.tipo_necessidade_especial) if solicitacao.tipo_necessidade_especial is not None else None
        data['superdotacao'] = model_to_dict(solicitacao.superdotacao) if solicitacao.superdotacao is not None else None
        data['poder_publico_responsavel_transporte'] = model_to_dict(solicitacao.poder_publico_responsavel_transporte) if solicitacao.poder_publico_responsavel_transporte is not None else None
        data['tipo_veiculo'] = model_to_dict(solicitacao.tipo_veiculo) if solicitacao.tipo_veiculo is not None else None
        data['tipo_sanguineo'] = model_to_dict(solicitacao.tipo_sanguineo) if solicitacao.tipo_sanguineo is not None else None
        data['pais_origem'] = model_to_dict(solicitacao.pais_origem) if solicitacao.pais_origem is not None else None
        data['estado_naturalidade'] = model_to_dict(solicitacao.estado_naturalidade) if solicitacao.estado_naturalidade is not None else None
        data['naturalidade'] = model_to_dict(solicitacao.naturalidade) if solicitacao.naturalidade is not None else None
        data['raca'] = model_to_dict(solicitacao.raca) if solicitacao.raca is not None else None
        data['uf_emissao_rg'] = model_to_dict(solicitacao.uf_emissao_rg) if solicitacao.uf_emissao_rg is not None else None
        data['orgao_emissao_rg'] = model_to_dict(solicitacao.orgao_emissao_rg) if solicitacao.orgao_emissao_rg is not None else None
        data['uf_emissao_titulo_eleitor'] = model_to_dict(solicitacao.uf_emissao_titulo_eleitor) if solicitacao.uf_emissao_titulo_eleitor is not None else None
        data['raestado_emissao_carteira_reservistaca'] = model_to_dict(solicitacao.raca) if solicitacao.raca is not None else None
        data['nivel_ensino_anterior'] = model_to_dict(solicitacao.nivel_ensino_anterior) if solicitacao.nivel_ensino_anterior is not None else None
        data['cidade'] = model_to_dict(solicitacao.cidade)
        data['sexo'] = model_to_dict(solicitacao.sexo)
        data['estado_civil'] = model_to_dict(solicitacao.estado_civil)
        data['estado_civil_mae'] = model_to_dict(solicitacao.estado_civil_mae)
        data['parentesco_responsavel'] = model_to_dict(solicitacao.parentesco_responsavel)
        data['tipo_zona_residencial'] = model_to_dict(solicitacao.tipo_zona_residencial)
        data['tipo_instituicao_origem'] = model_to_dict(solicitacao.tipo_instituicao_origem)
        data['ano_conclusao_estudo_anterior'] = model_to_dict(solicitacao.ano_conclusao_estudo_anterior)
        data['tipo_certidao'] = model_to_dict(solicitacao.tipo_certidao)
        data['documentos'] = documentos_data
        json_data = json.dumps(data, cls=CustomJSONEncoder, indent = 4)
        
        return json_data
        # print(json_data)




        # # Especifica o caminho do arquivo onde o JSON será salvo
        # caminho_atual = os.getcwd()
        # caminho_arquivo = os.path.join(caminho_atual, 'data.json')

        # # Salva o JSON no arquivo
        # with open(caminho_arquivo, 'w') as arquivo:
        #     arquivo.write(json_data)





        # Apenas para teste
        # solicitacoes = Solicitacao.objects.all()
        
        # for solicitaca in solicitacoes:
        #     if (solicitaca.selecionado.nacionalidade == None):
        #         data = model_to_dict(solicitaca)
        #         data = model_to_dict(solicitaca)
        #         data['utiliza_transporte_escolar_publico'] = model_to_dict(solicitaca.utiliza_transporte_escolar_publico)
        #         # data['linha_pesquisa'] = model_to_dict(solicitaca.linha_pesquisa) if solicitaca.linha_pesquisa != None else None
        #         break













        # for solicitacao in Solicitacao.objects.all():
        #     numero_edital = solicitacao.selecionado.chamada.edital.numero
        #     pasta_edital = os.path.join(settings.MEDIA_ROOT, numero_edital)
        #     os.makedirs(pasta_edital, exist_ok=True)
            
        #     # Cria um dicionário com os dados da solicitação
        #     dados_solicitacao = model_to_dict(solicitacao)
            
        #     # Caminho para o arquivo JSON
        #     json_path = os.path.join(pasta_edital, 'dados.json')
            
        #     # Salva os dados da solicitação no arquivo JSON
        #     with open(json_path, 'w') as f:
        #         json.dump(dados_solicitacao, f)
            
        #     # Cria uma pasta para os arquivos da solicitação
        #     pasta_solicitacao = os.path.join(pasta_edital, str(solicitacao.id))
        #     os.makedirs(pasta_solicitacao, exist_ok=True)
            
        #     # Copia os arquivos para a pasta da solicitação
        #     for documento in solicitacao.documentos.all():
        #         origem = documento.arquivo.path
        #         destino = os.path.join(pasta_solicitacao, os.path.basename(origem))
        #         shutil.copyfile(origem, destino)
            
        #     # Comprime a pasta em um arquivo ZIP
        #     zip_path = shutil.make_archive(pasta_edital, 'zip', pasta_edital)
            
        #     # Remove a pasta do edital
        #     shutil.rmtree(pasta_edital)
            
        #     # O processo recomeça com o próximo edital

    def create_zip_file(self, data, documentos, edital_numero, selecionado_cpf):
        # Criar o diretório para armazenar o arquivo ZIP
        zip_dir = os.path.join(settings.MEDIA_ROOT, 'zip_files')
        os.makedirs(zip_dir, exist_ok=True)

        # Criar um arquivo ZIP
        zip_file_path = os.path.join(zip_dir, f'{edital_numero}.zip')
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Salvar os dados recebidos como um arquivo JSON dentro do ZIP
            json_data = json.dumps(data, indent=4)
            zip_file.writestr(f'{selecionado_cpf}.json', json_data)

            # Adicionar os arquivos de documentos ao ZIP
            for documento in documentos:
                if documento.arquivo:
                    file_path = documento.arquivo.path
                    file_name = os.path.basename(file_path)
                    zip_file.write(file_path, file_name)

        # Retorna o caminho do arquivo ZIP gerado
        # return zip_file_path