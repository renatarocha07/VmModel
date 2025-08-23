# VmModel

📌 Projeto de Detecção de Objetos utilizando o modelo RT-DETR

Este projeto realiza a detecção automática de objetos em imagens, gerando bounding boxes (caixas delimitadoras) e armazenando os resultados processados em banco de dados.

🚀 Fluxo do Sistema

O diagrama abaixo representa o fluxo principal do código:
<img width="617" height="384" alt="image" src="https://github.com/user-attachments/assets/cb03e69f-c491-4777-a6d6-1c459835183e" />

📥 Input Image

O sistema recebe uma imagem de entrada (upload manual, captura de câmera ou integração com outro sistema).

🤖 Model - Detecção + Bounding Box

A imagem é processada por um modelo de visão computacional, no trabalho atual é usado RT-DETR. O modelo identifica os objetos de interesse 
e gera bounding boxes (caixas delimitadoras) ao redor deles.

Cada detecção contém:

- Classe do objeto

- Confiança da predição (%)

- Coordenadas da bounding box

🖼️ Output - Imagem Anotada

A imagem original é retornada com as caixas desenhadas e rótulos sobre os objetos detectados. Esse output serve tanto para visualização quanto para validação do modelo.

💾 Storage + Database

O banco de dados facilita consultas, análises e integração com outros serviços. A imagem anotada e seus metadados (objetos detectados, coordenadas, scores, timestamp, etc.) são armazenados em uma plataforma de desenvolvimento open-source que funciona como um "backend como serviço" (BaaS), a usada nesse projeto foi a Supabase.
