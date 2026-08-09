function signs = five_relations(g, first, second)
  identity = eye(rows(g));
  signs = [
    matrix_sign(first.' * g * first, g),
    matrix_sign(first * first, identity),
    matrix_sign(second.' * g * second, g),
    matrix_sign(second * second, identity),
    commutation_sign(first, second)
  ];
endfunction
