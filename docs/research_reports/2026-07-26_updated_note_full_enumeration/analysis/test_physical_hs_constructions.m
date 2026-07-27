function test_physical_hs_constructions()
  more off;
  format long g;

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif
  output_file = fullfile(table_dir, "physical_hs_slice_checks.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["example,statistics,class_name,field_type,field_value," ...
                "J1_word,J2_word,metric,max_relation_residual," ...
                "lie_residual,reality_residual," ...
                "max_fixed_contraction_eigenvalue,field_isometry_residual," ...
                "max_contraction_eigenvalue," ...
                "fixed_part_adjoint,field_generator_adjoint,total_slice_adjoint\n"]);

  % The sixteen blocks below mirror physical_model_catalog.py.  Every
  % continuous field multiplies a maximal-subgroup generator, so the
  % fixed strict margin is unchanged for either sign of the Gaussian field.

  % Boson J2g, s1=-1, q1=+1: single-mode pair quadrature.
  for phi = [-3, -1, 0, 2.5]
    fixed_part = -2 * word("Z");
    field_generator = 1i * word("Y");
    A = fixed_part + phi * field_generator;
    write_check(fid, "boson_pair_quadrature_single_mode", "boson", ...
                "B-J2g-s1-q1+", "continuous_gaussian", phi, ...
                "Z", "X", "J2g", A, fixed_part, field_generator);
  endfor

  % Boson J2g, s1=-1, q1=-1: bond-current interaction.
  for phi = [-3, -1, 0, 2.5]
    fixed_part = -2 * word("ZI");
    field_generator = word("IY");
    A = fixed_part + phi * field_generator;
    write_check(fid, "boson_bond_current", "boson", ...
                "B-J2g-s1-q1-", "continuous_gaussian", phi, ...
                "ZY", "XI", "J2g", A, fixed_part, field_generator);
  endfor

  % Boson J2g, s1=+1, q1=+1: relative-density HS field (Case 7).
  for phi = [-4, -1, 0, 3]
    fixed_part = -2 * word("ZI");
    field_generator = 1i * word("ZZ");
    A = fixed_part + phi * field_generator;
    write_check(fid, "boson_relative_density_case7", "boson", ...
                "B-J2g-s1+q1+", "continuous_gaussian", phi, ...
                "IX", "XI", "J2g", A, fixed_part, field_generator);
  endfor

  % Boson J2g, s1=+1, q1=-1: the same relative-density field with J1^2=-I.
  for phi = [-4, -1, 0, 3]
    fixed_part = -2 * word("ZI");
    field_generator = 1i * word("ZZ");
    A = fixed_part + phi * field_generator;
    write_check(fid, "boson_relative_density_kramers", "boson", ...
                "B-J2g-s1+q1-", "continuous_gaussian", phi, ...
                "IY", "XI", "J2g", A, fixed_part, field_generator);
  endfor

  % Boson iJ2g, s1=-1, q1=+1: collective-spin LMG dimer.
  for phi = [-3, -1, 0, 2]
    fixed_part = -1i * word("IY");
    field_generator = word("ZX");
    A = fixed_part + phi * field_generator;
    write_check(fid, "boson_lmg_fixed_number", "boson", ...
                "B-iJ2g-s1-q1+", "continuous_gaussian", phi, ...
                "ZX", "YY", "iJ2g", A, fixed_part, field_generator);
  endfor

  % Boson iJ2g, s1=-1, q1=-1: four-component collective model.
  for phi = [-3, -1, 0, 2]
    fixed_part = -1i * word("IYX");
    field_generator = word("ZIZ");
    A = fixed_part + phi * field_generator;
    write_check(fid, "boson_four_component_collective", "boson", ...
                "B-iJ2g-s1-q1-", "continuous_gaussian", phi, ...
                "XIY", "YYX", "iJ2g", A, fixed_part, field_generator);
  endfor

  % Boson iJ2g, s1=+1, q1=+1: two-mode pairing quadrature.
  for phi = [-3, -1, 0, 2]
    fixed_part = -1i * word("IY");
    field_generator = word("XX");
    A = fixed_part + phi * field_generator;
    write_check(fid, "boson_parametric_dimer", "boson", ...
                "B-iJ2g-s1+q1+", "continuous_gaussian", phi, ...
                "IX", "YY", "iJ2g", A, fixed_part, field_generator);
  endfor

  % Boson iJ2g, s1=+1, q1=-1: one-axis-twisting dimer.
  for phi = [-3, -1, 0, 2]
    fixed_part = -1i * word("IY");
    field_generator = word("ZZ");
    A = fixed_part + phi * field_generator;
    write_check(fid, "boson_one_axis_twisting", "boson", ...
                "B-iJ2g-s1+q1-", "continuous_gaussian", phi, ...
                "YX", "YY", "iJ2g", A, fixed_part, field_generator);
  endfor

  % Fermion J2g, s1=-1, q1=+1.  This tensor-extends the one-mode
  % representative so that the subgroup contains a bond-current field.
  for phi = [-3, -1, 0, 2]
    fixed_part = -2 * word("ZI") + 0.5 * word("ZX");
    field_generator = word("IY");
    A = fixed_part + phi * field_generator;
    write_check(fid, "fermion_bond_current_dimer", "fermion", ...
                "F-J2g-s1-q1+", "continuous_gaussian", phi, ...
                "ZI", "YI", "J2g", A, fixed_part, field_generator);
  endfor

  % Fermion J2g, s1=-1, q1=-1: pairing-channel attractive dot.
  for phi = [-3, -1, 0, 2]
    fixed_part = -2 * word("ZI");
    field_generator = 1i * word("XY");
    A = fixed_part + phi * field_generator;
    write_check(fid, "fermion_particle_hole_pair_dot", "fermion", ...
                "F-J2g-s1-q1-", "continuous_gaussian", phi, ...
                "ZY", "YI", "J2g", A, fixed_part, field_generator);
  endfor

  % Fermion J2g, s1=+1, q1=+1: reflected attractive dimer.
  for phi = [-3, -1, 0, 2]
    fixed_part = -2 * word("ZI") + 0.5 * word("ZX");
    field_generator = 1i * word("XY");
    A = fixed_part + phi * field_generator;
    write_check(fid, "fermion_majorana_reflection_dimer", "fermion", ...
                "F-J2g-s1+q1+", "continuous_gaussian", phi, ...
                "IX", "YI", "J2g", A, fixed_part, field_generator);
  endfor

  % Fermion J2g, s1=+1, q1=-1: Kramers pair quadrature.
  for phi = [-3, -1, 0, 2]
    fixed_part = -2 * word("ZI");
    field_generator = word("YY");
    A = fixed_part + phi * field_generator;
    write_check(fid, "fermion_kramers_pair_dot", "fermion", ...
                "F-J2g-s1+q1-", "continuous_gaussian", phi, ...
                "IY", "YI", "J2g", A, fixed_part, field_generator);
  endfor

  % Fermion iJ2g, s1=-1, q1=+1: proximitized attractive dot.
  for phi = [-3, -1, 0, 2]
    fixed_part = -1i * word("XY");
    field_generator = word("ZI");
    A = fixed_part + phi * field_generator;
    write_check(fid, "fermion_proximitized_charging_dot", "fermion", ...
                "F-iJ2g-s1-q1+", "continuous_gaussian", phi, ...
                "ZI", "IY", "iJ2g", A, fixed_part, field_generator);
  endfor

  % Fermion iJ2g, s1=-1, q1=-1: spin-polarization interaction.
  for phi = [-3, -1, 0, 2]
    fixed_part = -1i * word("XY");
    field_generator = 1i * word("ZZ");
    A = fixed_part + phi * field_generator;
    write_check(fid, "fermion_spin_polarization_dot", "fermion", ...
                "F-iJ2g-s1-q1-", "continuous_gaussian", phi, ...
                "YI", "IY", "iJ2g", A, fixed_part, field_generator);
  endfor

  % Fermion iJ2g, s1=+1, q1=+1: reflected proximitized dimer.
  for phi = [-3, -1, 0, 2]
    fixed_part = -2i * word("XY") + 0.5 * word("ZX");
    field_generator = 1i * word("ZZ");
    A = fixed_part + phi * field_generator;
    write_check(fid, "fermion_reflected_proximitized_dimer", "fermion", ...
                "F-iJ2g-s1+q1+", "continuous_gaussian", phi, ...
                "IX", "IY", "iJ2g", A, fixed_part, field_generator);
  endfor

  % Fermion iJ2g, s1=+1, q1=-1: four-mode pairing island.
  for phi = [-3, -1, 0, 2]
    fixed_part = -1i * word("XYI");
    field_generator = word("ZII");
    A = fixed_part + phi * field_generator;
    write_check(fid, "fermion_four_mode_pairing_island", "fermion", ...
                "F-iJ2g-s1+q1-", "continuous_gaussian", phi, ...
                "IXY", "IYI", "iJ2g", A, fixed_part, field_generator);
  endfor

  fclose(fid);
  printf("Octave version: %s\n", version());
  printf("Wrote %s\n", output_file);
endfunction


function write_check(fid, example, statistics, class_name, field_type, ...
                     field_value, J1_word, J2_word, metric_name, A, ...
                     fixed_part, field_generator)
  n = length(J1_word);
  g = canonical_g(statistics, n);
  J1 = word(J1_word);
  J2 = word(J2_word);
  dimension = rows(g);
  if strcmp(metric_name, "J2g")
    eta = J2 * g;
  else
    eta = 1i * J2 * g;
  endif
  signs = [
    matrix_sign(J1.' * g * J1, g);
    matrix_sign(J1 * J1, eye(dimension));
    matrix_sign(J2.' * g * J2, g);
    matrix_sign(J2 * J2, eye(dimension));
    commutation_sign(J1, J2)
  ];
  expected_signs = class_signs(class_name);
  assert(all(signs(:).' == expected_signs));
  relation_residual = max([
    norm(J1.' * g * J1 - signs(1) * g, "fro");
    norm(J1 * J1 - signs(2) * eye(dimension), "fro");
    norm(J2.' * g * J2 - signs(3) * g, "fro");
    norm(J2 * J2 - signs(4) * eye(dimension), "fro");
    norm(J1 * J2 - signs(5) * J2 * J1, "fro")
  ]);
  lie_residual = norm(g * A + A.' * g, "fro");
  reality_residual = norm(J1.' * A * J1 - conj(A), "fro");
  fixed_lie_residual = norm(g * fixed_part + fixed_part.' * g, "fro");
  field_lie_residual = ...
      norm(g * field_generator + field_generator.' * g, "fro");
  fixed_reality_residual = ...
      norm(J1.' * fixed_part * J1 - conj(fixed_part), "fro");
  field_reality_residual = ...
      norm(J1.' * field_generator * J1 - conj(field_generator), "fro");
  fixed_contraction_matrix = ...
      eta * fixed_part + fixed_part' * eta;
  fixed_contraction_matrix = ...
      (fixed_contraction_matrix + fixed_contraction_matrix') / 2;
  maximum_fixed_contraction_eigenvalue = ...
      max(real(eig(fixed_contraction_matrix)));
  field_contraction_matrix = ...
      eta * field_generator + field_generator' * eta;
  field_isometry_residual = norm(field_contraction_matrix, "fro");
  contraction_matrix = eta * A + A' * eta;
  contraction_matrix = (contraction_matrix + contraction_matrix') / 2;
  maximum_contraction_eigenvalue = max(real(eig(contraction_matrix)));
  fixed_part_adjoint = physical_adjoint_type(g, fixed_part, n);
  field_generator_adjoint = physical_adjoint_type(g, field_generator, n);
  total_slice_adjoint = physical_adjoint_type(g, A, n);

  assert(max([relation_residual, lie_residual, reality_residual, ...
              fixed_lie_residual, field_lie_residual, ...
              fixed_reality_residual, field_reality_residual, ...
              field_isometry_residual]) < 1e-11);
  assert(maximum_fixed_contraction_eigenvalue < -1e-11);
  assert(maximum_contraction_eigenvalue < 1e-11);
  fprintf(fid, ...
          ["%s,%s,%s,%s,%.16g,%s,%s,%s,%.16g,%.16g,%.16g," ...
           "%.16g,%.16g,%.16g," ...
           "%s,%s,%s\n"], ...
          example, statistics, class_name, field_type, field_value, ...
          J1_word, J2_word, metric_name, relation_residual, lie_residual, ...
          reality_residual, maximum_fixed_contraction_eigenvalue, ...
          field_isometry_residual, maximum_contraction_eigenvalue, ...
          fixed_part_adjoint, field_generator_adjoint, total_slice_adjoint);
endfunction


function signs = class_signs(class_name)
  switch class_name
    case "B-J2g-s1-q1+"
      signs = [-1, 1, -1, 1, -1];
    case "B-J2g-s1-q1-"
      signs = [-1, -1, -1, 1, -1];
    case "B-J2g-s1+q1+"
      signs = [1, 1, -1, 1, 1];
    case "B-J2g-s1+q1-"
      signs = [1, -1, -1, 1, 1];
    case "B-iJ2g-s1-q1+"
      signs = [-1, 1, 1, 1, 1];
    case "B-iJ2g-s1-q1-"
      signs = [-1, -1, 1, 1, 1];
    case "B-iJ2g-s1+q1+"
      signs = [1, 1, 1, 1, -1];
    case "B-iJ2g-s1+q1-"
      signs = [1, -1, 1, 1, -1];
    case "F-J2g-s1-q1+"
      signs = [-1, 1, -1, -1, -1];
    case "F-J2g-s1-q1-"
      signs = [-1, -1, -1, -1, -1];
    case "F-J2g-s1+q1+"
      signs = [1, 1, -1, -1, 1];
    case "F-J2g-s1+q1-"
      signs = [1, -1, -1, -1, 1];
    case "F-iJ2g-s1-q1+"
      signs = [-1, 1, 1, -1, 1];
    case "F-iJ2g-s1-q1-"
      signs = [-1, -1, 1, -1, 1];
    case "F-iJ2g-s1+q1+"
      signs = [1, 1, 1, -1, -1];
    case "F-iJ2g-s1+q1-"
      signs = [1, -1, 1, -1, -1];
    otherwise
      error("Unknown strict class: %s", class_name);
  endswitch
endfunction


function answer = physical_adjoint_type(g, A, n)
  exchange = kron(word("X"), eye(2^(n - 1)));
  coefficient = g * A;
  adjoint_coefficient = exchange * coefficient' * exchange;
  if norm(adjoint_coefficient - coefficient, "fro") < 1e-11
    answer = "Hermitian";
  elseif norm(adjoint_coefficient + coefficient, "fro") < 1e-11
    answer = "anti-Hermitian";
  else
    answer = "neither";
  endif
endfunction


function g = canonical_g(statistics, n)
  if strcmp(statistics, "boson")
    g = kron(-word("Y"), eye(2^(n - 1)));
  else
    g = kron(word("X"), eye(2^(n - 1)));
  endif
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
