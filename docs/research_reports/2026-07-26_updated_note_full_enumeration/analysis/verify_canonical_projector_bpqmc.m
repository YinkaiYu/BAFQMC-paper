function verify_canonical_projector_bpqmc()
  more off;
  format long g;
  rng(20260802, "twister");

  here = fileparts(mfilename("fullpath"));
  output_file = fullfile(here, "..", "tables", ...
                         "canonical_projector_bpqmc_checks.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["trial,orbitals,particle_number,overlap_relative_error," ...
                "local_ratio_relative_error,one_body_relative_error," ...
                "conjugate_pair_imaginary_residual\n"]);

  trial_count = 10;
  worst_overlap_error = 0;
  worst_ratio_error = 0;
  worst_one_body_error = 0;
  worst_pair_residual = 0;

  for trial = 1:trial_count
    orbitals = 3;
    particle_number = 4;
    p = randn(orbitals, 1) + 1i * randn(orbitals, 1);
    p /= norm(p);

    left_generator = 0.10 * (randn(orbitals) + 1i * randn(orbitals));
    right_generator = 0.10 * (randn(orbitals) + 1i * randn(orbitals));
    B_left = expm(left_generator);
    B_right = expm(right_generator);
    B = B_left * B_right;

    [fock_B, occupations] = symmetric_power_operator(B, particle_number);
    trial_state = rank_one_state(p, occupations, particle_number);
    explicit_overlap = trial_state' * fock_B * trial_state;
    single_particle_overlap = p' * B * p;
    formula_overlap = single_particle_overlap^particle_number;
    overlap_error = relative_error(explicit_overlap, formula_overlap);

    update_left = 0.035 * (randn(orbitals, 1) + ...
                           1i * randn(orbitals, 1));
    update_right = randn(orbitals, 1) + 1i * randn(orbitals, 1);
    B_updated = B_left * ...
                (eye(orbitals) + update_left * update_right') * B_right;
    fock_B_updated = symmetric_power_operator(B_updated, particle_number);
    explicit_updated = trial_state' * fock_B_updated * trial_state;

    p_left = p' * B_left;
    p_right = B_right * p;
    updated_single_overlap = single_particle_overlap + ...
        (p_left * update_left) * (update_right' * p_right);
    formula_ratio = (updated_single_overlap / ...
                     single_particle_overlap)^particle_number;
    explicit_ratio = explicit_updated / explicit_overlap;
    ratio_error = relative_error(explicit_ratio, formula_ratio);

    fock_left = symmetric_power_operator(B_left, particle_number);
    fock_right = symmetric_power_operator(B_right, particle_number);
    explicit_one_body = inserted_one_body( ...
        trial_state, fock_left, fock_right, occupations, ...
        explicit_overlap);
    formula_one_body = particle_number * ...
        (p_right * p_left) / single_particle_overlap;
    one_body_error = norm(explicit_one_body - formula_one_body, "fro") / ...
                     max(1, norm(explicit_one_body, "fro"));

    conjugate_pair_weight = formula_overlap * conj(formula_overlap);
    pair_residual = abs(imag(conjugate_pair_weight));
    assert(real(conjugate_pair_weight) >= 0);

    fprintf(fid, "%d,%d,%d,%.16g,%.16g,%.16g,%.16g\n", ...
            trial, orbitals, particle_number, overlap_error, ratio_error, ...
            one_body_error, pair_residual);
    worst_overlap_error = max(worst_overlap_error, overlap_error);
    worst_ratio_error = max(worst_ratio_error, ratio_error);
    worst_one_body_error = max(worst_one_body_error, one_body_error);
    worst_pair_residual = max(worst_pair_residual, pair_residual);
  endfor

  % A separate projection check: the midpoint estimator approaches N E_0.
  one_body_hamiltonian = diag([-1.3, -0.2, 0.8]);
  p = [1; 2; -1i];
  p /= norm(p);
  particle_number = 5;
  theta = 10;
  p_right = expm(-theta * one_body_hamiltonian) * p;
  p_left = p' * expm(-theta * one_body_hamiltonian);
  projected_energy = particle_number * ...
      (p_left * one_body_hamiltonian * p_right) / (p_left * p_right);
  ground_energy = particle_number * one_body_hamiltonian(1, 1);
  projection_error = abs(projected_energy - ground_energy);

  fclose(fid);
  assert(worst_overlap_error < 2e-11);
  assert(worst_ratio_error < 2e-11);
  assert(worst_one_body_error < 2e-11);
  assert(worst_pair_residual < 2e-11);
  assert(projection_error < 2e-7);

  printf("Octave version: %s\n", version());
  printf(["Verified rank-one projector overlap, local ratio, midpoint " ...
          "one-body estimator, and conjugate-pair positivity in %d trials.\n"], ...
         trial_count);
  printf(["Worst relative errors: overlap %.3e, ratio %.3e, " ...
          "one-body %.3e.\n"], ...
         worst_overlap_error, worst_ratio_error, worst_one_body_error);
  printf("Projection energy error at theta=%g: %.3e.\n", ...
         theta, projection_error);
  printf("Wrote %s\n", output_file);
endfunction


function state = rank_one_state(p, occupations, particle_number)
  state = zeros(rows(occupations), 1);
  for index = 1:rows(occupations)
    occupation = occupations(index, :);
    coefficient = sqrt(factorial(particle_number) / ...
                       prod(factorial(occupation)));
    state(index) = coefficient * prod((p.').^occupation);
  endfor
endfunction


function one_body = inserted_one_body( ...
    trial_state, fock_left, fock_right, occupations, overlap)
  orbitals = columns(occupations);
  one_body = zeros(orbitals);
  for creation = 1:orbitals
    for annihilation = 1:orbitals
      observable = one_body_operator( ...
          occupations, creation, annihilation);
      one_body(annihilation, creation) = ...
          trial_state' * fock_left * observable * ...
          fock_right * trial_state / overlap;
    endfor
  endfor
endfunction


function observable = one_body_operator(occupations, creation, annihilation)
  sector_dimension = rows(occupations);
  observable = zeros(sector_dimension);
  for ket_index = 1:sector_dimension
    ket = occupations(ket_index, :);
    if ket(annihilation) == 0
      continue;
    endif
    bra = ket;
    amplitude = sqrt(bra(annihilation));
    bra(annihilation) -= 1;
    amplitude *= sqrt(bra(creation) + 1);
    bra(creation) += 1;
    bra_index = find(all(occupations == bra, 2));
    assert(numel(bra_index) == 1);
    observable(bra_index, ket_index) = amplitude;
  endfor
endfunction


function [operator, occupations] = symmetric_power_operator( ...
    B, particle_number)
  orbitals = rows(B);
  occupations = occupation_compositions(particle_number, orbitals);
  sector_dimension = rows(occupations);
  operator = zeros(sector_dimension);
  for row_index = 1:sector_dimension
    row_labels = repeated_labels(occupations(row_index, :));
    row_factorial = prod(factorial(occupations(row_index, :)));
    for column_index = 1:sector_dimension
      column_labels = repeated_labels(occupations(column_index, :));
      column_factorial = prod(factorial(occupations(column_index, :)));
      repeated_matrix = B(row_labels, column_labels);
      operator(row_index, column_index) = ...
          matrix_permanent(repeated_matrix) / ...
          sqrt(row_factorial * column_factorial);
    endfor
  endfor
endfunction


function occupations = occupation_compositions(total, parts)
  if parts == 1
    occupations = total;
    return;
  endif
  occupations = [];
  for first = 0:total
    tails = occupation_compositions(total - first, parts - 1);
    occupations = [occupations; ...
                   first * ones(rows(tails), 1), tails];
  endfor
endfunction


function labels = repeated_labels(occupation)
  labels = [];
  for orbital = 1:numel(occupation)
    labels = [labels, orbital * ones(1, occupation(orbital))];
  endfor
endfunction


function value = matrix_permanent(matrix)
  dimension = rows(matrix);
  if dimension == 0
    value = 1;
    return;
  endif
  permutations = perms(1:dimension);
  value = 0;
  for index = 1:rows(permutations)
    product = 1;
    for row_index = 1:dimension
      product *= matrix(row_index, permutations(index, row_index));
    endfor
    value += product;
  endfor
endfunction


function error_value = relative_error(left, right)
  error_value = abs(left - right) / max([1, abs(left), abs(right)]);
endfunction
