from funcoes import GerarGridDoArquivo,CalcularCaminhoGrid, COD_OBSTACULO


def main():
	grid = GerarGridDoArquivo()
	path = CalcularCaminhoGrid(grid, grid.pt_inicial, grid.pt_final, COD_OBSTACULO)
	grid.GerarGridCaminho(path)

	print()
	print(grid)

	print(" ".join(["-"]*20))

	if len(path) == 0: 
		print("NÃO HÁ CAMINHOS POSSÍVEIS!!!\n")
		return
	else:
		print("PONTOS percorridos (X, Y):", [pt.to_tuple() for pt in path])
		print("Distância: {}\n".format(len(path)))

	return 0

main()