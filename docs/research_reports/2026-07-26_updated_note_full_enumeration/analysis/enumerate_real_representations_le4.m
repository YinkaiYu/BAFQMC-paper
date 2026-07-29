function enumerate_real_representations_le4()
  % Enumerate every real orthogonal representation of the signed relations
  % in matrix dimensions two and four.  The generators form a finite real
  % *-algebra.  Its irreducible modules have signed-permutation models, and
  % every orthogonal module is an orthogonal direct sum of those models.
  % Enumerating signed-permutation triples therefore includes both the
  % irreducible Pauli realizations and all reducible low-dimensional ones.
  %
  % J and -J impose the same anti-linear constraint, so each generator is
  % canonicalized up to its global sign.  We retain J1=J2 as a separately
  % flagged representation: it supplies only one independent anti-linear
  % symmetry, but its larger A space is part of the five-relation problem.
  % Character-equivalent triples are merged only after an explicit
  % g-preserving orthogonal intertwiner is found.
  more off;
  format long g;
  rng(20260730, "twister");

  here = fileparts(mfilename("fullpath"));
  output_file = fullfile(here, "..", "tables", ...
                         "real_representation_orbits_le4.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, [ ...
    "statistics,class_id,matrix_dimension,orbit_id,orbit_size," ...
    "representative_J1,representative_J2,all_pairs,metric," ...
    "eta_phase,eta_matrix,strict_interior,character_key," ...
    "distinct_J1_J2,physical_adjoint_compatible," ...
    "group_literal_dimension,cone_literal_dimension," ...
    "group_terms,cone_terms,intertwiner_worst_residual\n"]);

  statistics_names = {"boson", "fermion"};
  expected_orbit_counts = [10, 50; 16, 73];
  total_rows = 0;

  for statistics_index = 1:numel(statistics_names)
    statistics = statistics_names{statistics_index};
    for n = 1:2
      dimension = 2^n;
      pairs = enumerate_pairs(statistics, dimension);
      orbit_count = 0;

      for class_index = 1:32
        class_pair_indices = find([pairs.class_index] == class_index);
        if isempty(class_pair_indices)
          continue;
        endif

        orbit_keys = {};
        orbit_members = {};
        for pair_index = class_pair_indices
          key = pairs(pair_index).character_key;
          orbit_index = find(strcmp(orbit_keys, key), 1);
          if isempty(orbit_index)
            orbit_keys{end + 1} = key;
            orbit_members{end + 1} = pair_index;
          else
            orbit_members{orbit_index}(end + 1) = pair_index;
          endif
        endfor

        for local_orbit = 1:numel(orbit_keys)
          orbit_count += 1;
          total_rows += 1;
          member_indices = orbit_members{local_orbit};
          g = canonical_g(statistics, dimension);
          representative_index = member_indices(1);
          for candidate_index = member_indices
            candidate = pairs(candidate_index);
            if physical_adjoint_pair( ...
                statistics, dimension, candidate.J1, candidate.J2, ...
                candidate.signs)
              representative_index = candidate_index;
              break;
            endif
          endfor
          representative = pairs(representative_index);
          [eta, eta_phase, eta_matrix, metric_name] = canonical_metric( ...
              statistics, g, representative.J2, representative.signs);

          group_terms = tensor_term_bases( ...
              g, representative.J1, representative.J2, 1);
          cone_terms = tensor_term_bases( ...
              g, representative.J1, representative.J2, -1);
          group_literal_dimension = literal_dimension(group_terms);
          cone_literal_dimension = literal_dimension(cone_terms);

          pair_names = cell(1, numel(member_indices));
          worst_residual = 0;
          for member_position = 1:numel(member_indices)
            member = pairs(member_indices(member_position));
            pair_names{member_position} = ...
                [member.J1_name, "/", member.J2_name];
            residual = intertwiner_residual( ...
                g, representative.J1, representative.J2, ...
                member.J1, member.J2);
            assert(residual < 1e-9);
            worst_residual = max(worst_residual, residual);
          endfor

          strict = strict_interior(statistics, representative.signs);
          distinct_J1_J2 = ...
              norm(representative.J1 - representative.J2, "fro") > 1e-11;
          physical_adjoint_compatible = physical_adjoint_pair( ...
              statistics, dimension, representative.J1, representative.J2, ...
              representative.signs);
          fprintf(fid, [ ...
              "%s,%s,%d,O%02d,%d,%s,%s,%s,%s,%s,%s,%d,%s," ...
              "%d,%d,%d,%d,%s,%s,%.16g\n"], ...
              statistics, class_label(representative.signs), dimension, ...
              local_orbit, numel(member_indices), ...
              csv_quote(representative.J1_name), ...
              csv_quote(representative.J2_name), ...
              csv_quote(strjoin(pair_names, ";")), ...
              metric_name, eta_phase, ...
              csv_quote(serialize_matrix(eta_matrix)), strict, ...
              csv_quote(representative.character_key), ...
              distinct_J1_J2, physical_adjoint_compatible, ...
              group_literal_dimension, cone_literal_dimension, ...
              csv_quote(serialize_terms(group_terms)), ...
              csv_quote(serialize_terms(cone_terms)), ...
              worst_residual);
        endfor
      endfor

      assert(orbit_count == expected_orbit_counts(statistics_index, n));
      printf(["%s, dimension %d: %d ordered signed-" ...
              "permutation pairs in %d representation orbits.\n"], ...
             statistics, dimension, numel(pairs), orbit_count);
    endfor
  endfor
  fclose(fid);

  assert(total_rows == sum(expected_orbit_counts(:)));
  printf("Octave version: %s\n", version());
  printf("Wrote %d complete low-dimensional representation rows to %s\n", ...
         total_rows, output_file);

  physical_output_file = fullfile( ...
      here, "..", "tables", ...
      "bosonic_physical_representation_suborbits_le4.csv");
  physical_rows = enumerate_bosonic_physical_suborbits( ...
      physical_output_file);
  printf("Wrote %d bosonic physical-suborbit rows to %s\n", ...
         physical_rows, physical_output_file);
endfunction


function total_rows = enumerate_bosonic_physical_suborbits(output_file)
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, [ ...
    "statistics,class_id,matrix_dimension,physical_orbit_id," ...
    "orbit_size,representative_J1,representative_J2,all_pairs," ...
    "metric,eta_phase,eta_matrix,strict_interior,distinct_J1_J2," ...
    "algebra_character_key,physical_character_key," ...
    "group_literal_dimension,cone_literal_dimension," ...
    "group_terms,cone_terms,physical_intertwiner_worst_residual\n"]);

  expected_orbit_counts = [4, 40];
  total_rows = 0;

  for n = 1:2
    dimension = 2^n;
    g = canonical_g("boson", dimension);
    conjugation = kron(pauli_matrix("X"), eye(dimension / 2));
    pairs = enumerate_pairs("boson", dimension);

    physical_pair_indices = [];
    for pair_index = 1:numel(pairs)
      pair = pairs(pair_index);
      if physical_adjoint_pair( ...
          "boson", dimension, pair.J1, pair.J2, pair.signs)
        pairs(pair_index).physical_character_key = ...
            canonical_physical_character_key( ...
                g, conjugation, pair.J1, pair.J2);
        physical_pair_indices(end + 1) = pair_index;
      endif
    endfor

    orbit_count = 0;
    for class_index = 1:32
      class_pair_indices = physical_pair_indices( ...
          [pairs(physical_pair_indices).class_index] == class_index);
      if isempty(class_pair_indices)
        continue;
      endif

      orbit_keys = {};
      orbit_members = {};
      for pair_index = class_pair_indices
        key = pairs(pair_index).physical_character_key;
        orbit_index = find(strcmp(orbit_keys, key), 1);
        if isempty(orbit_index)
          orbit_keys{end + 1} = key;
          orbit_members{end + 1} = pair_index;
        else
          orbit_members{orbit_index}(end + 1) = pair_index;
        endif
      endfor

      for local_orbit = 1:numel(orbit_keys)
        orbit_count += 1;
        total_rows += 1;
        member_indices = orbit_members{local_orbit};
        representative = pairs(member_indices(1));
        [eta, eta_phase, eta_matrix, metric_name] = canonical_metric( ...
            "boson", g, representative.J2, representative.signs);

        group_terms = tensor_term_bases( ...
            g, representative.J1, representative.J2, 1);
        cone_terms = tensor_term_bases( ...
            g, representative.J1, representative.J2, -1);
        group_literal_dimension = literal_dimension(group_terms);
        cone_literal_dimension = literal_dimension(cone_terms);

        pair_names = cell(1, numel(member_indices));
        worst_residual = 0;
        for member_position = 1:numel(member_indices)
          member = pairs(member_indices(member_position));
          pair_names{member_position} = ...
              [member.J1_name, "/", member.J2_name];
          residual = physical_intertwiner_residual( ...
              g, conjugation, ...
              representative.J1, representative.J2, ...
              member.J1, member.J2);
          assert(residual < 1e-9);
          worst_residual = max(worst_residual, residual);
        endfor

        strict = strict_interior("boson", representative.signs);
        distinct_J1_J2 = ...
            norm(representative.J1 - representative.J2, "fro") > 1e-11;
        fprintf(fid, [ ...
            "boson,%s,%d,P%02d,%d,%s,%s,%s,%s,%s,%s,%d,%d," ...
            "%s,%s,%d,%d,%s,%s,%.16g\n"], ...
            class_label(representative.signs), dimension, ...
            local_orbit, numel(member_indices), ...
            csv_quote(representative.J1_name), ...
            csv_quote(representative.J2_name), ...
            csv_quote(strjoin(pair_names, ";")), ...
            metric_name, eta_phase, ...
            csv_quote(serialize_matrix(eta_matrix)), strict, ...
            distinct_J1_J2, ...
            csv_quote(representative.character_key), ...
            csv_quote(representative.physical_character_key), ...
            group_literal_dimension, cone_literal_dimension, ...
            csv_quote(serialize_terms(group_terms)), ...
            csv_quote(serialize_terms(cone_terms)), ...
            worst_residual);
      endfor
    endfor

    assert(orbit_count == expected_orbit_counts(n));
    printf(["boson physical, dimension %d: %d ordered signed-" ...
            "permutation pairs in %d physical suborbits.\n"], ...
           dimension, numel(physical_pair_indices), orbit_count);
  endfor

  fclose(fid);
  assert(total_rows == sum(expected_orbit_counts));
endfunction


function compatible = physical_adjoint_pair( ...
    statistics, dimension, J1, J2, signs)
  if strcmp(statistics, "fermion")
    compatible = true;
    return;
  endif
  conjugation = kron(pauli_matrix("X"), eye(dimension / 2));
  compatible = ...
      norm(conjugation * J1 * conjugation - signs(1) * J1, "fro") ...
        < 1e-11 && ...
      norm(conjugation * J2 * conjugation - signs(3) * J2, "fro") ...
        < 1e-11;
endfunction


function key = canonical_physical_character_key( ...
    g, conjugation, J1, J2)
  candidates = zeros(4, 16);
  sign_choices = [1, 1; 1, -1; -1, 1; -1, -1];
  for choice = 1:rows(sign_choices)
    epsilon1 = sign_choices(choice, 1);
    epsilon2 = sign_choices(choice, 2);
    entry = 0;
    for conjugation_power = 0:1
      for g_power = 0:1
        for first_power = 0:1
          for second_power = 0:1
            entry += 1;
            matrix = eye(rows(g));
            if conjugation_power == 1
              matrix *= conjugation;
            endif
            if g_power == 1
              matrix *= g;
            endif
            if first_power == 1
              matrix *= epsilon1 * J1;
            endif
            if second_power == 1
              matrix *= epsilon2 * J2;
            endif
            candidates(choice, entry) = round(real(trace(matrix)));
          endfor
        endfor
      endfor
    endfor
  endfor
  candidates = sortrows(candidates);
  key_rows = cell(1, rows(candidates));
  for row_index = 1:rows(candidates)
    key_rows{row_index} = sprintf("%d:", candidates(row_index, :));
  endfor
  key = strjoin(key_rows, "|");
endfunction


function pairs = enumerate_pairs(statistics, dimension)
  [candidate_names, candidates] = signed_permutation_generators( ...
      statistics, dimension);
  g = canonical_g(statistics, dimension);
  pair_capacity = numel(candidates)^2;
  pairs = repmat(struct(), pair_capacity, 1);
  next_pair = 0;

  for first = 1:numel(candidates)
    for second = 1:numel(candidates)
      J1 = candidates{first};
      J2 = candidates{second};
      relation = commutation_sign_or_zero(J1, J2);
      if relation == 0
        continue;
      endif
      next_pair += 1;
      signs = [
        matrix_sign(J1.' * g * J1, g),
        matrix_sign(J1 * J1, eye(dimension)),
        matrix_sign(J2.' * g * J2, g),
        matrix_sign(J2 * J2, eye(dimension)),
        relation
      ];
      pairs(next_pair).J1_name = candidate_names{first};
      pairs(next_pair).J2_name = candidate_names{second};
      pairs(next_pair).J1 = J1;
      pairs(next_pair).J2 = J2;
      pairs(next_pair).signs = signs;
      pairs(next_pair).class_index = signs_to_index(signs);
      pairs(next_pair).character_key = ...
          canonical_character_key(g, J1, J2);
    endfor
  endfor
  pairs = pairs(1:next_pair);
endfunction


function [names, matrices] = signed_permutation_generators( ...
    statistics, dimension)
  permutations = perms(1:dimension);
  sign_rows = dec2bin(0:(2^dimension - 1), dimension) - "0";
  g = canonical_g(statistics, dimension);
  names = {};
  matrices = {};

  for permutation_index = 1:rows(permutations)
    permutation = permutations(permutation_index, :);
    for sign_index = 1:rows(sign_rows)
      signs = 1 - 2 * sign_rows(sign_index, :);
      matrix = zeros(dimension);
      for column = 1:dimension
        matrix(permutation(column), column) = signs(column);
      endfor
      nonzero_entries = matrix(find(matrix, 1));
      if nonzero_entries(1) < 0
        continue;
      endif
      if !is_signed_identity(matrix * matrix)
        continue;
      endif
      if !is_signed_copy(matrix.' * g * matrix, g)
        continue;
      endif
      names{end + 1} = signed_permutation_label(matrix);
      matrices{end + 1} = matrix;
    endfor
  endfor
endfunction


function label = signed_permutation_label(matrix)
  dimension = rows(matrix);
  entries = cell(1, dimension);
  for column = 1:dimension
    row = find(matrix(:, column), 1);
    value = matrix(row, column) * row;
    entries{column} = sprintf("%+d", value);
  endfor
  label = ["[", strjoin(entries, " "), "]"];
endfunction


function result = is_signed_identity(matrix)
  identity = eye(rows(matrix));
  result = norm(matrix - identity, "fro") < 1e-11 || ...
           norm(matrix + identity, "fro") < 1e-11;
endfunction


function result = is_signed_copy(left, right)
  result = norm(left - right, "fro") < 1e-11 || ...
           norm(left + right, "fro") < 1e-11;
endfunction


function key = canonical_character_key(g, J1, J2)
  candidates = zeros(4, 8);
  sign_choices = [1, 1; 1, -1; -1, 1; -1, -1];
  for choice = 1:rows(sign_choices)
    epsilon1 = sign_choices(choice, 1);
    epsilon2 = sign_choices(choice, 2);
    entry = 0;
    for g_power = 0:1
      for first_power = 0:1
        for second_power = 0:1
          entry += 1;
          matrix = eye(rows(g));
          if g_power == 1
            matrix *= g;
          endif
          if first_power == 1
            matrix *= epsilon1 * J1;
          endif
          if second_power == 1
            matrix *= epsilon2 * J2;
          endif
          candidates(choice, entry) = round(real(trace(matrix)));
        endfor
      endfor
    endfor
  endfor
  candidates = sortrows(candidates);
  key_rows = cell(1, rows(candidates));
  for row_index = 1:rows(candidates)
    key_rows{row_index} = sprintf("%d:", candidates(row_index, :));
  endfor
  key = strjoin(key_rows, "|");
endfunction


function residual = intertwiner_residual( ...
    g, representative_J1, representative_J2, target_J1, target_J2)
  dimension = rows(g);
  identity = eye(dimension);
  best_residual = Inf;

  for epsilon1 = [1, -1]
    for epsilon2 = [1, -1]
      linear_map = [
        kron(identity, g) - kron(g.', identity);
        kron(identity, target_J1) ...
          - epsilon1 * kron(representative_J1.', identity);
        kron(identity, target_J2) ...
          - epsilon2 * kron(representative_J2.', identity)
      ];
      intertwiner_basis = null(linear_map, 1e-11);
      basis_dimension = columns(intertwiner_basis);
      if basis_dimension == 0
        continue;
      endif

      coefficient_trials = [
        eye(basis_dimension);
        randn(256, basis_dimension)
      ];
      for trial = 1:rows(coefficient_trials)
        X = reshape( ...
            intertwiner_basis * coefficient_trials(trial, :).', ...
            dimension, dimension);
        if min(svd(X)) < 1e-9
          continue;
        endif
        [left, ~, right] = svd(X);
        U = left * right.';
        current_residual = max([
          norm(U.' * U - identity, "fro"),
          norm(U.' * g * U - g, "fro"),
          norm(target_J1 * U ...
               - epsilon1 * U * representative_J1, "fro"),
          norm(target_J2 * U ...
               - epsilon2 * U * representative_J2, "fro")
        ]);
        best_residual = min(best_residual, current_residual);
      endfor
    endfor
  endfor

  if !isfinite(best_residual)
    error("Character-equivalent triples have no invertible intertwiner.");
  endif
  residual = best_residual;
endfunction


function residual = physical_intertwiner_residual( ...
    g, conjugation, representative_J1, representative_J2, ...
    target_J1, target_J2)
  dimension = rows(g);
  identity = eye(dimension);
  best_residual = Inf;

  for epsilon1 = [1, -1]
    for epsilon2 = [1, -1]
      linear_map = [
        kron(identity, g) - kron(g.', identity);
        kron(identity, conjugation) ...
          - kron(conjugation.', identity);
        kron(identity, target_J1) ...
          - epsilon1 * kron(representative_J1.', identity);
        kron(identity, target_J2) ...
          - epsilon2 * kron(representative_J2.', identity)
      ];
      intertwiner_basis = null(linear_map, 1e-11);
      basis_dimension = columns(intertwiner_basis);
      if basis_dimension == 0
        continue;
      endif

      coefficient_trials = [
        eye(basis_dimension);
        randn(256, basis_dimension)
      ];
      for trial = 1:rows(coefficient_trials)
        X = reshape( ...
            intertwiner_basis * coefficient_trials(trial, :).', ...
            dimension, dimension);
        if min(svd(X)) < 1e-9
          continue;
        endif
        [left, ~, right] = svd(X);
        U = left * right.';
        current_residual = max([
          norm(U.' * U - identity, "fro"),
          norm(U.' * g * U - g, "fro"),
          norm(U.' * conjugation * U - conjugation, "fro"),
          norm(target_J1 * U ...
               - epsilon1 * U * representative_J1, "fro"),
          norm(target_J2 * U ...
               - epsilon2 * U * representative_J2, "fro")
        ]);
        best_residual = min(best_residual, current_residual);
      endfor
    endfor
  endfor

  if !isfinite(best_residual)
    error(["Character-equivalent physical triples have no " ...
           "adjoint-preserving intertwiner."]);
  endif
  residual = best_residual;
endfunction


function terms = tensor_term_bases(g, J1, J2, second_target)
  dimension = rows(g);
  coefficient_types = {
    "R_S", 1, 1;
    "R_A", -1, 1;
    "iR_S", 1, -1;
    "iR_A", -1, -1
  };
  terms = struct("coefficient_type", {}, "matrix", {});

  for type_index = 1:rows(coefficient_types)
    coefficient_type = coefficient_types{type_index, 1};
    transpose_sign = coefficient_types{type_index, 2};
    conjugation_sign = coefficient_types{type_index, 3};
    constraints = [
      linear_constraint(dimension, ...
        @(P) g * P + transpose_sign * P.' * g);
      linear_constraint(dimension, ...
        @(P) J1.' * P * J1 - conjugation_sign * P);
      linear_constraint(dimension, ...
        @(P) J2.' * P * J2 ...
          - second_target * conjugation_sign * P)
    ];
    basis = integer_null_basis(constraints);
    for basis_index = 1:columns(basis)
      terms(end + 1).coefficient_type = coefficient_type;
      terms(end).matrix = reshape( ...
          basis(:, basis_index), dimension, dimension);
    endfor
  endfor
endfunction


function operator = linear_constraint(dimension, transform)
  operator = zeros(dimension^2);
  for column = 1:(dimension^2)
    basis_matrix = zeros(dimension);
    basis_matrix(column) = 1;
    transformed = transform(basis_matrix);
    operator(:, column) = transformed(:);
  endfor
endfunction


function basis = integer_null_basis(matrix)
  tolerance = 1e-11;
  [reduced, pivots] = rref(matrix, tolerance);
  column_count = columns(matrix);
  free_columns = setdiff(1:column_count, pivots);
  basis = zeros(column_count, numel(free_columns));

  for free_index = 1:numel(free_columns)
    free_column = free_columns(free_index);
    vector = zeros(column_count, 1);
    vector(free_column) = 1;
    for pivot_index = 1:numel(pivots)
      vector(pivots(pivot_index)) = ...
          -reduced(pivot_index, free_column);
    endfor
    basis(:, free_index) = primitive_integer_vector(vector);
  endfor
endfunction


function integer_vector = primitive_integer_vector(vector)
  vector(abs(vector) < 1e-10) = 0;
  [numerators, denominators] = rat(vector, 1e-10);
  common_denominator = 1;
  for index = 1:numel(denominators)
    if numerators(index) != 0
      common_denominator = lcm( ...
          common_denominator, abs(denominators(index)));
    endif
  endfor
  integer_vector = round( ...
      numerators .* (common_denominator ./ denominators));
  divisor = 0;
  for value = integer_vector(:).'
    divisor = gcd(divisor, abs(value));
  endfor
  if divisor > 1
    integer_vector /= divisor;
  endif
  first_nonzero = find(integer_vector, 1);
  if !isempty(first_nonzero) && integer_vector(first_nonzero) < 0
    integer_vector *= -1;
  endif
endfunction


function dimension = literal_dimension(terms)
  dimension = 0;
  for term_index = 1:numel(terms)
    coefficient_type = terms(term_index).coefficient_type;
    if strcmp(coefficient_type, "R_S") || ...
       strcmp(coefficient_type, "iR_S")
      dimension += 1;
    endif
  endfor
endfunction


function serialized = serialize_terms(terms)
  entries = cell(1, numel(terms));
  for term_index = 1:numel(terms)
    entries{term_index} = [
      terms(term_index).coefficient_type, "@", ...
      serialize_matrix(terms(term_index).matrix)
    ];
  endfor
  serialized = strjoin(entries, ";");
endfunction


function serialized = serialize_matrix(matrix)
  row_strings = cell(1, rows(matrix));
  for row_index = 1:rows(matrix)
    entries = arrayfun( ...
        @(value) sprintf("%d", round(value)), ...
        matrix(row_index, :), "UniformOutput", false);
    row_strings{row_index} = strjoin(entries, " ");
  endfor
  serialized = strjoin(row_strings, "|");
endfunction


function [eta, phase_label, base_matrix, metric_name] = canonical_metric( ...
    statistics, g, J2, signs)
  if strcmp(statistics, "boson")
    transpose_sign = -1;
  else
    transpose_sign = 1;
  endif
  if transpose_sign * signs(4) * signs(3) == 1
    eta = J2 * g;
    phase_label = "1";
    base_matrix = J2 * g;
    metric_name = "J2g";
  else
    eta = 1i * J2 * g;
    phase_label = "i";
    base_matrix = J2 * g;
    metric_name = "iJ2g";
  endif
  assert(norm(eta - eta', "fro") < 1e-11);
  assert(norm(eta * eta - eye(rows(eta)), "fro") < 1e-11);
endfunction


function strict = strict_interior(statistics, signs)
  if strcmp(statistics, "boson")
    transpose_sign = -1;
  else
    transpose_sign = 1;
  endif
  strict = signs(4) == -transpose_sign && ...
           signs(5) == -signs(1) * signs(3);
endfunction


function g = canonical_g(statistics, dimension)
  if strcmp(statistics, "boson")
    g = kron(-pauli_matrix("Y"), eye(dimension / 2));
  else
    g = kron(pauli_matrix("X"), eye(dimension / 2));
  endif
endfunction


function matrix = pauli_matrix(label)
  switch label
    case "X"
      matrix = [0, 1; 1, 0];
    case "Y"
      matrix = [0, 1; -1, 0];
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
    error("Matrices are not equal up to sign.");
  endif
endfunction


function sign_value = commutation_sign_or_zero(first, second)
  if norm(first * second - second * first, "fro") < 1e-11
    sign_value = 1;
  elseif norm(first * second + second * first, "fro") < 1e-11
    sign_value = -1;
  else
    sign_value = 0;
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


function character = sign_character(sign_value)
  if sign_value == 1
    character = "+";
  else
    character = "-";
  endif
endfunction


function quoted = csv_quote(value)
  quoted = ['"', strrep(value, '"', '""'), '"'];
endfunction
