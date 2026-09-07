function sign_value = matrix_sign(left, right)
  tolerance = 1e-12;
  if norm(left - right, "fro") < tolerance
    sign_value = 1;
  elseif norm(left + right, "fro") < tolerance
    sign_value = -1;
  else
    error("Matrices are not equal up to sign.");
  endif
endfunction
