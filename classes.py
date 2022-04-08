from typing import List


class PontoGrid:

	def __init__(self, x: int, y: int, valor: object = None):
		self.x = x
		self.y = y
		self.valor = valor

	def to_tuple(self):
		return (self.x, self.y)

class PontoGridAstar(PontoGrid):

	def __init__(self, x: int, y: int, objeto: object = 0):
		self.f = 0
		self.g = 0
		self.h = 0
		self.pt_pai: PontoGridAstar = None
		super().__init__(x, y, objeto)

	

class Grid:
	n_linhas: int
	n_colunas: int
	n_pontos: int
	quadrante: int
	__mapa: dict = {}

	_pt_inicial: PontoGridAstar
	_pt_final: PontoGridAstar
	__y_mult = 1
	__x_mult = 1

	def __init__(self, qtd_linhas: int, qtd_colunas: int, quadrante: int):
		self.n_linhas = qtd_linhas
		self.n_colunas = qtd_colunas
		self.n_pontos = qtd_colunas * qtd_linhas
		self.quadrante = quadrante
		self.__mapa = self.GerarGrid(qtd_linhas, qtd_colunas, quadrante)

	@property
	def pt_inicial(self) -> PontoGridAstar:
		return self._pt_inicial

	@pt_inicial.setter
	def pt_inicial(self, ponto: PontoGrid):
		self._pt_inicial = self.__mapa[(ponto.x, ponto.y)]

	@property
	def pt_final(self) -> PontoGridAstar:
		return self._pt_final

	@pt_final.setter
	def pt_final(self, ponto: PontoGrid):
		self._pt_final = self.__mapa[(ponto.x, ponto.y)]

	def GerarGrid(self, qtd_linhas: int, qtd_colunas: int, quadrante: int) -> dict:

		mapa: dict = {}

		if (quadrante == 2):
			self.__x_mult = -1

		elif (quadrante == 3):
			self.__y_mult = -1
			self.__x_mult = -1

		if (quadrante == 4):
			self.__y_mult = -1

		for i_lin in range(qtd_linhas):
			for i_col in range(qtd_colunas):
				ponto = (self.__x_mult * i_col, self.__y_mult * i_lin)
				mapa[ponto] = PontoGridAstar(ponto[0], ponto[1])

		return mapa

	def GetPonto(self, x: int, y: int) -> PontoGridAstar:

		if (x, y) in self.__mapa: return self.__mapa[(x, y)]

		raise ValueError("O ponto com x = {} e y = {} não existe no plano!".format(x, y))

	def GetTodosPontos(self) -> List[PontoGridAstar]:
		return [self.__mapa[chave] for chave in self.__mapa]

	def get_posicoes_xy(self) -> List[tuple]:
		return [chave for chave in self.__mapa]

	def PontosAdjacentes(self, x: int, y: int) -> List[PontoGridAstar]:
		
		pts_saida = []

		# Se o ponto de entrada não existir no plano;
		if (x, y) not in self.__mapa:
			raise ValueError("O ponto(%d, %d) não existe no plano." % (x, y))

		if (x, y - 1) in self.__mapa: pts_saida.append(self.__mapa[(x, y - 1)])
		if (x - 1, y) in self.__mapa: pts_saida.append(self.__mapa[(x - 1, y)])
		if (x + 1, y) in self.__mapa: pts_saida.append(self.__mapa[(x + 1, y)])
		if (x, y + 1) in self.__mapa: pts_saida.append(self.__mapa[(x, y + 1)])

		return pts_saida

	def PontosObstaculos(self, simb_obstaculo: object) -> List[PontoGridAstar]:
		return [self.__mapa[xy] for xy in self.__mapa
		        if self.__mapa[xy].valor == simb_obstaculo]

	def GerarGridCaminho(self, trajeto_final: List[PontoGridAstar]):

		# Altere os símbolos dos pontos OBSTÁCULOS / barreiras;
		pts_bloqueados: List[PontoGridAstar] = self.PontosObstaculos(1)

		for obstaculo in pts_bloqueados:
			obstaculo.valor = "X"

		# Altere os símbolos dos pontos comuns;
		pts_comuns = [pt for pt in self.GetTodosPontos()
		              if (pt not in pts_bloqueados and pt not in trajeto_final)]

		for pt_comum in pts_comuns:
			pt_comum.valor = "-"

		# Altere os símbolos do ponto INICIAL e do ponto FINAL;
		self.pt_inicial.valor = "I"
		self.pt_final.valor = "F"

		for pt in trajeto_final:

			if (pt == self.pt_inicial or pt == self.pt_final): continue

			pt_plano = self.GetPonto(pt.x, pt.y)

			if (pt.x, pt.y) not in self.__mapa:
				raise ValueError(
					"O ponto (x = {}, y = {}) não pertence ao plano!".format(pt.x, pt.y))
			pt_plano.valor = "o"

			

	def __str__(self) -> str:

		# Monte a linha c/ numeração das colunas
		n_dig_col = len(str(self.n_colunas))

		# Concatene o índice de cada coluna, separando-os por um tab;
		numeracao_col = "     X\t" + "\t".join(
			[str(i * self.__x_mult).zfill(n_dig_col)
			 for i in range(self.n_colunas)]
		)
		barras_num_col = " Y\t" + "".join(["_\t"] * self.n_colunas)

		mapa_str = "{}\n{}\n".format(numeracao_col, barras_num_col)

		# Monte a linha c/ numeração das linhas
		n_dig_lin = len(str(self.n_linhas))

		for i_linha in range(self.n_linhas):
			# Multiple o índice da linha pelo -1 ou 1, obtido pelo quadrante;
			const_y = i_linha * self.__y_mult

			# Adicione o índice da linha atual;
			temp_linha_str = "{}|\t".format(str(const_y if const_y != 0 else " 0").zfill(n_dig_lin))

			# Concatene os símbolos de todos os pts da linha, insira um tab entre eles;
			temp_linha_str += "\t".join(
				[str(self.GetPonto(i_col * self.__x_mult, const_y).valor)
				 for i_col in range(self.n_colunas)]
			)
			mapa_str = "%s\n%s" % (mapa_str, temp_linha_str)

		return mapa_str

	def __contains__(self, ponto: PontoGrid):
		return (ponto.x, ponto.y) in self.__mapa
