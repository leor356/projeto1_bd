#!/usr/bin/python
# -*- coding: utf-8 -*-

arq_name = './tudao.csv'
w_arq_name = './t_unique.csv'

arq = open(arq_name, 'rb')
warq = open(w_arq_name, 'wb')


lines = arq.readlines()
lines.sort()
lines_set = set(lines)

warq.writelines(lines_set)

arq.close()
warq.close()