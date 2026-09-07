function [names, matrices] = pauli_words(number_of_factors)
  labels = "IXYZ";
  count = 4^number_of_factors;
  names = cell(count, 1);
  matrices = cell(count, 1);
  for value = 0:(count - 1)
    digits = dec2base(value, 4, number_of_factors) - "0";
    name = "";
    matrix = 1;
    for position = 1:number_of_factors
      label = labels(digits(position) + 1);
      name = [name, label];
      matrix = kron(matrix, pauli_matrix(label));
    endfor
    names{value + 1} = name;
    matrices{value + 1} = matrix;
  endfor
endfunction
