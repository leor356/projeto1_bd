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

delegacias = set()
pessoas = set()
ocorrencias = set()
bos = set()
enderecos = set()
veiculos = set()

id_delegacia = 1
id_pessoa = 1
id_ocorrencia = 1
id_bo = 1
id_endereco = 1
id_veiculo = 1

delegacias_l = []
pessoas_l = []
ocorrencias_l = []
bos_l = []
enderecos_l = []
veiculos_l = []

# Reading data
for row in ur:
    # Tuples from data
    delegacia = (row[22], row[23])
    pessoa = (row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37], row[38], row[39], row[40], row[41], row[42], row[43])
    ocorrencia = (row[1], row[5], row[6], row[7], row[10], row[17], row[18], row[20], row[24], row[25], row[26], row[27])
    bo = (row[0], row[1], row[2], row[3], row[4], row[8], row[9], row[11], row[21], row[22], row[23])
    endereco = (row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19])
    veiculo = (row[44], row[45], row[46], row[47], row[48], row[49], row[50], row[51])

    # Delegacia
    if delegacia not in delegacias:
        delegacias.add(delegacia)

        delegacia.append(id_delegacia)
        id_delegacia = id_delegacia + 1

        delegacias_l.append(delegacia)

    # Endereco
    if endereco not in enderecos:
        enderecos.add(endereco)

        endereco.append(id_endereco)
        id_endereco = id_endereco + 1

        enderecos_l.append(endereco)
    else:
        print(enderecos_l.find(endereco))

    # BO
    if bo not in bos:
        bos.add(bo)

        bo.append(id_bo)
        id_bo = id_bo + 1

        bos.append(bo)

    # Ocorrencias
    if ocorrencia not in ocorrencias:
        ocorrencias.add(ocorrencia)

        ocorrencia.append(id_ocorrencia)
        id_ocorrencia = id_ocorrencia + 1

        ocorrencias_l.append(ocorrencia)

    # Pessoas
    pessoas.add(pessoa)

   

    

    

    # Veiculo
    veiculos.add(veiculo)

    # Objeto


# Delegacia

uw_list[0].writerows(delegacias)

# Pessoas
l_pessoas = []
id_pessoa = 1
for p in pessoas:
    lp = list(p)
    lp.append(str(id_pessoa))
    l_pessoas.append(lp)
    id_pessoa += 1

uw_list[1].writerows(l_pessoas)

# Ocorrencias
l_ocorrencias = []
id_ocorrencia = 1
for o in ocorrencias:
    lo = list(o)
    lo.append(str(id_ocorrencia))
    l_ocorrencias.append(lo)
    id_ocorrencia += 1

uw_list[2].writerows(l_ocorrencias)

# BOs
uw_list[3].writerows(bos)

# Enderecos
uw_list[4].writerows(enderecos)

# Veiculos
uw_list[5].writerows(veiculos)


# Closing files
arq.close()
for warq in warq_list:
    warq.close()

