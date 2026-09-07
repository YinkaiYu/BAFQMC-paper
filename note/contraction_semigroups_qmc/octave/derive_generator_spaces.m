function derive_generator_spaces(output_file)
  more off;
  format long g;

  if nargin < 1
    here = fileparts(mfilename("fullpath"));
    output_file = fullfile(here, "..", "build", ...
                           "generator_spaces.csv");
  endif
  output_dir = fileparts(output_file);
  if !isempty(output_dir) && !exist(output_dir, "dir")
    mkdir(output_dir);
  endif
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,n,J1_word,J2_word,metric," ...
                "s1,q1,s2,q2,r,strict_interior," ...
                "maximal_terms,cone_linear_terms," ...
                "maximal_number_conserving_terms," ...
                "cone_number_conserving_terms," ...
                "maximal_dimension_formula,cone_dimension_formula," ...
                "maximal_residual,cone_residual\n"]);

  statistics_names = {"boson", "fermion"};
  row_count = 0;
  for statistics_index = 1:numel(statistics_names)
    statistics = statistics_names{statistics_index};
    witnesses = find_minimal_witnesses(statistics);
    for class_index = 1:32
      witness = witnesses{class_index};
      n = witness.n;
      g = canonical_g(statistics, n);
      [eta, metric_name] = contraction_metric( ...
          statistics, g, witness.J2, ...
          witness.signs(3), witness.signs(4));
      [names, matrices] = pauli_words(n);

      maximal_terms = {};
      cone_terms = {};
      maximal_number_terms = {};
      cone_number_terms = {};
      maximal_dimension_terms = {};
      cone_dimension_terms = {};
      maximal_residual = 0;
      cone_residual = 0;

      for index = 1:numel(names)
        P = matrices{index};
        transpose_sign = matrix_sign(P.' * g, g * P);
        J1_sign = matrix_sign(witness.J1.' * P * witness.J1, P);
        J2_sign = matrix_sign(witness.J2.' * P * witness.J2, P);
        coefficient_type = matrix_coefficient_type( ...
            transpose_sign, J1_sign);
        term = sprintf("%s:%s", names{index}, coefficient_type);
        dimension_term = coefficient_dimension_term(coefficient_type);
        number_conserving = names{index}(1) == "I" || ...
                            names{index}(1) == "Z";

        test_matrix = test_coefficient_matrix(coefficient_type);
        test_A = kron(P, test_matrix);
        test_g = kron(g, eye(rows(test_matrix)));
        test_J1 = kron(witness.J1, eye(rows(test_matrix)));
        test_J2 = kron(witness.J2, eye(rows(test_matrix)));
        test_eta = kron(eta, eye(rows(test_matrix)));

        if J2_sign == J1_sign
          maximal_terms{end + 1} = term;
          maximal_dimension_terms{end + 1} = dimension_term;
          if number_conserving
            maximal_number_terms{end + 1} = term;
          endif
          maximal_residual = max(maximal_residual, max([
            norm(test_g * test_A + test_A.' * test_g, "fro"),
            norm(test_J1.' * test_A * test_J1 - conj(test_A), "fro"),
            norm(test_J2.' * test_A * test_J2 - conj(test_A), "fro"),
            norm(test_eta * test_A + test_A' * test_eta, "fro")
          ]));
        else
          cone_terms{end + 1} = term;
          cone_dimension_terms{end + 1} = dimension_term;
          if number_conserving
            cone_number_terms{end + 1} = term;
          endif
          cone_residual = max(cone_residual, max([
            norm(test_g * test_A + test_A.' * test_g, "fro"),
            norm(test_J1.' * test_A * test_J1 - conj(test_A), "fro"),
            norm(test_J2.' * test_A * test_J2 + conj(test_A), "fro"),
            norm(test_eta * test_A - test_A' * test_eta, "fro")
          ]));
        endif
      endfor

      assert(maximal_residual < 1e-10);
      assert(cone_residual < 1e-10);
      strict = strict_contraction(statistics, witness.signs);
      fprintf(fid, ...
              ["%s,%s,%d,%s,%s,%s,%d,%d,%d,%d,%d,%d," ...
               "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"," ...
               "%.16g,%.16g\n"], ...
              statistics, class_label(witness.signs), n, ...
              witness.J1_name, witness.J2_name, metric_name, ...
              witness.signs, strict, ...
              strjoin(maximal_terms, ";"), strjoin(cone_terms, ";"), ...
              strjoin(maximal_number_terms, ";"), ...
              strjoin(cone_number_terms, ";"), ...
              join_dimension_formula(maximal_dimension_terms), ...
              join_dimension_formula(cone_dimension_terms), ...
              maximal_residual, cone_residual);
      row_count += 1;
    endfor
  endfor
  fclose(fid);

  assert(row_count == 64);
  printf("Octave version: %s\n", version());
  printf("Verified tensor-block formulas for %d classes.\n", row_count);
  printf("Wrote %s\n", output_file);
endfunction


function coefficient_type = matrix_coefficient_type( ...
    transpose_sign, reality_sign)
  if transpose_sign == 1
    transpose_label = "A";
  else
    transpose_label = "S";
  endif
  if reality_sign == 1
    coefficient_type = ["R_", transpose_label];
  else
    coefficient_type = ["iR_", transpose_label];
  endif
endfunction


function dimension_term = coefficient_dimension_term(coefficient_type)
  if endsWith(coefficient_type, "_S")
    dimension_term = "m(m+1)/2";
  else
    dimension_term = "m(m-1)/2";
  endif
endfunction


function formula = join_dimension_formula(terms)
  symmetric_count = sum(strcmp(terms, "m(m+1)/2"));
  antisymmetric_count = sum(strcmp(terms, "m(m-1)/2"));
  pieces = {};
  if symmetric_count > 0
    pieces{end + 1} = sprintf("%d*m*(m+1)/2", symmetric_count);
  endif
  if antisymmetric_count > 0
    pieces{end + 1} = sprintf("%d*m*(m-1)/2", antisymmetric_count);
  endif
  if isempty(pieces)
    formula = "0";
  else
    formula = strjoin(pieces, "+");
  endif
endfunction


function matrix = test_coefficient_matrix(coefficient_type)
  symmetric = [1, 2; 2, -1];
  antisymmetric = [0, 1; -1, 0];
  if endsWith(coefficient_type, "_S")
    matrix = symmetric;
  else
    matrix = antisymmetric;
  endif
  if startsWith(coefficient_type, "i")
    matrix *= 1i;
  endif
endfunction
