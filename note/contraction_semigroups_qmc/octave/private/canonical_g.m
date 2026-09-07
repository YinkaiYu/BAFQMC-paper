function g = canonical_g(statistics, number_of_factors)
  internal = eye(2^(number_of_factors - 1));
  if strcmp(statistics, "boson")
    g = kron(-pauli_matrix("Y"), internal);
  elseif strcmp(statistics, "fermion")
    g = kron(pauli_matrix("X"), internal);
  else
    error("Unknown statistics: %s", statistics);
  endif
endfunction
