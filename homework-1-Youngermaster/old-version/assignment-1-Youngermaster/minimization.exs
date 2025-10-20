defmodule Minimization do
  # Entry point: read input.txt and process all cases.
  def main do
    input = File.read!("input.txt")
    lines = input |> String.trim() |> String.split("\n", trim: true)
    [cases_line | rest] = lines
    num_cases = String.to_integer(cases_line)
    outputs = process_cases(rest, num_cases, [])
    Enum.each(outputs, &IO.puts/1)
  end

  # Process each test case recursively.
  # defp process_cases(lines, 0, acc), do: Enum.reverse(acc)
  defp process_cases(_, 0, acc), do: Enum.reverse(acc)

  defp process_cases(lines, num_cases, acc) do
    # Read the number of states.
    [n_line | rest] = lines
    n = String.to_integer(n_line)

    # Next line: alphabet symbols (we only need its length).
    [alphabet_line | rest] = rest
    alphabet = String.split(alphabet_line, " ")

    # Next line: final states (as a set for fast membership checks).
    [final_states_line | rest] = rest

    final_states =
      final_states_line
      |> String.split()
      |> Enum.map(&String.to_integer/1)
      |> MapSet.new()

    # Next n lines: the transition table.
    {transition_lines, rest} = Enum.split(rest, n)
    transitions = parse_transitions(transition_lines)

    # Although the input is assumed to have no inaccessible states, we remove them.
    reachable_set = remove_inaccessible_states(transitions, alphabet, 0)
    reachable = reachable_set |> MapSet.to_list() |> Enum.sort()

    # Generate all ordered pairs (p, q) with p < q among reachable states.
    pairs = for p <- reachable, q <- reachable, p < q, do: {p, q}

    # Initially mark pairs where one state is final and the other is not.
    initial_marked =
      Enum.reduce(pairs, MapSet.new(), fn {p, q}, marked ->
        if (MapSet.member?(final_states, p) and not MapSet.member?(final_states, q)) or
             (not MapSet.member?(final_states, p) and MapSet.member?(final_states, q)) do
          MapSet.put(marked, {p, q})
        else
          marked
        end
      end)

    # Iteratively refine the marked set.
    marked = refine(pairs, alphabet, transitions, initial_marked)

    # The equivalent (i.e. collapsible) pairs are those not marked.
    equivalent_pairs =
      pairs
      |> Enum.filter(fn pair -> not MapSet.member?(marked, pair) end)
      |> Enum.sort(fn {a1, b1}, {a2, b2} ->
        if a1 == a2, do: b1 <= b2, else: a1 <= a2
      end)

    # Format the pairs as "(p, q)" and join them with a space.
    output_line =
      equivalent_pairs
      |> Enum.map(fn {p, q} ->
        "(" <> Integer.to_string(p) <> ", " <> Integer.to_string(q) <> ")"
      end)
      |> Enum.join(" ")

    process_cases(rest, num_cases - 1, [output_line | acc])
  end

  # Parse the transition lines into a list where the i-th element is a list of transitions for state i.
  defp parse_transitions(lines) do
    lines
    |> Enum.map(fn line ->
      values = line |> String.split() |> Enum.map(&String.to_integer/1)
      {hd(values), tl(values)}
    end)
    |> Enum.sort_by(fn {state, _} -> state end)
    |> Enum.map(fn {_state, transitions} -> transitions end)
  end

  # Given a transitions table, get the next state for a given state and symbol index.
  defp get_transition(transitions, state, symbol_index) do
    transitions
    |> Enum.at(state)
    |> Enum.at(symbol_index)
  end

  # Perform a breadth-first search starting at initial_state to find all reachable states.
  defp remove_inaccessible_states(transitions, alphabet, initial_state) do
    do_bfs([initial_state], MapSet.new(), transitions, alphabet)
  end

  defp do_bfs([], visited, _transitions, _alphabet), do: visited

  defp do_bfs([state | queue], visited, transitions, alphabet) do
    if MapSet.member?(visited, state) do
      do_bfs(queue, visited, transitions, alphabet)
    else
      visited = MapSet.put(visited, state)

      next_states =
        Enum.map(0..(length(alphabet) - 1), fn i ->
          get_transition(transitions, state, i)
        end)

      do_bfs(queue ++ next_states, visited, transitions, alphabet)
    end
  end

  # Helper: returns the canonical (ordered) pair.
  defp canonical_pair(a, b) do
    if a <= b, do: {a, b}, else: {b, a}
  end

  # Iteratively mark non-equivalent pairs.
  defp refine(pairs, alphabet, transitions, marked) do
    new_marked =
      Enum.reduce(pairs, marked, fn {p, q} = pair, acc ->
        if MapSet.member?(acc, pair) do
          acc
        else
          # For each symbol, check if the transitions lead to a pair that is already marked.
          mark_this =
            Enum.any?(0..(length(alphabet) - 1), fn i ->
              p_next = get_transition(transitions, p, i)
              q_next = get_transition(transitions, q, i)

              if p_next == q_next do
                false
              else
                canonical_pair(p_next, q_next)
                |> (fn cp -> MapSet.member?(acc, cp) end).()
              end
            end)

          if mark_this, do: MapSet.put(acc, pair), else: acc
        end
      end)

    if MapSet.size(new_marked) == MapSet.size(marked) do
      marked
    else
      refine(pairs, alphabet, transitions, new_marked)
    end
  end
end

Minimization.main()
