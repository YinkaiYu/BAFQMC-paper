function scan_pauli_realizations()
  more off;
  format long g;

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  output_file = fullfile(table_dir, "pauli_realization_scan.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,n,matrix_dimension,realization_count," ...
                "maximal_dimensions,cone_linear_dimensions," ...
                "maximal_min_dimension,maximal_max_dimension," ...
                "cone_min_dimension,cone_max_dimension," ...
                "min_maximal_pair,max_maximal_pair," ...
                "min_cone_pair,max_cone_pair,strict_interior," ...
                "worst_A0_lie_residual,worst_A0_reality_residual," ...
                "worst_A0_contraction_residual\n"]);

  statistics_names = {"boson", "fermion"};
  output_rows = 0;
  checked_realizations = 0;
  strict_realizations = 0;

  for statistics_index = 1:numel(statistics_names)
    statistics = statistics_names{statistics_index};
    for n = 1:3
      [names, matrices] = pauli_words(n);
      g = canonical_g(statistics, n);
      dimension = rows(g);
      aggregates = cell(32, 1);

      for first = 1:numel(names)
        J1 = matrices{first};
        for second = 1:numel(names)
          if first == second
            continue;
          endif
          J2 = matrices{second};
          signs = [
            matrix_sign(J1.' * g * J1, g),
            matrix_sign(J1 * J1, eye(dimension)),
            matrix_sign(J2.' * g * J2, g),
            matrix_sign(J2 * J2, eye(dimension)),
            commutation_sign(J1, J2)
          ];
          class_index = signs_to_index(signs);
          [eta, ~] = canonical_metric( ...
              statistics, g, J2, signs(3), signs(4));
          [maximal_dimension, cone_dimension] = ...
              structure_dimensions(g, J1, eta, n);
          pair_name = [names{first}, "/", names{second}];
          strict = strict_interior(statistics, signs);

          if isempty(aggregates{class_index})
            entry.signs = signs;
            entry.count = 0;
            entry.maximal_dimensions = [];
            entry.cone_dimensions = [];
            entry.min_maximal = Inf;
            entry.max_maximal = -Inf;
            entry.min_cone = Inf;
            entry.max_cone = -Inf;
            entry.min_maximal_pair = "";
            entry.max_maximal_pair = "";
            entry.min_cone_pair = "";
            entry.max_cone_pair = "";
            entry.strict = strict;
            entry.worst_lie = 0;
            entry.worst_reality = 0;
            entry.worst_contraction = 0;
          else
            entry = aggregates{class_index};
            assert(entry.strict == strict);
          endif

          entry.count += 1;
          entry.maximal_dimensions(end + 1) = maximal_dimension;
          entry.cone_dimensions(end + 1) = cone_dimension;
          if maximal_dimension < entry.min_maximal
            entry.min_maximal = maximal_dimension;
            entry.min_maximal_pair = pair_name;
          endif
          if maximal_dimension > entry.max_maximal
            entry.max_maximal = maximal_dimension;
            entry.max_maximal_pair = pair_name;
          endif
          if cone_dimension < entry.min_cone
            entry.min_cone = cone_dimension;
            entry.min_cone_pair = pair_name;
          endif
          if cone_dimension > entry.max_cone
            entry.max_cone = cone_dimension;
            entry.max_cone_pair = pair_name;
          endif

          if strict
            A0 = -eta;
            entry.worst_lie = max( ...
                entry.worst_lie, norm(g * A0 + A0.' * g, "fro"));
            entry.worst_reality = max( ...
                entry.worst_reality, ...
                norm(J1.' * A0 * J1 - conj(A0), "fro"));
            entry.worst_contraction = max( ...
                entry.worst_contraction, ...
                norm(eta * A0 + A0' * eta + 2 * eye(dimension), ...
                     "fro"));
            strict_realizations += 1;
          endif

          aggregates{class_index} = entry;
          checked_realizations += 1;
        endfor
      endfor

      for class_index = 1:32
        if isempty(aggregates{class_index})
          continue;
        endif
        entry = aggregates{class_index};
        maximal_values = unique(entry.maximal_dimensions);
        cone_values = unique(entry.cone_dimensions);
        if entry.strict
          assert(entry.worst_lie < 1e-10);
          assert(entry.worst_reality < 1e-10);
          assert(entry.worst_contraction < 1e-10);
        endif
        fprintf(fid, ...
                ["%s,%s,%d,%d,%d,\"%s\",\"%s\",%d,%d,%d,%d," ...
                 "%s,%s,%s,%s,%d,%.16g,%.16g,%.16g\n"], ...
                statistics, class_label(entry.signs), n, dimension, ...
                entry.count, integer_list(maximal_values), ...
                integer_list(cone_values), ...
                entry.min_maximal, entry.max_maximal, ...
                entry.min_cone, entry.max_cone, ...
                entry.min_maximal_pair, entry.max_maximal_pair, ...
                entry.min_cone_pair, entry.max_cone_pair, ...
                entry.strict, entry.worst_lie, entry.worst_reality, ...
                entry.worst_contraction);
        output_rows += 1;
      endfor
    endfor
  endfor
  fclose(fid);

  printf("Octave version: %s\n", version());
  printf("Checked %d distinct ordered Pauli realizations.\n", ...
         checked_realizations);
  printf(["Verified A0=-eta for all %d strict-class realizations " ...
          "encountered.\n"], strict_realizations);
  printf("Wrote %d aggregate rows to %s\n", output_rows, output_file);
endfunction


function [maximal_dimension, cone_dimension] = ...
    structure_dimensions(g, J1, eta, n)
  [~, matrices] = pauli_words(n);
  maximal_dimension = 0;
  cone_dimension = 0;
  for word_index = 1:numel(matrices)
    for phase = [1, 1i]
      A = phase * matrices{word_index};
      if norm(g * A + A.' * g, "fro") > 1e-11
        continue;
      endif
      if norm(J1.' * A * J1 - conj(A), "fro") > 1e-11
        continue;
      endif
      if norm(eta * A + A' * eta, "fro") < 1e-11
        maximal_dimension += 1;
      endif
      if norm(eta * A - A' * eta, "fro") < 1e-11
        cone_dimension += 1;
      endif
    endfor
  endfor
endfunction


function value = integer_list(values)
  pieces = cell(1, numel(values));
  for index = 1:numel(values)
    pieces{index} = sprintf("%d", values(index));
  endfor
  value = strjoin(pieces, ";");
endfunction


function [eta, metric_name] = canonical_metric( ...
    statistics, g, J2, s2, q2)
  if strcmp(statistics, "boson")
    tau = -1;
  else
    tau = 1;
  endif
  if tau * q2 * s2 == 1
    eta = J2 * g;
    metric_name = "J2g";
  else
    eta = 1i * J2 * g;
    metric_name = "iJ2g";
  endif
  assert(norm(eta - eta', "fro") < 1e-11);
  assert(norm(eta * eta - eye(rows(eta)), "fro") < 1e-11);
endfunction


function strict = strict_interior(statistics, signs)
  if strcmp(statistics, "boson")
    tau = -1;
  else
    tau = 1;
  endif
  strict = signs(4) == -tau && signs(5) == -signs(1) * signs(3);
endfunction


function g = canonical_g(statistics, n)
  if strcmp(statistics, "boson")
    g = kron(-pauli_matrix("Y"), eye(2^(n - 1)));
  else
    g = kron(pauli_matrix("X"), eye(2^(n - 1)));
  endif
endfunction


function [names, matrices] = pauli_words(n)
  labels = "IXYZ";
  names = cell(4^n, 1);
  matrices = cell(4^n, 1);
  for value = 0:(4^n - 1)
    digits = dec2base(value, 4, n) - "0";
    name = "";
    matrix = 1;
    for position = 1:n
      label = labels(digits(position) + 1);
      name = [name, label];
      matrix = kron(matrix, pauli_matrix(label));
    endfor
    names{value + 1} = name;
    matrices{value + 1} = matrix;
  endfor
endfunction


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
      error("Unknown Pauli label %s", label);
  endswitch
endfunction


function sign_value = matrix_sign(left, right)
  if norm(left - right, "fro") < 1e-11
    sign_value = 1;
  elseif norm(left + right, "fro") < 1e-11
    sign_value = -1;
  else
    error("Matrices are not equal up to sign");
  endif
endfunction


function sign_value = commutation_sign(first, second)
  if norm(first * second - second * first, "fro") < 1e-11
    sign_value = 1;
  elseif norm(first * second + second * first, "fro") < 1e-11
    sign_value = -1;
  else
    error("Matrices neither commute nor anticommute");
  endif
endfunction


function index = signs_to_index(signs)
  bits = (signs == -1);
  index = 1 + [16, 8, 4, 2, 1] * bits(:);
endfunction


function label = class_label(signs)
  labels = {"s1", "q1", "s2", "q2", "r"};
  pieces = cell(1, 5);
  for index = 1:5
    if signs(index) == 1
      sign_label = "+";
    else
      sign_label = "-";
    endif
    pieces{index} = [labels{index}, sign_label];
  endfor
  label = strjoin(pieces, "_");
endfunction
