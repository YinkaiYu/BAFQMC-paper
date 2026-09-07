function scan_pauli_realizations(output_file)
  more off;
  format long g;

  if nargin < 1
    here = fileparts(mfilename("fullpath"));
    output_file = fullfile(here, "..", "build", ...
                           "pauli_realization_scan.csv");
  endif
  output_dir = fileparts(output_file);
  if !isempty(output_dir) && !exist(output_dir, "dir")
    mkdir(output_dir);
  endif
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,n,matrix_dimension,realization_count," ...
                "maximal_dimensions,cone_linear_dimensions," ...
                "maximal_min_dimension,maximal_max_dimension," ...
                "cone_min_dimension,cone_max_dimension," ...
                "min_maximal_pair,max_maximal_pair," ...
                "min_cone_pair,max_cone_pair,strict_interior," ...
                "worst_A0_lie_residual,worst_A0_reality_residual," ...
                "worst_A0_J2_residual,worst_A0_contraction_residual\n"]);

  statistics_names = {"boson", "fermion"};
  output_rows = 0;
  checked_realizations = 0;
  strict_realizations = 0;

  for statistics_index = 1:numel(statistics_names)
    statistics = statistics_names{statistics_index};
    for n = 1:3
      [names, matrices] = pauli_words(n);
      g = canonical_g(statistics, n);
      dimension = rows(g);
      aggregates = cell(32, 1);

      for first = 1:numel(names)
        J1 = matrices{first};
        for second = 1:numel(names)
          if first == second
            continue;
          endif
          J2 = matrices{second};
          signs = five_relations(g, J1, J2);
          class_index = signs_to_index(signs);
          [eta, ~] = contraction_metric( ...
              statistics, g, J2, signs(3), signs(4));
          [maximal_dimension, cone_dimension] = ...
              structure_dimensions(g, J1, eta, n);
          pair_name = [names{first}, "/", names{second}];
          strict = strict_contraction(statistics, signs);

          if isempty(aggregates{class_index})
            entry.signs = signs;
            entry.count = 0;
            entry.maximal_dimensions = [];
            entry.cone_dimensions = [];
            entry.min_maximal = Inf;
            entry.max_maximal = -Inf;
            entry.min_cone = Inf;
            entry.max_cone = -Inf;
            entry.min_maximal_pair = "";
            entry.max_maximal_pair = "";
            entry.min_cone_pair = "";
            entry.max_cone_pair = "";
            entry.strict = strict;
            entry.worst_lie = 0;
            entry.worst_reality = 0;
            entry.worst_J2 = 0;
            entry.worst_contraction = 0;
          else
            entry = aggregates{class_index};
            assert(entry.strict == strict);
          endif

          entry.count += 1;
          entry.maximal_dimensions(end + 1) = maximal_dimension;
          entry.cone_dimensions(end + 1) = cone_dimension;
          if maximal_dimension < entry.min_maximal
            entry.min_maximal = maximal_dimension;
            entry.min_maximal_pair = pair_name;
          endif
          if maximal_dimension > entry.max_maximal
            entry.max_maximal = maximal_dimension;
            entry.max_maximal_pair = pair_name;
          endif
          if cone_dimension < entry.min_cone
            entry.min_cone = cone_dimension;
            entry.min_cone_pair = pair_name;
          endif
          if cone_dimension > entry.max_cone
            entry.max_cone = cone_dimension;
            entry.max_cone_pair = pair_name;
          endif

          if strict
            A0 = -eta;
            entry.worst_lie = max( ...
                entry.worst_lie, norm(g * A0 + A0.' * g, "fro"));
            entry.worst_reality = max( ...
                entry.worst_reality, ...
                norm(J1.' * A0 * J1 - conj(A0), "fro"));
            entry.worst_J2 = max( ...
                entry.worst_J2, ...
                norm(J2.' * A0 * J2 + conj(A0), "fro"));
            entry.worst_contraction = max( ...
                entry.worst_contraction, ...
                norm(eta * A0 + A0' * eta + 2 * eye(dimension), ...
                     "fro"));
            strict_realizations += 1;
          endif

          aggregates{class_index} = entry;
          checked_realizations += 1;
        endfor
      endfor

      for class_index = 1:32
        if isempty(aggregates{class_index})
          continue;
        endif
        entry = aggregates{class_index};
        maximal_values = unique(entry.maximal_dimensions);
        cone_values = unique(entry.cone_dimensions);
        if entry.strict
          assert(entry.worst_lie < 1e-10);
          assert(entry.worst_reality < 1e-10);
          assert(entry.worst_J2 < 1e-10);
          assert(entry.worst_contraction < 1e-10);
        endif
        fprintf(fid, ...
                ["%s,%s,%d,%d,%d,\"%s\",\"%s\",%d,%d,%d,%d," ...
                 "%s,%s,%s,%s,%d,%.16g,%.16g,%.16g,%.16g\n"], ...
                statistics, class_label(entry.signs), n, dimension, ...
                entry.count, integer_list(maximal_values), ...
                integer_list(cone_values), ...
                entry.min_maximal, entry.max_maximal, ...
                entry.min_cone, entry.max_cone, ...
                entry.min_maximal_pair, entry.max_maximal_pair, ...
                entry.min_cone_pair, entry.max_cone_pair, ...
                entry.strict, entry.worst_lie, entry.worst_reality, ...
                entry.worst_J2, entry.worst_contraction);
        output_rows += 1;
      endfor
    endfor
  endfor
  fclose(fid);

  printf("Octave version: %s\n", version());
  printf("Checked %d distinct ordered Pauli realizations.\n", ...
         checked_realizations);
  printf(["Verified A0=-eta for all %d strict-class realizations " ...
          "encountered.\n"], strict_realizations);
  printf("Wrote %d aggregate rows to %s\n", output_rows, output_file);
endfunction


function [maximal_dimension, cone_dimension] = ...
    structure_dimensions(g, J1, eta, n)
  [~, matrices] = pauli_words(n);
  maximal_dimension = 0;
  cone_dimension = 0;
  for word_index = 1:numel(matrices)
    for phase = [1, 1i]
      A = phase * matrices{word_index};
      if norm(g * A + A.' * g, "fro") > 1e-11
        continue;
      endif
      if norm(J1.' * A * J1 - conj(A), "fro") > 1e-11
        continue;
      endif
      if norm(eta * A + A' * eta, "fro") < 1e-11
        maximal_dimension += 1;
      endif
      if norm(eta * A - A' * eta, "fro") < 1e-11
        cone_dimension += 1;
      endif
    endfor
  endfor
endfunction


function value = integer_list(values)
  pieces = cell(1, numel(values));
  for index = 1:numel(values)
    pieces{index} = sprintf("%d", values(index));
  endfor
  value = strjoin(pieces, ";");
endfunction
