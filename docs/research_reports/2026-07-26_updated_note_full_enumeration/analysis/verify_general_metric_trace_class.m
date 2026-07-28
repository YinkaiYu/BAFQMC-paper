function verify_general_metric_trace_class()
  more off;
  format long g;

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  sx = [0, 1; 1, 0];
  sy_real = [0, -1; 1, 0];
  sz = [1, 0; 0, -1];
  gamma = 0.7;

  % Standard one-mode physical metric.
  g_one = sy_real;
  eta_physical_one = sz;
  A_standard = -gamma * eta_physical_one;
  assert(norm(g_one * A_standard + A_standard.' * g_one, "fro") < 1e-12);
  standard_contraction = ...
      eta_physical_one * A_standard + A_standard' * eta_physical_one;
  assert(max(real(eig(standard_contraction))) < -1e-12);
  standard_trace_norm = exp(-gamma / 2) / (1 - exp(-gamma));

  % A nonmatching metric: strict at matrix level, unitary on physical Fock space.
  eta_quadrature = 1i * g_one;
  A_quadrature = -eta_quadrature;
  assert(norm(g_one * A_quadrature + A_quadrature.' * g_one, "fro") < 1e-12);
  quadrature_contraction = ...
      eta_quadrature * A_quadrature + A_quadrature' * eta_quadrature;
  assert(max(real(eig(quadrature_contraction))) < -1.9);
  assert(norm(g_one * A_quadrature - 1i * eye(2), "fro") < 1e-12);

  % The original displayed Case 8 metric.
  g_case8 = kron(sy_real, eye(2));
  J1_case8 = kron(sy_real, sz);
  J2_case8 = kron(sx, sx);
  eta_case8 = J2_case8 * g_case8;
  A_case8 = -gamma * eta_case8;
  assert(norm(J1_case8.' * g_case8 * J1_case8 - g_case8, "fro") < 1e-12);
  assert(norm(J1_case8 * J1_case8 + eye(4), "fro") < 1e-12);
  assert(norm(J2_case8.' * g_case8 * J2_case8 + g_case8, "fro") < 1e-12);
  assert(norm(J2_case8 * J2_case8 - eye(4), "fro") < 1e-12);
  assert(norm(J1_case8 * J2_case8 - J2_case8 * J1_case8, "fro") < 1e-12);
  assert(norm(g_case8 * A_case8 + A_case8.' * g_case8, "fro") < 1e-12);
  assert(norm(J1_case8.' * A_case8 * J1_case8 - conj(A_case8), "fro") < 1e-12);
  case8_contraction = eta_case8 * A_case8 + A_case8' * eta_case8;
  assert(max(real(eig(case8_contraction))) < -1e-12);

  physical_particle_generator = -gamma * sx;
  case8_quadratic_matrix = g_case8 * A_case8;
  assert(norm(case8_quadratic_matrix(1:2, 3:4) - ...
              physical_particle_generator.', "fro") < 1e-12);
  assert(norm(case8_quadratic_matrix(3:4, 1:2) - ...
              physical_particle_generator, "fro") < 1e-12);
  particle_rates = sort(real(eig(physical_particle_generator)));
  assert(norm(particle_rates - [-gamma; gamma]) < 1e-12);
  cutoff = 20;
  case8_partial_trace = ...
      sum(exp(-gamma * (0:cutoff))) * sum(exp(gamma * (0:cutoff)));
  case8_previous_partial_trace = ...
      sum(exp(-gamma * (0:cutoff - 1))) * ...
      sum(exp(gamma * (0:cutoff - 1)));
  assert(case8_partial_trace > case8_previous_partial_trace);

  % An alternative representative of the same five Case 8 relations.
  J1_physical = kron(eye(2), sy_real);
  J2_physical = kron(sx, eye(2));
  eta_physical = J2_physical * g_case8;
  A_physical = -gamma * eta_physical;
  assert(norm(J1_physical.' * g_case8 * J1_physical - g_case8, "fro") < 1e-12);
  assert(norm(J1_physical * J1_physical + eye(4), "fro") < 1e-12);
  assert(norm(J2_physical.' * g_case8 * J2_physical + g_case8, "fro") < 1e-12);
  assert(norm(J2_physical * J2_physical - eye(4), "fro") < 1e-12);
  assert(norm(J1_physical * J2_physical - J2_physical * J1_physical, "fro") < 1e-12);
  assert(norm(eta_physical - kron(sz, eye(2)), "fro") < 1e-12);
  assert(norm(J1_physical.' * A_physical * J1_physical - ...
              conj(A_physical), "fro") < 1e-12);
  physical_contraction = ...
      eta_physical * A_physical + A_physical' * eta_physical;
  assert(max(real(eig(physical_contraction))) < -1e-12);
  physical_trace_norm = standard_trace_norm^2;

  output_file = fullfile(table_dir, "general_metric_trace_class_checks.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ...
          "scenario,largest_contraction_eigenvalue,trace_class,diagnostic_value\n");
  fprintf(fid, "standard_one_mode,%.16g,yes,%.16g\n", ...
          max(real(eig(standard_contraction))), standard_trace_norm);
  fprintf(fid, "eta_equals_i_g,%.16g,no,Inf\n", ...
          max(real(eig(quadrature_contraction))));
  fprintf(fid, "case8_displayed_metric,%.16g,no,%.16g\n", ...
          max(real(eig(case8_contraction))), case8_partial_trace);
  fprintf(fid, "case8_physical_representative,%.16g,yes,%.16g\n", ...
          max(real(eig(physical_contraction))), physical_trace_norm);
  fclose(fid);

  printf("Octave version: %s\n", version());
  printf("Standard one-mode trace norm: %.16g\n", standard_trace_norm);
  printf("eta=i*g gives a unitary physical Fock operator; trace norm is infinite.\n");
  printf("Case 8 partial bare trace at cutoff %d: %.16g\n", ...
         cutoff, case8_partial_trace);
  printf("Case 8 physical-representative trace norm: %.16g\n", ...
         physical_trace_norm);
  printf("Wrote %s\n", output_file);
endfunction
