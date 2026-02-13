---
title: "Crash Course em Criptografia Homomórfica"
slug: "crash-course-em-criptografia-homomorfica"
date: 2026-02-11T21:10:05
draft: false
description: "Post description here"
tags: []
categories: []
---

A ideia deste post é prover uma linha do tempo alto nível do surgimento e evolução da criptografia homomórfica, conceitos iniciais, principais pontos de destaque, sem se aprofundar na matemática e formalidade do tema neste momento. Servindo como uma síntese da história dessa área de estudo.


## Conceituação e Primeiros Passos

A possibilidade de realizar computação utilizando dados cifrados foi concebida em 1978 e publicada no artigo [_On Data Banks and Privacy Homomorphisms_](https://luca-giuzzi.unibs.it/corsi/Support/papers-cryptography/RAD78.pdf), escrito por parte dos autores do RSA. Eles introduzem o conceito de Homomorfismo de Privacidade (Privacy Homomorfism), referindo-se a um subconjunto especial de funções criptográficas que permitem a operação sobre dados cifrados.

São explorados no artigo exemplos de operações que poderiam ser utilizadas sobre dados cifrados, e apresentados esquemas onde já poderíamos utilizar essas operações, sendo o RSA um exemplo de esquema com homomorfismo multiplicativo.

Isso era possível, pois um texto cifrado pelo RSA tem a forma:

$$
c = m^e \pmod{n} \\
$$

Onde:

$$
\begin{aligned}
m:\quad &\text{A mensagem em texto claro.}\\
e:\quad & \text{Expoente público.}\\
n:\quad & \text{Módulo, faz parte da chave pública.}\\
c:\quad & \text{Criptograma da mensagem m.} \\
E:\quad & \text{Função de encriptação}
\end{aligned}
$$

Dessa forma, sejam as mensagem \(m_1\) e \(m_2\):
$$
\begin{aligned}
c_1 &= m_1^e \pmod{n} \\
c_2 &= m_2^e \pmod{n}
\end{aligned}
$$

O produto de suas cifras resulta na cifra da multiplicação de suas mensagens:
$$
\begin{aligned}
c_1 \cdot c_2 \equiv (m_1^e) \cdot (m_2^e) &\equiv (m_1 \cdot m_2)^e \pmod{n} \\
\therefore \quad c_1 \cdot c_2 &= E(m_1 \cdot m_2)  \pmod{n} 
\end{aligned}
$$

### Partially Homomorphic Encryption

Pelo exemplo apresentado anterior, podemos perceber que estamos limitados na variedade de operações que podemos realizar utilizando um esquema, e essa foi a realidade por algum tempo com os esquemas chamados _Partially Homomorphic Encryption_, que permitiam soma ou multiplicação, mas não ambas ilimitadamente.

Como exemplo para a múltiplicação temos o RSA e o ElGamal. Para adição temos o Goldwasser-Micaeli que permitia a operação XOR, com expansão significativa do tamanho do texto cifrado, e Paillier, que permite a adição de textos cifrados, e a multiplicação de um texto cifrado por um escalar(texto claro).

### Somewhat Homomorphic Encryption

Existiram alguns esquemas que implementaram ambas as operações, adição e múltiplicação, mas com um número limitado de operações, como o BGN (Boneh-Goh-Nissim), baseado em Grupos Bilineares (_Paired-base Cryptography_). Ele permitia somente uma única multiplicação sobre os valores encriptados, e uma profundidade arbitrária para adição. Esquemas que possuem essa limitação na profundidade dos circuitos que podem computar pertencem ao grupo _Somewhat Homomorphic Encryption_.


## Primeira Geração de Criptografia Totalmente Homomórfica
Para um esquema ser considerado totalmente homomórfico (_Fully Homomorphic Encryption_), ele precisa conseguir realizar um conjunto de funções que seja funcionalmente completo (e.g.:\( \{\text{XOR}, \text{AND}\}\)). Portanto, as duas funções básicas para tal são a adição e multiplicação binárias, sendo elas, respectivamente, isomorfas ao XOR e AND booleanos.

### Bootstrap the Bootstrapping
Craig Gentry publicou em 2009, quando ainda era doutorando em Stanford, sua tese intitulada [_Fully Homomorphic Encryption Using Ideal Lattices_](https://www.cs.cmu.edu/~odonnell/hits09/gentry-homomorphic-encryption.pdf). Ele adotou um sistema de criptografia baseada em reticulados (_lattice-based cryptography_), já existente, mas que possuia um problema com ruído (_noise_), pela aritmética não ser exata, um pequeno termo de erro aleatório que é introduzido durante a encriptação para garantir a segurança. Dessa forma, ao realizarmos as operações:
- Adição: Ao somar texto cifrados, seus ruídos são somados, crescendo de forma linear.
- Multiplicação: Ao multiplicar textos cifrados multiplica seus ruídos, tendo assim um crescimento exponencial.

O problema é que se o ruído crescer mais do que o teto definido no sistema, é impossível decifrar o texto cifrado, causando erros de decodificação, e tornando o esquema em _Somewhat Homomorphic_ (SHE).

Para solucionar este problema, o artigo inovou apresentando a técnica de _Bootstrapping_. Irei falar mais sobre este tema em outro post, mas simplificando, é uma forma de reiniciar o ruído acumulado no texto cifrado. Tranformando a criptografia homomórfica em uma realidade matemática construível, mas ainda ineficiente no momento, podendo levar cerca de [30 minutos](https://eprint.iacr.org/2010/520.pdf) para a conclusão de uma única porta lógica.


### DGHV
Houve também, em 2010, a publicação do paper [_Fully Homomorphic Encryption over the Integers_](https://eprint.iacr.org/2009/616.pdf) apresentando o esquema DGHV, onde a estrutura de reticulado foi substituída por inteiros. A função de encriptação era dada por:

$$
\begin{align}
c = E(m) = pq + 2r + m
\end{align}
$$

Sendo \(m\) a mensagem, \(p\) a chave publica, e \(q, r\) inteiros escolhidos aleatoriamente em um intervalo prescrito, sendo \(2r < p/2\) em valores absolutos.
O objetivo principal deste trabalho era demonstrar a possibilidade de obter FHE com conceitos simples, sem a necessidade da utilização de reticulados ideais.

## Segunda Geração

Em 2010 o artigo [_On Ideal Lattices and Learning with Errors Over Rings_](https://eprint.iacr.org/2012/230.pdf) introduziu o problema do _Ring Learning With Errors_ (RLWE), uma variante em anéis do _Learning With Errors_ (LWE), juntamente com outras técnicas para gerenciamento de ruído mais sofisticadas.

O RLWE se consolidou como um problema chave devido a sua eficiência, pois enquanto o LWE opera com vetores sobre inteiros, o RLWE opera com polinômios em anéis ciclotômicos (e.g.: \(R_q = \mathbb{Z}_q[X]/(X^N + 1)\)). Dessa forma, ele permite o empacotamento de múltiplos valores de textos claros em um único texto cifrado, representado pelo polinômio. Essa junção permite a utilização de operações SIMD (Single-instruction Multiple-data), de forma que uma única operação homomórfica é aplicada simultaneamente em múltiplos slots de dados. 

Essa evolução aumentou o _throughput_ da FHE ordens de magnitude.

### BGV (Brakerski-Gentry-Vaikuntanathan)

O esquema foi apresentado pelos pesquisadores em 2011 no artigo [_Fully Homomorphic Encryption without Bootstrapping_](https://eprint.iacr.org/2011/277.pdf), e representou uma evolução para a área. Ele introduziu uma técnica de gerenciamento de ruído chamada Troca de Módulo (_Modulus Switching_), onde um texto cifrado módulo q, ao ter seu ruído aumentado significativamente, é convertido para ser um texto cifrado módulo \(q'\), \(q' < q\). Assim a magnitude do ruído é diminuído por um fator \(q'/q\).

### BFV (Brakerski/Fan-Vercauteren)

Proposto em 2012 no artigo [_Somewhat Practical Fully Homomorphic Encryption_](https://eprint.iacr.org/2012/144.pdf), ele é uma variante do BGV onde gerenciamento do ruído ocorre pela própria estrutura aritmética do esquema, mantendo o módulo do texto cifrado constante durante as operações homomórficas.

Ambos os esquemas suportam aritmética exata de inteiros, e possuem a necessidade de relinearização, onde em uma multiplicação de dois textos cifrados resulta em um trio, que precisam ser relinearizados, sendo essa uma operação custosa computacionalmente.

## Terceira Geração

### GSW (Gentry-Sahai-Waters)
Um esquema baseado em autovetores aproximados (_approximate eigenvectors_). Com essa nova abordagem, foi possível eliminar a necessidade de relinearização. O ruído cresce de forma assimétrica, mas o tamanho dos textos cifrados (matrizes quadradas) é significativamente maior, limitando seu uso em certos casos de uso.

### FHEW e TFHE

Com avanços significativos na diminuição do tempo de boostrapping, temos o FHEW ([_Fastest Homomorphic Encryption in the West_](https://eprint.iacr.org/2016/870.pdf)) em 2014, e o TFHE ([_Torus FHE_](https://eprint.iacr.org/2018/421.pdf)) em 2016 que realizavam o boostrapping em milissegundos. Essa nova geração tornou viável a avaliação de circuitos booleanos arbitrários, dessa forma, podendo representar qualquer programa de computador (Pois todo programa pode ser representado por um circuito booleano).

## Quarta Geração

Com as gerações anteriores focando na otimização dos cálculos na aritmética exata, essa geração marca uma mudança de paradigma ao introduzir a aritmética aproximada. Tendo como uma das principais inovações a reinterpretação do ruído criptográfico. 

### CKKS (Cheon-Kim-Kim-Song)

O esquema foi proposto em 2016 no artigo [_Homomorphic Encryption for Arithmetic of approximate Numbers_](https://eprint.iacr.org/2016/421.pdf), também conhecido como HEAAN, e introduziu o conceito de Criptografia Homomórfica Aproximada. Ele trata o ruído criptográfico do RLWE como parte do erro numérico de aproximação inerente à computação com ponto flutuante (como um erro de arredondamento). Ele permite que o ruído afete somente os bits menos significativos da mensagem decifrada. Para obter seus resultados, uma técnica de encoding que utiliza a inversa do _Canonical Embedding_ mapeia vetores de números complexos \((\mathbb{C}^{N/2})\) em polinômios de coeficientes inteiros do anel RLWE, aplicando um escalonamento e arredondamento para discretização.

Os avanços obtidos habilitaram a aplicação da criptografia homomórfica em diversas áreas que possuem uma sinergia com cálculos de ponto flutuante, como aplicações de Machine Learning, Redes Neurais, análise de dados genômicos, etc; o CKKS criou o padrão para o que se tornaria o _Privacy-Preserving Machine Learning (PPML)_ baseado em Criptografia Homomórfica.

## Avanços paralelos

### CHIMERA 

Com o objetivo de utilizar as especializações de cada esquema, o [CHIMERA](https://eprint.iacr.org/2018/758.pdf) é uma abordagem híbrida que nos permite transformar o texto cifrado entre os esquemas TFHE, BFV e CKKS. Ele obtém esse resultado com o mapeamento dos espaços de mensagens de cada esquema para uma nova estrutura comum, baseada em Torus \((\mathbb{T} = \mathbb{R} / \mathbb{Z})\), o que permite a transformação sem a necessidade de decifragem.

### Bibliotecas

Existem diversas opções de implementações do esquemas mais importantes disponíveis em bibliotecas open-source, como a [OpenFHE](https://github.com/openfheorg/openfhe-development), que é a sucessora que unificou diversos projetos anteriormente isolados e a opção mais completa até o momento, e a [MicrosoftSEAL](https://github.com/microsoft/SEAL), que foca nos esquemas BGV e CKKS. Essas bibliotecas são bases robustas para qualquer desenvolvedor, ou pesquisador, que queria utilizar a criptografia homomórfica sem a necessidade de implementar todas a matemática do zero.

### Aceleração de Hardware

Embora os esquemas homomórficos tenham sido otimizados drasticamente nos últimos anos, eles ainda possuem custos proibitivos para algumas aplicações práticas, como 23 min para a execução da ResNet-20 em CPU, exemplificado no artigo do [_CraterLake_](https://people.csail.mit.edu/devadas/pubs/craterlake.pdf). Por esse motivo, existem estudos de técnicas de [aceleração de Hardware](https://www.sigarch.org/a-brief-guide-to-fully-homomorphic-encryption-for-computer-architects-part-ii/) utilizando GPU, FPGA, ou implementando ASICs, como o Intel [_HERACLES_](https://www.semanticscholar.org/paper/Intel-HERACLES%3A-Homomorphic-Encryption-Accelerator-Cammarota/baadabb09cbdbd35c7c407b6c028da4e5ab73a60) que utiliza uma arquitetura _near-memory_ com unidades interconectadas voltadas ao processamento de polinômios de anel (_Ring Polynomials_) nativamente. Ele foi desenvolvido sobre o programa [_DPRIVE_](https://www.darpa.mil/news/2021/homomorphic-encryption) da DARPA.


Acho que já deu para termos uma pequena noção sobre parte do passado da criptografia homomórfica, e entendermos um pouco sobre o presente da área. Para os interessados em um aprofundamento na área, recomendo olharem o [Awesome Homomorphic Encryption](https://github.com/jonaschn/awesome-he), uma lista contendo materiais diversificados sobre a área.


## References

[FHE Organization - History](https://fhe.org/history/)  
[The Rise of Fully Homomorphic Encryption](https://spawn-queue.acm.org/doi/pdf/10.1145/3561800)  
[The Continuing Evolution of Modern Fully Homomorphic Encryption Schemes](https://www.tfhe.com/evolution-of-homomorphic-encryption-schemes)  
[A brief history on Homomorphic learning: A privacy-focused approach to machine learning](https://arxiv.org/pdf/2009.04587)   
[A Review of Homomorphic Encryption for Privacy-Preserving Biometrics](https://researchmgt.monash.edu/ws/portalfiles/portal/575329596/487332020_oa.pdf)  
[On Data Banks and Privacy Homomorphisms](https://luca-giuzzi.unibs.it/corsi/Support/papers-cryptography/RAD78.pdf)  
[Fully Homomorphic Encryption Using Ideal Lattices](https://www.cs.cmu.edu/~odonnell/hits09/gentry-homomorphic-encryption.pdf)  
[Fully Homomorphic Encryption over the Integers](https://eprint.iacr.org/2009/616.pdf)  
[Implementing Gentry’s Fully-Homomorphic Encryption Scheme](https://eprint.iacr.org/2010/520.pdf)  
[On Ideal Lattices and Learning with Errors Over Rings](https://eprint.iacr.org/2012/230.pdf)  
[Fully Homomorphic Encryption without Bootstrapping](https://eprint.iacr.org/2011/277.pdf)  
[Somewhat Practical Fully Homomorphic Encryption](https://eprint.iacr.org/2012/144.pdf)  
[Building Blocks of FHE: Exploring the GSW Scheme and Its Foundations](https://medium.com/@fhera/building-blocks-of-fhe-exploring-the-gsw-scheme-and-its-foundations-7104f1e22e01)  
[Fastest Homomorphic Encryption in the West](https://eprint.iacr.org/2016/870.pdf)  
[Torus FHE](https://eprint.iacr.org/2018/421.pdf)  
[Homomorphic Encryption for Arithmetic of approximate Numbers](https://eprint.iacr.org/2016/421.pdf)  
[CHIMERA](https://eprint.iacr.org/2018/758.pdf)  
[OpenFHE](https://github.com/openfheorg/openfhe-development)  
[MicrosoftSEAL](https://github.com/microsoft/SEAL)  
[CraterLake](https://people.csail.mit.edu/devadas/pubs/craterlake.pdf)  
[HERACLES](https://www.semanticscholar.org/paper/Intel-HERACLES%3A-Homomorphic-Encryption-Accelerator-Cammarota/baadabb09cbdbd35c7c407b6c028da4e5ab73a60)  
[DPRIVE_](https://www.darpa.mil/news/2021/homomorphic-encryption)  
[Awesome Homomorphic Encryption](https://github.com/jonaschn/awesome-he)
