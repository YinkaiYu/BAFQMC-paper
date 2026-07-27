function verify_boson_iJ2g_canonical()
  more off;
  format long g;

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  cases = {
    "B-iJ2g-s1+q1+", "IX",  "YY",  "IY",  "ZX";
    "B-iJ2g-s1+q1-", "YX",  "YY",  "IY",  "ZZ";
    "B-iJ2g-s1-q1+", "ZX",  "YY",  "IY",  "ZX";
    "B-iJ2g-s1-q1-", "XIY", "YYX", "IYX", "ZIZ"
  };

  random_configurations = 400;
  slices = 7;
  maximum_particle_number = 8;
  fixed_strength = 0.31;
  field_scale = 0.65;
  rand("seed", 20260728);
  randn("seed", 20260728);

  output_file = fullfile(table_dir, "boson_iJ2g_canonical_checks.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["class_name,mode_count,field_word,random_configurations," ...
                "minimum_particle_eigenvalue_real," ...
                "maximum_particle_eigenvalue_imag," ...
                "minimum_fixed_N_weight," ...
                "maximum_fixed_N_weight_relative_imag," ...
                "largest_full_contraction_eigenvalue," ...
                "reference_N4_weight,minimum_spectral_radius," ...
                "stable_grand_canonical_generator_contraction_max\n"]);

  for case_index = 1:rows(cases)
    class_name = cases{case_index, 1};
    J1_name = cases{case_index, 2};
    J2_name = cases{case_index, 3};
    fixed_internal_word = cases{case_index, 4};
    field_name = cases{case_index, 5};
    n = length(J1_name);
    mode_count = 2^(n - 1);
    dimension = 2 * mode_count;

    g = kron(-word("Y"), eye(mode_count));
    J1 = word(J1_name);
    J2 = word(J2_name);
    eta = 1i * J2 * g;
    fixed_generator = -1i * word(fixed_internal_word);
    field_generator = word(field_name);

    assert(norm(g * fixed_generator + fixed_generator.' * g, "fro") < 1e-11);
    assert(norm(g * field_generator + field_generator.' * g, "fro") < 1e-11);
    assert(norm(J1.' * fixed_generator * J1 - ...
                conj(fixed_generator), "fro") < 1e-11);
    assert(norm(J1.' * field_generator * J1 - ...
                conj(field_generator), "fro") < 1e-11);
    assert(max(real(eig(eta * fixed_generator + ...
                        fixed_generator' * eta))) < -1.9);
    assert(norm(eta * field_generator + ...
                field_generator' * eta, "fro") < 1e-11);

    minimum_particle_eigenvalue_real = Inf;
    maximum_particle_eigenvalue_imag = 0;
    minimum_fixed_N_weight = Inf;
    maximum_fixed_N_weight_relative_imag = 0;
    largest_full_contraction_eigenvalue = -Inf;
    minimum_spectral_radius = Inf;

    for configuration = 1:random_configurations
      fields = field_scale * randn(1, slices);
      full_matrix = eye(dimension);
      for slice = 1:slices
        full_matrix = full_matrix * ...
            expm(fixed_strength * fixed_generator) * ...
            expm(fields(slice) * field_generator);
      endfor

      off_diagonal_norm = ...
          norm(full_matrix(1:mode_count, mode_count + 1:end), "fro") + ...
          norm(full_matrix(mode_count + 1:end, 1:mode_count), "fro");
      assert(off_diagonal_norm < 1e-10);
      particle_matrix = full_matrix(1:mode_count, 1:mode_count);
      particle_eigenvalues = eig(particle_matrix);

      minimum_particle_eigenvalue_real = min( ...
          minimum_particle_eigenvalue_real, ...
          min(real(particle_eigenvalues)));
      maximum_particle_eigenvalue_imag = max( ...
          maximum_particle_eigenvalue_imag, ...
          max(abs(imag(particle_eigenvalues))));
      minimum_spectral_radius = min( ...
          minimum_spectral_radius, max(abs(particle_eigenvalues)));

      assert(min(real(particle_eigenvalues)) > 1e-9);
      assert(max(abs(imag(particle_eigenvalues))) < 1e-8);
      assert(abs(det(particle_matrix) - 1) < 1e-7);
      assert(max(abs(particle_eigenvalues)) > 1 + 1e-9);

      for particle_number = 1:maximum_particle_number
        weight = symmetric_power_trace( ...
            particle_eigenvalues, particle_number);
        minimum_fixed_N_weight = min( ...
            minimum_fixed_N_weight, real(weight));
        maximum_fixed_N_weight_relative_imag = max( ...
            maximum_fixed_N_weight_relative_imag, ...
            abs(imag(weight)) / (1 + abs(real(weight))));
        assert(real(weight) > 1e-8);
        assert(abs(imag(weight)) < 1e-6 * (1 + abs(real(weight))));
      endfor

      contraction_matrix = ...
          full_matrix' * eta * full_matrix - eta;
      contraction_matrix = ...
          (contraction_matrix + contraction_matrix') / 2;
      largest_full_contraction_eigenvalue = max( ...
          largest_full_contraction_eigenvalue, ...
          max(real(eig(contraction_matrix))));
      assert(max(real(eig(contraction_matrix))) < -1e-9);
    endfor

    reference_particle_matrix = ...
        expm(slices * fixed_strength * ...
             fixed_generator(1:mode_count, 1:mode_count));
    reference_N4_weight = real(symmetric_power_trace( ...
        eig(reference_particle_matrix), 4));
    assert(reference_N4_weight > 0);

    stable_generator = -2 * kron(word("Z"), eye(mode_count));
    stable_contraction_matrix = ...
        eta * stable_generator + stable_generator' * eta;
    stable_generator_contraction_max = ...
        max(real(eig(stable_contraction_matrix)));
    assert(stable_generator_contraction_max > 1);

    fprintf(fid, ...
            ["%s,%d,%s,%d,%.16g,%.16g,%.16g,%.16g," ...
             "%.16g,%.16g,%.16g,%.16g\n"], ...
            class_name, mode_count, field_name, random_configurations, ...
            minimum_particle_eigenvalue_real, ...
            maximum_particle_eigenvalue_imag, ...
            minimum_fixed_N_weight, maximum_fixed_N_weight_relative_imag, ...
            largest_full_contraction_eigenvalue, reference_N4_weight, ...
            minimum_spectral_radius, stable_generator_contraction_max);
  endfor

  fclose(fid);
  printf("Octave version: %s\n", version());
  printf("Verified four canonical bosonic iJ2g models.\n");
  printf("Wrote %s\n", output_file);
endfunction


function answer = symmetric_power_trace(eigenvalues, particle_number)
  coefficients = zeros(particle_number + 1, 1);
  coefficients(1) = 1;
  for eigenvalue_index = 1:length(eigenvalues)
    eigenvalue = eigenvalues(eigenvalue_index);
    for order = 1:particle_number
      coefficients(order + 1) = ...
          coefficients(order + 1) + ...
          eigenvalue * coefficients(order);
    endfor
  endfor
  answer = coefficients(particle_number + 1);
endfunction


function matrix = word(name)
  matrix = 1;
  for position = 1:length(name)
    switch name(position)
      case "I"
        factor = eye(2);
      case "X"
        factor = [0, 1; 1, 0];
      case "Y"
        factor = [0, 1; -1, 0];
      case "Z"
        factor = [1, 0; 0, -1];
      otherwise
        error("Unknown Pauli label.");
    endswitch
    matrix = kron(matrix, factor);
  endfor
endfunction
