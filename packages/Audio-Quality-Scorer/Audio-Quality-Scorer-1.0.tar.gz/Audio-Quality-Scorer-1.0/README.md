# AudioQualityScorer

O código  é uma implementação de uma função chamada "audio_quality_score", que calcula uma pontuação de qualidade de áudio para um arquivo de áudio específico. Essa pontuação é baseada em três métricas: relação sinal-ruído (SNR), distorção harmônica total (THD) e razão de cresta (CR).

A função começa lendo o arquivo de áudio fornecido usando a função "read" da biblioteca "scipy.io.wavfile". Ele então aplica uma janela de Hann, que é uma técnica comumente usada para suavizar as bordas do sinal de áudio, aos dados lidos.

Em seguida, a função calcula a transformada de Fourier do sinal de áudio, que é armazenada na variável "fft_data". A partir desse ponto, o código calcula cada uma das três métricas mencionadas acima:

A relação sinal-ruído (SNR) é calculada como 10 * log10 (soma dos quadrados dos valores absolutos de fft_data / soma dos quadrados dos valores (data - média dos valores de data))
A distorção harmônica total (THD) é calculada como a soma dos quadrados dos valores absolutos de fft_data, começando do índice 2, dividido pela soma dos quadrados dos valores absolutos de fft_data
A razão de cresta (CR) é calculada como o valor máximo dos valores absolutos de fft_data dividido pela média dos valores absolutos de fft_data
Finalmente, a função atribui uma nota final usando uma combinação ponderada dessas três métricas. A relação sinal-ruído (SNR) contribui com 40% da nota, a distorção harmônica total (THD) contribui com 30% e a razão de cresta (CR) contribui com 30%. A função retorna essa nota final.

Fora da função, o código define um diretório onde os arquivos de áudio estão localizados, e usa essa pasta para criar um arquivo CSV com as notas de qualidade de áudio para cada arquivo de áudio encontrado no diretório. Ele também gera um gráfico de barras mostrando as notas de qualidade de áudio para cada arquivo.

_
Sinal-ruído (SNR) é uma medida da relação entre o sinal desejado e o ruído presente em um sistema. É geralmente medido em decibéis (dB). Quanto maior o valor de SNR, melhor a qualidade do sinal. É amplamente utilizado na avaliação de sistemas de comunicação, áudio e vídeo.

A distorção harmônica total (THD) é uma medida da distorção presente em um sinal elétrico. Ele é medido como a razão entre a potência total das harmônicas presentes no sinal e a potência fundamental. Quanto menor o valor de THD, menor a distorção no sinal e, portanto, melhor a qualidade do sinal. A THD é amplamente utilizada na avaliação de sistemas de áudio e eletrônicos.

A razão de cresta (CR) é uma medida da relação entre o pico máximo e a média de um sinal elétrico. Ele é geralmente medido como a razão entre o pico máximo do sinal e a média do sinal. Quanto maior a razão de cresta, maior a amplitude do sinal e, portanto, melhor a qualidade do sinal. A CR é amplamente utilizada na avaliação de sistemas de áudio e eletrônicos.

A combinação desses três parâmetros permite avaliar a qualidade de um sinal de áudio de forma mais completa. O SNR mede a relação entre o sinal desejado e o ruído, a THD mede a distorção presente no sinal e a CR mede a amplitude do sinal. Juntos, esses três parâmetros fornecem uma visão geral da qualidade do sinal de áudio.

É importante notar que os valores ideais para SNR, THD e CR variam de acordo com a aplicação específica. Por exemplo, em sistemas de comunicação, é desejável um alto SNR, enquanto em sistemas de áudio é desejável um baixo THD. Portanto, é importante entender as especificações do sistema específico antes de utilizar essas medidas para avaliar a qualidade de um sinal de áudio.

Em geral, o código acima pode ser utilizado para avaliar a qualidade de arquivos de áudio em um determinado diretório, calculando os valores de SNR, THD e CR para cada arquivo e, em seguida, combinando-os para calcular uma pontuação geral.



