function sign_value = commutation_sign(first, second)
  tolerance = 1e-12;
  if norm(first * second - second * first, "fro") < tolerance
    sign_value = 1;
  elseif norm(first * second + second * first, "fro") < tolerance
    sign_value = -1;
  else
    error("Matrices neither commute nor anticommute.");
  endif
endfunction
