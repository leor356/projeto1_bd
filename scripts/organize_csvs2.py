#!/usr/bin/python
# -*- coding: utf-8 -*-

# UTF8 Stuff

import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# Defining paths

path_in = './files/'
arq_name = path_in + 't_unique.csv'

path_out = './files/orga/'
list_of_files = []
list_of_files.append(path_out + 'delegacias.csv')
list_of_files.append(path_out + 'pessoas.csv')
list_of_files.append(path_out + 'ocorrencias.csv')
list_of_files.append(path_out + 'bo.csv')
list_of_files.append(path_out + 'endereco.csv')
list_of_files.append(path_out + 'veiculo.csv')
list_of_files.append(path_out + 'objeto.csv')

list_of_files.append(path_out + 'les_corporal.csv')
list_of_files.append(path_out + 'morte_susp.csv')
list_of_files.append(path_out + 'homicidio.csv')
list_of_files.append(path_out + 'roubo.csv')
list_of_files.append(path_out + 'furto.csv')
list_of_files.append(path_out + 'outras_oco.csv')

list_of_files.append(path_out + 'registro_obito_iml.csv')
list_of_files.append(path_out + 'declaracao_obito.csv')

# Printing list of files
# for st in list_of_files:
#     print(st)


# Opening input file
csv_props =  {'delimiter':'\t', 'quotechar':'\"'}

arq = open(arq_name, 'rb')
ur = UnicodeReader(arq, **csv_props)


# Opening output files
uw_list = []
warq_list = []
for warq_name in list_of_files:
    warq = open(warq_name, 'wb')
    warq_list.append(warq)
    uw_list.append(UnicodeWriter(warq, quoting=csv.QUOTE_MINIMAL, **csv_props))


# Organizing data
id_delegacia = 1
id_pessoa = 1
id_ocorrencia = 1
id_bo = 1
id_endereco = 1
id_objeto = 1

delegacias = dict()
pessoas = dict()
ocorrencias = dict()
bos = dict()
enderecos = dict()
objetos = dict()

veiculos = set()
les_corporal_tab = set()
morte_suspeita_tab = set()
homicidio_tab = set()
outras_oc_tab = set()
roubo_tab = set()
furto_tab = set()

# Reading data
for row in ur:
    # Tuples from data

   # Delegacia = nome, circunscricao
    delegacia = (row[22], row[23])

    if delegacia not in delegacias:
        delegacias[delegacia] = id_delegacia
        id_delegacia += 1

    # pessoa = NOMEPESSOA, TIPOPESSOA, VITIMAFATAL, RG, RG_UF, NATURALIDADE, NACIONALIDADE, SEXO, 
    #   DATANASCIMENTO, IDADE, ESTADOCIVIL, PROFISSAO, GRAUINSTRUCAO, CORCUTIS, NATUREZAVINCULADA, TIPOVINCULO
    pessoa = (row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37], row[38], row[39], row[40], row[41], row[42], row[43])
    if pessoa not in pessoas:
        pessoas[pessoa] = id_pessoa
        id_pessoa += 1

    # Veiculo = placa, UF, CIDADE, COR, MARCA, ANO_FABRICACAO, ANO_MODELO, TIPO_VEICULO
    veiculo = (row[44], row[45], row[46], row[47], row[48], row[49], row[50], row[51])

    if veiculo not in veiculos:
        veiculos.add(veiculo)

    # objeto = nome
    if (row[25].lower().find(u'roubo') != -1) or (row[25].lower().find(u'furto') != -1):
        if row[25].lower().find(u'interior de veiculo') != -1:
            objeto = (u'interior de veiculo', u'0')

        elif row[25].lower().find(u'veículo') != -1 or row[25].lower().find(u'veiculo') != -1:
            objeto = (u'veiculo', str(veiculo[0]))

        elif row[25].lower().find(u'transeunte') != -1:
            objeto = (u'transeunte', u'0')

        elif row[25].lower().find(u'estabelecimento') != -1:
            objeto = (u'estabelecimento comercial', u'0')

        elif row[25].lower().find(u'carga') != -1:
            objeto = (u'outros', u'0')

        elif row[25].lower().find(u'residencia') != -1:
            objeto = (u'residencia', u'0')

        elif row[25].lower().find(u'interior de transporte') != -1:
            objeto = ( u'interior transporte coletivo', u'0')

        else:
            objeto = (u'outros', u'0')

        if objeto not in objetos:
            objetos[objeto] = id_objeto
            id_objeto += 1


    # Endereco = LOGRADOURO, NUMERO, BAIRRO, CIDADE, UF, LATITUDE, LONGITUDE, DESCRICAOLOCAL
    endereco = (row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19])

    if endereco not in enderecos:
        enderecos[endereco] = id_endereco
        id_endereco += 1

    # bo = ANO_BO, NUM_BO, NUMERO_BOLETIM, BO_INICIADO, BO_EMITIDO, DATAELABORACAO, BO_AUTORIA, NUMERO_BOLETIM_PRINCIPAL, SOLUCAO, ID_DELEGACIA
    bo = (row[0], row[1], row[2], row[3], row[4], row[8], row[9], row[11], row[21], str(delegacias[delegacia]))
    if bo not in bos:
        bos[bo] = id_bo
        id_bo += 1

    # ocorrencia = ID_BO, DATAOCORRENCIA, PERIDOOCORRENCIA, DATACOMUNICACAO, FLAGRANTE, ID_ENDERECO, EXAME, ESPECIE, RUBRICA, DESDOBRAMENTO, STATUS
    ocorrencia = (str(bos[bo]), row[5], row[6], row[7], row[10], str(enderecos[endereco]), row[20], row[24], row[25], row[26], row[27])
    if ocorrencia not in ocorrencias:
        # Tratando os tipos de ocorrencia
        if row[25].lower().find(u'lesão') != -1:

            if row[25].lower().find(u'morte') != -1:
                les_corporal = (str(id_ocorrencia), u'S', str(pessoas[pessoa]))
            else:
                les_corporal = (str(id_ocorrencia), u'N', str(pessoas[pessoa]))
            les_corporal_tab.add(les_corporal)

        elif row[25].lower().find(u'morte') != -1:
            morte_susp = (str(id_ocorrencia), u'', str(pessoas[pessoa]))
            morte_suspeita_tab.add(morte_susp)

        elif row[25].lower().find(u'homicídio') != -1:
            if row[25].lower().find(u'simples') != -1:
                homicidio = (str(id_ocorrencia), u'simples', str(pessoas[pessoa]))
            else:
                homicidio = (str(id_ocorrencia), u'qualificado', str(pessoas[pessoa]))
            homicidio_tab.add(homicidio)

        elif row[25].lower().find(u'roubo') != -1:
            roubo = (str(id_ocorrencia), str(pessoas[pessoa]), str(objetos[objeto]))
            roubo_tab.add(roubo)

        elif row[25].lower().find(u'furto') != -1:
            furto = (str(id_ocorrencia), str(pessoas[pessoa]), str(objetos[objeto]))
            furto_tab.add(furto)
        else:
            outro = (str(id_ocorrencia), str(pessoas[pessoa]))

        ocorrencias[ocorrencia] = id_ocorrencia
        id_ocorrencia += 1

arq.close()    

######
# IML 
######

arq_name = path_in + 'iml.csv'

# Opening input file
arq = open(arq_name, 'rb')
ur = UnicodeReader(arq, **csv_props)

# Opening output files
uw_list = []
warq_list = []
for warq_name in list_of_files:
    warq = open(warq_name, 'wb')
    warq_list.append(warq)
    uw_list.append(UnicodeWriter(warq, quoting=csv.QUOTE_MINIMAL, **csv_props))

registros_obitos = dict()
declaracoes_obito = dict()
id_registro = 1
id_declaracao = 1

for row in ur:
    # Declaracao Obito
    declaracao_obito = (row[10], row[9])
    if declaracao_obito not in declaracoes_obito:
        declaracoes_obito[declaracao_obito] = id_declaracao
        id_declaracao += 1

    # Delegacias
    delegacia = (row[4], u'')
    if delegacia not in delegacias:
        delegacias[delegacia] = id_delegacia
        id_delegacia += 1

    # bo = ANO_BO, NUM_BO, NUMERO_BOLETIM, BO_INICIADO, BO_EMITIDO, DATAELABORACAO, BO_AUTORIA, NUMERO_BOLETIM_PRINCIPAL, SOLUCAO, ID_DELEGACIA
    bo = (row[1], row[2], u'', u'', u'', u'', u'', u'', u'', str(delegacias[delegacia]))
    if bo not in bos:
        bos[bo] = id_bo
        id_bo += 1

    # Ocorrencia = ID_BO, DATAOCORRENCIA, PERIDOOCORRENCIA, DATACOMUNICACAO, FLAGRANTE, ID_ENDERECO, EXAME, ESPECIE, RUBRICA, DESDOBRAMENTO, STATUS
    ocorrencia = (str(bos[bo]), u'', u'', u'', u'', u'0', u'', u'', u'', u'', u'')
    if ocorrencia not in ocorrencias:
        ocorrencias[ocorrencia] = id_ocorrencia
        id_ocorrencia += 1

    # registro_obito = DataEntradaIML, num_laudo, ano_laudo, id_declaracao_obito, id_ocorrencia
    registro_obito = (row[0], row[5], row[6], str(declaracoes_obito[declaracao_obito]), str(ocorrencias[ocorrencia]))
    if registro_obito not in registros_obitos:
        registros_obitos[registro_obito] = id_registro
        id_registro += 1

# Delegacia
delegacias_l = []
for d in delegacias:
    id_delegacia = delegacias[d]
    d = list(d)
    d.append(str(id_delegacia))
    delegacias_l.append(d)

uw_list[0].writerows(delegacias_l)

# Pessoas
pessoas_l = []
for p in pessoas:
    id_pessoa = pessoas[p]
    p = list(p)
    p.append(str(id_pessoa))
    pessoas_l.append(p)

uw_list[1].writerows(pessoas_l)

# Ocorrencias
ocorrencias_l = []
for o in ocorrencias:
    id_ocorrencia = ocorrencias[o]
    o = list(o)
    o.append(str(id_ocorrencia))
    ocorrencias_l.append(o)

uw_list[2].writerows(ocorrencias_l)

# BOs
bos_l = []
for b in bos:
    id_bo = bos[b]
    b = list(b)
    b.append(str(id_bo))
    bos_l.append(b)

uw_list[3].writerows(bos_l)

# Enderecos
enderecos_l = []
for e in enderecos:
    id_endereco = enderecos[e]
    e = list(e)
    e.append(str(id_endereco))
    enderecos_l.append(e)

uw_list[4].writerows(enderecos_l)

# Veiculos
uw_list[5].writerows(veiculos)

# Objetos
objetos_l = []
for o in objetos:
    id_objeto = objetos[o]
    o = list(o)
    o.append(str(id_objeto))
    objetos_l.append(o)

uw_list[6].writerows(objetos_l)

# Lesao corporal
uw_list[7].writerows(les_corporal_tab)

# Morte suspeita
uw_list[8].writerows(morte_suspeita_tab)

# Homicidio
uw_list[9].writerows(homicidio_tab)

# Roubo
uw_list[10].writerows(roubo_tab)

# Furto
uw_list[11].writerows(furto_tab)

# Outras Ocorrencias
uw_list[12].writerows(outras_oc_tab)

# registro_obito_iml
registros_obitos_l = []
for r in registros_obitos:
    id_registro_obito = registros_obitos[r]
    r = list(r)
    r.append(str(id_registro_obito))
    registros_obitos_l.append(r)

uw_list[13].writerows(registros_obitos_l)

# declaracao_obito
declaracoes_obito_l = []
for d in declaracoes_obito:
    id_declaracao = declaracoes_obito[d]
    d = list(d)
    d.append(str(id_declaracao))
    declaracoes_obito_l.append(d)

uw_list[14].writerows(declaracoes_obito_l)

# Closing files
arq.close()
for warq in warq_list:
    warq.close()
