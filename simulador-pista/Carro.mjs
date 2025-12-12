export default class Carro {
  constructor(id, nome, equipe, last) {
    this.id = id;
    this.nome = nome;
    this.equipe = equipe;
    this.posicao = 0;

    this.pressaoPneus = {
      pneu1: 50,
      pneu2: 50,
      pneu3: 50,
      pneu4: 50
    }
    
    let velocidadekmh = 210 + this.obterVariancia(); //210-220
    this.velocidadeMedia = velocidadekmh / 3.6; // km/h para m/s
  }


  obtemEstadoPneus() {
    let chance = 5;
    for (let pneu in this.pressaoPneus) {
      let reduzir = Math.random() * 100 < chance;
      if (reduzir) {
        this.pressaoPneus[pneu] -= Math.floor(Math.random() * 3) + 1; // reduz entre 1 e 3
        if (this.pressaoPneus[pneu] < 20) {
          this.pressaoPneus[pneu] = 20; // pressão mínima
        }
      }
    }
    return this.pressaoPneus;
  }

  obterVariancia () {
    return Math.floor(Math.random() * 10) + 1; //1 a 10
  }

  obtemVelocidadeVariavel() {
    let velocidade = this.velocidadeMedia;
    let txVariancia = this.obterVariancia();
    let variancia = (this.velocidadeMedia * txVariancia) / 100;
    
    let aumentar = Math.random() < 0.5;
    
    if (aumentar) {
      velocidade += variancia;
    } else {
      velocidade -= variancia;
    }
    
    return velocidade;
  }

  obtemVelocidadeVariavelPorPonto(txVelMedia) {
    return this.obtemVelocidadeVariavel() * (txVelMedia / 100);
  }

  publicaEvento(ponto, tempo, velocidade) {
    console.log(`${ponto.pos}: ${ponto.name} - Carro ${this.nome} passou em ${tempo.toFixed(2)} segundos com velocidade de ${velocidade.toFixed(2)} m/s. Pressão dos pneus: ${JSON.stringify(this.obtemEstadoPneus())}`);

  }

  correr(pontos) {
    pontos.forEach(ponto => {
      let velocidade = this.obtemVelocidadeVariavelPorPonto(ponto.txVelMedia);
      
      let tempo = ponto.distancia / this.velocidadeMedia;

      setTimeout(() => {
        this.publicaEvento(ponto, tempo, velocidade);
        if(ponto.replay) this.correr(pontos)
      }, tempo * 1000)

    })
    
  }

}

