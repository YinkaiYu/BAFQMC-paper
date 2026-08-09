function witnesses = find_minimal_witnesses(statistics)
  witnesses = cell(32, 1);
  for number_of_factors = 1:3
    [names, matrices] = pauli_words(number_of_factors);
    g = canonical_g(statistics, number_of_factors);
    for first_index = 1:numel(names)
      first = matrices{first_index};
      for second_index = 1:numel(names)
        if first_index == second_index
          continue;
        endif
        second = matrices{second_index};
        signs = five_relations(g, first, second);
        index = signs_to_index(signs);
        if isempty(witnesses{index})
          witness.n = number_of_factors;
          witness.signs = signs;
          witness.J1_name = names{first_index};
          witness.J2_name = names{second_index};
          witness.J1 = first;
          witness.J2 = second;
          witnesses{index} = witness;
        endif
      endfor
    endfor
  endfor
endfunction
