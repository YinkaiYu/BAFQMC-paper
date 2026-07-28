function derive_strict_generator_structures()
  more off;
  format long g;

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  cases = strict_cases();
  output_file = fullfile(table_dir, "strict_generator_structures.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_name,n,J1_word,J2_word,metric," ...
                "s1,q1,s2,q2,r,eta,A0,maximal_subgroup_dimension," ...
                "invariant_cone_dimension,maximal_subgroup_basis," ...
                "invariant_cone_basis,maximal_tensor_terms," ...
                "invariant_cone_tensor_terms," ...
                "maximal_number_tensor_terms," ...
                "invariant_cone_number_tensor_terms," ...
                "maximal_tensor_dimension_formula," ...
                "invariant_cone_tensor_dimension_formula," ...
                "A0_physical_adjoint," ...
                "A0_number_conserving,A0_boson_stability," ...
                "relation_residual,lie_residual,reality_residual," ...
                "cone_residual\n"]);

  for case_index = 1:rows(cases)
    statistics = cases{case_index, 1};
    class_name = cases{case_index, 2};
    J1_word = cases{case_index, 3};
    J2_word = cases{case_index, 4};
    metric_name = cases{case_index, 5};
    expected_signs = cell2mat(cases(case_index, 6:10));
    n = length(J1_word);

    g = canonical_g(statistics, n);
    J1 = pauli_word(J1_word);
    J2 = pauli_word(J2_word);
    dimension = rows(g);
    if strcmp(metric_name, "J2g")
      eta = J2 * g;
    else
      eta = 1i * J2 * g;
    endif
    A0 = -eta;

    signs = [
      matrix_sign(J1.' * g * J1, g),
      matrix_sign(J1 * J1, eye(dimension)),
      matrix_sign(J2.' * g * J2, g),
      matrix_sign(J2 * J2, eye(dimension)),
      commutation_sign(J1, J2)
    ];
    signs = signs(:).';
    if !all(signs == expected_signs)
      error("%s: signs %s do not match expected %s", class_name, ...
            mat2str(signs), mat2str(expected_signs));
    endif

    [subgroup_basis, cone_basis, subgroup_matrices, cone_matrices] = ...
        generator_bases(g, J1, eta, n);
    assert(length(subgroup_basis) + length(cone_basis) > 0);
    assert(in_real_span(A0, cone_matrices));

    relation_residual = pauli_relation_residuals(g, J1, J2, signs);
    lie_residual = norm(g * A0 + A0.' * g, "fro");
    reality_residual = norm(J1.' * A0 * J1 - conj(A0), "fro");
    cone_residual = norm(eta * A0 + A0' * eta + 2 * eye(dimension), "fro");
    assert(max([relation_residual, lie_residual, reality_residual, ...
                cone_residual]) < 1e-11);

    [physical_adjoint, number_conserving, boson_stability] = ...
        physical_diagnostics(statistics, g, A0, n);
    [maximal_tensor_terms, cone_tensor_terms, ...
     maximal_number_tensor_terms, cone_number_tensor_terms, ...
     maximal_tensor_dimension_formula, cone_tensor_dimension_formula] = ...
        tensor_generator_terms(g, J1, J2, eta, n);

    fprintf(fid, ...
            ["%s,%s,%d,%s,%s,%s,%d,%d,%d,%d,%d,%s,%s,%d,%d," ...
             "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"," ...
             "%s,%d,%s,%.16g,%.16g,%.16g,%.16g\n"], ...
            statistics, class_name, n, J1_word, J2_word, metric_name, ...
            signs, matrix_label(eta, n), matrix_label(A0, n), ...
            length(subgroup_basis), length(cone_basis), ...
            strjoin(subgroup_basis, ";"), strjoin(cone_basis, ";"), ...
            strjoin(maximal_tensor_terms, ";"), ...
            strjoin(cone_tensor_terms, ";"), ...
            strjoin(maximal_number_tensor_terms, ";"), ...
            strjoin(cone_number_tensor_terms, ";"), ...
            maximal_tensor_dimension_formula, cone_tensor_dimension_formula, ...
            physical_adjoint, number_conserving, boson_stability, ...
            relation_residual, lie_residual, reality_residual, cone_residual);
  endfor
  fclose(fid);

  printf("Octave version: %s\n", version());
  printf("Verified %d strict classes.\n", rows(cases));
  printf("Wrote %s\n", output_file);
endfunction


function [maximal_terms, cone_terms, maximal_number_terms, ...
          cone_number_terms, maximal_formula, cone_formula] = ...
    tensor_generator_terms(g, J1, J2, eta, n)
  [word_names, word_matrices] = pauli_words(n);
  maximal_terms = {};
  cone_terms = {};
  maximal_number_terms = {};
  cone_number_terms = {};
  maximal_dimension_terms = {};
  cone_dimension_terms = {};

  for word_index = 1:length(word_names)
    P = word_matrices{word_index};
    transpose_sign = matrix_sign(P.' * g, g * P);
    J1_sign = matrix_sign(J1.' * P * J1, P);
    J2_sign = matrix_sign(J2.' * P * J2, P);
    coefficient_type = tensor_coefficient_type(transpose_sign, J1_sign);
    term = sprintf("%s:%s", word_names{word_index}, coefficient_type);
    dimension_term = tensor_coefficient_dimension(coefficient_type);
    number_conserving = ...
        word_names{word_index}(1) == "I" || word_names{word_index}(1) == "Z";

    coefficient = tensor_test_coefficient(coefficient_type);
    test_A = kron(P, coefficient);
    test_g = kron(g, eye(rows(coefficient)));
    test_J1 = kron(J1, eye(rows(coefficient)));
    test_eta = kron(eta, eye(rows(coefficient)));
    assert(norm(test_g * test_A + test_A.' * test_g, "fro") < 1e-10);
    assert(norm(test_J1.' * test_A * test_J1 - conj(test_A), "fro") < 1e-10);

    if J2_sign == J1_sign
      assert(norm(test_eta * test_A + test_A' * test_eta, "fro") < 1e-10);
      maximal_terms{end + 1} = term;
      maximal_dimension_terms{end + 1} = dimension_term;
      if number_conserving
        maximal_number_terms{end + 1} = term;
      endif
    else
      assert(norm(test_eta * test_A - test_A' * test_eta, "fro") < 1e-10);
      cone_terms{end + 1} = term;
      cone_dimension_terms{end + 1} = dimension_term;
      if number_conserving
        cone_number_terms{end + 1} = term;
      endif
    endif
  endfor

  maximal_formula = tensor_dimension_formula(maximal_dimension_terms);
  cone_formula = tensor_dimension_formula(cone_dimension_terms);
endfunction


function coefficient_type = tensor_coefficient_type( ...
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


function dimension_term = tensor_coefficient_dimension(coefficient_type)
  if endsWith(coefficient_type, "_S")
    dimension_term = "m(m+1)/2";
  else
    dimension_term = "m(m-1)/2";
  endif
endfunction


function formula = tensor_dimension_formula(terms)
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


function coefficient = tensor_test_coefficient(coefficient_type)
  symmetric = [1, 2; 2, -1];
  antisymmetric = [0, 1; -1, 0];
  if endsWith(coefficient_type, "_S")
    coefficient = symmetric;
  else
    coefficient = antisymmetric;
  endif
  if startsWith(coefficient_type, "i")
    coefficient *= 1i;
  endif
endfunction


function cases = strict_cases()
  % The first tensor factor is always Nambu.  Y denotes the real matrix
  % i*sigma_y.  Representatives are chosen so that J2g=Z in the standard
  % branch and A0=-eta has a transparent operator interpretation.
  cases = {
    "boson", "B-J2g-s1+q1+", "IX",  "XI",  "J2g",  1,  1, -1,  1,  1;
    "boson", "B-J2g-s1+q1-", "IY",  "XI",  "J2g",  1, -1, -1,  1,  1;
    "boson", "B-J2g-s1-q1+", "Z",   "X",   "J2g", -1,  1, -1,  1, -1;
    "boson", "B-J2g-s1-q1-", "ZY",  "XI",  "J2g", -1, -1, -1,  1, -1;
    "boson", "B-iJ2g-s1+q1+", "IX",  "YY",  "iJ2g",  1,  1,  1,  1, -1;
    "boson", "B-iJ2g-s1+q1-", "YX",  "YY",  "iJ2g",  1, -1,  1,  1, -1;
    "boson", "B-iJ2g-s1-q1+", "ZX",  "YY",  "iJ2g", -1,  1,  1,  1,  1;
    "boson", "B-iJ2g-s1-q1-", "XIY", "YYX", "iJ2g", -1, -1,  1,  1,  1;
    "fermion", "F-J2g-s1+q1+", "IX",  "YI",  "J2g",  1,  1, -1, -1,  1;
    "fermion", "F-J2g-s1+q1-", "IY",  "YI",  "J2g",  1, -1, -1, -1,  1;
    "fermion", "F-J2g-s1-q1+", "Z",   "Y",   "J2g", -1,  1, -1, -1, -1;
    "fermion", "F-J2g-s1-q1-", "ZY",  "YI",  "J2g", -1, -1, -1, -1, -1;
    "fermion", "F-iJ2g-s1+q1+", "IX",  "IY",  "iJ2g",  1,  1,  1, -1, -1;
    "fermion", "F-iJ2g-s1+q1-", "IXY", "IYI", "iJ2g",  1, -1,  1, -1, -1;
    "fermion", "F-iJ2g-s1-q1+", "ZI",  "IY",  "iJ2g", -1,  1,  1, -1,  1;
    "fermion", "F-iJ2g-s1-q1-", "YI",  "IY",  "iJ2g", -1, -1,  1, -1,  1
  };
endfunction


function [subgroup_names, cone_names, subgroup_matrices, cone_matrices] = ...
    generator_bases(g, J1, eta, n)
  [word_names, word_matrices] = pauli_words(n);
  subgroup_names = {};
  cone_names = {};
  subgroup_matrices = {};
  cone_matrices = {};
  for word_index = 1:length(word_names)
    for phase_index = 1:2
      if phase_index == 1
        phase = 1;
        candidate_name = word_names{word_index};
      else
        phase = 1i;
        candidate_name = ["i", word_names{word_index}];
      endif
      A = phase * word_matrices{word_index};
      if norm(g * A + A.' * g, "fro") > 1e-11
        continue;
      endif
      if norm(J1.' * A * J1 - conj(A), "fro") > 1e-11
        continue;
      endif
      if norm(eta * A + A' * eta, "fro") < 1e-11
        subgroup_names{end + 1} = candidate_name;
        subgroup_matrices{end + 1} = A;
      endif
      if norm(eta * A - A' * eta, "fro") < 1e-11
        cone_names{end + 1} = candidate_name;
        cone_matrices{end + 1} = A;
      endif
    endfor
  endfor
endfunction


function [physical_adjoint, number_conserving, boson_stability] = ...
    physical_diagnostics(statistics, g, A, n)
  internal_dimension = 2^(n - 1);
  exchange = kron(pauli_matrix("X"), eye(internal_dimension));
  coefficient = g * A;
  adjoint_coefficient = exchange * coefficient' * exchange;
  if norm(adjoint_coefficient - coefficient, "fro") < 1e-11
    physical_adjoint = "Hermitian";
  elseif norm(adjoint_coefficient + coefficient, "fro") < 1e-11
    physical_adjoint = "anti-Hermitian";
  else
    physical_adjoint = "neither";
  endif

  upper_right = A(1:internal_dimension, internal_dimension + 1:end);
  lower_left = A(internal_dimension + 1:end, 1:internal_dimension);
  number_conserving = ...
      norm(upper_right, "fro") + norm(lower_left, "fro") < 1e-11;

  boson_stability = "not_applicable";
  if strcmp(statistics, "boson") && number_conserving && ...
      strcmp(physical_adjoint, "Hermitian")
    B = A(1:internal_dimension, 1:internal_dimension);
    eigenvalues = eig(B);
    if max(real(eigenvalues)) < -1e-11
      boson_stability = "grand_canonical_stable";
    elseif min(real(eigenvalues)) < -1e-11 && ...
           max(real(eigenvalues)) > 1e-11
      boson_stability = "mixed_sign_one_body_spectrum";
    else
      boson_stability = "not_strictly_stable";
    endif
  endif
endfunction


function answer = in_real_span(target, basis)
  if isempty(basis)
    answer = false;
    return;
  endif
  target_vector = [real(target(:)); imag(target(:))];
  basis_matrix = zeros(length(target_vector), length(basis));
  for index = 1:length(basis)
    vector = basis{index}(:);
    basis_matrix(:, index) = [real(vector); imag(vector)];
  endfor
  coefficients = basis_matrix \ target_vector;
  answer = norm(basis_matrix * coefficients - target_vector) < 1e-10;
endfunction


function label = matrix_label(matrix, n)
  [names, matrices] = pauli_words(n);
  dimension = rows(matrix);
  for index = 1:length(names)
    coefficient = trace(matrices{index}' * matrix) / dimension;
    if abs(coefficient) < 1e-11
      continue;
    endif
    if norm(matrix - coefficient * matrices{index}, "fro") < 1e-11
      if abs(coefficient - 1) < 1e-11
        label = names{index};
      elseif abs(coefficient + 1) < 1e-11
        label = ["-", names{index}];
      elseif abs(coefficient - 1i) < 1e-11
        label = ["i", names{index}];
      elseif abs(coefficient + 1i) < 1e-11
        label = ["-i", names{index}];
      else
        label = sprintf("%.12g*%s", coefficient, names{index});
      endif
      return;
    endif
  endfor
  error("Matrix is not a single Pauli word.");
endfunction


function g = canonical_g(statistics, n)
  if strcmp(statistics, "boson")
    g = kron(-pauli_matrix("Y"), eye(2^(n - 1)));
  elseif strcmp(statistics, "fermion")
    g = kron(pauli_matrix("X"), eye(2^(n - 1)));
  else
    error("Unknown statistics: %s", statistics);
  endif
endfunction


function [names, matrices] = pauli_words(n)
  labels = "IXYZ";
  word_count = 4^n;
  names = cell(word_count, 1);
  matrices = cell(word_count, 1);
  for value = 0:(word_count - 1)
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


function matrix = pauli_word(name)
  matrix = 1;
  for position = 1:length(name)
    matrix = kron(matrix, pauli_matrix(name(position)));
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
  if norm(left - right, "fro") < 1e-11
    sign = 1;
  elseif norm(left + right, "fro") < 1e-11
    sign = -1;
  else
    error("Matrices are not related by a sign.");
  endif
endfunction


function sign = commutation_sign(J1, J2)
  if norm(J1 * J2 - J2 * J1, "fro") < 1e-11
    sign = 1;
  elseif norm(J1 * J2 + J2 * J1, "fro") < 1e-11
    sign = -1;
  else
    error("Matrices neither commute nor anticommute.");
  endif
endfunction


function residual = pauli_relation_residuals(g, J1, J2, signs)
  dimension = rows(g);
  residual = max([
    norm(J1.' * g * J1 - signs(1) * g, "fro"),
    norm(J1 * J1 - signs(2) * eye(dimension), "fro"),
    norm(J2.' * g * J2 - signs(3) * g, "fro"),
    norm(J2 * J2 - signs(4) * eye(dimension), "fro"),
    norm(J1 * J2 - signs(5) * J2 * J1, "fro")
  ]);
endfunction
