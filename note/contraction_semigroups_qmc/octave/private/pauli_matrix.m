function matrix = pauli_matrix(label)
  switch label
    case "I"
      matrix = eye(2);
    case "X"
      matrix = [0, 1; 1, 0];
    case "Y"
      matrix = [0, 1; -1, 0];
    case "Z"
      matrix = [1, 0; 0, -1];
    otherwise
      error("Unknown real Pauli label: %s", label);
  endswitch
endfunction
