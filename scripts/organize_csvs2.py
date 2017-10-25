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
id_veiculo = 1

delegacias = dict()
pessoas = dict()
ocorrencias = dict()
bos = dict()
enderecos = dict()
veiculos = dict()

# Reading data
for row in ur:
    # Tuples from data

   # Delegacia = nome, circunscricao
    delegacia = (row[22], row[23])

    if delegacia not in delegacias:
        delegacias[delegacia] = id_delegacia
        id_delegacia += 1

    # Veiculo = placa, UF, CIDADE, COR, MARCA, ANO_FABRICACAO, ANO_MODELO, TIPO_VEICULO
    veiculo = (row[44], row[45], row[46], row[47], row[48], row[49], row[50], row[51])

    if veiculo not in veiculos:
        veiculos[veiculo] = id_veiculo
        id_veiculo += 1

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

        ocorrencias[ocorrencia] = id_ocorrencia
        id_ocorrencia += 1

    # pessoa = NOMEPESSOA, TIPOPESSOA, VITIMAFATAL, RG, RG_UF, NATURALIDADE, NACIONALIDADE, SEXO, 
    #   DATANASCIMENTO, IDADE, ESTADOCIVIL, PROFISSAO, GRAUINSTRUCAO, CORCUTIS, NATUREZAVINCULADA, TIPOVINCULO
    pessoa = (row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37], row[38], row[39], row[40], row[41], row[42], row[43])
    if pessoa not in pessoas:
        pessoas[pessoa] = id_pessoa
        id_pessoa += 1


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

uw_list[2].writerows(l_ocorrencias)

# BOs
bos_l = []
for b in bos:
    id_bo = bos[b]
    b = list(b)
    b.append(str(id_bo))
    bos_l.append(b)

uw_list[3].writerows(bos)

# Enderecos
enderecos_l = []
for e in enderecos:
    id_endereco = enderecos[endereco]
    e = list(e)
    e.append(str(id_endereco))
    enderecos_l.append(e)

uw_list[4].writerows(enderecos)

# Veiculos
uw_list[5].writerows(veiculos)


# Closing files
arq.close()
for warq in warq_list:
    warq.close()

