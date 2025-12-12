let proporcao = 0.095755556 * 1000 //metros;

let pontos = [
    {pos: 0, name:  'Inicio',             distancia: proporcao * 0,    txVelMedia: 100},
    {pos: 1, name:  'Senna S',            distancia: proporcao * 3.5,  txVelMedia: 80},
    {pos: 2, name:  'Curva do Sol',       distancia: proporcao * 4,    txVelMedia: 90},
    {pos: 3, name:  'Inicio reta oposta', distancia: proporcao * 7,    txVelMedia: 110},
    {pos: 4, name:  'Fim Reta Oposta',    distancia: proporcao * 14,   txVelMedia: 75},
    {pos: 5, name:  'Descida do Lago',    distancia: proporcao * 16,   txVelMedia: 90},
    {pos: 6, name:  'Ferradura',          distancia: proporcao * 20,   txVelMedia: 80},
    {pos: 7, name:  'Laranjinha',         distancia: proporcao * 21,   txVelMedia: 70},
    {pos: 8, name:  'Esse',               distancia: proporcao * 23,   txVelMedia: 60},
    {pos: 9, name:  'Pinheirinho',        distancia: proporcao * 25,   txVelMedia: 70},
    {pos: 10, name: 'Pinheirinho 2',      distancia: proporcao * 26,   txVelMedia: 75},
    {pos: 11, name: 'Bico de PAto',       distancia: proporcao * 27.5, txVelMedia: 60},
    {pos: 12, name: 'Mergulho',           distancia: proporcao * 30,   txVelMedia: 90},
    {pos: 13, name: 'Juncao',             distancia: proporcao * 33,   txVelMedia: 80},
    {pos: 14, name: 'Arquibancadas',      distancia: proporcao * 38,   txVelMedia: 100},
    {pos: 15, name: 'Reta final',         distancia: proporcao * 42,   txVelMedia: 120},
    {pos: 16, name: 'Fim',                distancia: proporcao * 45,   txVelMedia: 100, replay: true},
  ]

export default pontos

