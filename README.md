# Ocean_YOLO
 
<h1>Documentação do Código: Detecção de Objetos com Nível de Toxicidade</h2>
Descrição Geral
Este programa utiliza a biblioteca YOLO para detectar objetos em tempo real a partir da câmera do computador. O sistema fornece informações sobre os objetos detectados, incluindo descrição, uso e uma avaliação de seu "poder de destruição". O aplicativo também exibe um gráfico de barras mostrando a quantidade de cada objeto detectado e calcula um nível total de toxicidade com base nos objetos.

<h2>Dependências</h2><br>
<b> tkinter: </b> Para a criação da interface gráfica.</h3><br>
<b> ultralytics: </b> Para a detecção de objetos usando o modelo YOLO.<br>
<b> cv2 (OpenCV): </b> Para captura de vídeo e manipulação de imagens.<br>
<b> threading: </b> Para executar tarefas em paralelo.<br>
<b> time: </b> Para controlar intervalos de tempo.<br>
<b> pyttsx3: </b> Para síntese de voz.<br>
<b> PIL (Pillow): </b> Para manipulação de imagens.<br>
<b> requests: </b> Para chamadas à API do Wikidata.<br>
<b> geocoder: </b> Para obter a localização geográfica do usuário.<br>
<b> matplotlib: </b> Para gerar gráficos.<br>
<h2> Estrutura do Código </h2><br>
<h2>Inicialização</h2>
O motor de síntese de voz é inicializado para permitir a narração de objetos detectados.
Dicionários e variáveis são definidos para armazenar informações sobre objetos detectados e seus "poderes de destruição".<br>
<b>TEMPO_LIMITE_RECONTAGEM </b> controla a frequência com que um objeto pode ser recontado.<br>
<h3>Funções Principais</h3><br>
<b>consultar_wikidata(nome_objeto):</b><br>
Consulta a API do Wikidata para obter informações sobre um objeto detectado.<br>
Retorna a descrição e o uso do objeto.<br>
<b>narrar(texto):</b><br>
<b>Utiliza o motor de síntese de voz para narrar o texto fornecido.</b><br>
<b>calcular_toxicidade():</b><br>
<b>Calcula o nível total de toxicidade com base nos objetos detectados e seu poder de destruição.</b><br>
<b>exibir_grafico():</b><br>
<b>Gera e exibe um gráfico de barras com a quantidade de cada objeto detectado.</b><br>
<b>Atualiza a interface Tkinter com o gráfico.</b><br>
<b>obter_geolocalizacao():</b><br>
Obtém a localização geográfica do usuário usando o endereço IP.</b><br>
<b>atualizar_info():</b><br>
Atualiza a interface do usuário com as informações dos objetos detectados, incluindo descrição, uso, quantidade e nível total de toxicidade.</b><br>
<b>Exibe o gráfico atualizado.</b><br>
<b>detectar():</b><br>
Captura vídeo da câmera, processa os frames e detecta objetos usando o modelo YOLO.</b><br>
Atualiza as informações na interface e narra objetos detectados.<br>
<b>pausar_deteccao():</b><br>
Pausa ou retoma a detecção de objetos com base no estado atual.</b><br>
<b>limpar_deteccoes():</b><br>
Limpa todas as detecções de objetos e atualiza a interface.</b><br>
Configuração da Interface Tkinter</b><br>
A janela principal é configurada com três frames:<br>
<b>frame_video:</b> Para exibir o vídeo da câmera.<br>
<b>frame_info:</b> Para mostrar informações sobre objetos detectados e botões de controle.<br>
<b>frame_grafico: </b>Para exibir gráficos e mensagens de erro.<br>
Botões de controle para pausar a detecção e limpar as detecções são criados.<br>
<h1> Primeira Execução</h1>
O modelo YOLO é carregado a partir de um arquivo pré-treinado (yolov8n.pt).<br>
A detecção é iniciada em uma thread separada para garantir que a interface permaneça responsiva.<br>
O loop principal da interface Tkinter é iniciado.<br>
<h1>Considerações Finais</h1>
Este aplicativo é uma demonstração do uso de visão computacional e interface gráfica para monitorar e informar sobre a poluição ambiental. A combinação de detecção de objetos e análise de toxicidade proporciona uma ferramenta útil para conscientização e educação sobre o impacto de resíduos no meio ambiente.

