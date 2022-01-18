import cmath
import math

class Quaternion:
	'''Classe em que são definidas as operações entre quaternions e entre quaternions e números reais e complexos.'''
    
	def __init__(self, a1, a2, a3, a4):
		'''Inicializa o número quaterniônico.'''
		self._a1 = a1
		self._a2 = a2
		self._a3 = a3
		self._a4 = a4
	 
	def __add__(self, other):
		'''Implementa a soma de dois quaternions e a de um quaternion com um número à direita.'''
		if type(other) == Quaternion:
			return self._a1 + other._a1, self._a2 + other._a2, self._a3 + other._a3, self._a4 + other._a4
		if type(other) == int or type(other) == float:
			return self._a1 + other, self._a2, self._a3, self._a4
		if type(other) == complex:
			return self._a1 + other.real, self._a2 + other.imag, self._a3, self._a4
	
	def __radd__(self, other):
		'''Implementa a soma de um quaternion com um número à esquerda.'''
		if type(other) == int or type(other) == float:
			return self._a1 + other, self._a2, self._a3, self._a4
		if type(other) == complex:
			return self._a1 + other.real, self._a2 + other.imag, self._a3, self._a4
			
	def __iadd__(self, other):
		'''Implementa a soma de dois quaternions e a de um quaternion com um número a partir do operador +=.'''
		if type(other) == Quaternion:
			return self._a1 + other._a1, self._a2 + other._a2, self._a3 + other._a3, self._a4 + other._a4
		if type(other) == int or type(other) == float:
			return self._a1 + other, self._a2, self._a3, self._a4
		if type(other) == complex:
			return self._a1 + other.real, self._a2 + other.imag, self._a3, self._a4
	
	def __sub__(self, other):
		'''Implementa a subtração de dois quaternions e a de um quaternion com um número à direita.'''
		if type(other) == Quaternion:
			return self._a1 - other._a1, self._a2 - other._a2, self._a3 - other._a3, self._a4 - other._a4
		if type(other) == int or type(other) == float:
			return self._a1 - other, self._a2, self._a3, self._a4
		if type(other) == complex:
			return self._a1 - other.real, self._a2 - other.imag, self._a3, self._a4
		
	def __rsub__(self, other):
		'''Implementa a subtração de um quaternion com um número à esquerda.'''
		if type(other) == int or type(other) == float:
			return self._a1 - other, -self._a2, -self._a3, -self._a4
		if type(other) == complex:
			return self._a1 - other.real, self._a2 - other.imag, -self._a3, -self._a4
			
	def __isub__(self, other):
		'''Implementa a subtração de dois quaternions e a de um quaternion com um número a partir do operador -=.'''
		if type(other) == Quaternion:
			return self._a1 - other._a1, self._a2 - other._a2, self._a3 - other._a3, self._a4 - other._a4
		if type(other) == int or type(other) == float:
			return self._a1 - other, self._a2, self._a3, self._a4
		if type(other) == complex:
			return self._a1 - other.real, self._a2 - other.imag, self._a3, self._a4
			
	def conjugate(self):
		'''Dado um quaternion, retorna seu conjugado.'''
		return self._a1, self._a2 - 2*self._a2, self._a3 - 2*self._a3, self._a4 - 2*self._a4
	
	def __mul__(self, other):
		'''Implementa a multiplicação de dois quaternions e a de um quaternion com um número à direita.'''
		if type(other) == Quaternion:
			return self._a1*other._a1 - self._a2*other._a2 - self._a3*other._a3 - self._a4*other._a4, self._a1*other._a2 + self._a2*other._a1 + self._a3*other._a4 - self._a4*other._a3, self._a1*other._a3 - self._a2*other._a4 + self._a3*other._a1 + self._a4*other._a2, self._a1*other._a4 + self._a2*other._a3 - self._a3*other._a2 + self._a4*other._a1
		if type(other) == int or type(other) == float:
			return self._a1*other, self._a2*other, self._a3*other, self._a4*other
		if type(other) == complex:
			return self._a1*other.real - self._a2*other.imag, self._a1*other.imag + self._a2*other.real, self._a3*other.real + self._a4*other.imag, -self._a3*other.imag + self._a4*other.real
	
	def __rmul__(self, other):
		'''Implementa a multiplicação de um quaternion com um número à esquerda.'''
		if type(other) == int or type(other) == float:
			return self._a1*other, self._a2*other, self._a3*other, self._a4*other
		if type(other) == complex:
			return self._a1*other.real - self._a2*other.imag, self._a1*other.imag + self._a2*other.real, self._a3*other.real - self._a4*other.imag, self._a3*other.imag + self._a4*other.real
		
	def __imul__(self, other):
		'''Implementa a multiplicação de dois quaternions e a de um quaternion com um número a partir do operador *=.'''
		if type(other) == Quaternion:
			return self._a1*other._a1 - self._a2*other._a2 - self._a3*other._a3 - self._a4*other._a4, self._a1*other._a2 + self._a2*other._a1 + self._a3*other._a4 - self._a4*other._a3, self._a1*other._a3 - self._a2*other._a4 + self._a3*other._a1 + self._a4*other._a2, self._a1*other._a4 + self._a2*other._a3 - self._a3*other._a2 + self._a4*other._a1
		if type(other) == int or type(other) == float:
			return self._a1*other, self._a2*other, self._a3*other, self._a4*other
		if type(other) == complex:
			return self._a1*other.real - self._a2*other.imag, self._a1*other.imag + self._a2*other.real, self._a3*other.real + self._a4*other.imag, -self._a3*other.imag + self._a4*other.real
    
	def norm(self):
		'''Dado um quaternion, retorna sua norma.'''
		return math.sqrt(self._a1**2 + self._a2**2 + self._a3**2 + self._a4**2)
		
	def inverse(self):
		'''Dado um quaternion, retorna seu inverso.'''
		return self.conjugate()[0]/(self._a1**2 + self._a2**2 + self._a3**2 + self._a4**2), self.conjugate()[1]/(self._a1**2 + self._a2**2 + self._a3**2 + self._a4**2), self.conjugate()[2]/(self._a1**2 + self._a2**2 + self._a3**2 + self._a4**2), self.conjugate()[3]/(self._a1**2 + self._a2**2 + self._a3**2 + self._a4**2) 
	
	def __truediv__(self, other):
		'''Implementa a divisão de dois quaternions e a de um quaternion com um número à direita.'''
		if type(other) == Quaternion:
			return self._a1*other.inverse()[0] - self._a2*other.inverse()[1] - self._a3*other.inverse()[2] - self._a4*other.inverse()[3], self._a1*other.inverse()[1] + self._a2*other.inverse()[0] + self._a3*other.inverse()[3] - self._a4*other.inverse()[2], self._a1*other.inverse()[2] - self._a2*other.inverse()[3] + self._a3*other.inverse()[0] + self._a4*other.inverse()[1], self._a1*other.inverse()[3] + self._a2*other.inverse()[2] - self._a3*other.inverse()[1] + self._a4*other.inverse()[0]
		if type(other) == int or type(other) == float:
			return self._a1/other, self._a2/other, self._a3/other, self._a4/other 
		if type(other) == complex:
			new = Quaternion(other.real, other.imag, 0, 0)
			return self._a1*new.inverse()[0] - self._a2*new.inverse()[1] - self._a3*new.inverse()[2] - self._a4*new.inverse()[3], self._a1*new.inverse()[1] + self._a2*new.inverse()[0] + self._a3*new.inverse()[3] - self._a4*new.inverse()[2], self._a1*new.inverse()[2] - self._a2*new.inverse()[3] + self._a3*new.inverse()[0] + self._a4*new.inverse()[1], self._a1*new.inverse()[3] + self._a2*new.inverse()[2] - self._a3*new.inverse()[1] + self._a4*new.inverse()[0]
		
	def __rtruediv__(self, other):
		'''Implementa a divisão de um quaternion com um número à esquerda.'''
		new_truediv = Quaternion(self.__truediv__(other)[0], self.__truediv__(other)[1], self.__truediv__(other)[2], self.__truediv__(other)[3])
		if type(other) == int or type(other) == float:
			return new_truediv.inverse()
		if type(other) == complex:
			return new_truediv.inverse()
