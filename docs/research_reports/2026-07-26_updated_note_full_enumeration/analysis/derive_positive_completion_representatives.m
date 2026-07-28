function derive_positive_completion_representatives()
  more off;
  format long g;

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  output_file = fullfile(table_dir, ...
      "positive_completion_representatives.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,n,J1_word,J2_word,metric," ...
                "s1,q1,s2,q2,r,free_generator,hs_generator," ...
                "kramers_generator,relation_residual,slice_residual," ...
                "kramers_residual,sample_propagator_norm," ...
                "sample_weight,sample_propagator_kramers_residual\n"]);

  statistics_names = {"boson", "fermion"};
  row_count = 0;
  for statistics_index = 1:numel(statistics_names)
    statistics = statistics_names{statistics_index};
    representatives = find_representatives(statistics);
    assert(all(!cellfun(@isempty, representatives)));

    for class_index = 1:32
      representative = representatives{class_index};
      n = representative.n;
      signs = representative.signs;
      g = canonical_g(statistics, n);
      J1 = representative.J1;
      J2 = representative.J2;
      [eta, metric_name] = canonical_metric( ...
          statistics, g, J2, signs(3), signs(4));
      free_generator = -kron(pauli_matrix("Z"), eye(2^(n - 1)));
      hs_hermitian_part = kron( ...
          kron(pauli_matrix("Z"), pauli_matrix("Z")), ...
          eye(2^(n - 2)));
      hs_generator = 1i * hs_hermitian_part;
      kramers_generator = kron( ...
          kron(pauli_matrix("I"), pauli_matrix("Y")), ...
          eye(2^(n - 2)));

      relation_residual = max([
        norm(J1.' * J1 - eye(2^n), "fro"),
        norm(J2.' * J2 - eye(2^n), "fro"),
        norm(J1.' * g * J1 - signs(1) * g, "fro"),
        norm(J1 * J1 - signs(2) * eye(2^n), "fro"),
        norm(J2.' * g * J2 - signs(3) * g, "fro"),
        norm(J2 * J2 - signs(4) * eye(2^n), "fro"),
        norm(J1 * J2 - signs(5) * J2 * J1, "fro")
      ]);
      slice_residual = max([
        norm(g * free_generator + free_generator.' * g, "fro"),
        norm(g * hs_generator + hs_generator.' * g, "fro"),
        norm(J1.' * free_generator * J1 - conj(free_generator), "fro"),
        norm(J1.' * hs_generator * J1 - conj(hs_generator), "fro"),
        norm(J2.' * free_generator * J2 - conj(free_generator), "fro"),
        norm(J2.' * hs_generator * J2 - conj(hs_generator), "fro"),
        norm(eta * free_generator + free_generator' * eta, "fro"),
        norm(eta * hs_generator + hs_generator' * eta, "fro")
      ]);
      kramers_residual = max([
        norm(kramers_generator.' * kramers_generator - ...
             eye(2^n), "fro"),
        norm(kramers_generator * kramers_generator + eye(2^n), "fro"),
        norm(kramers_generator.' * free_generator * ...
             kramers_generator - conj(free_generator), "fro"),
        norm(kramers_generator.' * hs_generator * ...
             kramers_generator - conj(hs_generator), "fro")
      ]);
      assert(max([relation_residual, slice_residual, ...
                  kramers_residual]) < 1e-11);
      [sample_norm, sample_weight, sample_kramers_residual] = ...
          sample_propagator(statistics, n);
      assert(sample_norm < 1);
      assert(sample_weight > 0);
      assert(sample_kramers_residual < 1e-11);

      fprintf(fid, ...
              ["%s,%s,%d,%s,%s,%s,%d,%d,%d,%d,%d,%s,%s,%s," ...
               "%.16g,%.16g,%.16g,%.16g,%.16g,%.16g\n"], ...
              statistics, class_label(signs), n, ...
              representative.J1_word, representative.J2_word, ...
              metric_name, signs, ...
              matrix_label(free_generator, n), ...
              matrix_label(hs_generator, n), ...
              matrix_label(kramers_generator, n), ...
              relation_residual, slice_residual, kramers_residual, ...
              sample_norm, sample_weight, sample_kramers_residual);
      row_count += 1;
    endfor
  endfor
  fclose(fid);

  assert(row_count == 64);
  printf("Octave version: %s\n", version());
  printf(["Verified Kramers/reflection-positive intersections for " ...
          "%d classes.\n"], row_count);
  printf("Wrote %s\n", output_file);
endfunction


function [propagator_norm, weight, kramers_residual] = ...
    sample_propagator(statistics, n)
  orbital_count = 2^(n - 2);
  site_count = 2;
  delta_tau = 0.2;
  field_coupling = 0.37;
  hopping = [1.4, 0.25; 0.25, 1.1];
  fields = [-0.8, 0.3; 0.5, -0.4; 0.2, 0.7];

  internal_identity = eye(2 * orbital_count);
  free_factor = expm(-delta_tau * kron(internal_identity, hopping));
  propagator = eye(2 * orbital_count * site_count);
  for slice = 1:rows(fields)
    field_matrix = kron( ...
        kron(pauli_matrix("Z"), eye(orbital_count)), ...
        diag(fields(slice, :)));
    field_factor = expm(1i * field_coupling * field_matrix);
    propagator = free_factor * field_factor * propagator;
  endfor

  kramers = kron( ...
      kron(pauli_matrix("Y"), eye(orbital_count)), eye(site_count));
  kramers_residual = norm( ...
      kramers.' * propagator * kramers - conj(propagator), "fro");
  propagator_norm = norm(propagator, 2);
  if strcmp(statistics, "boson")
    complex_weight = 1 / det(eye(rows(propagator)) - propagator);
  else
    complex_weight = det(eye(rows(propagator)) + propagator);
  endif
  assert(abs(imag(complex_weight)) < 1e-11);
  weight = real(complex_weight);
endfunction


function representatives = find_representatives(statistics)
  representatives = cell(32, 1);
  for n = 2:3
    [names, matrices] = pauli_words(n);
    g = canonical_g(statistics, n);
    free_generator = -kron(pauli_matrix("Z"), eye(2^(n - 1)));
    hs_hermitian_part = kron( ...
        kron(pauli_matrix("Z"), pauli_matrix("Z")), ...
        eye(2^(n - 2)));

    candidate_indices = [];
    candidate_signs = {};
    for index = 1:numel(names)
      J = matrices{index};
      if norm(J.' * free_generator * J - free_generator, "fro") > 1e-11
        continue;
      endif
      if norm(J.' * hs_hermitian_part * J + ...
              hs_hermitian_part, "fro") > 1e-11
        continue;
      endif
      s = matrix_sign(J.' * g * J, g);
      q = matrix_sign(J * J, eye(2^n));
      candidate_indices(end + 1) = index;
      candidate_signs{end + 1} = [s, q];
    endfor

    for first_position = 1:numel(candidate_indices)
      first_index = candidate_indices(first_position);
      J1 = matrices{first_index};
      first_signs = candidate_signs{first_position};
      for second_position = 1:numel(candidate_indices)
      second_index = candidate_indices(second_position);
      J2 = matrices{second_index};
      second_signs = candidate_signs{second_position};
      if norm(J1 - J2, "fro") < 1e-11 || ...
          norm(J1 + J2, "fro") < 1e-11
        continue;
      endif
      r = commutation_sign(J1, J2);
        signs = [first_signs, second_signs, r];
        class_index = signs_to_index(signs);
        if !isempty(representatives{class_index})
          continue;
        endif

        representative.n = n;
        representative.signs = signs;
        representative.J1_word = names{first_index};
        representative.J2_word = names{second_index};
        representative.J1 = J1;
        representative.J2 = J2;
        representatives{class_index} = representative;
      endfor
    endfor
  endfor
endfunction


function [eta, metric_name] = canonical_metric( ...
    statistics, g, J2, s2, q2)
  if strcmp(statistics, "boson")
    transpose_sign = -1;
  else
    transpose_sign = 1;
  endif
  if transpose_sign * q2 * s2 == 1
    eta = J2 * g;
    metric_name = "J2g";
  else
    eta = 1i * J2 * g;
    metric_name = "iJ2g";
  endif
  assert(norm(eta - eta', "fro") < 1e-11);
  assert(norm(eta * eta - eye(rows(eta)), "fro") < 1e-11);
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


function label = matrix_label(matrix, n)
  [names, matrices] = pauli_words(n);
  for index = 1:numel(names)
    if norm(matrix - matrices{index}, "fro") < 1e-11
      label = names{index};
      return;
    endif
    if norm(matrix + matrices{index}, "fro") < 1e-11
      label = ["-", names{index}];
      return;
    endif
    if norm(matrix - 1i * matrices{index}, "fro") < 1e-11
      label = ["i", names{index}];
      return;
    endif
    if norm(matrix + 1i * matrices{index}, "fro") < 1e-11
      label = ["-i", names{index}];
      return;
    endif
  endfor
  error("Matrix is not a signed Pauli word.");
endfunction
