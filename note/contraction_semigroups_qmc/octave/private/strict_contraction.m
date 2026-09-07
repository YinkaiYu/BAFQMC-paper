function answer = strict_contraction(statistics, signs)
  if strcmp(statistics, "boson")
    statistics_sign = -1;
  elseif strcmp(statistics, "fermion")
    statistics_sign = 1;
  else
    error("Unknown statistics: %s", statistics);
  endif
  answer = signs(4) == -statistics_sign && ...
           signs(5) == -signs(1) * signs(3);
endfunction
