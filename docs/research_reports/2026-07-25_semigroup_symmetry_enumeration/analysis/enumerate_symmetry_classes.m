function enumerate_symmetry_classes()
  more off;
  format long g;
  rng(20260725, "twister");

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  printf("Octave version: %s\n", version());
  printf("Random seed: 20260725 (twister)\n");
  printf("Convention: Y = i*sigma_y = [0,1;-1,0]\n");

  class_file = fullfile(table_dir, "pauli_class_witnesses.csv");
  fid = fopen(class_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,s1,q1,s2,q2,r,min_qubits," ...
                "J1_word,J2_word\n"]);

  all_witnesses = cell(2, 1);
  statistics_names = {"boson", "fermion"};
  for statistics_index = 1:2
    statistics = statistics_names{statistics_index};
    witnesses = find_minimal_witnesses(statistics);
    all_witnesses{statistics_index} = witnesses;
    found_count = 0;
    for class_index = 1:32
      witness = witnesses{class_index};
      if isempty(witness)
        continue;
      endif
      found_count += 1;
      signs = witness.signs;
      fprintf(fid, "%s,%s,%d,%d,%d,%d,%d,%d,%s,%s\n", ...
              statistics, class_label(signs), signs(1), signs(2), ...
              signs(3), signs(4), signs(5), witness.n, ...
              witness.J1_name, witness.J2_name);
    endfor
    printf("%s: %d/32 abstract sign classes have distinct, nonidentity ", ...
           statistics, found_count);
    printf("real-Pauli-string witnesses with at most three tensor factors.\n");
    assert(found_count == 32);
  endfor
  fclose(fid);

  verify_collaborator_examples();
  write_true_eta_class_table(all_witnesses, table_dir);
  write_boson_reference_diagnostic(table_dir);
  result_file = scan_true_eta_maximal_subgroups(table_dir);
  write_boson_partner_test(table_dir);
  write_boson_four_partner_test(table_dir);
  printf("Wrote %s\n", class_file);
  printf("Wrote %s\n", result_file);
endfunction


function witnesses = find_minimal_witnesses(statistics)
  witnesses = cell(32, 1);
  for n = 1:3
    current = find_witnesses_at_n(statistics, n);
    for class_index = 1:32
      if isempty(witnesses{class_index}) && !isempty(current{class_index})
        witnesses{class_index} = current{class_index};
      endif
    endfor
  endfor
endfunction


function witnesses = find_witnesses_at_n(statistics, n)
  [names, matrices] = pauli_words(n);
  witnesses = cell(32, 1);
  dimension = 2^n;
  if strcmp(statistics, "boson")
    g = kron(-pauli_matrix("Y"), eye(2^(n - 1)));
  elseif strcmp(statistics, "fermion")
    g = kron(pauli_matrix("X"), eye(2^(n - 1)));
  else
    error("Unknown statistics: %s", statistics);
  endif

  for first = 1:numel(names)
    if all(names{first} == "I")
      continue;
    endif
    J1 = matrices{first};
    for second = 1:numel(names)
      if first == second || all(names{second} == "I")
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
  tolerance = 1e-12;
  if norm(left - right, "fro") < tolerance
    sign = 1;
  elseif norm(left + right, "fro") < tolerance
    sign = -1;
  else
    error("Matrices are not related by a sign.");
  endif
endfunction


function sign = commutation_sign(J1, J2)
  tolerance = 1e-12;
  if norm(J1 * J2 - J2 * J1, "fro") < tolerance
    sign = 1;
  elseif norm(J1 * J2 + J2 * J1, "fro") < tolerance
    sign = -1;
  else
    error("Pauli words neither commute nor anticommute.");
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


function verify_collaborator_examples()
  I = pauli_matrix("I");
  X = pauli_matrix("X");
  Y = pauli_matrix("Y");
  Z = pauli_matrix("Z");
  g_boson = kron(-Y, I);

  J1_yinkai = kron(I, X);
  J2_yinkai = -kron(X, I);
  yinkai_signs = classify_pair(g_boson, J1_yinkai, J2_yinkai);
  assert(all(yinkai_signs(:).' == [1, 1, -1, 1, 1]));

  J1_case_II = -kron(Y, Z);
  J2_case_II = kron(X, X);
  case_II_signs = classify_pair(g_boson, J1_case_II, J2_case_II);
  assert(all(case_II_signs(:).' == [1, -1, -1, 1, 1]));
  printf("Collaborator examples reproduce their stated five signs exactly.\n");
endfunction


function write_true_eta_class_table(all_witnesses, table_dir)
  output_file = fullfile(table_dir, "true_eta_contraction_classes.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,tau,s1,q1,s2,q2,r," ...
                "metric_factor,min_qubits,J1_word,J2_word," ...
                "metric_hermiticity_residual,min_abs_metric_eigenvalue\n"]);

  statistics_names = {"boson", "fermion"};
  for statistics_index = 1:2
    statistics = statistics_names{statistics_index};
    if strcmp(statistics, "boson")
      tau = -1;
    else
      tau = 1;
    endif
    witnesses = all_witnesses{statistics_index};
    class_count = 0;
    for class_index = 1:32
      witness = witnesses{class_index};
      signs = witness.signs;
      s1 = signs(1);
      s2 = signs(3);
      q2 = signs(4);
      commutation = signs(5);
      if q2 != -tau || commutation != -s1 * s2
        continue;
      endif
      class_count += 1;
      n = witness.n;
      if strcmp(statistics, "boson")
        g = kron(-pauli_matrix("Y"), eye(2^(n - 1)));
      else
        g = kron(pauli_matrix("X"), eye(2^(n - 1)));
      endif
      if s2 == -1
        eta = -witness.J2 * g;
        metric_factor = "-J2g";
      else
        eta = -1i * witness.J2 * g;
        metric_factor = "-iJ2g";
      endif
      hermiticity_residual = norm(eta - eta', "fro");
      minimum_metric_eigenvalue = min(abs(eig(eta)));
      assert(hermiticity_residual < 1e-12);
      assert(minimum_metric_eigenvalue > 1e-12);
      fprintf(fid, ...
              "%s,%s,%d,%d,%d,%d,%d,%d,%s,%d,%s,%s,%.16g,%.16g\n", ...
              statistics, class_label(signs), tau, signs(1), signs(2), ...
              signs(3), signs(4), signs(5), metric_factor, n, ...
              witness.J1_name, witness.J2_name, ...
              hermiticity_residual, minimum_metric_eigenvalue);
    endfor
    assert(class_count == 8);
    printf("%s: wrote the eight true eta-contraction sign classes ", ...
           statistics);
    printf("(q2=-tau and r=-s1*s2).\n");
  endfor
  fclose(fid);
endfunction


function write_boson_reference_diagnostic(table_dir)
  output_file = fullfile(table_dir, ...
                         "boson_pole_reference_diagnostic.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["point,B,P,rho_P,det_I_minus_P,continued_weight," ...
                "endpoint_pole_free,bare_trace_convergent," ...
                "same_pole_free_component_as_stable_reference\n"]);

  B_values = [-1, 1];
  names = {"stable_reference", "algebraic_other_side"};
  same_components = [1, 0];
  for point = 1:2
    B = B_values(point);
    P = exp(B);
    determinant = 1 - P;
    continued_weight = exp(B / 2) / determinant;
    fprintf(fid, "%s,%.16g,%.16g,%.16g,%.16g,%.16g,%d,%d,%d\n", ...
            names{point}, B, P, abs(P), determinant, ...
            continued_weight, abs(determinant) > 1e-12, ...
            abs(P) < 1, same_components(point));
  endfor
  fclose(fid);

  printf("Boson reference diagnostic: B=-1 has a convergent positive trace; ");
  printf("B=+1 is pole-free only algebraically and has a negative continued ");
  printf("weight. The path crosses the pole at B=0.\n");
endfunction


function output_file = scan_true_eta_maximal_subgroups(table_dir)
  output_file = fullfile(table_dir, "true_eta_maximal_subgroup_scan.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,s1,q1,s2,q2,r,J1_word,J2_word," ...
                "eta_factor,edge_dim,commutator_closure_residual," ...
                "min_real_weight,max_abs_imag_weight,negative_count," ...
                "algebraic_nonsingular_count,unit_disk_spectral_count," ...
                "min_unit_disk_spectral_real_weight," ...
                "negative_unit_disk_spectral_count," ...
                "trials,slices,scale\n"]);

  statistics_names = {"boson", "fermion"};
  trial_count = 300;
  slice_count = 4;
  scale = 0.8;
  for statistics_index = 1:2
    statistics = statistics_names{statistics_index};
    witnesses = find_witnesses_at_n(statistics, 3);
    if strcmp(statistics, "boson")
      tau = -1;
      g = kron(-pauli_matrix("Y"), eye(4));
    else
      tau = 1;
      g = kron(pauli_matrix("X"), eye(4));
    endif
    scanned_count = 0;
    for class_index = 1:32
      witness = witnesses{class_index};
      signs = witness.signs;
      s1 = signs(1);
      s2 = signs(3);
      if signs(4) != -tau || signs(5) != -s1 * s2
        continue;
      endif
      scanned_count += 1;
      if s2 == -1
        eta_phase = 1;
        eta_factor = "-J2g";
      else
        eta_phase = 1i;
        eta_factor = "-iJ2g";
      endif
      eta = -eta_phase * witness.J2 * g;
      assert(norm(eta - eta', "fro") < 1e-12);
      C_edge = eta_edge_constraint_matrix(g, witness.J1, eta);
      V_edge = real_null_basis(C_edge);
      closure_residual = commutator_closure_residual(V_edge, 8);

      rng(20260725 + 1000 * statistics_index + class_index, "twister");
      [minimum_weight, maximum_imaginary_part, negative_count, ...
       nonsingular_count, convergent_count, minimum_convergent_weight, ...
       negative_convergent_count] = ...
          random_metric_weight_scan(V_edge, 8, statistics, ...
                                    trial_count, slice_count, scale);
      fprintf(fid, ...
              "%s,%s,%d,%d,%d,%d,%d,%s,%s,%s,%d,%.16g,%.16g,%.16g,%d,%d,%d,%.16g,%d,%d,%d,%.16g\n", ...
              statistics, class_label(signs), signs(1), signs(2), ...
              signs(3), signs(4), signs(5), witness.J1_name, ...
              witness.J2_name, eta_factor, columns(V_edge), ...
              closure_residual, minimum_weight, maximum_imaginary_part, ...
              negative_count, nonsingular_count, convergent_count, ...
              minimum_convergent_weight, negative_convergent_count, ...
              trial_count, slice_count, scale);
    endfor
    assert(scanned_count == 8);
    printf("%s: scanned all eight corrected eta-maximal-subgroup ", statistics);
    printf("classes after removing pairing.\n");
  endfor
  fclose(fid);
endfunction


function C = eta_edge_constraint_matrix(g, J1, eta)
  dimension = rows(g);
  particle_dimension = dimension / 2;
  variable_count = dimension^2;
  columns_list = cell(2 * variable_count, 1);
  for variable = 1:(2 * variable_count)
    A = zeros(dimension);
    if variable <= variable_count
      A(variable) = 1;
    else
      A(variable - variable_count) = 1i;
    endif
    residuals = {
      g * A + A.' * g,
      J1.' * A * J1 - conj(A),
      eta * A + A' * eta,
      A(1:particle_dimension, (particle_dimension + 1):end),
      A((particle_dimension + 1):end, 1:particle_dimension)
    };
    columns_list{variable} = residual_vector(residuals);
  endfor
  C = cell2mat(columns_list.');
endfunction


function [minimum_weight, maximum_imaginary_part, negative_count, ...
          nonsingular_count, convergent_count, minimum_convergent_weight, ...
          negative_convergent_count] = ...
    random_metric_weight_scan(V_null, dimension, statistics, ...
                              trial_count, slice_count, scale)
  particle_dimension = dimension / 2;
  basis_dimension = columns(V_null);
  minimum_weight = Inf;
  maximum_imaginary_part = 0;
  negative_count = 0;
  nonsingular_count = 0;
  convergent_count = 0;
  minimum_convergent_weight = Inf;
  negative_convergent_count = 0;
  for trial = 1:trial_count
    product = eye(particle_dimension);
    trace_sum = 0;
    for slice = 1:slice_count
      coefficients = scale * randn(basis_dimension, 1);
      A = vector_to_matrix(V_null * coefficients, dimension);
      B = A(1:particle_dimension, 1:particle_dimension);
      product = product * expm(B);
      trace_sum += trace(B);
    endfor
    is_convergent = false;
    if strcmp(statistics, "fermion")
      determinant = det(eye(particle_dimension) + product);
      weight = exp(-trace_sum / 2) * determinant;
      convergent_count += 1;
      is_convergent = true;
    else
      determinant = det(eye(particle_dimension) - product);
      if abs(determinant) > 1e-10
        weight = exp(trace_sum / 2) / determinant;
      else
        weight = NaN;
      endif
      if max(abs(eig(product))) < 1 - 1e-10
        convergent_count += 1;
        is_convergent = true;
      endif
    endif
    if abs(determinant) <= 1e-10
      continue;
    endif
    nonsingular_count += 1;
    minimum_weight = min(minimum_weight, real(weight));
    maximum_imaginary_part = max(maximum_imaginary_part, abs(imag(weight)));
    if real(weight) < -1e-8 && abs(imag(weight)) < 1e-7
      negative_count += 1;
    endif
    if is_convergent
      minimum_convergent_weight = min( ...
          minimum_convergent_weight, real(weight));
      if real(weight) < -1e-8 && abs(imag(weight)) < 1e-7
        negative_convergent_count += 1;
      endif
    endif
  endfor
endfunction


function write_boson_partner_test(table_dir)
  I = pauli_matrix("I");
  X = pauli_matrix("X");
  Y = pauli_matrix("Y");
  Z = pauli_matrix("Z");
  g = -kron(Y, I);
  J1 = kron(I, X);
  J2 = kron(I, Z);
  signs = classify_pair(g, J1, J2);
  assert(all(signs(:).' == [1, 1, 1, 1, -1]));

  eta = -1i * J2 * g;
  A_free = -kron(Z, I);
  A_cone = -eta;
  Q_free = eta * A_free + A_free' * eta;
  Q_cone = eta * A_cone + A_cone' * eta;
  assert(norm(g * A_free + A_free.' * g, "fro") < 1e-12);
  assert(norm(g * A_cone + A_cone.' * g, "fro") < 1e-12);
  assert(norm(J1.' * A_free * J1 - conj(A_free), "fro") < 1e-12);
  assert(norm(J1.' * A_cone * J1 - conj(A_cone), "fro") < 1e-12);
  assert(norm(Q_free, "fro") < 1e-12);
  assert(norm(Q_cone + 2 * eye(4), "fro") < 1e-12);

  output_file = fullfile(table_dir, "boson_s2_plus_partner_test.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["class_id,J1_word,J2_word,t," ...
                "E," ...
                "max_eta_contraction_eigenvalue,min_unit_circle_distance," ...
                "det_I_minus_M,operator_branch_weight_closed_form," ...
                "trace_class_from_reference," ...
                "Q_free_residual,Q_cone_minus_target_residual\n"]);
  t_values = [0, 0.25, 0.5, 1, 2];
  for t = t_values
    M = expm(A_free) * expm(t * A_cone);
    contraction = M' * eta * M - eta;
    contraction = (contraction + contraction') / 2;
    eigenvalues = eig(M);
    determinant = det(eye(4) - M);
    assert(abs(imag(determinant)) < 1e-12 && real(determinant) > 0);
    weight = 1 / sqrt(real(determinant));
    assert(weight > 0);
    fprintf(fid, "%s,IX,IZ,%.16g,1,%.16g,%.16g,%.16g,%.16g,1,%.16g,%.16g\n", ...
            class_label(signs), t, max(real(eig(contraction))), ...
            min(abs(abs(eigenvalues) - 1)), real(determinant), weight, ...
            norm(Q_free, "fro"), norm(Q_cone + 2 * eye(4), "fro"));
  endfor
  fclose(fid);
  printf("Boson s2=+ partner: explicit eta-edge/free and strict-cone ");
  printf("generators remain pole-free with a positive closed-form branch weight.\n");
endfunction


function write_boson_four_partner_test(table_dir)
  I = pauli_matrix("I");
  X = pauli_matrix("X");
  Y = pauli_matrix("Y");
  Z = pauli_matrix("Z");
  g = -kron(kron(Y, I), I);
  J2 = kron(kron(I, Z), I);
  eta = -1i * J2 * g;
  A_free = -kron(kron(Z, I), I);
  A_cone = -eta;
  J1_words = {"IXI", "IYI", "ZII", "ZIY"};
  J1_matrices = {
    kron(kron(I, X), I),
    kron(kron(I, Y), I),
    kron(kron(Z, I), I),
    kron(kron(Z, I), Y)
  };
  expected_signs = {
    [1, 1, 1, 1, -1],
    [1, -1, 1, 1, -1],
    [-1, 1, 1, 1, 1],
    [-1, -1, 1, 1, 1]
  };

  lie_free_residual = norm(g * A_free + A_free.' * g, "fro");
  lie_cone_residual = norm(g * A_cone + A_cone.' * g, "fro");
  Q_free = eta * A_free + A_free' * eta;
  Q_cone = eta * A_cone + A_cone' * eta;
  assert(max([lie_free_residual, lie_cone_residual, ...
              norm(Q_free, "fro"), ...
              norm(Q_cone + 2 * eye(8), "fro")]) < 1e-12);

  M = expm(A_free) * expm(A_cone);
  contraction = M' * eta * M - eta;
  contraction = (contraction + contraction') / 2;
  strict_maximum = max(real(eig(contraction)));
  determinant = real(det(eye(8) - M));
  weight = 1 / sqrt(determinant);
  assert(strict_maximum < -1e-8 && determinant > 0 && weight > 0);

  output_file = fullfile( ...
      table_dir, "boson_s2_plus_four_class_witness_test.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["class_id,s1,q1,s2,q2,r,J1_word,J2_word," ...
                "lie_free_residual,lie_cone_residual," ...
                "J1_free_residual,J1_cone_residual," ...
                "Q_free_residual,Q_cone_minus_target_residual," ...
                "strict_max_eigenvalue," ...
                "operator_branch_weight_closed_form_E1_t1," ...
                "trace_class_from_reference,nambu_dimension\n"]);

  for class_index = 1:numel(J1_matrices)
    J1 = J1_matrices{class_index};
    signs = classify_pair(g, J1, J2);
    assert(all(signs(:).' == expected_signs{class_index}));
    J1_free_residual = norm( ...
        J1.' * A_free * J1 - conj(A_free), "fro");
    J1_cone_residual = norm( ...
        J1.' * A_cone * J1 - conj(A_cone), "fro");
    assert(max([J1_free_residual, J1_cone_residual]) < 1e-12);

    fprintf(fid, ...
            "%s,%d,%d,%d,%d,%d,%s,IZI,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g,1,8\n", ...
            class_label(signs), signs(1), signs(2), signs(3), ...
            signs(4), signs(5), J1_words{class_index}, ...
            lie_free_residual, lie_cone_residual, ...
            J1_free_residual, J1_cone_residual, ...
            norm(Q_free, "fro"), norm(Q_cone + 2 * eye(8), "fro"), ...
            strict_maximum, weight);
  endfor
  fclose(fid);
  printf("Boson s2=+ partner quartet: one common eight-dimensional ");
  printf("trace-class construction satisfies all four J1 realities.\n");
endfunction


function signs = classify_pair(g, J1, J2)
  dimension = rows(g);
  signs = [
    matrix_sign(J1.' * g * J1, g),
    matrix_sign(J1 * J1, eye(dimension)),
    matrix_sign(J2.' * g * J2, g),
    matrix_sign(J2 * J2, eye(dimension)),
    commutation_sign(J1, J2)
  ];
endfunction


function vector = residual_vector(residuals)
  vector = [];
  for residual_index = 1:numel(residuals)
    residual = residuals{residual_index};
    vector = [vector; real(residual(:)); imag(residual(:))];
  endfor
endfunction


function V_null = real_null_basis(C)
  [~, singular_values, V] = svd(C, 0);
  diagonal = diag(singular_values);
  rank_C = sum(diagonal > 1e-10);
  V_null = V(:, (rank_C + 1):end);
endfunction


function A = vector_to_matrix(vector, dimension)
  variable_count = dimension^2;
  A = reshape(vector(1:variable_count) + ...
              1i * vector((variable_count + 1):end), ...
              dimension, dimension);
endfunction


function vector = matrix_to_vector(A)
  vector = [real(A(:)); imag(A(:))];
endfunction


function residual = commutator_closure_residual(V_null, dimension)
  basis_dimension = columns(V_null);
  if basis_dimension == 0
    residual = 0;
    return;
  endif
  residual = 0;
  for first = 1:basis_dimension
    A = vector_to_matrix(V_null(:, first), dimension);
    for second = 1:basis_dimension
      B = vector_to_matrix(V_null(:, second), dimension);
      commutator = A * B - B * A;
      vector = matrix_to_vector(commutator);
      outside = vector - V_null * (V_null.' * vector);
      residual = max(residual, norm(outside));
    endfor
  endfor
endfunction
