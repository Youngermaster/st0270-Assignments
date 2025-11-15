class Grammar:
    def __init__(self):
        self.productions = {}
        self.terminals = set()
        self.non_terminals = set()
        self.first_sets = {}
        self.follow_sets = {}
        self.parse_table_ll1 = {}
        self.action_table = {}
        self.goto_table = {}
        
    def parse_input(self, n):
        """Lee n producciones de la entrada."""
        for _ in range(n):
            line = input().strip()
            parts = line.split(' -> ')
            nt = parts[0].strip()
            rhs_list = parts[1].strip().split()
            
            if nt not in self.productions:
                self.productions[nt] = []
                self.non_terminals.add(nt)
            
            for rhs_str in rhs_list:
                # Convertir la cadena en una lista de símbolos
                # (considerando operadores como '+', '*', etc. como símbolos individuales)
                symbols = list(rhs_str)
                self.productions[nt].append(symbols)
                
                # Extraer terminales y no terminales
                for symbol in symbols:
                    if symbol.isupper():
                        self.non_terminals.add(symbol)
                    elif symbol not in ['e']:
                        self.terminals.add(symbol)
        
        # Agregar marcador de fin
        self.terminals.add('$')
        
        # Calcular conjuntos FIRST y FOLLOW
        self.compute_first_sets()
        self.compute_follow_sets()
    
    def compute_first_sets(self):
        """Calcula los conjuntos FIRST para todos los símbolos."""
        # Inicializar conjuntos FIRST
        for nt in self.non_terminals:
            self.first_sets[nt] = set()
        
        # Los terminales tienen a sí mismos en su conjunto FIRST
        for t in self.terminals:
            self.first_sets[t] = {t}
        
        # Épsilon tiene a sí mismo en su conjunto FIRST
        self.first_sets['e'] = {'e'}
        
        # Algoritmo iterativo para calcular conjuntos FIRST
        changed = True
        while changed:
            changed = False
            
            for nt, productions in self.productions.items():
                for prod in productions:
                    # Si es una producción épsilon, agregar épsilon a FIRST(nt)
                    if prod == ['e']:
                        if 'e' not in self.first_sets[nt]:
                            self.first_sets[nt].add('e')
                            changed = True
                        continue
                    
                    # Para cada símbolo en la producción
                    all_can_derive_epsilon = True
                    for symbol in prod:
                        # Si es épsilon, continuar
                        if symbol == 'e':
                            continue
                        
                        # Agregar FIRST(symbol) - {e} a FIRST(nt)
                        for fs in self.first_sets.get(symbol, set()) - {'e'}:
                            if fs not in self.first_sets[nt]:
                                self.first_sets[nt].add(fs)
                                changed = True
                        
                        # Si este símbolo no puede derivar épsilon, detener el proceso
                        if 'e' not in self.first_sets.get(symbol, set()):
                            all_can_derive_epsilon = False
                            break
                    
                    # Si todos los símbolos pueden derivar épsilon, agregar épsilon a FIRST(nt)
                    if all_can_derive_epsilon and 'e' not in self.first_sets[nt]:
                        self.first_sets[nt].add('e')
                        changed = True
    
    def compute_follow_sets(self):
        """Calcula los conjuntos FOLLOW para todos los no terminales."""
        # Inicializar conjuntos FOLLOW
        for nt in self.non_terminals:
            self.follow_sets[nt] = set()
        
        # Agregar $ a FOLLOW(S) para el símbolo inicial
        self.follow_sets['S'].add('$')
        
        # Algoritmo iterativo para calcular conjuntos FOLLOW
        changed = True
        while changed:
            changed = False
            
            for nt, productions in self.productions.items():
                for prod in productions:
                    if prod == ['e']:
                        continue
                    
                    for i, symbol in enumerate(prod):
                        if symbol in self.non_terminals:
                            # Caso 1: A -> αBβ, agregar FIRST(β) - {e} a FOLLOW(B)
                            if i + 1 < len(prod):
                                rest = prod[i+1:]
                                first_of_rest = self.compute_first_of_string(rest)
                                
                                for fs in first_of_rest - {'e'}:
                                    if fs not in self.follow_sets[symbol]:
                                        self.follow_sets[symbol].add(fs)
                                        changed = True
                                
                                # Caso 2: Si β =>* ε, agregar FOLLOW(A) a FOLLOW(B)
                                if 'e' in first_of_rest:
                                    for fs in self.follow_sets[nt]:
                                        if fs not in self.follow_sets[symbol]:
                                            self.follow_sets[symbol].add(fs)
                                            changed = True
                            
                            # Caso 3: A -> αB, agregar FOLLOW(A) a FOLLOW(B)
                            else:
                                for fs in self.follow_sets[nt]:
                                    if fs not in self.follow_sets[symbol]:
                                        self.follow_sets[symbol].add(fs)
                                        changed = True
    
    def compute_first_of_string(self, symbols):
        """Calcula el conjunto FIRST para una cadena de símbolos."""
        if not symbols:
            return {'e'}
        
        result = set()
        all_derive_epsilon = True
        
        for symbol in symbols:
            if symbol == 'e':
                continue
                
            # Agregar FIRST(symbol) - {e} a result
            symbol_first = self.first_sets.get(symbol, set())
            for fs in symbol_first - {'e'}:
                result.add(fs)
            
            # Si este símbolo no puede derivar épsilon, detener el proceso
            if 'e' not in symbol_first:
                all_derive_epsilon = False
                break
        
        # Si todos los símbolos pueden derivar épsilon, agregar épsilon a result
        if all_derive_epsilon:
            result.add('e')
        
        return result
    
    def is_ll1(self):
        """Verifica si la gramática es LL(1) y construye la tabla de análisis."""
        self.parse_table_ll1 = {}
        
        # Inicializar tabla de análisis
        for nt in self.non_terminals:
            self.parse_table_ll1[nt] = {}
            for t in self.terminals:
                self.parse_table_ll1[nt][t] = None
        
        # Construir tabla LL(1)
        for nt, productions in self.productions.items():
            for i, prod in enumerate(productions):
                # Para cada terminal en FIRST(prod)
                first_of_prod = self.compute_first_of_string(prod)
                
                for terminal in first_of_prod - {'e'}:
                    # Comprobar conflictos
                    if self.parse_table_ll1[nt].get(terminal) is not None:
                        return False  # No es LL(1): conflicto
                    self.parse_table_ll1[nt][terminal] = (i, prod)
                
                # Si épsilon está en FIRST(prod), agregar producción a FOLLOW(nt)
                if 'e' in first_of_prod:
                    for terminal in self.follow_sets[nt]:
                        # Comprobar conflictos
                        if self.parse_table_ll1[nt].get(terminal) is not None:
                            return False  # No es LL(1): conflicto
                        self.parse_table_ll1[nt][terminal] = (i, prod)
        
        return True  # Es LL(1)
    
    def is_slr1(self):
        """Verifica si la gramática es SLR(1) y construye las tablas action y goto."""
        # Aumentar la gramática con S' -> S
        augmented_prods = {'S\'': [['S']]}
        for nt, prods in self.productions.items():
            augmented_prods[nt] = prods.copy()
        
        # Calcular la colección canónica de LR(0)
        canonical_collection = self.compute_canonical_collection(augmented_prods)
        
        # Inicializar tablas action y goto
        self.action_table = {}
        self.goto_table = {}
        
        for i in range(len(canonical_collection)):
            self.action_table[i] = {}
            self.goto_table[i] = {}
        
        # Construir tablas de análisis SLR(1)
        for i, state in enumerate(canonical_collection):
            for item in state:
                nt, prod, dot_pos = item
                
                # Si el punto está al final, es una acción de reducción
                if dot_pos == len(prod):
                    if nt == 'S\'' and prod == ['S']:
                        # Aceptar si es la producción inicial aumentada
                        self.action_table[i]['$'] = ('accept', None)
                    else:
                        # Para todos los terminales en FOLLOW(nt), agregar acción de reducción
                        for terminal in self.follow_sets.get(nt, []):
                            # Encontrar el índice de la producción
                            prod_idx = -1
                            for idx, p in enumerate(self.productions.get(nt, [])):
                                if p == prod:
                                    prod_idx = idx
                                    break
                            
                            # Agregar acción de reducción
                            if prod_idx != -1:
                                # Verificar conflictos
                                if terminal in self.action_table[i]:
                                    current_action = self.action_table[i][terminal]
                                    # Conflicto shift-reduce o reduce-reduce
                                    if (current_action[0] == 'shift' or 
                                        (current_action[0] == 'reduce' and current_action[1] != (nt, prod_idx))):
                                        return False  # No es SLR(1)
                                
                                self.action_table[i][terminal] = ('reduce', (nt, prod_idx))
                
                # Si el punto no está al final, ver el siguiente símbolo
                elif dot_pos < len(prod):
                    next_symbol = prod[dot_pos]
                    
                    # Calcular estado al que se va con este símbolo
                    goto_state = self.compute_goto_state(canonical_collection, i, next_symbol)
                    
                    if goto_state is not None:
                        # Para terminales, agregar acción shift
                        if next_symbol in self.terminals:
                            # Verificar conflictos
                            if next_symbol in self.action_table[i]:
                                current_action = self.action_table[i][next_symbol]
                                if current_action[0] == 'reduce':
                                    return False  # No es SLR(1): conflicto shift-reduce
                            
                            self.action_table[i][next_symbol] = ('shift', goto_state)
                        
                        # Para no terminales, agregar transición goto
                        elif next_symbol in self.non_terminals:
                            self.goto_table[i][next_symbol] = goto_state
        
        return True  # Es SLR(1)
    
    def compute_canonical_collection(self, augmented_prods):
        """Calcula la colección canónica de conjuntos de elementos LR(0)."""
        # Empezar con closure de {[S' -> .S]}
        initial_item = ('S\'', ['S'], 0)
        initial_state = self.compute_closure([initial_item], augmented_prods)
        
        # Inicializar colección con el estado inicial
        canonical_collection = [initial_state]
        states_hash = {self.state_to_hash(initial_state)}
        
        i = 0
        while i < len(canonical_collection):
            state = canonical_collection[i]
            
            # Encontrar todos los símbolos después de los puntos
            symbols = set()
            for item in state:
                nt, prod, dot_pos = item
                if dot_pos < len(prod):
                    symbols.add(prod[dot_pos])
            
            # Calcular GOTO para cada símbolo
            for symbol in symbols:
                next_state = self.compute_goto(state, symbol, augmented_prods)
                if not next_state:
                    continue
                
                # Verificar si este estado ya está en la colección
                next_state_hash = self.state_to_hash(next_state)
                if next_state_hash not in states_hash:
                    canonical_collection.append(next_state)
                    states_hash.add(next_state_hash)
            
            i += 1
        
        return canonical_collection
    
    def compute_closure(self, items, all_prods):
        """Calcula el closure de un conjunto de elementos LR(0)."""
        result = items.copy()
        item_set = {(nt, tuple(prod), pos) for nt, prod, pos in result}
        
        changed = True
        while changed:
            changed = False
            new_items = []
            
            for nt, prod, dot_pos in result:
                if dot_pos < len(prod) and prod[dot_pos] in self.non_terminals:
                    B = prod[dot_pos]
                    
                    for B_prod in all_prods.get(B, []):
                        new_item = (B, B_prod, 0)
                        new_item_key = (B, tuple(B_prod), 0)
                        
                        if new_item_key not in item_set:
                            new_items.append(new_item)
                            item_set.add(new_item_key)
                            changed = True
            
            result.extend(new_items)
        
        return result
    
    def compute_goto(self, state, symbol, all_prods):
        """Calcula el estado al que se llega desde un estado dado con un símbolo."""
        next_items = []
        
        for nt, prod, dot_pos in state:
            if dot_pos < len(prod) and prod[dot_pos] == symbol:
                next_items.append((nt, prod, dot_pos + 1))
        
        if not next_items:
            return []
        
        return self.compute_closure(next_items, all_prods)
    
    def compute_goto_state(self, canonical_collection, state_idx, symbol):
        """Encuentra el índice del estado al que se llega con un símbolo."""
        state = canonical_collection[state_idx]
        next_state = self.compute_goto(state, symbol, {nt: prods for nt, prods in self.productions.items()})
        
        if not next_state:
            return None
        
        # Buscar si este estado ya existe en la colección
        next_state_hash = self.state_to_hash(next_state)
        for i, s in enumerate(canonical_collection):
            if self.state_to_hash(s) == next_state_hash:
                return i
        
        return None
    
    def state_to_hash(self, state):
        """Convierte un estado a una representación hasheable."""
        return frozenset((nt, tuple(prod), pos) for nt, prod, pos in state)
    
    def parse_ll1(self, input_str):
        """Analiza una cadena usando el algoritmo LL(1)."""
        if not input_str.endswith('$'):
            input_str += '$'
        
        # Inicializar pila con símbolo inicial y marcador de fin
        stack = ['$', 'S']
        input_pos = 0
        
        while stack:
            # Obtener elemento superior de la pila
            X = stack[-1]
            
            # Obtener símbolo actual de entrada
            a = input_str[input_pos] if input_pos < len(input_str) else '$'
            
            # Caso 1: Coincidencia de terminal
            if X in self.terminals or X == '$':
                if X == a:
                    stack.pop()
                    input_pos += 1
                else:
                    return False  # Error
            
            # Caso 2: Expandir no terminal
            elif X in self.non_terminals:
                if a in self.parse_table_ll1.get(X, {}) and self.parse_table_ll1[X][a] is not None:
                    stack.pop()
                    _, production = self.parse_table_ll1[X][a]
                    
                    # Insertar producción en orden inverso
                    if production != ['e']:  # Omitir épsilon
                        for symbol in reversed(production):
                            stack.append(symbol)
                else:
                    return False  # Error
            
            else:
                return False  # Error
        
        # Verificar si se consumió toda la entrada
        return input_pos >= len(input_str)
    
    def parse_slr1(self, input_str):
        """Analiza una cadena usando el algoritmo SLR(1)."""
        if not input_str.endswith('$'):
            input_str += '$'
        
        # Inicializar pila con estado inicial
        stack = [(0, '$')]
        input_pos = 0
        
        while True:
            state = stack[-1][0]
            a = input_str[input_pos] if input_pos < len(input_str) else '$'
            
            if a in self.action_table.get(state, {}):
                action, value = self.action_table[state][a]
                
                if action == 'shift':
                    stack.append((value, a))
                    input_pos += 1
                
                elif action == 'reduce':
                    nt, prod_idx = value
                    production = self.productions[nt][prod_idx]
                    
                    # Desapilar |production| símbolos
                    if production != ['e']:  # Manejar producción épsilon
                        for _ in range(len(production)):
                            stack.pop()
                    
                    # Ir al nuevo estado
                    prev_state = stack[-1][0]
                    if nt in self.goto_table.get(prev_state, {}):
                        new_state = self.goto_table[prev_state][nt]
                        stack.append((new_state, nt))
                    else:
                        return False  # Error
                
                elif action == 'accept':
                    return True
                
                else:
                    return False  # Error
            
            else:
                return False  # Error


def main():
    # Leer número de no terminales
    n = int(input().strip())
    
    # Crear e inicializar la gramática
    grammar = Grammar()
    grammar.parse_input(n)
    
    # Verificar si la gramática es LL(1) y/o SLR(1)
    is_ll1 = grammar.is_ll1()
    is_slr1 = grammar.is_slr1()
    
    if is_ll1 and is_slr1:
        print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
        while True:
            choice = input().strip().upper()
            
            if choice == 'Q':
                break
            elif choice == 'T':
                parse_strings(grammar, 'LL1')
                print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
            elif choice == 'B':
                parse_strings(grammar, 'SLR1')
                print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
    
    elif is_ll1:
        print("Grammar is LL(1).")
        parse_strings(grammar, 'LL1')
    
    elif is_slr1:
        print("Grammar is SLR(1).")
        parse_strings(grammar, 'SLR1')
    
    else:
        print("Grammar is neither LL(1) nor SLR(1).")


def parse_strings(grammar, parser_type):
    """Analiza cadenas de entrada usando el parser especificado."""
    while True:
        input_str = input().strip()
        if not input_str:
            break
        
        if parser_type == 'LL1':
            result = grammar.parse_ll1(input_str)
        else:  # SLR1
            result = grammar.parse_slr1(input_str)
        
        print("yes" if result else "no")


if __name__ == "__main__":
    main()