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

Um anel é um conjunto \(\mathbb{R}\) equipado com duas operações, denotadas por \(+\) e \(\star\), que satisfazem propriedades como a existência do elemento neutro, associatividade, comutatividade e distributividade entre as operações, além de possuir o inverso aditivo. Caso o anel possua um elemento neutro multiplicativo, ele é chamado de "anel unitário". Exemplificando, temos o famoso anel dos inteiros \(\mathbb{Z}\).

Ao definirmos \(R/(q) = R/qR\), sendo \(q \in \mathbb{R}\) e \(q \neq 0\), construimos um **anel quociente**. Ele é obtido ao tomando o quociente de \(R\) pelo ideal \(qR = \{qk : k \in \mathbb{Z}\}\). Os elementos de \(R/(q)\) são as classes de equivalência módulo q:

$$
\begin{aligned}
\bar{0}, \, \bar{1},& \, \ldots, \, \overline{q-1}\\
\end{aligned}
$$

onde \(\bar{a} = \{ a + qk \mid k \in \mathbb{Z} \}\).

Anéis quocientes são um elemento importante na criptografia, pois essas estruturas criam limites e garantem que os resultados das operações se mantenham no conjunto estipulado.

Se \(q\) for um números primo, todo elemento não nulo possuí um inverso multiplicativo, e a estrutura passa a ser chamada de **corpo**.

### Anéis de Polinômios

Ao utilizarmos valores de um anél \(R\) como coeficientes de polinômios, podemos criar um anél polinomial \(R[x]\) como sendo o conjunto de todos os polinômios na variável \(x\) com coeficientes de \(R\). Definimos um anél polinomial da seguinte forma:

$$
\begin{aligned}
R[x] = {a_0 + a_1x + 1_2x^2 + \ldots + a_n x^n : n \geq 0 \text{ e } a_0, a_1, \ldots, a_n \in R}
\end{aligned}
$$

Podemos exemplificar com \(R = \mathbb{Z}_q\), criando \(\mathbb{Z_q[x]}\), o anél de polinômios cujos coeficientes são inteiros módulo \(q\). Nesses anéis a adição é coeficiente a coeficiente, e a multiplicação segue a regra de expansão, onde cada termo de um polinômio multiplica todos os termos do outro. Os polinômios podem possuir qualquer grau, mas fica evidente a facilidade no crescimento do mesmo a cada multiplicação, podemos se tornar impraticável em algumas aplicações.

### Anéis Quociente de Polinômios

Similar ao que apresentamos anteriormente para limitar os elementos de um anél, podemos aplicar a mesma ideiaa do quociente para evitarmos que o grau dos polinômios aumente exacerbadamente. Para tal escolhemos um polinômio \(f(x)\) e e formamos o anel quociente \(\mathbb{Z}_q[x] / (f(x))\), onde dois polinômios são equivalentes se sua diferença é divisível por \(f(x)\). Por exemplo, sejam \(q = 7\) e \(f(x) = x^4 + 1\), teremos o seguinte anél polinômial:
$$
\begin{aligned}
\underbrace{\mathbb{Z}_7[x]}_{\text{polinômios com coefs em }\{0,\ldots,6\}}
  \;\xrightarrow{\;\bmod\;(x^4+1)\;}\;
  \underbrace{\mathbb{Z}_7[x]/(x^4+1)}_{R:\;\text{grau}\,\leq 3,\;\text{coefs em }\{0,\ldots,6\}}
\end{aligned}
$$

Dessa forma, temos como número total de elementos: 
$$
\begin{aligned}
q^\text{grau do polinômio módulo} = 7^4 = 2401
\end{aligned}
$$

## Anel \(R_q = \mathbb{Z}_q[x]/ (x^n+1) \)





## References

[*An Introduction to Mathematical Cryptography*](https://link.springer.com/book/10.1007/978-1-4939-1711-2). Springer. Capítulos 2, 6 e 7.

[*Number Theoretic Transform - A Gentle Introduction: Part I*](https://cryptographycaffe.sandboxaq.com/posts/ntt-01/)  