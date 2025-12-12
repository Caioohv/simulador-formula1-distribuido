import carro from './Carro.mjs';
import pontos from './Pista.mjs';

const carros = [
  new carro(1, 'Vettel', 'Aston Martin'),
  new carro(2, 'Leclerc', 'Ferrari'),
  new carro(3, 'Hamilton', 'Mercedes'),
  new carro(4, 'Verstappen', 'Red Bull'),
];


carros.forEach(carro => {
  carro.correr(pontos);
});