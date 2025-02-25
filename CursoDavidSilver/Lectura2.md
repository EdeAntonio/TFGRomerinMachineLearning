# Procesos de decisión Markov MDP
## Procesos Markov
### Introducción a los MDPs
Un MDP es un exosistema de aprendizaje por refuerzo totalmente observable. La mayorí de los problemas sobre AR se pueden formalizar como MDPs.
### Proceso Markov o Cadena Markov
Un proceso Markov es un proceso aleatorio que recorre una secuencia de estados, donde los estados son finitos y existe una probabilidad de transicionar de uno a otro. Esta probabilidad se recoge en la matriz de transición Markov.
### Matriz de transición Markov
La matriz de transición comprende todas las probabilidades de pasar de un estado a otro. En un conjunto de tres estados se podría describir una matriz de transición 3x3 de modo que:

P={(P_1a1, P_1a2, P_1a3), (P_2a1, P_2a2, P_2a3), (P_3a1, P_3a2, P_3a3)} donde P_iaj=P[S_t+1 = S_j | S_t=S_i]

![MatrizTransicionMarkov](../ImagenesRelevantes/MatrizTransicionMarkov.png)

## Proceso de recompensa Markov
Un proceso de recompensa Markov es un proceso markov con valores. El proceso de recompens Markov contiene estados finitos S, matriz de probabilidad P, función de recompensa R y factor de descuento dto.
### Retorno.
El retorno es la recompensa total descontada para un paso de tiempo t tal que:

    G_t = R_t1+dto\*R_t2+...=Sum(k=0; inf;k++){(dto\*\*k)\*R(t+k+1)}

### Función de Valor
La función de valor devuelve para un estado valores a largo plazo de ese estado, de modo que:

    v(s) = E[G_t | S_t = s] = E[R_t1 + dto\*R_t2 + (dto\*\*k)\*R_t3+... | S_t = s]

### Ecuación Belman para MRPs
La función de valor entonces se puede descomponer en dos partes, la recompensa inmediata R_t1 y el valor del siguiente estado, ya que:

    v(s) = E[R_t+1 + dto(R_t2 + dto\*R_t3+...) | S_t = s] = E[R_t1 + dto\*Gt1 | S_t = s]

Por tanto para una V\[n_estados\], R\[n_estados\], P\[n_estados\]\[n_estados\], encontramos la ecuación:
    V = R + dto \* P \* V
    V = (1- dto \* P) \*\* -1 \* R

