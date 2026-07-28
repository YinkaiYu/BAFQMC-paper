function verify_canonical_boson_afqmc()
  more off;
  format long g;
  rng(20260728, "twister");

  here = fileparts(mfilename("fullpath"));
  output_file = fullfile(here, "..", "tables", ...
                         "canonical_boson_afqmc_checks.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["trial,orbitals,particle_number,recurrence_weight," ...
                "explicit_fock_weight,weight_relative_error," ...
                "one_body_relative_error,particle_number_residual," ...
                "low_rank_weight_relative_error\n"]);

  trial_count = 12;
  worst_weight_error = 0;
  worst_one_body_error = 0;
  worst_number_residual = 0;
  worst_update_error = 0;
  for trial = 1:trial_count
    orbitals = 3;
    particle_number = 4;
    B = eye(orbitals);
    for slice = 1:4
      generator = 0.12 * (randn(orbitals) + 1i * randn(orbitals));
      B = expm(generator) * B;
    endfor

    [weights, one_body] = canonical_recurrence(B, particle_number);
    weight = weights(particle_number + 1);
    [fock_operator, occupations] = symmetric_power_operator( ...
        B, particle_number);
    explicit_weight = trace(fock_operator);
    explicit_one_body = explicit_one_body_trace( ...
        fock_operator, occupations, particle_number) / explicit_weight;

    weight_error = relative_error(weight, explicit_weight);
    one_body_error = norm(one_body - explicit_one_body, "fro") / ...
                     max(1, norm(explicit_one_body, "fro"));
    number_residual = abs(trace(one_body) - particle_number);

    update_left = 0.04 * (randn(orbitals, 1) + ...
                          1i * randn(orbitals, 1));
    update_right = randn(orbitals, 1) + 1i * randn(orbitals, 1);
    B_updated = B + update_left * update_right';
    updated_weights = inverse_characteristic_series( ...
        characteristic_coefficients(B_updated), particle_number);
    ratio_series = polynomial_ratio_series( ...
        characteristic_coefficients(B), ...
        characteristic_coefficients(B_updated), particle_number);
    convolution_weight = 0;
    for order = 0:particle_number
      convolution_weight += ratio_series(order + 1) * ...
                            weights(particle_number - order + 1);
    endfor
    update_error = relative_error( ...
        convolution_weight, updated_weights(particle_number + 1));

    fprintf(fid, ["%d,%d,%d,%.16g%+.16gi,%.16g%+.16gi," ...
                  "%.16g,%.16g,%.16g,%.16g\n"], ...
            trial, orbitals, particle_number, real(weight), imag(weight), ...
            real(explicit_weight), imag(explicit_weight), ...
            weight_error, one_body_error, number_residual, update_error);
    worst_weight_error = max(worst_weight_error, weight_error);
    worst_one_body_error = max(worst_one_body_error, one_body_error);
    worst_number_residual = max(worst_number_residual, number_residual);
    worst_update_error = max(worst_update_error, update_error);
  endfor
  fclose(fid);

  assert(worst_weight_error < 2e-11);
  assert(worst_one_body_error < 2e-11);
  assert(worst_number_residual < 2e-11);
  assert(worst_update_error < 2e-11);

  printf("Octave version: %s\n", version());
  printf(["Verified canonical recurrence, one-body estimator, and exact " ...
          "rank-one update convolution in %d trials.\n"], trial_count);
  printf("Worst relative errors: weight %.3e, one-body %.3e, update %.3e.\n", ...
         worst_weight_error, worst_one_body_error, worst_update_error);
  printf("Wrote %s\n", output_file);
endfunction


function [weights, one_body] = canonical_recurrence(B, particle_number)
  orbitals = rows(B);
  weights = zeros(particle_number + 1, 1);
  weights(1) = 1;
  powers = cell(particle_number, 1);
  current_power = eye(orbitals);
  power_traces = zeros(particle_number, 1);
  for order = 1:particle_number
    current_power = current_power * B;
    powers{order} = current_power;
    power_traces(order) = trace(current_power);
  endfor

  for number = 1:particle_number
    total = 0;
    for order = 1:number
      total += power_traces(order) * weights(number - order + 1);
    endfor
    weights(number + 1) = total / number;
  endfor

  one_body = zeros(orbitals);
  for order = 1:particle_number
    one_body += weights(particle_number - order + 1) * powers{order};
  endfor
  one_body /= weights(particle_number + 1);
endfunction


function coefficients = characteristic_coefficients(B)
  coefficients = poly(B);
  coefficients(abs(coefficients) < 1e-14) = 0;
endfunction


function weights = inverse_characteristic_series( ...
    coefficients, particle_number)
  degree = numel(coefficients) - 1;
  weights = zeros(particle_number + 1, 1);
  weights(1) = 1;
  for number = 1:particle_number
    total = 0;
    for order = 1:min(number, degree)
      total += coefficients(order + 1) * ...
               weights(number - order + 1);
    endfor
    weights(number + 1) = -total;
  endfor
endfunction


function ratio = polynomial_ratio_series( ...
    numerator, denominator, particle_number)
  numerator_degree = numel(numerator) - 1;
  denominator_degree = numel(denominator) - 1;
  ratio = zeros(particle_number + 1, 1);
  ratio(1) = 1;
  for number = 1:particle_number
    if number <= numerator_degree
      total = numerator(number + 1);
    else
      total = 0;
    endif
    for order = 1:min(number, denominator_degree)
      total -= denominator(order + 1) * ratio(number - order + 1);
    endfor
    ratio(number + 1) = total;
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


function one_body = explicit_one_body_trace( ...
    fock_operator, occupations, particle_number)
  orbitals = columns(occupations);
  sector_dimension = rows(occupations);
  one_body = zeros(orbitals);
  for creation = 1:orbitals
    for annihilation = 1:orbitals
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
      % The returned matrix follows G_{ij}=<a_j^+ a_i>.
      one_body(annihilation, creation) = ...
          trace(fock_operator * observable);
    endfor
  endfor
endfunction


function error_value = relative_error(left, right)
  error_value = abs(left - right) / max([1, abs(left), abs(right)]);
endfunction
