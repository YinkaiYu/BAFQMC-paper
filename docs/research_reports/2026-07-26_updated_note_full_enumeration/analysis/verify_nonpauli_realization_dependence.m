function verify_nonpauli_realization_dependence()
  more off;
  format long g;

  here = fileparts(mfilename("fullpath"));
  output_file = fullfile(here, "..", "tables", ...
                         "nonpauli_realization_dependence.csv");
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["realization,matrix_dimension,tr_J1,tr_J2,tr_J1J2," ...
                "maximal_subgroup_dimension,cone_linear_dimension," ...
                "relation_residual\n"]);

  % This is the fermionic all-plus class in a basis where
  % g = diag(I_4,-I_4).  It is orthogonally equivalent to X tensor I_4.
  g = diag([ones(1, 4), -ones(1, 4)]);
  realizations = {
    "balanced_Pauli_family", ...
      diag([1, 1, -1, -1, 1, 1, -1, -1]), ...
      diag([1, -1, 1, -1, 1, -1, 1, -1]);
    "uneven_but_same_dimensions", ...
      diag([1, 1, 1, 1, 1, 1, -1, -1]), ...
      diag([1, 1, -1, -1, 1, -1, 1, -1]);
    "uneven_different_dimensions", ...
      diag([1, 1, 1, 1, 1, 1, 1, -1]), ...
      diag([1, 1, 1, 1, 1, 1, -1, -1])
  };

  for index = 1:rows(realizations)
    name = realizations{index, 1};
    J1 = realizations{index, 2};
    J2 = realizations{index, 3};
    eta = J2 * g;
    relation_residual = max([
      norm(J1.' * g * J1 - g, "fro"),
      norm(J1 * J1 - eye(8), "fro"),
      norm(J2.' * g * J2 - g, "fro"),
      norm(J2 * J2 - eye(8), "fro"),
      norm(J1 * J2 - J2 * J1, "fro"),
      norm(eta - eta', "fro"),
      norm(eta * eta - eye(8), "fro")
    ]);
    assert(relation_residual < 1e-11);

    maximal_dimension = real_linear_nullity(g, J1, eta, 1);
    cone_dimension = real_linear_nullity(g, J1, eta, -1);
    fprintf(fid, "%s,8,%d,%d,%d,%d,%d,%.16g\n", ...
            name, trace(J1), trace(J2), trace(J1 * J2), ...
            maximal_dimension, cone_dimension, relation_residual);
  endfor
  fclose(fid);

  assert(real_linear_nullity( ...
      g, realizations{1, 2}, realizations{1, 3} * g, 1) == 12);
  assert(real_linear_nullity( ...
      g, realizations{3, 2}, realizations{3, 3} * g, 1) == 21);

  printf("Octave version: %s\n", version());
  printf(["Same all-plus sign class and same dimension: maximal-subgroup " ...
          "dimensions 12 and 21 both occur.\n"]);
  printf("Wrote %s\n", output_file);
endfunction


function nullity = real_linear_nullity(g, J1, eta, metric_sign)
  dimension = rows(g);
  variable_count = 2 * dimension^2;
  constraint_count = 6 * dimension^2;
  linear_map = zeros(constraint_count, variable_count);

  for variable = 1:variable_count
    A = zeros(dimension);
    if variable <= dimension^2
      A(variable) = 1;
    else
      A(variable - dimension^2) = 1i;
    endif
    constraints = {
      g * A + A.' * g,
      J1.' * A * J1 - conj(A),
      eta * A + metric_sign * A' * eta
    };
    column = [];
    for index = 1:numel(constraints)
      matrix = constraints{index};
      column = [column; real(matrix(:)); imag(matrix(:))];
    endfor
    linear_map(:, variable) = column;
  endfor
  nullity = variable_count - rank(linear_map, 1e-10);
endfunction
