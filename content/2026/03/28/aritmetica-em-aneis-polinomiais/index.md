---
title: "Aritmética em Anéis Polinomiais"
slug: "aritmetica-em-aneis-polinomiais"
date: 2026-03-28T10:51:39
draft: true
description: "Post description here"
tags: []
categories: []
---

Após apresentar brevemente a história da Criptografia Homomórfica no [primeiro post](https://mauricioleite.github.io/2026/02/11/crash-course-em-criptografia-homomorfica/), iremos começar a construir a base matemática que sustenta esquemas importantes como o BFV: aritmética em anéis polinomiais. Todos os dados processados pelo BFV (texto claros e textos cifrados) são compostos por polinômios, e toda operação homomórfica, e.g: adição, multiplicação; se reduz a operações nesse anel. Entender profudamente os conceitos aqui apresentados auxiliam em implementações mais corretas, e seguras, dos esquemas que utilizam essa base.

## Preceitos Algébricos

Para chegarmos ao anel utilizado no BFV, precisamos inicialmente de alguns conceitos de álgebra abstrata. Essa seção resume parte do capítulo 2 do livro [*An Introduction to Mathematical Cryptography*](https://link.springer.com/book/10.1007/978-1-4939-1711-2), filtrando o conteúdo mais relevante para o nosso contexto.

### Anéis
Um **anel** é uma tripla \((R, +, \cdot)\) onde \((R, +)\) forma um grupo abeliano, sendo \(\cdot\) uma operação associativa e distributiva sobre a adição. Se \(\cdot\) admite elemento neutro, o anel é chamado de **unitário**. O exemplo mais famoso seria \((\mathbb{Z}, +, \cdot)\).

Ao definirmos \(R/(q) = R/qR\), sendo \(q \in R\) e \(q \neq 0\), construímos um **anel quociente**. Ele é obtido ao tomarmos o quociente de \(R\) pelo ideal \(qR = \{qk : k \in R\}\). Por exemplo, seja \(R=\mathbb{Z}\), os elementos de \(R/(q)\) são as classes de equivalência módulo q:

$$
\begin{aligned}
\bar{0}, \, \bar{1},& \, \ldots, \, \overline{q-1}\\
\end{aligned}
$$

onde \(\bar{a} = \{ a + qk \mid k \in \mathbb{Z} \}\).

Anéis quocientes são um elemento importante na criptografia, pois essas estruturas criam limites e garantem que os resultados das operações se mantenham no conjunto estipulado.

Para \(R=\mathbb{Z}\), se \(q\) for um número primo, todo elemento não nulo possui um inverso multiplicativo, e a estrutura passa a ser chamada de **corpo**.

### Anéis de Polinômios

Ao utilizarmos valores de um anél \(R\) como coeficientes de polinômios, podemos criar um anél polinomial \(R[x]\) como sendo o conjunto de todos os polinômios na variável \(x\) com coeficientes de \(R\). Definimos um anél polinomial da seguinte forma:

$$
\begin{aligned}
R[x] = {a_0 + a_1x + a_2x^2 + \ldots + a_n x^n : n \geq 0 \text{ e } a_0, a_1, \ldots, a_n \in R}
\end{aligned}
$$

Podemos exemplificar com \(R = \mathbb{Z}_q\), criando \(\mathbb{Z}_q[x]\), o anél de polinômios cujos coeficientes são inteiros módulo \(q\). Nesses anéis a adição é coeficiente a coeficiente, e a multiplicação segue a regra de expansão, onde cada termo de um polinômio multiplica todos os termos do outro. Os polinômios podem possuir qualquer grau, mas fica evidente a facilidade no crescimento do mesmo a cada multiplicação, podemos se tornar impraticável em algumas aplicações.

### Anéis Quociente de Polinômios

Similar ao que apresentamos anteriormente para limitar os elementos de um anel, podemos aplicar a mesma ideia do quociente para evitarmos que o grau dos polinômios aumente exacerbadamente. Para tal escolhemos um polinômio \(\phi(x)\) e formamos o anel quociente \(R=\mathbb{Z}_q[x] / (\phi(x))\), onde dois polinômios são equivalentes se sua diferença é divisível por \(\phi(x)\). As operações básicas seguem as regras já conhecidas, com o adendo de reduzirmos o resultado módulo \(\phi(x)\). Definimos \(n = \deg(\phi(x))\), sendo assim, todo elemento de \(R\) possui grau estritamente menor que \(n\), portanto, o grau máximo é \(n-1\). 

Por exemplo, sejam \(q = 7\) e \(\phi(x) = x^4 + 1\), teremos o seguinte anel polinomial:
$$
\begin{aligned}
\underbrace{\mathbb{Z}_7[x]}_{\text{polinômios com coefs em }\{0,\ldots,6\}}
  \;\xrightarrow{\;\bmod\;(x^4+1)\;}\;
  \underbrace{\mathbb{Z}_7[x]/(x^4+1)}_{R:\;\text{grau}\,\leq 3,\;\text{coefs em }\{0,\ldots,6\}}
\end{aligned}
$$

Note que no anel em questão \(x^4 + 1 \equiv 0 \), de onde derivamos a relação:
$$
x^4 \equiv -1 \equiv 6 \pmod{7}
$$

Consideremos a multiplicação dos polinômios \(P(x),Q(x) \in R\), definidos abaixo:
$$
\begin{aligned}
P(x) &= x^2 + x \\
Q(x) &= x^3 + 1 \\
P(x) \cdot Q(x) \bmod \phi(x) &= (x^2 + x) \cdot (x^3 + 1) \bmod (x^4+1) \\
&= x^5 + x^4 + x^2 + x \bmod (x^4+1) \\
&= x^2 - 1 \bmod (x^4 + 1) \\
\end{aligned}
$$

Realizando a redução dos coeficientes módulo \(q = 7\), obtemos um polinômio que pertence ao anel:
$$
\begin{aligned}
x^2 - 1 \equiv x^2 + 6 \pmod{7}  
\end{aligned}
$$

Em relação ao número de elementos do anel \(R\), como \(\mathbb{Z}_7\) possuí 7 elementos, e temos aqui 4 coeficiente livres, cada um com 7 opções, totalizamos:
$$
\begin{aligned}
q^\text{n} = 7^4 = 2401 \text{ polinômios distintos em } R
\end{aligned}
$$

## Anel do BFV

Com a base algébrica apresentada, conseguimos definir com maior clareza o anel utilizado pelo BFV. Ele é definido como:
$$
\begin{aligned}
R_q = \mathbb{Z}_q[x] / (X^n+1)
\end{aligned}
$$

Sendo cada elemento um polinômio de grau máximo \(n-1\), e cada coeficiente pertencendo à \(\mathbb{Z}_q\). Exemplificando, seja \(n=4\) e \(q=17\):
$$
\begin{aligned}
a(x) = 13 + 0x + 4x^2 + 9x^3
\end{aligned}
$$

Em implementações, representamos um polinômio com uma lista, e todo polinômio do anel é armazenado como exatamente \(n\) coeficientes. Do exemplo a lista `[13, 0, 4, 9]` representaria o polinômio \(a(x)\) em memória.

### Adição
Sendo coeficiente a coeficiente módulo \(q\).
$$
\begin{aligned}
c(x) = a(x) + b(x), \ c_i(x) = (a_i + b_i) \bmod q
\end{aligned}
$$

 Um detalhe que podemos utilizar é que \( a_i + b_i \leq 2(q-1)\), bastante uma única subtração em \(q\) quando necessária:

 ``` python
 def addition(a, b, q):
	c = len(a) * [0]
	for i in range(len(a)):
		c[i] = a[i] + b[i]
		if c[i] >= q:
			c[i] -= q
	return c
 ```

### Subtração
Similar a adição, mas exige uma atenção para evitar que ocorra _underflow_ quando \(a_i < b_i \), sendo necessário somarmos \(q\) para mantermos o resultado no intervalo do anél:
 ``` python
 def subtraction(a, b, q):
	c = len(a) * [0]
	for i in range(len(a)):
		c[i] = a[i] - b[i]
		if a[i] < b[i]:
			c[i] += q
	return c
 ```

### Negação
Operação que retorna o inverso aditivo \(b(x)\) de um polinômio \(a(x)\),  coeficiente a coeficiente, tal que \(a(x) + b(x) \equiv 0 \pmod{q}\).
 ``` python
 def negation(a, q):
	return [0 if a[i] == 0 else q - b[i] for i in range(len(a))]
 ```

### Multiplicação por escalar
Sendo \(s\) um escalar, a multiplicação por ele é aplicada a individualmente a cada coeficiente:
$$
\begin{aligned}
c_i(x) = s \cdot a_i \bmod q
\end{aligned}
$$

 ``` python
 def scalar_multiplication(a, s, q):
	return [a[i] * s % q for i in range(len(a))]
 ```

### Multiplicação Polinomial
Operação mais importante no contexto de criptografia, pois é o local onde diversa otimizações podem ser aplicadas. 

Iremos começar com a multiplicação básica, sem redução pelo anel, onde dados dois polinômios de grau \(n-1\), seu produto tem grau até \(2n-2\). Os coeficientes \(d_k\) são obtidos da soma dos produtos de coeficientes cujos índices somam \(k\). Essa operação também é chamada de **convolução**.
$$
\begin{aligned}
d_k = \sum_{i+j=k} a_i \cdot b_i \pmod{q}, k = 0, \ldots, 2n-2
\end{aligned}
$$

 ``` python
 def poly_multiplication_naive(a, b, q):
	n = len(a)
	d = [0] * (2*n-1)
	for i in range(n):
		for j in range(n):
			d[i + j] = (d[i + j] + a[i] + b[j]) % q
	return b
 ```

#### Redução via Convolução Cíclica ou Negacíclica
A redução modular opera de formas diferentes dependendo do polinômio redutor do anél. Irei abordar aqui as duas escolhas mais comuns na criptografia baseada em reticulados:

- **Convolução Cíclica (CC)**: Para o anél \(\mathbb{Z}_q[x] / (X^n-1)\), onde \(x^n \equiv 1\). Assim, os termos de grau alto são somados aos de graus baixos sem nenhuma inversão de sinal:

$$
\begin{aligned}
c_k = (d_k + d_{k+n}) \bmod q
\end{aligned}
$$

 ``` python
 def poly_multiplication_cc(a, b, q):
	n = len(a)
	c = poly_multiplication_naive(a, b, q)
	for i in range(n-1):
		c[i] = (c[i] + c[i+n]) % q
	return c[:n]
 ```

- **Convolução Negacíclica (NWC)**: Para o anél \(\mathbb{Z}_q[x] / (X^n+1)\), onde \(x^n \equiv -1\). Assim, os termos de grau alto são somados aos de graus baixos sofrendo uma inversão de sinal:
$$
\begin{aligned}
c_k = (d_k - d_{k+n}) \bmod q
\end{aligned}
$$

 ``` python
 def poly_multiplication_nwc(a, b, q):
	n = len(a)
	c = poly_multiplication_naive(a, b, q)
	for i in range(n-1):
		c[i] = (c[i] - c[i+n]) % q
	return c[:n]
 ```

#### Polinômio Redutor do BFV

O polinômio \(x^n+1\) não foi escolhido arbitráriamente para o BFV. Quando \(n = 2^d, d\in \mathbb{N}^*\), ele é o \(2n\)-nésimo polinômio ciclotômico, garantindo 

## References

[*An Introduction to Mathematical Cryptography*](https://link.springer.com/book/10.1007/978-1-4939-1711-2). Springer. Capítulos 2, 6 e 7.

[*Number Theoretic Transform - A Gentle Introduction: Part I*](https://cryptographycaffe.sandboxaq.com/posts/ntt-01/)  