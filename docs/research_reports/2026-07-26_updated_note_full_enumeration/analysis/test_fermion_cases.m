function test_fermion_cases()
  more off;
  format long g;
  rng(20260725, "twister");

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  I = pauli("I");
  X = pauli("X");
  Y = pauli("Y");
  Z = pauli("Z");
  g = kron(X, I);

  printf("Octave version: %s\n", version());
  printf("Random seed: 20260725 (twister)\n");
  printf("Y denotes i*sigma_y, not the complex Hermitian sigma_y.\n\n");

  cases = {
    make_case("3", kron(Y, Y), kron(Y, I), {X, Z}, ...
              [-1, 1, -1, -1, 1]),
    make_case("4", kron(Y, I), kron(Y, X), {1i * Z, Y}, ...
              [-1, -1, -1, -1, 1]),
    make_case("6", kron(Y, I), kron(Y, Y), {1i * Z, 1i * X}, ...
              [-1, -1, -1, 1, 1])
  };

  output_file = fullfile(table_dir, "fermion_cases_3_4_6_tests.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["case,class_id,basis_dim,max_lie_residual," ...
                "max_J1_residual,max_V_formal_edge_residual," ...
                "max_ToY_edge_residual,commutator_closure_residual," ...
                "min_random_real_weight,max_random_abs_imag_weight," ...
                "random_negative_count,max_unitarity_residual," ...
                "explicit_weight,node_parameter,node_abs_weight,trials,seed\n"]);

  trial_count = 10000;
  for case_index = 1:numel(cases)
    current = cases{case_index};
    actual_signs = classify_pair(g, current.J1, current.J2);
    assert(all(actual_signs(:).' == current.expected_signs));

    [lie_residual, J1_residual, V_formal_residual, toy_residual] = ...
        validate_basis(g, current.J1, current.J2, current.B_basis);
    closure_residual = particle_closure_residual(current.B_basis);
    rng(20260725 + str2num(current.name), "twister");
    [minimum_weight, maximum_imaginary_part, negative_count, ...
     maximum_unitarity_residual] = random_particle_scan( ...
        current.B_basis, trial_count, 8, 2.5);

    explicit_weight = NaN;
    node_parameter = NaN;
    node_abs_weight = NaN;
    if strcmp(current.name, "3")
      explicit_B = {
        -2 * X - 2 * Z,
        -2 * X,
        2 * X + Z
      };
      explicit_weight = particle_weight(explicit_B);
      assert(real(explicit_weight) < -20);
      [explicit_lie, explicit_J1, explicit_V_formal, explicit_toy] = ...
          validate_basis(g, current.J1, current.J2, explicit_B);
      assert(max([explicit_lie, explicit_J1, explicit_V_formal, ...
                  explicit_toy]) < 1e-12);
      node_parameter = bisection_node(explicit_B);
      scaled_B = scale_generators(explicit_B, node_parameter);
      node_abs_weight = abs(particle_weight(scaled_B));

      printf("Case 3 exact counterexample:\n");
      printf("  B1=-2X-2Z, B2=-2X, B3=2X+Z\n");
      printf("  W=det(I+exp(B1)exp(B2)exp(B3))=%.15g\n", ...
             explicit_weight);
      printf("  A node occurs on the connected scaling path at t=%.15g", ...
             node_parameter);
      printf(" (|W|=%.3e).\n\n", node_abs_weight);
    elseif strcmp(current.name, "4")
      node_B = {pi * Y};
      node_parameter = pi;
      node_abs_weight = abs(particle_weight(node_B));
    elseif strcmp(current.name, "6")
      node_B = {1i * pi * Z};
      node_parameter = pi;
      node_abs_weight = abs(particle_weight(node_B));
    endif

    fprintf(fid, ...
            "%s,%s,%d,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g,%d,%.16g,%.16g,%.16g,%.16g,%d,%d\n", ...
            current.name, class_label(actual_signs), ...
            numel(current.B_basis), lie_residual, J1_residual, ...
            V_formal_residual, toy_residual, closure_residual, ...
            minimum_weight, maximum_imaginary_part, negative_count, ...
            maximum_unitarity_residual, explicit_weight, ...
            node_parameter, node_abs_weight, trial_count, ...
            20260725 + str2num(current.name));

    printf("Case %s: basis dimension %d, commutator-closure residual %.6g\n", ...
           current.name, numel(current.B_basis), closure_residual);
    printf("  random min Re(W)=%.12g, max |Im(W)|=%.3e, negatives=%d/%d\n", ...
           minimum_weight, maximum_imaginary_part, ...
           negative_count, trial_count);
    if strcmp(current.name, "4") || strcmp(current.name, "6")
      printf("  every basis generator is traceless anti-Hermitian; ");
      printf("products lie in SU(2), so W=4*cos(theta/2)^2 >= 0.\n");
      printf("  U=-I is allowed and gives a zero: |W|=%.3e.\n\n", ...
             node_abs_weight);
    endif
  endfor
  fclose(fid);

  test_case_1(X, Y, Z, table_dir);
  test_case_5(g, X, Y, Z, table_dir);
  test_full_pairing_case_6(I, X, Y, Z, table_dir);
  test_inequality_signs(I, X, Y, Z, table_dir);

  printf("Wrote %s\n", output_file);
endfunction


function test_full_pairing_case_6(I, X, Y, Z, table_dir)
  g = kron(X, I);
  J1 = kron(Z, Y);
  J2 = kron(Z, I);
  A = -(3 * pi / 2) * kron(I, Y) - 1i * pi * kron(Y, Y);
  signs = classify_pair(g, J1, J2);
  assert(all(signs(:).' == [-1, -1, -1, 1, 1]));

  [chi, fock_dimension] = two_mode_fermion_nambu_operators(I, Z);
  h = quadratic_fock_operator(g * A, chi, fock_dimension);
  h_eigenvalues = eig(h);
  target_imaginary_spectrum = pi * [-3 / 2; -1; 1; 3 / 2];
  assert(norm(real(h_eigenvalues)) < 1e-12);
  assert(norm(sort(imag(h_eigenvalues)) - target_imaginary_spectrum) < 1e-12);
  lie_residual = norm(g * A + A.' * g, "fro");
  J1_residual = norm(J1.' * A * J1 - conj(A), "fro");
  J2_residual = norm(J2.' * A * J2 - conj(A), "fro");
  assert(max([lie_residual, J1_residual, J2_residual]) < 1e-12);

  output_file = fullfile( ...
      table_dir, "fermion_full_pairing_case_6_counterexample.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["scale,exact_fock_weight,closed_form_weight," ...
                "lie_residual,J1_residual,J2_residual\n"]);
  for scale = [0, 0.2, 0.4, 0.6, 0.8, 1]
    exact_weight = trace(expm(scale * h));
    closed_form = 4 * cos(5 * pi * scale / 4) * ...
                      cos(pi * scale / 4);
    assert(abs(exact_weight - closed_form) < 1e-12);
    fprintf(fid, "%.16g,%.16g,%.16g,%.16g,%.16g,%.16g\n", ...
            scale, real(exact_weight), closed_form, lie_residual, ...
            J1_residual, J2_residual);
  endfor
  fclose(fid);

  printf("Case 6 full-pairing exact counterexample:\n");
  printf("  spec(h)=i*pi*{-3/2,-1,1,3/2}.\n");
  printf("  W(s)=4*cos(5*pi*s/4)*cos(pi*s/4), ");
  printf("W(1)=%.15g.\n\n", real(trace(expm(h))));
endfunction


function [chi, fock_dimension] = two_mode_fermion_nambu_operators(I, Z)
  lowering = [0, 1; 0, 0];
  c1 = kron(lowering, I);
  c2 = kron(Z, lowering);
  chi = {c1, c2, c1', c2'};
  fock_dimension = rows(c1);
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


function current = make_case(name, J1, J2, B_basis, expected_signs)
  current.name = name;
  current.J1 = J1;
  current.J2 = J2;
  current.B_basis = B_basis;
  current.expected_signs = expected_signs;
endfunction


function matrix = pauli(label)
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
      error("Unknown Pauli label.");
  endswitch
endfunction


function signs = classify_pair(g, J1, J2)
  dimension = rows(g);
  signs = [
    signed_equal(J1.' * g * J1, g),
    signed_equal(J1 * J1, eye(dimension)),
    signed_equal(J2.' * g * J2, g),
    signed_equal(J2 * J2, eye(dimension)),
    commute_or_anticommute(J1, J2)
  ];
endfunction


function sign = signed_equal(left, right)
  if norm(left - right, "fro") < 1e-12
    sign = 1;
  elseif norm(left + right, "fro") < 1e-12
    sign = -1;
  else
    error("Matrices differ by more than a sign.");
  endif
endfunction


function sign = commute_or_anticommute(J1, J2)
  if norm(J1 * J2 - J2 * J1, "fro") < 1e-12
    sign = 1;
  elseif norm(J1 * J2 + J2 * J1, "fro") < 1e-12
    sign = -1;
  else
    error("Matrices neither commute nor anticommute.");
  endif
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


function A = nambu_generator(B)
  particle_dimension = rows(B);
  A = [B, zeros(particle_dimension); ...
       zeros(particle_dimension), -B.'];
endfunction


function [lie_residual, J1_residual, V_formal_residual, toy_residual] = ...
    validate_basis(g, J1, J2, B_basis)
  lie_residual = 0;
  J1_residual = 0;
  V_formal_residual = 0;
  toy_residual = 0;
  for basis_index = 1:numel(B_basis)
    A = nambu_generator(B_basis{basis_index});
    V = g * A;
    lie_residual = max(lie_residual, norm(g * A + A.' * g, "fro"));
    J1_residual = max(J1_residual, ...
                      norm(J1.' * A * J1 - conj(A), "fro"));
    V_formal_residual = max(V_formal_residual, ...
                            norm(1i * (J2 * V - conj(V) * J2), "fro"));
    toy_residual = max(toy_residual, ...
                       norm(1i * J2 * g * A - ...
                            1i * A' * J2 * g, "fro"));
  endfor
endfunction


function residual = particle_closure_residual(B_basis)
  column_matrix = [];
  for basis_index = 1:numel(B_basis)
    B = B_basis{basis_index};
    column_matrix = [column_matrix, [real(B(:)); imag(B(:))]];
  endfor
  projector = column_matrix * pinv(column_matrix);
  residual = 0;
  for first = 1:numel(B_basis)
    for second = 1:numel(B_basis)
      commutator = B_basis{first} * B_basis{second} - ...
                   B_basis{second} * B_basis{first};
      vector = [real(commutator(:)); imag(commutator(:))];
      residual = max(residual, norm(vector - projector * vector));
    endfor
  endfor
endfunction


function weight = particle_weight(B_slices)
  particle_dimension = rows(B_slices{1});
  product = eye(particle_dimension);
  trace_sum = 0;
  for slice = 1:numel(B_slices)
    B = B_slices{slice};
    product = product * expm(B);
    trace_sum += trace(B);
  endfor
  weight = exp(-trace_sum / 2) * ...
           det(eye(particle_dimension) + product);
endfunction


function scaled = scale_generators(generators, scale)
  scaled = cell(size(generators));
  for generator_index = 1:numel(generators)
    scaled{generator_index} = scale * generators{generator_index};
  endfor
endfunction


function root = bisection_node(generators)
  left = 0;
  right = 1;
  left_value = real(particle_weight(scale_generators(generators, left)));
  right_value = real(particle_weight(scale_generators(generators, right)));
  assert(left_value > 0 && right_value < 0);
  for iteration = 1:100
    middle = (left + right) / 2;
    middle_value = real( ...
        particle_weight(scale_generators(generators, middle)));
    if middle_value > 0
      left = middle;
    else
      right = middle;
    endif
  endfor
  root = (left + right) / 2;
endfunction


function [minimum_weight, maximum_imaginary_part, negative_count, ...
          maximum_unitarity_residual] = random_particle_scan( ...
              B_basis, trial_count, max_slices, scale)
  particle_dimension = rows(B_basis{1});
  minimum_weight = Inf;
  maximum_imaginary_part = 0;
  negative_count = 0;
  maximum_unitarity_residual = 0;
  all_antihermitian = true;
  for basis_index = 1:numel(B_basis)
    B = B_basis{basis_index};
    all_antihermitian &= norm(B + B', "fro") < 1e-12;
  endfor

  for trial = 1:trial_count
    slice_count = 2 + randi(max_slices - 1);
    B_slices = cell(slice_count, 1);
    product = eye(particle_dimension);
    for slice = 1:slice_count
      B = zeros(particle_dimension);
      for basis_index = 1:numel(B_basis)
        B += scale * randn() * B_basis{basis_index};
      endfor
      B_slices{slice} = B;
      product = product * expm(B);
    endfor
    weight = particle_weight(B_slices);
    minimum_weight = min(minimum_weight, real(weight));
    maximum_imaginary_part = max(maximum_imaginary_part, abs(imag(weight)));
    if real(weight) < -1e-8 && abs(imag(weight)) < 1e-7
      negative_count += 1;
    endif
    if all_antihermitian
      maximum_unitarity_residual = max( ...
          maximum_unitarity_residual, ...
          norm(product' * product - eye(particle_dimension), "fro"));
    endif
  endfor
endfunction


function test_case_1(X, Y, Z, table_dir)
  g = X;
  J1 = X;
  J2 = Y;
  signs = classify_pair(g, J1, J2);
  assert(all(signs(:).' == [1, 1, -1, -1, -1]));
  eta = -J2 * g;

  output_file = fullfile(table_dir, "fermion_case_1_counterexample.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["y,weight,lie_residual,J1_residual," ...
                "ToY_max_eigenvalue,ToY_min_eigenvalue," ...
                "true_eta_edge_residual,spectral_radius_expA\n"]);

  y_values = [0.5, pi, 2 * pi];
  for y = y_values
    A = 1i * y * Z;
    B = 1i * y;
    V = g * A;
    Q_toy = 1i * J2 * g * A - 1i * A' * J2 * g;
    Q_V_formal = 1i * (J2 * V - conj(V) * J2);
    Q_eta = eta * A + A' * eta;
    assert(norm(Q_toy - Q_V_formal, "fro") < 1e-12);
    assert(norm(Q_toy + 2 * y * eye(2), "fro") < 1e-12);
    weight = particle_weight({B});
    fprintf(fid, "%.16g,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g\n", ...
            y, real(weight), norm(g * A + A.' * g, "fro"), ...
            norm(J1.' * A * J1 - conj(A), "fro"), ...
            max(eig(Q_toy)), min(eig(Q_toy)), ...
            norm(Q_eta, "fro"), max(abs(eig(expm(A)))));
  endfor
  fclose(fid);

  negative_weight = particle_weight({1i * 2 * pi});
  assert(abs(negative_weight + 2) < 1e-12);
  printf("Case 1 literal-inequality counterexample:\n");
  printf("  g=X, J1=X, J2=Y, A=i*y*Z gives Q_ToY=-2*y*I<0,\n");
  printf("  but e^A stays on the unit circle and W=2*cos(y/2).\n");
  printf("  W(pi)=0 and W(2*pi)=%.15g. The true eta edge residual is zero.\n\n", ...
         negative_weight);
endfunction


function test_case_5(g, X, Y, Z, table_dir)
  I = eye(2);
  J1 = kron(Z, I);
  explicit_B = {
    -2 * X - 2 * Z,
    -2 * X,
    2 * X + Z
  };
  maximum_lie_residual = 0;
  maximum_J1_residual = 0;
  for slice = 1:numel(explicit_B)
    A = nambu_generator(explicit_B{slice});
    maximum_lie_residual = max( ...
        maximum_lie_residual, norm(g * A + A.' * g, "fro"));
    maximum_J1_residual = max( ...
        maximum_J1_residual, norm(J1.' * A * J1 - conj(A), "fro"));
  endfor
  weight = particle_weight(explicit_B);
  assert(maximum_lie_residual < 1e-12);
  assert(maximum_J1_residual < 1e-12);
  assert(real(weight) < -20);

  output_file = fullfile(table_dir, "fermion_case_5_counterexample.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, "case,s1,q1,J1_word,weight,lie_residual,J1_residual\n");
  fprintf(fid, "5,-1,1,ZI,%.16g,%.16g,%.16g\n", ...
          weight, maximum_lie_residual, maximum_J1_residual);
  fclose(fid);
  printf("Case 5 single-J1 condition has the same W=%.15g counterexample.\n\n", ...
         weight);
endfunction


function test_inequality_signs(I, X, Y, Z, table_dir)
  output_file = fullfile(table_dir, "fermion_inequality_sign_diagnostics.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["example,lie_residual,toy_hermiticity_residual," ...
                "V_formal_hermiticity_residual,toy_norm,V_formal_norm," ...
                "plus_norm,max_abs_eigenvalue_expA\n"]);

  % This is the diagnostic suggested in the collaboration message. It is
  % deliberately recorded together with its Lie-algebra residual: iZ is
  % symmetric, so with g=I it is outside so(2,C).
  g = I;
  A = 1i * Z;
  J2 = Y;
  [lie_residual, toy_hermiticity, V_formal_hermiticity, toy_norm, ...
   V_formal_norm, plus_norm, spectral_radius] = ...
      inequality_diagnostics(g, A, J2);
  fprintf(fid, "suggested_iZ,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g\n", ...
          lie_residual, toy_hermiticity, V_formal_hermiticity, ...
          toy_norm, V_formal_norm, plus_norm, spectral_radius);

  % A=Y is a valid skew generator for g=I. The literal fixed-minus
  % expression is not Hermitian, so the matrix inequality is undefined;
  % the formal V expression vanishes, as expected for an orthogonal rotation.
  A = Y;
  [lie_residual, toy_hermiticity, V_formal_hermiticity, toy_norm, ...
   V_formal_norm, plus_norm, spectral_radius] = ...
      inequality_diagnostics(g, A, J2);
  fprintf(fid, "valid_skew_Y,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g\n", ...
          lie_residual, toy_hermiticity, V_formal_hermiticity, ...
          toy_norm, V_formal_norm, plus_norm, spectral_radius);
  fclose(fid);

  printf("Inequality-sign diagnostics:\n");
  printf("  For g=I and valid A=Y, the ToY fixed-minus matrix has ");
  printf("Hermiticity residual %.6g;\n", toy_hermiticity);
  printf("  the formal Wei expression applied to V=gA is Hermitian and zero;\n");
  printf("  this V expression is not by itself a contraction test for e^A.\n\n");
endfunction


function [lie_residual, toy_hermiticity, V_formal_hermiticity, toy_norm, ...
          V_formal_norm, plus_norm, spectral_radius] = ...
    inequality_diagnostics(g, A, J2)
  V = g * A;
  Q_toy = 1i * J2 * g * A - 1i * A' * J2 * g;
  Q_V_formal = 1i * (J2 * V - conj(V) * J2);
  Q_plus = 1i * J2 * g * A + 1i * A' * J2 * g;
  lie_residual = norm(g * A + A.' * g, "fro");
  toy_hermiticity = norm(Q_toy - Q_toy', "fro");
  V_formal_hermiticity = norm(Q_V_formal - Q_V_formal', "fro");
  toy_norm = norm(Q_toy, "fro");
  V_formal_norm = norm(Q_V_formal, "fro");
  plus_norm = norm(Q_plus, "fro");
  spectral_radius = max(abs(eig(expm(A))));
endfunction
