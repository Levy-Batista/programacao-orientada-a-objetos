from quaternion.quaternion import Quaternion 
import math

class Cube:
	'''Classe para representar o cubo, com um método que rotaciona seus vértices e um método para visualizar esses vértices.'''

	def __init__(self, vertices):
		'''Inicializa os vértices do cubo.'''
		self._vertices = [(vertices[0][0], vertices[0][1], vertices[0][2]), (vertices[1][0], vertices[1][1], vertices[1][2]), (vertices[2][0], vertices[2][1], vertices[2][2]), (vertices[3][0], vertices[3][1], vertices[3][2]), (vertices[4][0], vertices[4][1], vertices[4][2]), (vertices[5][0], vertices[5][1], vertices[5][2]), (vertices[6][0], vertices[6][1], vertices[6][2]), (vertices[7][0], vertices[7][1], vertices[7][2])]
		
		#Lista que guarda as novas coordenadas dos vértices após a rotação.
		self._newvertices = []
		
	def rotation(self, axis, angle):
		'''Rotaciona os vértices com a fórmula rpr^-1, dada no roteiro, como um produto quaterniônico.'''
	
		#Define r como um quaternion.
		r = Quaternion(math.cos(angle/2), math.sin(angle/2)/math.sqrt(axis[0]**2 + axis[1]**2 + axis[2]**2)*axis[0], math.sin(angle/2)/math.sqrt(axis[0]**2 + axis[1]**2 + axis[2]**2)*axis[1], math.sin(angle/2)/math.sqrt(axis[0]**2 + axis[1]**2 + axis[2]**2)*axis[2])
		
		#Aplica o mesmo processo para cada um dos 8 vértices.
		for i in range(len(self._vertices)):
			p = Quaternion(0, self._vertices[i][0], self._vertices[i][1], self._vertices[i][2]) 
			intermediate = r*p
			
			#r*p retorna uma tupla, então é necessário inicializar um novo quaternion new_rp com os valores de r*p.
			new_rp = Quaternion(intermediate[0], intermediate[1], intermediate[2], intermediate[3])
			
			#Da mesma forma, r.inverse() retorna uma tupla, então r_inverse é inicializado como quaternion para ser o termo r^-1. 
			r_inverse = Quaternion(r.inverse()[0], r.inverse()[1], r.inverse()[2], r.inverse()[3])
			p_rot = new_rp*r_inverse
			
			#Como citado no roteiro, o termo a0 de a0 + a1*i + a2*j + a3*k não interessa para encontrar as novas coordenadas do vértice.
			coord = [p_rot[1], p_rot[2], p_rot[3]]
			
			#Arredonda todas as coordenadas na sexta casa decimal.
			for j in range(len(coord)):
				if abs(coord[j] - round(coord[j], 6)) <= 10**(-6):
					if round(coord[j], 6) == 0:
						coord[j] = 0.0
					else:
						coord[j] = round(coord[j], 6)
			point = (coord[0], coord[1], coord[2])
			
			#Guarda as novas coordenadas do vértice que estão em uma tupla.
			self._newvertices.append(point)
			
	def get_vertices(self):
		'''Retorna as novas coordenadas dos vértices.'''
		return self._newvertices

#Cria-se um objeto com as coordenadas originais do cubo.		
solid = Cube([(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1)])

#A ausência de condição de parada se deve à possibilidade do usuário fazer quantas rotações quiser.
while True:
	line = input('Digite as coordenadas do ponto que, junto com a origem, definem um eixo (separadas por espaço): ').split()
	for i in range(len(line)):
		line[i] = float(line[i])
	alpha = float(input('Digite um ângulo de rotação, em graus: '))
	solid.rotation(line, math.pi*alpha/180)
	print(solid.get_vertices())
	
	#Cria-se uma nova referência para o objeto solid, agora o cubo rotacionado passa a ser o original e o processo segue.
	solid = Cube(solid.get_vertices())
