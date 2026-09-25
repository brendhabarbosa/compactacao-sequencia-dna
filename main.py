from bitarray import bitarray
import os 

dna_dict = {
    'A': bitarray('00'),
    'C': bitarray('01'),
    'G': bitarray('10'),
    'T': bitarray('11')
}

dna_dict_reverse = {
    '00': 'A',
    '01': 'C',
    '10': 'G',
    '11': 'T'
}

with open('sequencia.txt', 'r') as origem:
    caractere = origem.read()

resultado = bitarray()
for letra in caractere:
    if letra in dna_dict:
        valor = dna_dict[letra]
        resultado = resultado + valor

quantidade = len(caractere)

with open('sequencia_compactada.txt', 'wb') as destino:
    destino.write(quantidade.to_bytes(4, byteorder='big'))
    destino.write(resultado.tobytes())

with open('sequencia_compactada.txt', 'rb') as origem:
    dados = origem.read()
    quantidade = int.from_bytes(dados[:4], byteorder='big')
    dados_compactados = dados[4:]

    resultado = bitarray()
    resultado.frombytes(dados_compactados)
    resultado = resultado[:quantidade * 2]

with open('sequencia_descompactada.txt', 'w') as destino:
    for i in range(0, len(resultado), 2):
        valor = resultado[i:i+2].to01()
        if valor in dna_dict_reverse:
            letra = dna_dict_reverse[valor]
            destino.write(letra)

with open('sequencia.txt', 'r') as origem:
    original = origem.read()

with open('sequencia_descompactada.txt', 'r') as descompactada:
    recuperada = descompactada.read()

if original == recuperada:
    print("Os arquivos são iguais.") 
    tamanho_original = os.path.getsize('sequencia.txt')
    tamanho_compactado = os.path.getsize('sequencia_compactada.txt')
    reducao = ((tamanho_original - tamanho_compactado) / tamanho_original) * 100
    print(f"Tamanho original: {tamanho_original} bytes")
    print(f"Tamanho compactado: {tamanho_compactado} bytes")
    print(f"Redução: {reducao:.2f}%")
else:
    print("Os arquivos são diferentes.")
