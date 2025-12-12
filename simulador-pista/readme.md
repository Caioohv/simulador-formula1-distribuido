## Descrição

Fiz esse pequeno simulador usando node, brincando com o event loop e setTimeout para simular o tempo de passagem dos carros pelos pontos da pista. 

Cada carro tem uma velocidade média, que varia um pouco a cada ponto, e o tempo de passagem é calculado com base na distância do ponto e na velocidade média do carro. 

Quando o carro passa por um ponto, existe uma pequena chance (5%) da pressão dos pneus baixar entre 1 e 3 PSI.

Toda vez que cada carro passa por um ponto, ele emite um evento com o tempo de passagem, a velocidade naquele ponto e a pressão dos pneus. Quando chega ao final da pista, ele reinicia o percurso (indefinidamente).

## Como usar

Basta executar usando `node index.mjs`.
É necessário fazer o npm install para baixar as dependências.
O Docker compose fará isso automaticamente se você usar o comando `docker-compose up --build`.

## Estrutura do código

- `index.mjs`: código central do simulador, onde os carros são criados e começam a correr na pista.
- `Pista.mjs`: define os pontos da pista, suas distâncias e velocidades médias esperadas (feito meio manualmente, medi a pista no maps aproximadamente e converti para metros).
- `Carro.mjs`: define a classe Carro, que tem métodos para correr na pista, calcular velocidades variáveis, publicar eventos, e também gerenciar a pressão dos pneus. Ela brinca com a variação de velocidade usando números aleatórios, o que adiciona um pouco de imprevisibilidade ao simulador. Também brinca com a pressão dos pneus, simulando uma pequena chance de queda de pressão a cada ponto. Não tratei para quando os pneus chegam a 0 PSI, mas poderia ser uma melhoria futura interessante.
- `publisher.js`: executa a publicação de eventos usando MQTT, conectando ao broker e publicando as mensagens. Poderia ser Redis Pub/sub, Kafka, ou qualquer outro sistema de mensagens, mas usei MQTT por ser mais alinhado ao contexto de sensores e aplicações embarcadas.
