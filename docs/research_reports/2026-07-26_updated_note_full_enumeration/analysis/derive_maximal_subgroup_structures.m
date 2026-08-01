function derive_maximal_subgroup_structures()
  more off;
  format long g;
  rng(20260728, "twister");

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  output_file = fullfile(table_dir, "maximal_subgroup_structures.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,n,J1_word,J2_word,metric," ...
                "s1,q1,s2,q2,r,strict_interior," ...
                "maximal_subgroup_dimension,maximal_subgroup_basis," ...
                "number_conserving_dimension,number_conserving_basis," ...
                "second_antilinear_residual,lie_closure_residual," ...
                "majorana_q1,majorana_q2,majorana_r," ...
                "majorana_transport_residual,mtr_class," ...
                "maximal_subgroup_sign_guaranteed," ...
                "random_min_real_weight,random_max_abs_imag_weight," ...
                "random_negative_count,random_trials\n"]);

  statistics_names = {"boson", "fermion"};
  total_rows = 0;
  fermion_guaranteed = 0;
  fermion_strict = 0;
  fermion_guaranteed_boundary_only = 0;

  for statistics_index = 1:numel(statistics_names)
    statistics = statistics_names{statistics_index};
    witnesses = find_minimal_witnesses(statistics);
    for class_index = 1:32
      witness = witnesses{class_index};
      signs = witness.signs;
      s1 = signs(1);
      q1 = signs(2);
      s2 = signs(3);
      q2 = signs(4);
      r = signs(5);
      n = witness.n;
      g = canonical_g(statistics, n);
      [eta, metric_name] = canonical_metric( ...
          statistics, g, witness.J2, s2, q2);

      [basis_names, basis_matrices, number_names] = ...
          maximal_subgroup_basis(g, witness.J1, eta, n);
      second_residual = second_antilinear_residual( ...
          basis_matrices, witness.J2);
      closure_residual = lie_closure_residual(basis_matrices);
      assert(second_residual < 1e-10);
      assert(closure_residual < 1e-9);

      strict = strict_interior(statistics, signs);
      majorana_q1 = NaN;
      majorana_q2 = NaN;
      majorana_r = NaN;
      majorana_transport_residual = NaN;
      mtr_class = "not_applicable";
      sign_guaranteed = 0;
      random_minimum = NaN;
      random_maximum_imaginary = NaN;
      random_negative_count = 0;
      random_trials = 0;

      if strcmp(statistics, "fermion")
        [majorana_q1, majorana_q2, majorana_r, ...
         majorana_transport_residual] = ...
            majorana_symmetry_signs(witness.J1, witness.J2, n);
        assert(majorana_transport_residual < 1e-10);
        [mtr_class, sign_guaranteed] = classify_mtr_pair( ...
            majorana_q1, majorana_q2, majorana_r);

        random_trials = 600;
        rng(20260728 + class_index, "twister");
        if isempty(basis_matrices)
          random_minimum = 2^(2^(n - 1));
          random_maximum_imaginary = 0;
          random_negative_count = 0;
        else
          [random_minimum, random_maximum_imaginary, ...
           random_negative_count] = exact_fermion_fock_scan( ...
              g, basis_matrices, n, random_trials);
        endif

        if sign_guaranteed
          fermion_guaranteed += 1;
          assert(random_minimum > -1e-8);
          assert(random_maximum_imaginary < 1e-8);
          if strict
            fermion_strict += 1;
          else
            fermion_guaranteed_boundary_only += 1;
          endif
        endif
      endif

      fprintf(fid, ...
              ["%s,%s,%d,%s,%s,%s,%d,%d,%d,%d,%d,%d,%d,\"%s\"," ...
               "%d,\"%s\",%.16g,%.16g,%.16g,%.16g,%.16g,%.16g," ...
               "%s,%d,%.16g,%.16g,%d,%d\n"], ...
              statistics, class_label(signs), n, ...
              witness.J1_name, witness.J2_name, metric_name, signs, ...
              strict, numel(basis_names), strjoin(basis_names, ";"), ...
              numel(number_names), strjoin(number_names, ";"), ...
              second_residual, closure_residual, ...
              majorana_q1, majorana_q2, majorana_r, ...
              majorana_transport_residual, mtr_class, sign_guaranteed, ...
              random_minimum, random_maximum_imaginary, ...
              random_negative_count, random_trials);
      total_rows += 1;
    endfor
  endfor
  fclose(fid);

  assert(total_rows == 64);
  assert(fermion_strict == 8);
  assert(fermion_guaranteed_boundary_only == 4);
  assert(fermion_guaranteed == 12);

  printf("Octave version: %s\n", version());
  printf("Verified maximal-subgroup bases for %d classes.\n", total_rows);
  printf(["Fermions: %d classes have an actual Spin half-power proof on " ...
          "A_group (%d conjugate-Majorana and %d Kramers-particle-space " ...
          "classes).\n"], ...
         fermion_guaranteed, fermion_guaranteed - ...
         fermion_guaranteed_boundary_only, ...
         fermion_guaranteed_boundary_only);
  printf(["Among them, %d classes also admit a strict A_cone, but the " ...
          "A_group proof does not automatically extend to nonzero " ...
          "A_cone.\n"], fermion_strict);
  printf("Wrote %s\n", output_file);
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
  for index = 1:32
    assert(!isempty(witnesses{index}));
  endfor
endfunction


function [eta, metric_name] = canonical_metric( ...
    statistics, g, J2, s2, q2)
  if strcmp(statistics, "boson")
    tau = -1;
  else
    tau = 1;
  endif
  delta = tau * q2 * s2;
  if delta == 1
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
  s1 = signs(1);
  s2 = signs(3);
  q2 = signs(4);
  r = signs(5);
  strict = (q2 == -tau) && (r == -s1 * s2);
endfunction


function [basis_names, basis_matrices, number_names] = ...
    maximal_subgroup_basis(g, J1, eta, n)
  [word_names, word_matrices] = pauli_words(n);
  basis_names = {};
  basis_matrices = {};
  number_names = {};
  internal_dimension = 2^(n - 1);
  for word_index = 1:numel(word_names)
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
      if norm(eta * A + A' * eta, "fro") > 1e-11
        continue;
      endif
      basis_names{end + 1} = candidate_name;
      basis_matrices{end + 1} = A;
      upper_right = ...
          A(1:internal_dimension, internal_dimension + 1:end);
      lower_left = ...
          A(internal_dimension + 1:end, 1:internal_dimension);
      if norm(upper_right, "fro") + norm(lower_left, "fro") < 1e-11
        number_names{end + 1} = candidate_name;
      endif
    endfor
  endfor
endfunction


function residual = second_antilinear_residual(basis, J2)
  residual = 0;
  for index = 1:numel(basis)
    A = basis{index};
    residual = max(residual, ...
                   norm(J2.' * A * J2 - conj(A), "fro"));
  endfor
endfunction


function residual = lie_closure_residual(basis)
  if isempty(basis)
    residual = 0;
    return;
  endif
  columns = zeros(2 * numel(basis{1}), numel(basis));
  for index = 1:numel(basis)
    vector = basis{index}(:);
    columns(:, index) = [real(vector); imag(vector)];
  endfor
  projector = columns * pinv(columns);
  residual = 0;
  for first = 1:numel(basis)
    for second = 1:numel(basis)
      commutator = basis{first} * basis{second} - ...
                   basis{second} * basis{first};
      vector = [real(commutator(:)); imag(commutator(:))];
      residual = max(residual, norm(vector - projector * vector));
    endfor
  endfor
endfunction


function [q1, q2, r, residual] = ...
    majorana_symmetry_signs(J1, J2, n)
  internal_dimension = 2^(n - 1);
  identity = eye(internal_dimension);
  U = [identity, identity; -1i * identity, 1i * identity];
  U_inverse_conjugate = conj(inv(U));

  T1_raw = U * J1 * U_inverse_conjugate;
  T2_raw = U * J2 * U_inverse_conjugate;
  [T1, residual1] = real_majorana_representative(T1_raw);
  [T2, residual2] = real_majorana_representative(T2_raw);

  dimension = rows(T1);
  q1 = matrix_sign(T1 * T1, eye(dimension));
  q2 = matrix_sign(T2 * T2, eye(dimension));
  r = commutation_sign(T1, T2);
  orthogonal_residual = max([
    norm(T1.' * T1 - eye(dimension), "fro"),
    norm(T2.' * T2 - eye(dimension), "fro")
  ]);
  residual = max([residual1, residual2, orthogonal_residual]);
endfunction


function [T, residual] = real_majorana_representative(T_raw)
  candidates = {T_raw, 1i * T_raw, -1i * T_raw, -T_raw};
  best_residual = Inf;
  best = [];
  for index = 1:numel(candidates)
    candidate = candidates{index};
    current_residual = norm(imag(candidate), "fro");
    if current_residual < best_residual
      best_residual = current_residual;
      best = real(candidate);
    endif
  endfor
  T = best;
  residual = best_residual;
endfunction


function [class_name, sign_guaranteed] = classify_mtr_pair(q1, q2, r)
  sign_guaranteed = 0;
  if r == -1 && q1 == -1 && q2 == -1
    class_name = "Kramers_Tminus_Tminus";
    sign_guaranteed = 1;
  elseif r == -1 && q1 * q2 == -1
    class_name = "Majorana_Tplus_Tminus";
    sign_guaranteed = 1;
  elseif r == -1
    class_name = "Tplus_Tplus_not_generic";
  else
    class_name = "commuting_pair_not_generic";
  endif
endfunction


function [minimum_weight, maximum_imaginary, negative_count] = ...
    exact_fermion_fock_scan(g, basis, n, trial_count)
  internal_dimension = 2^(n - 1);
  [chi, fock_dimension] = fermion_nambu_operators(internal_dimension);
  fock_basis = cell(numel(basis), 1);
  for index = 1:numel(basis)
    fock_basis{index} = quadratic_fock_operator( ...
        g * basis{index}, chi, fock_dimension);
  endfor

  minimum_weight = Inf;
  maximum_imaginary = 0;
  negative_count = 0;
  coefficient_scale = 1.2 / sqrt(numel(fock_basis));
  for trial = 1:trial_count
    slice_count = 1 + randi(4);
    product = eye(fock_dimension);
    for slice = 1:slice_count
      h = zeros(fock_dimension);
      for index = 1:numel(fock_basis)
        h += coefficient_scale * randn() * fock_basis{index};
      endfor
      product = product * expm(h);
    endfor
    weight = trace(product);
    minimum_weight = min(minimum_weight, real(weight));
    maximum_imaginary = max(maximum_imaginary, abs(imag(weight)));
    if real(weight) < -1e-8 && abs(imag(weight)) < 1e-7
      negative_count += 1;
    endif
  endfor
endfunction


function [chi, fock_dimension] = fermion_nambu_operators(mode_count)
  lowering = [0, 1; 0, 0];
  parity = [1, 0; 0, -1];
  identity = eye(2);
  annihilation = cell(mode_count, 1);
  for mode = 1:mode_count
    operator = 1;
    for position = 1:mode_count
      if position < mode
        operator = kron(operator, parity);
      elseif position == mode
        operator = kron(operator, lowering);
      else
        operator = kron(operator, identity);
      endif
    endfor
    annihilation{mode} = operator;
  endfor
  chi = cell(2 * mode_count, 1);
  for mode = 1:mode_count
    chi{mode} = annihilation{mode};
    chi{mode_count + mode} = annihilation{mode}';
  endfor
  fock_dimension = 2^mode_count;
endfunction


function h = quadratic_fock_operator(coefficient, chi, fock_dimension)
  h = zeros(fock_dimension);
  for first = 1:numel(chi)
    for second = 1:numel(chi)
      h += 0.5 * coefficient(first, second) * ...
           chi{first} * chi{second};
    endfor
  endfor
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
