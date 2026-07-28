function derive_tensor_block_structures()
  more off;
  format long g;

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  output_file = fullfile(table_dir, "tensor_block_structures.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,n,J1_word,J2_word,metric," ...
                "s1,q1,s2,q2,r,strict_interior," ...
                "maximal_terms,cone_linear_terms," ...
                "maximal_number_conserving_terms," ...
                "cone_number_conserving_terms," ...
                "maximal_dimension_formula,cone_dimension_formula," ...
                "maximal_residual,cone_residual\n"]);

  statistics_names = {"boson", "fermion"};
  row_count = 0;
  for statistics_index = 1:numel(statistics_names)
    statistics = statistics_names{statistics_index};
    witnesses = find_minimal_witnesses(statistics);
    for class_index = 1:32
      witness = witnesses{class_index};
      n = witness.n;
      g = canonical_g(statistics, n);
      [eta, metric_name] = canonical_metric( ...
          statistics, g, witness.J2, ...
          witness.signs(3), witness.signs(4));
      [names, matrices] = pauli_words(n);

      maximal_terms = {};
      cone_terms = {};
      maximal_number_terms = {};
      cone_number_terms = {};
      maximal_dimension_terms = {};
      cone_dimension_terms = {};
      maximal_residual = 0;
      cone_residual = 0;

      for index = 1:numel(names)
        P = matrices{index};
        transpose_sign = matrix_sign(P.' * g, g * P);
        J1_sign = matrix_sign(witness.J1.' * P * witness.J1, P);
        J2_sign = matrix_sign(witness.J2.' * P * witness.J2, P);
        coefficient_type = matrix_coefficient_type( ...
            transpose_sign, J1_sign);
        term = sprintf("%s:%s", names{index}, coefficient_type);
        dimension_term = coefficient_dimension_term(coefficient_type);
        number_conserving = names{index}(1) == "I" || ...
                            names{index}(1) == "Z";

        test_matrix = test_coefficient_matrix(coefficient_type);
        test_A = kron(P, test_matrix);
        test_g = kron(g, eye(rows(test_matrix)));
        test_J1 = kron(witness.J1, eye(rows(test_matrix)));
        test_J2 = kron(witness.J2, eye(rows(test_matrix)));
        test_eta = kron(eta, eye(rows(test_matrix)));

        if J2_sign == J1_sign
          maximal_terms{end + 1} = term;
          maximal_dimension_terms{end + 1} = dimension_term;
          if number_conserving
            maximal_number_terms{end + 1} = term;
          endif
          maximal_residual = max(maximal_residual, max([
            norm(test_g * test_A + test_A.' * test_g, "fro"),
            norm(test_J1.' * test_A * test_J1 - conj(test_A), "fro"),
            norm(test_J2.' * test_A * test_J2 - conj(test_A), "fro"),
            norm(test_eta * test_A + test_A' * test_eta, "fro")
          ]));
        else
          cone_terms{end + 1} = term;
          cone_dimension_terms{end + 1} = dimension_term;
          if number_conserving
            cone_number_terms{end + 1} = term;
          endif
          cone_residual = max(cone_residual, max([
            norm(test_g * test_A + test_A.' * test_g, "fro"),
            norm(test_J1.' * test_A * test_J1 - conj(test_A), "fro"),
            norm(test_J2.' * test_A * test_J2 + conj(test_A), "fro"),
            norm(test_eta * test_A - test_A' * test_eta, "fro")
          ]));
        endif
      endfor

      assert(maximal_residual < 1e-10);
      assert(cone_residual < 1e-10);
      strict = strict_interior(statistics, witness.signs);
      fprintf(fid, ...
              ["%s,%s,%d,%s,%s,%s,%d,%d,%d,%d,%d,%d," ...
               "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"," ...
               "%.16g,%.16g\n"], ...
              statistics, class_label(witness.signs), n, ...
              witness.J1_name, witness.J2_name, metric_name, ...
              witness.signs, strict, ...
              strjoin(maximal_terms, ";"), strjoin(cone_terms, ";"), ...
              strjoin(maximal_number_terms, ";"), ...
              strjoin(cone_number_terms, ";"), ...
              join_dimension_formula(maximal_dimension_terms), ...
              join_dimension_formula(cone_dimension_terms), ...
              maximal_residual, cone_residual);
      row_count += 1;
    endfor
  endfor
  fclose(fid);

  assert(row_count == 64);
  printf("Octave version: %s\n", version());
  printf("Verified tensor-block formulas for %d classes.\n", row_count);
  printf("Wrote %s\n", output_file);
endfunction


function coefficient_type = matrix_coefficient_type( ...
    transpose_sign, reality_sign)
  if transpose_sign == 1
    transpose_label = "A";
  else
    transpose_label = "S";
  endif
  if reality_sign == 1
    coefficient_type = ["R_", transpose_label];
  else
    coefficient_type = ["iR_", transpose_label];
  endif
endfunction


function dimension_term = coefficient_dimension_term(coefficient_type)
  if endsWith(coefficient_type, "_S")
    dimension_term = "m(m+1)/2";
  else
    dimension_term = "m(m-1)/2";
  endif
endfunction


function formula = join_dimension_formula(terms)
  symmetric_count = sum(strcmp(terms, "m(m+1)/2"));
  antisymmetric_count = sum(strcmp(terms, "m(m-1)/2"));
  pieces = {};
  if symmetric_count > 0
    pieces{end + 1} = sprintf("%d*m*(m+1)/2", symmetric_count);
  endif
  if antisymmetric_count > 0
    pieces{end + 1} = sprintf("%d*m*(m-1)/2", antisymmetric_count);
  endif
  if isempty(pieces)
    formula = "0";
  else
    formula = strjoin(pieces, "+");
  endif
endfunction


function matrix = test_coefficient_matrix(coefficient_type)
  symmetric = [1, 2; 2, -1];
  antisymmetric = [0, 1; -1, 0];
  if endsWith(coefficient_type, "_S")
    matrix = symmetric;
  else
    matrix = antisymmetric;
  endif
  if startsWith(coefficient_type, "i")
    matrix *= 1i;
  endif
endfunction


function witnesses = find_minimal_witnesses(statistics)
  witnesses = cell(32, 1);
  for n = 1:3
    [names, matrices] = pauli_words(n);
    g = canonical_g(statistics, n);
    dimension = rows(g);
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
        if isempty(witnesses{class_index})
          witness.n = n;
          witness.signs = signs;
          witness.J1_name = names{first};
          witness.J2_name = names{second};
          witness.J1 = J1;
          witness.J2 = J2;
          witnesses{class_index} = witness;
        endif
      endfor
    endfor
  endfor
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
      error("Unknown Pauli label: %s", label);
  endswitch
endfunction


function sign = matrix_sign(left, right)
  if norm(left - right, "fro") < 1e-10
    sign = 1;
  elseif norm(left + right, "fro") < 1e-10
    sign = -1;
  else
    error("Matrices are not related by a sign.");
  endif
endfunction


function sign = commutation_sign(J1, J2)
  if norm(J1 * J2 - J2 * J1, "fro") < 1e-10
    sign = 1;
  elseif norm(J1 * J2 + J2 * J1, "fro") < 1e-10
    sign = -1;
  else
    error("Matrices neither commute nor anticommute.");
  endif
endfunction


function index = signs_to_index(signs)
  bits = (signs == -1);
  index = 1 + bits(:).' * [16; 8; 4; 2; 1];
endfunction


function label = class_label(signs)
  label = sprintf("s1%s_q1%s_s2%s_q2%s_r%s", ...
                  sign_character(signs(1)), sign_character(signs(2)), ...
                  sign_character(signs(3)), sign_character(signs(4)), ...
                  sign_character(signs(5)));
endfunction


function character = sign_character(sign)
  if sign == 1
    character = "+";
  else
    character = "-";
  endif
endfunction
