function enumerate_updated_note()
  more off;
  format long g;

  here = fileparts(mfilename("fullpath"));
  table_dir = fullfile(here, "..", "tables");
  if !exist(table_dir, "dir")
    mkdir(table_dir);
  endif

  printf("Octave version: %s\n", version());
  printf("Convention: Y = i*sigma_y = [0,1;-1,0]\n");
  printf("Classification: eta is the Hermitian involution induced directly by J2.\n\n");

  full_file = fullfile(table_dir, "full_64_class_enumeration.csv");
  fid = fopen(full_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,tau,s1,q1,s2,q2,r,min_qubits," ...
                "J1_word,J2_word,delta,metric,kappa,strict_interior," ...
                "status,metric_hermiticity_residual,metric_square_residual," ...
                "witness_lie_residual,witness_reality_residual," ...
                "witness_contraction_residual,max_pauli_relation_residual\n"]);

  statistics_names = {"boson", "fermion"};
  all_witnesses = cell(2, 1);
  for statistics_index = 1:2
    statistics = statistics_names{statistics_index};
    if strcmp(statistics, "boson")
      tau = -1;
    else
      tau = 1;
    endif
    witnesses = find_minimal_witnesses(statistics);
    all_witnesses{statistics_index} = witnesses;
    found = 0;
    passed = 0;
    j2g_passed = 0;
    i_j2g_passed = 0;

    for class_index = 1:32
      witness = witnesses{class_index};
      assert(!isempty(witness));
      found += 1;
      signs = witness.signs;
      s1 = signs(1);
      q1 = signs(2);
      s2 = signs(3);
      q2 = signs(4);
      r = signs(5);
      delta = tau * q2 * s2;
      kappa = delta * r * s1;

      if delta == 1
        phase = 1;
        metric_name = "J2g";
      else
        phase = 1i;
        metric_name = "iJ2g";
      endif
      dimension = rows(witness.J1);
      g = canonical_g(statistics, witness.n);
      eta = phase * witness.J2 * g;
      metric_hermiticity_residual = norm(eta - eta', "fro");
      metric_square_residual = norm(eta * eta - eye(dimension), "fro");
      relation_residual = pauli_relation_residuals( ...
          g, witness.J1, witness.J2, signs);

      strict = (q2 == -tau) && (r == -s1 * s2);
      witness_lie_residual = NaN;
      witness_reality_residual = NaN;
      witness_contraction_residual = NaN;
      if strict
        passed += 1;
        if delta == 1
          j2g_passed += 1;
        else
          i_j2g_passed += 1;
        endif
        status = "strict";
        A0 = -eta;
        witness_lie_residual = norm(g * A0 + A0.' * g, "fro");
        witness_reality_residual = norm( ...
            witness.J1.' * A0 * witness.J1 - conj(A0), "fro");
        H0 = eta * A0 + A0' * eta;
        witness_contraction_residual = norm(H0 + 2 * eye(dimension), "fro");
        assert(max([witness_lie_residual, witness_reality_residual, ...
                    witness_contraction_residual]) < 1e-11);
      elseif q2 != -tau
        status = "boundary_only_trace_obstruction";
      else
        status = "boundary_only_reality_flip";
      endif

      assert(metric_hermiticity_residual < 1e-11);
      assert(metric_square_residual < 1e-11);
      assert(relation_residual < 1e-11);
      fprintf(fid, ...
              ["%s,%s,%d,%d,%d,%d,%d,%d,%d,%s,%s,%d,%s,%d,%d,%s," ...
               "%.16g,%.16g,%.16g,%.16g,%.16g,%.16g\n"], ...
              statistics, class_label(signs), tau, s1, q1, s2, q2, r, ...
              witness.n, witness.J1_name, witness.J2_name, delta, ...
              metric_name, kappa, strict, status, ...
              metric_hermiticity_residual, metric_square_residual, ...
              witness_lie_residual, witness_reality_residual, ...
              witness_contraction_residual, relation_residual);
    endfor
    assert(found == 32);
    assert(passed == 8);
    assert(j2g_passed == 4);
    assert(i_j2g_passed == 4);
    printf("%s: 32/32 classes have Pauli witnesses; ", statistics);
    printf("8 have a strict canonical contraction interior ", statistics);
    printf("(4 J2g and 4 iJ2g).\n");
  endfor
  fclose(fid);

  comparison_file = fullfile(table_dir, "updated_note_hand_comparison.csv");
  write_hand_comparison(comparison_file);

  comment_file = fullfile(table_dir, "comment_pair_checks.csv");
  write_comment_pair_checks(comment_file);

  printf("\nWrote %s\n", full_file);
  printf("Wrote %s\n", comparison_file);
  printf("Wrote %s\n", comment_file);
endfunction


function witnesses = find_minimal_witnesses(statistics)
  witnesses = cell(32, 1);
  for n = 1:3
    [names, matrices] = pauli_words(n);
    g = canonical_g(statistics, n);
    dimension = rows(g);
    for first = 1:numel(names)
      J1 = matrices{first};
      for second = 1:numel(names)
        if first == second
          continue;
        endif
        J2 = matrices{second};
        signs = [
          matrix_sign(J1.' * g * J1, g),
          matrix_sign(J1 * J1, eye(dimension)),
          matrix_sign(J2.' * g * J2, g),
          matrix_sign(J2 * J2, eye(dimension)),
          commutation_sign(J1, J2)
        ];
        class_index = signs_to_index(signs);
        if isempty(witnesses{class_index})
          witness.n = n;
          witness.signs = signs;
          witness.J1_name = names{first};
          witness.J2_name = names{second};
          witness.J1 = J1;
          witness.J2 = J2;
          witnesses{class_index} = witness;
        endif
      endfor
    endfor
  endfor
endfunction


function g = canonical_g(statistics, n)
  if strcmp(statistics, "boson")
    g = kron(-pauli_matrix("Y"), eye(2^(n - 1)));
  elseif strcmp(statistics, "fermion")
    g = kron(pauli_matrix("X"), eye(2^(n - 1)));
  else
    error("Unknown statistics: %s", statistics);
  endif
endfunction


function [names, matrices] = pauli_words(n)
  labels = "IXYZ";
  word_count = 4^n;
  names = cell(word_count, 1);
  matrices = cell(word_count, 1);
  for value = 0:(word_count - 1)
    digits = dec2base(value, 4, n) - "0";
    name = "";
    matrix = 1;
    for position = 1:n
      label = labels(digits(position) + 1);
      name = [name, label];
      matrix = kron(matrix, pauli_matrix(label));
    endfor
    names{value + 1} = name;
    matrices{value + 1} = matrix;
  endfor
endfunction


function matrix = pauli_matrix(label)
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
      error("Unknown Pauli label: %s", label);
  endswitch
endfunction


function sign = matrix_sign(left, right)
  tolerance = 1e-12;
  if norm(left - right, "fro") < tolerance
    sign = 1;
  elseif norm(left + right, "fro") < tolerance
    sign = -1;
  else
    error("Matrices are not related by a sign.");
  endif
endfunction


function sign = commutation_sign(J1, J2)
  tolerance = 1e-12;
  if norm(J1 * J2 - J2 * J1, "fro") < tolerance
    sign = 1;
  elseif norm(J1 * J2 + J2 * J1, "fro") < tolerance
    sign = -1;
  else
    error("Pauli words neither commute nor anticommute.");
  endif
endfunction


function residual = pauli_relation_residuals(g, J1, J2, signs)
  dimension = rows(g);
  residual = max([
    norm(J1.' * g * J1 - signs(1) * g, "fro"),
    norm(J1 * J1 - signs(2) * eye(dimension), "fro"),
    norm(J2.' * g * J2 - signs(3) * g, "fro"),
    norm(J2 * J2 - signs(4) * eye(dimension), "fro"),
    norm(J1 * J2 - signs(5) * J2 * J1, "fro")
  ]);
endfunction


function index = signs_to_index(signs)
  bits = (signs == -1);
  index = 1 + bits(:).' * [16; 8; 4; 2; 1];
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


function write_hand_comparison(output_file)
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,note_case,s1,q1,s2,q2,r,note_label," ...
                "canonical_strict,comparison_comment\n"]);

  boson_rows = {
    "3",   1,  1, -1,  1, -1, "Failed";
    "4",   1, -1, -1,  1, -1, "Failed";
    "5",  -1,  1, -1,  1, -1, "Passed";
    "6",  -1, -1, -1,  1, -1, "Passed";
    "7",   1,  1, -1,  1,  1, "Passed";
    "8",   1, -1, -1,  1,  1, "Passed";
    "9",  -1,  1, -1,  1,  1, "Failed";
    "10", -1, -1, -1,  1,  1, "Failed";
    "11",  1,  1,  1, -1, -1, "Failed";
    "12",  1, -1,  1, -1, -1, "Failed";
    "13", -1,  1,  1, -1, -1, "Failed";
    "14", -1, -1,  1, -1, -1, "Failed";
    "15",  1,  1,  1, -1,  1, "Failed";
    "16", -1,  1,  1, -1,  1, "Failed"
  };
  for index = 1:rows(boson_rows)
    signs = cell2mat(boson_rows(index, 2:6));
    strict = canonical_strict(-1, signs);
    note_label = boson_rows{index, 7};
    if strict == strcmp(note_label, "Passed")
      comment = "agrees";
    else
      comment = "disagrees";
    endif
    fprintf(fid, "boson,%s,%d,%d,%d,%d,%d,%s,%d,%s\n", ...
            boson_rows{index, 1}, signs, note_label, strict, comment);
  endfor

  fermion_rows = {
    "3prime",   1,  1, -1, -1, -1, "Passed";
    "4prime",   1, -1, -1, -1, -1, "Passed";
    "5prime",  -1,  1, -1, -1, -1, "Passed";
    "6prime",  -1, -1, -1, -1, -1, "Passed";
    "7prime",   1,  1, -1, -1,  1, "Passed";
    "8prime",   1, -1, -1, -1,  1, "Passed";
    "9prime",  -1,  1, -1, -1,  1, "Passed";
    "10prime", -1, -1, -1, -1,  1, "Failed"
  };
  for index = 1:rows(fermion_rows)
    signs = cell2mat(fermion_rows(index, 2:6));
    strict = canonical_strict(1, signs);
    note_label = fermion_rows{index, 7};
    if strict == strcmp(note_label, "Passed")
      comment = "same_label_different_fermion_inequality";
    else
      comment = "not_same_predicate_note_uses_iJ2gA_minus_iAdJ2g";
    endif
    fprintf(fid, "fermion,%s,%d,%d,%d,%d,%d,%s,%d,%s\n", ...
            fermion_rows{index, 1}, signs, note_label, strict, comment);
  endfor
  fclose(fid);
endfunction


function strict = canonical_strict(tau, signs)
  s1 = signs(1);
  s2 = signs(3);
  q2 = signs(4);
  r = signs(5);
  strict = (q2 == -tau) && (r == -s1 * s2);
endfunction


function write_comment_pair_checks(output_file)
  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,note_pair,s1,q1,s2,q2,r," ...
                "canonical_strict,kappa,meaning\n"]);

  rows_to_check = {
    "fermion", "1tripleprime",  1,  1, -1, -1, -1;
    "fermion", "5tripleprime",  1,  1, -1, -1,  1;
    "fermion", "2tripleprime",  1, -1, -1, -1, -1;
    "fermion", "6tripleprime",  1, -1, -1, -1,  1;
    "fermion", "3tripleprime", -1,  1, -1, -1, -1;
    "fermion", "7tripleprime", -1,  1, -1, -1,  1
  };
  for index = 1:rows(rows_to_check)
    statistics = rows_to_check{index, 1};
    if strcmp(statistics, "boson")
      tau = -1;
    else
      tau = 1;
    endif
    signs = cell2mat(rows_to_check(index, 3:7));
    delta = tau * signs(4) * signs(3);
    kappa = delta * signs(5) * signs(1);
    strict = canonical_strict(tau, signs);
    if strict
      meaning = "compatible_strict_interior";
    else
      meaning = "reality_maps_negative_cone_to_positive_cone";
    endif
    fprintf(fid, "%s,%s,%d,%d,%d,%d,%d,%d,%d,%s\n", ...
            statistics, rows_to_check{index, 2}, signs, strict, ...
            kappa, meaning);
  endfor
  fclose(fid);
endfunction
