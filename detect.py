import tkinter as tk
from ultralytics import YOLO
import cv2
import threading
import time
import pyttsx3
from PIL import Image, ImageTk
import requests
import geocoder
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Inicializando o motor de síntese de voz (Inglês)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Dicionário para manter as informações dos objetos detectados
objetos_detectados = {}
cache_detectados = {}
TEMPO_LIMITE_RECONTAGEM = 2.0
capturando = True

# Dicionário de "poder de destruição" para diferentes objetos
poder_destruicao = {
    "plastic": 5,
    "glass": 4,
    "metal": 6,
    "paper": 2,
    "electronics": 8,
    "other": 1
}

# Função para consultar a API do Wikidata com tratamento de erros
def consultar_wikidata(nome_objeto):
    try:
        url = f"https://www.wikidata.org/w/rest.php/wikibase/v0/entities/search?search={nome_objeto}&language=en"
        response = requests.get(url)
        data = response.json()
        
        if 'search' in data and data['search']:
            item = data['search'][0]
            descricao = item.get('description', "No description available")
            uso = item.get('label', "No usage information available")
            return descricao, uso
        else:
            return "No description available", "No usage information available"
    except Exception as e:
        return f"Error fetching data: {str(e)}", "No usage information available"

# Função para narrar em inglês
def narrar(texto):
    engine.say(texto)
    engine.runAndWait()

# Função para calcular a toxicidade
def calcular_toxicidade():
    toxicidade_total = 0
    for obj, data in objetos_detectados.items():
        poder = poder_destruicao.get(obj, 1)
        toxicidade_total += poder * data['quantidade']
    return toxicidade_total

# Função para exibir gráfico
def exibir_grafico():
    try:
        objetos = list(objetos_detectados.keys())
        quantidades = [data['quantidade'] for data in objetos_detectados.values()]
        poderes = [poder_destruicao.get(obj, 1) for obj in objetos]
        
        fig, ax = plt.subplots(figsize=(5, 4))  # Define o tamanho do gráfico
        ax.bar(objetos, quantidades, label="Quantidade")
        ax.set_xlabel("Objetos")
        ax.set_ylabel("Quantidade")
        
        # Limpar o gráfico anterior
        for widget in frame_grafico.winfo_children():
            widget.destroy()
        
        # Exibe o gráfico no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Permite que o gráfico se expanda
        return canvas
    except Exception as e:
        erro_grafico.set(f"Erro ao gerar gráfico: {str(e)}")

# Função para obter geolocalização com tratamento de erros
def obter_geolocalizacao():
    try:
        g = geocoder.ip('me')
        if g.latlng:
            return g.latlng
        else:
            return "Location not found"
    except Exception as e:
        return f"Error: {str(e)}"

# Função que atualizará as informações na interface
def atualizar_info():
    for widget in frame_info.winfo_children():
        widget.destroy()

    if not objetos_detectados:
        tk.Label(frame_info, text="No objects detected yet.").pack()
    
    for obj, data in objetos_detectados.items():
        tk.Label(frame_info, text=f"Name: {obj}").pack()
        tk.Label(frame_info, text=f"Description: {data['descricao']}").pack()
        tk.Label(frame_info, text=f"Usage: {data['uso']}").pack()
        tk.Label(frame_info, text=f"Quantity: {data['quantidade']}").pack()
        tk.Label(frame_info, text="---").pack()

    total_toxicidade = calcular_toxicidade()
    tk.Label(frame_info, text=f"Total Toxicity Level: {total_toxicidade}").pack()

    # Exibe localização
    localizacao = obter_geolocalizacao()
    tk.Label(frame_info, text=f"Location: {localizacao}").pack()

    # Atualiza gráfico
    exibir_grafico()

# Função para detectar objetos
def detectar():
    global objetos_detectados, cache_detectados, capturando
    cap = cv2.VideoCapture(0)

    while True:
        if capturando:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 480))
                results = modelo(frame)

                for result in results[0].boxes:
                    if result.conf > 0.5:
                        classe = modelo.names[int(result.cls)]
                        agora = time.time()
                        
                        if classe not in cache_detectados or (agora - cache_detectados[classe]) > TEMPO_LIMITE_RECONTAGEM:
                            cache_detectados[classe] = agora
                            
                            if classe not in objetos_detectados:
                                descricao, uso = consultar_wikidata(classe)
                                objetos_detectados[classe] = {
                                    "descricao": descricao,
                                    "uso": uso,
                                    "quantidade": 1
                                }
                                threading.Thread(target=narrar, args=(f"New object detected: {classe},",)).start()
                            else:
                                objetos_detectados[classe]["quantidade"] += 1
                                threading.Thread(target=narrar, args=(f"{classe} detected again. Total: {objetos_detectados[classe]['quantidade']}.",)).start()

                frame = results[0].plot()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(img)
                label_video.imgtk = img_tk
                label_video.configure(image=img_tk)

            time.sleep(0.1)

        # Atualiza informações a cada segundo
        atualizar_info()

    cap.release()
    cv2.destroyAllWindows()

# Função para pausar/retomar a detecção
def pausar_deteccao():
    global capturando
    capturando = not capturando
    botao_pausar.config(text="Resume" if not capturando else "Pause")

# Função para limpar as detecções
def limpar_deteccoes():
    global objetos_detectados
    objetos_detectados = {}
    atualizar_info()

# Configuração da janela Tkinter
janela = tk.Tk()
janela.title("Object Detection with Toxicity Level")
janela.geometry("1200x800")

# Configurando a interface
frame_video = tk.Frame(janela)
frame_video.grid(row=0, column=0, padx=10, pady=10)

frame_info = tk.Frame(janela)
frame_info.grid(row=0, column=1, padx=10, pady=10)

frame_grafico = tk.Frame(janela)
frame_grafico.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Rótulo para mensagens de erro
erro_grafico = tk.StringVar()
tk.Label(frame_grafico, textvariable=erro_grafico, fg="red").pack()

label_video = tk.Label(frame_video)
label_video.pack(fill=tk.BOTH, expand=True)  # Permite que o vídeo se expanda

botao_pausar = tk.Button(frame_info, text="Pause", command=pausar_deteccao)
botao_pausar.pack()

botao_limpar = tk.Button(frame_info, text="Clear Detections", command=limpar_deteccoes)
botao_limpar.pack()

# Carregar modelo YOLO
modelo = YOLO("yolov8n.pt")

# Iniciar a detecção em uma thread separada
threading.Thread(target=detectar).start()

# Loop da janela principal
janela.mainloop()
