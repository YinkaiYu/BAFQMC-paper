function [eta, metric_name] = contraction_metric( ...
    statistics, g, second, action_on_g, square)
  if strcmp(statistics, "boson")
    statistics_sign = -1;
  elseif strcmp(statistics, "fermion")
    statistics_sign = 1;
  else
    error("Unknown statistics: %s", statistics);
  endif
  if statistics_sign * square * action_on_g == 1
    eta = second * g;
    metric_name = "J2g";
  else
    eta = 1i * second * g;
    metric_name = "iJ2g";
  endif
  assert(norm(eta - eta', "fro") < 1e-12);
  assert(norm(eta * eta - eye(rows(eta)), "fro") < 1e-12);
endfunction
