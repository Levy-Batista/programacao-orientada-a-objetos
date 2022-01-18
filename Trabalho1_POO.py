import sys

entrada = open(sys.argv[1], encoding='utf-8')
saida = open(sys.argv[1] + '.ana', 'w', encoding='utf-8')

#dicionário em que os anagramas serão armazenados.
#palavras que são anagramas terão o mesmo valor retornado pela função sorted().
#esses sorted() serão as chaves e os valores associados serão listas com todos os anagramas.
conjunto_anagrama = {}

for palavra in entrada.readlines():
	#é necessário a conversão str() porque a função sorted() retorna uma lista.
	s = str(sorted(palavra.strip().lower()))
	#verifica se já existe anagramas da str palavra no dicionário.
	if s in conjunto_anagrama.keys():
		conjunto_anagrama[s].append(palavra.strip().lower())
	#caso contrário, cria-se uma nova chave associada a essa palavra.
	else:
		conjunto_anagrama[s] = []
		conjunto_anagrama[s].append(palavra.strip().lower())


for chave in conjunto_anagrama.keys():
	#organiza os conjuntos de anagramas em ordem alfanumérica.
	linha = sorted(conjunto_anagrama[chave])
	saida.write(linha[0])
	for k in range(1, len(linha)):
		saida.write(', ' + linha[k])
	saida.write('\n')

entrada.close()
saida.close()
