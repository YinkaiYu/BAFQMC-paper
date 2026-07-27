function verify_low_rank_branch_update()
  more off;
  format long g;

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  mode_count = 4;
  dimension = 2 * mode_count;
  damping = 1.25;
  pairing = 0.19;
  turns_to_test = 0:2;

  zero = zeros(mode_count);
  exchange = zeros(mode_count);
  exchange(1, 2) = 1;
  exchange(2, 1) = 1;
  damping_generator = [
    -damping * eye(mode_count), zero;
    zero, damping * eye(mode_count)
  ];
  pairing_generator = [
    zero, pairing * exchange;
    pairing * exchange, zero
  ];
  old_matrix = expm(damping_generator) * expm(pairing_generator);

  local_indices = [1, mode_count + 1];
  embedding = zeros(dimension, 2);
  embedding(local_indices(1), 1) = 1;
  embedding(local_indices(2), 2) = 1;
  left_factor = old_matrix;
  old_right_factor = eye(dimension);

  output_file = fullfile(table_dir, "low_rank_branch_update_check.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["rotation_turns,local_dimension,continuous_phase_over_2pi," ...
                "weight_ratio_real,weight_ratio_imag," ...
                "endpoint_determinant_ratio_real," ...
                "endpoint_determinant_ratio_imag," ...
                "minimum_reduced_determinant," ...
                "minimum_reduced_singular_value,green_update_residual," ...
                "determinant_lemma_residual,integration_error\n"]);

  for turns = turns_to_test
    angle = 2 * pi * turns;
    local_generator = diag([-1i * angle, 1i * angle]);
    local_ratio = @(t) expm(t * local_generator);
    local_ratio_derivative = @(t) ...
        local_generator * expm(t * local_generator);

    [weight_ratio, new_matrix, new_green, diagnostics] = ...
        boson_branch_low_rank_update( ...
            old_matrix, left_factor, old_right_factor, embedding, ...
            local_ratio, local_ratio_derivative, 0);

    expected_ratio = (-1)^turns;
    assert(abs(weight_ratio - expected_ratio) < 1e-9);
    assert(norm(new_matrix - old_matrix, "fro") < 1e-10);
    assert(norm(new_green - ...
                ((eye(dimension) - new_matrix) \ eye(dimension)), ...
                "fro") < 1e-9);
    assert(diagnostics.minimum_reduced_determinant > 0.5);
    assert(diagnostics.minimum_reduced_singular_value > 0.5);
    assert(diagnostics.green_update_residual < 1e-10);
    assert(diagnostics.determinant_lemma_residual < 1e-10);

    continuous_phase = ...
        imag(diagnostics.continuous_log_determinant_ratio) / (2 * pi);
    printf("turns=%d, ratio=%+.12g%+.12gi, determinant winding=%+.12g\n", ...
           turns, real(weight_ratio), imag(weight_ratio), continuous_phase);
    assert(abs(continuous_phase - turns) < 1e-8);

    fprintf(fid, ...
            ["%d,%d,%.16g,%.16g,%.16g,%.16g,%.16g," ...
             "%.16g,%.16g,%.16g,%.16g,%.16g\n"], ...
            turns, 2, continuous_phase, ...
            real(weight_ratio), imag(weight_ratio), ...
            real(diagnostics.endpoint_determinant_ratio), ...
            imag(diagnostics.endpoint_determinant_ratio), ...
            diagnostics.minimum_reduced_determinant, ...
            diagnostics.minimum_reduced_singular_value, ...
            diagnostics.green_update_residual, ...
            diagnostics.determinant_lemma_residual, ...
            diagnostics.integration_error);
  endfor

  fclose(fid);
  printf("Octave version: %s\n", version());
  printf("Verified branch-resolved rank-2 updates for 0, 2pi, and 4pi rotations.\n");
  printf("Wrote %s\n", output_file);
endfunction
