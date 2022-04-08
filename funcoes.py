from os import path
from classes import Grid, PontoGridAstar, PontoGrid
from typing import List

COD_OBSTACULO = 1

def CalcularDistanciaPontos(ponto_1: PontoGrid, ponto_2: PontoGrid) -> int:
	return abs(ponto_1.x - ponto_2.x) + abs(ponto_1.y - ponto_2.y)

def CalcularCaminhoGrid(plano: Grid, pt_inicial: PontoGrid, pt_final: PontoGrid,
                 simbolo_bloqueio: object) -> List[PontoGridAstar]:

	# Defina como o primeiro ponto corrente, o ponto inicial recebido;
	pt_atual = pt_inicial

	# Armazene os nós já percorridos (p/ evitar laços s/ fim e mov. desnecessários)
	pts_fechados: List[PontoGridAstar] = []
	pts_abertos: List[PontoGridAstar] = [pt_atual]

	# Armazene os pontos que representam obstáculos;
	obstaculos = plano.PontosObstaculos(simbolo_bloqueio)

	encontrou = False

	# Enquanto houver pontos candidatos a serem verificados;
	while (pts_abertos):

		# Obtenha o pt da lista de abertos c/ o menor custo final;
		pts_abertos = sorted(pts_abertos, key=lambda pt: pt.f)
		pt_atual: PontoGridAstar = pts_abertos.pop(0)

		# Adicione o ponto atual na lista de pontos percorridos;
		pts_fechados.append(pt_atual)

		if pt_atual == pt_final:
			encontrou = True
			break

		# Obtenha os pontos vizinhos verticais e horizontais do ponto atual;
		vizinhos: List[PontoGridAstar] = plano.PontosAdjacentes(pt_atual.x, pt_atual.y)

		# Remova os obstáculos dos pontos vizinhos;
		vizinhos = [pt for pt in vizinhos if pt not in obstaculos]

		# Remova os pontos já percorridos da lista de pontos vizinhos;
		vizinhos = [pt for pt in vizinhos if pt not in pts_fechados]

		# Para cada vizinho do ponto atual;
		for pt_viz in vizinhos:

			# Se o vizinho atual já estiver na lista de candidatos;
			if (pt_viz in pts_abertos):

				# Calcule a dist. G do ponto atual até o vizinho atual;
				g_dist = pt_atual.g + CalcularDistanciaPontos(pt_atual, pt_viz)

				# Se G do pt atual até o viz. for menor que o G antigo do viz;
				if (g_dist < pt_viz.g):
					# Defina o pt atual como pai do pt vizinho E atualize seu G;
					pt_viz.pt_pai = pt_atual
					pt_viz.g = g_dist

			# Senão, atualize as distâncias do pt vizinho e defina seu pt pai;
			else:

				pt_viz.pt_pai = pt_atual

				# Calcule sua distância (valor G) até o ponto atual;
				pt_viz.g = pt_atual.g + CalcularDistanciaPontos(pt_atual, pt_viz)

				# Calcule a dist. H do vizinho até o objetivo;
				pt_viz.h = CalcularDistanciaPontos(pt_viz, pt_final)

				pts_abertos.append(pt_viz)

	saida = []

	if encontrou:

		# Adicione o pai do ponto no trajeto final até que um ponto sem pai
		# seja encontrado;
		while (pt_atual.pt_pai):
			saida.append(pt_atual.pt_pai)
			pt_atual = pt_atual.pt_pai

		saida.remove(pt_inicial)

		# Remova o ponto inicial do trajeto; Por fim inverta o trajeto;
		saida.reverse()
		saida.append(pt_final)

	return saida

def LerArquivo(quadrante: int = 4) -> Grid:

	linhas = []

	dirname = path.dirname(__file__)
	filename = path.join(dirname, 'Mapa_A _V03.txt')
	with open(filename, mode="r") as arq:
		linhas = arq.readlines()

	qtd_colunas = len(linhas[0].split(" "))
	qtd_linhas = len(linhas)

	plano = Grid(qtd_linhas, qtd_colunas, quadrante)

	y = -1 if (quadrante == 3 or quadrante == 4) else 1
	x = -1 if (quadrante == 2 or quadrante == 3) else 1

	for i, linha in enumerate(linhas):
		pts = linha.strip().split(" ")

		for j, pt in enumerate(pts):
			ponto: PontoGridAstar = plano.GetPonto(x*j, y*i)
			ponto.valor = int(pt)

	return plano

def LerEntradaPontoInicial() -> PontoGridAstar:

	texto = input("\nInsira a coordenada do ponto inicial (Ex.: '1,5'):\n")

	ponto: PontoGridAstar = None

	# Se a entrada de fato for: dois inteiros separados por espaço, crie um ponto;
	try:
		ponto_split = texto.split(",")
		x, y = int(ponto_split[0]), int(ponto_split[1])
		ponto = PontoGridAstar(x, y)

	except:
		pass

	return ponto

def LerEntradaPontoFinal() -> PontoGridAstar:

	texto = input("\nInsira a coordenada do ponto final (Ex.: '6,3'):\n")

	ponto: PontoGridAstar = None

	# Se a entrada de fato for: dois inteiros separados por espaço, crie um ponto;
	try:
		ponto_split = texto.split(",")
		x, y = int(ponto_split[0]), int(ponto_split[1])
		ponto = PontoGridAstar(x, y)

	except:
		pass

	return ponto

def ValidaPontoGrid(ponto: PontoGrid, plano: Grid, simb_obst: object) -> bool:
	
	
	# Se a entrada do ponto for inválida, conter letras, caracteres não aceitos;
	if (not ponto):
		print("\nCoordenadas digitadas inválidas, tente novamente.")
		return False
	
	# Se o ponto não existir no plano;
	if (ponto not in plano):
		print("\nCoordenadas inexistentes.")
		return False
	
	# Se o ponto existir, mas for um obstáculo / barreira;
	if (plano.GetPonto(ponto.x, ponto.y).valor == simb_obst):
		print("\nCoordenadas refrentes a um obstáculo!")
		return False

	return True

def GerarGridDoArquivo() -> Grid:
	
	plano: Grid = LerArquivo()

	print()
	print(plano)

	ponto_inicial = LerEntradaPontoInicial()

	while(not ValidaPontoGrid(ponto_inicial, plano, COD_OBSTACULO)):
		ponto_inicial = LerEntradaPontoInicial()

	ponto_final = LerEntradaPontoFinal()

	while(not ValidaPontoGrid(ponto_final, plano, COD_OBSTACULO)):
		ponto_final = LerEntradaPontoFinal()

	plano.pt_inicial = ponto_inicial
	plano.pt_final = ponto_final
	
	return plano