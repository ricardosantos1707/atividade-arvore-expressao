# -*- coding: utf-8 -*-


class No:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def obter_altura(self, no):
        if not no:
            return 0
        return no.altura

    def obter_fator_balanceamento(self, no):
        if not no:
            return 0
        return self.obter_altura(no.esquerda) - self.obter_altura(no.direita)

    def _atualizar_altura(self, no):
        no.altura = 1 + max(self.obter_altura(no.esquerda), self.obter_altura(no.direita))

    def obter_no_valor_minimo(self, no):
        atual = no
        while atual.esquerda:
            atual = atual.esquerda
        return atual

    def _rotacao_direita(self, no_pivo):
        novo_pai = no_pivo.esquerda
        no_pivo.esquerda = novo_pai.direita
        novo_pai.direita = no_pivo

        self._atualizar_altura(no_pivo)
        self._atualizar_altura(novo_pai)
        return novo_pai

    def _rotacao_esquerda(self, no_pivo):
        novo_pai = no_pivo.direita
        no_pivo.direita = novo_pai.esquerda
        novo_pai.esquerda = no_pivo

        self._atualizar_altura(no_pivo)
        self._atualizar_altura(novo_pai)
        return novo_pai

    def inserir(self, chave):
        self.raiz = self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no_atual, chave):
        if not no_atual:
            return No(chave)
        elif chave < no_atual.chave:
            no_atual.esquerda = self._inserir_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._inserir_recursivo(no_atual.direita, chave)
        else:
            raise ValueError("Chave duplicada não permitida.")

        self._atualizar_altura(no_atual)

        balanceamento = self.obter_fator_balanceamento(no_atual)

        # Caso 1: Esquerda-Esquerda
        if balanceamento > 1 and chave < no_atual.esquerda.chave:
            return self._rotacao_direita(no_atual)

        # Caso 2: Direita-Direita
        if balanceamento < -1 and chave > no_atual.direita.chave:
            return self._rotacao_esquerda(no_atual)

        # Caso 3: Esquerda-Direita
        if balanceamento > 1 and chave > no_atual.esquerda.chave:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)

        # Caso 4: Direita-Esquerda
        if balanceamento < -1 and chave < no_atual.direita.chave:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    def deletar(self, chave):
        self.raiz = self._deletar_recursivo(self.raiz, chave)

    def _deletar_recursivo(self, no_atual, chave):
        if not no_atual:
            return no_atual

        if chave < no_atual.chave:
            no_atual.esquerda = self._deletar_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._deletar_recursivo(no_atual.direita, chave)
        else:
            # Caso 1: Um ou nenhum filho
            if not no_atual.esquerda:
                return no_atual.direita
            elif not no_atual.direita:
                return no_atual.esquerda

            # Caso 2: Dois filhos
            temp = self.obter_no_valor_minimo(no_atual.direita)
            no_atual.chave = temp.chave
            no_atual.direita = self._deletar_recursivo(no_atual.direita, temp.chave)

        self._atualizar_altura(no_atual)

        balanceamento = self.obter_fator_balanceamento(no_atual)

        # Caso 1: Esquerda-Esquerda
        if balanceamento > 1 and self.obter_fator_balanceamento(no_atual.esquerda) >= 0:
            return self._rotacao_direita(no_atual)

        # Caso 2: Esquerda-Direita
        if balanceamento > 1 and self.obter_fator_balanceamento(no_atual.esquerda) < 0:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)

        # Caso 3: Direita-Direita
        if balanceamento < -1 and self.obter_fator_balanceamento(no_atual.direita) <= 0:
            return self._rotacao_esquerda(no_atual)

        # Caso 4: Direita-Esquerda
        if balanceamento < -1 and self.obter_fator_balanceamento(no_atual.direita) > 0:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    def encontrar_nos_intervalo(self, chave1, chave2):
        resultado = []
        self._buscar_intervalo(self.raiz, chave1, chave2, resultado)
        return resultado

    def _buscar_intervalo(self, no, chave1, chave2, resultado):
        if not no:
            return
        if chave1 < no.chave:
            self._buscar_intervalo(no.esquerda, chave1, chave2, resultado)
        if chave1 <= no.chave <= chave2:
            resultado.append(no.chave)
        if chave2 > no.chave:
            self._buscar_intervalo(no.direita, chave1, chave2, resultado)

    def obter_profundidade_no(self, chave):
        return self._buscar_profundidade(self.raiz, chave, 0)

    def _buscar_profundidade(self, no, chave, nivel):
        if not no:
            return -1
        if chave == no.chave:
            return nivel
        elif chave < no.chave:
            return self._buscar_profundidade(no.esquerda, chave, nivel + 1)
        else:
            return self._buscar_profundidade(no.direita, chave, nivel + 1)


# --- Bloco de Teste ---
if __name__ == "__main__":
    arvore_avl = ArvoreAVL()

    print("\n--- ATIVIDADE PRÁTICA: ÁRVORE AVL ---")

    print("\n--- 1. Inserindo nós ---")
    chaves_para_inserir = [9, 5, 10, 0, 6, 11, -1, 1, 2]
    try:
        for chave in chaves_para_inserir:
            arvore_avl.inserir(chave)
        print("Inserção concluída (sem erros).")
    except Exception as e:
        print(f"\nERRO DURANTE A INSERÇÃO: {e}")

    print("\n--- 2. Deletando nós ---")
    try:
        chaves_para_deletar = [10, 11]
        for chave in chaves_para_deletar:
            arvore_avl.deletar(chave)
        print("Deleção concluída (sem erros).")
    except Exception as e:
        print(f"\nERRO DURANTE A DELEÇÃO: {e}")

    print("\n--- 3. Buscando nós no intervalo [1, 9] ---")
    try:
        nos_no_intervalo = arvore_avl.encontrar_nos_intervalo(1, 9)
        if nos_no_intervalo is not None:
            print(f"Nós encontrados: {sorted(nos_no_intervalo)}")
        else:
            print("Método `encontrar_nos_intervalo` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE A BUSCA POR INTERVALO: {e}")

        print("\n--- 4. Calculando profundidade do nó 6 ---")
    try:
        profundidade = arvore_avl.obter_profundidade_no(6)
        if profundidade is not None:
            if profundidade != -1:
                print(f"O nó 6 está no nível/profundidade: {profundidade}")
            else:
                print("O nó 6 não foi encontrado.")
        else:
            print("Método `obter_profundidade_no` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE O CÁLCULO DE PROFUNDIDADE: {e}")