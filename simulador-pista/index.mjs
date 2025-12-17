import carro from './Carro.mjs';
import pontos from './Pista.mjs';

const carros = [
  new carro(1, 'Vettel', 'Aston Martin'),
  new carro(2, 'Leclerc', 'Ferrari'),
  new carro(3, 'Hamilton', 'Mercedes'),
  new carro(4, 'Verstappen', 'Red Bull'),
  new carro(5, 'Perez', 'Red Bull'),
  new carro(6, 'Sainz', 'Ferrari'),
  new carro(7, 'Russell', 'Mercedes'),
  new carro(8, 'Alonso', 'Aston Martin'),
  new carro(9, 'Norris', 'McLaren'),
  new carro(10, 'Piastri', 'McLaren'),
  new carro(11, 'Gasly', 'Alpine'),
  new carro(12, 'Ocon', 'Alpine'),
  new carro(13, 'Bottas', 'Alfa Romeo'),
  new carro(14, 'Zhou', 'Alfa Romeo'),
  new carro(15, 'Albon', 'Williams'),
  new carro(16, 'Sargeant', 'Williams'),
  new carro(17, 'Magnussen', 'Haas'),
  new carro(18, 'Hulkenberg', 'Haas'),
  new carro(19, 'Tsunoda', 'AlphaTauri'),
  new carro(20, 'Ricciardo', 'AlphaTauri'),
  new carro(21, 'Stroll', 'IFMG'),
  new carro(22, 'De Vries', 'UFSJ'),
  new carro(23, 'Raikkonen', 'IFMG'),
  new carro(24, 'Button', 'UFSJ'),
];


carros.forEach(carro => {
  carro.correr(pontos);
});