function enumerate_semigroup_classes(output_file)
  more off;
  format long g;

  if nargin < 1
    here = fileparts(mfilename("fullpath"));
    output_file = fullfile(here, "..", "build", ...
                           "semigroup_classes.csv");
  endif
  output_dir = fileparts(output_file);
  if !isempty(output_dir) && !exist(output_dir, "dir")
    mkdir(output_dir);
  endif

  printf("Octave version: %s\n", version());
  printf("Convention: Y = i*sigma_y = [0,1;-1,0]\n");
  printf("Classification: eta is the Hermitian involution induced directly by J2.\n\n");

  fid = fopen(output_file, "w");
  assert(fid >= 0);
  fprintf(fid, ["statistics,class_id,tau,s1,q1,s2,q2,r,min_qubits," ...
                "J1_word,J2_word,delta,metric,kappa,strict_interior," ...
                "status,metric_hermiticity_residual,metric_square_residual," ...
                "witness_lie_residual,witness_reality_residual," ...
                "witness_J2_residual,witness_contraction_residual," ...
                "max_pauli_relation_residual\n"]);

  statistics_names = {"boson", "fermion"};
  for statistics_index = 1:2
    statistics = statistics_names{statistics_index};
    if strcmp(statistics, "boson")
      tau = -1;
    else
      tau = 1;
    endif
    witnesses = find_minimal_witnesses(statistics);
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

      dimension = rows(witness.J1);
      g = canonical_g(statistics, witness.n);
      [eta, metric_name] = contraction_metric( ...
          statistics, g, witness.J2, s2, q2);
      metric_hermiticity_residual = norm(eta - eta', "fro");
      metric_square_residual = norm(eta * eta - eye(dimension), "fro");
      relation_residual = pauli_relation_residuals( ...
          g, witness.J1, witness.J2, signs);

      strict = strict_contraction(statistics, signs);
      witness_lie_residual = NaN;
      witness_reality_residual = NaN;
      witness_J2_residual = NaN;
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
        witness_J2_residual = norm( ...
            witness.J2.' * A0 * witness.J2 + conj(A0), "fro");
        H0 = eta * A0 + A0' * eta;
        witness_contraction_residual = norm(H0 + 2 * eye(dimension), "fro");
        assert(max([witness_lie_residual, witness_reality_residual, ...
                    witness_J2_residual, ...
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
               "%.16g,%.16g,%.16g,%.16g,%.16g,%.16g,%.16g\n"], ...
              statistics, class_label(signs), tau, s1, q1, s2, q2, r, ...
              witness.n, witness.J1_name, witness.J2_name, delta, ...
              metric_name, kappa, strict, status, ...
              metric_hermiticity_residual, metric_square_residual, ...
              witness_lie_residual, witness_reality_residual, ...
              witness_J2_residual, witness_contraction_residual, ...
              relation_residual);
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

  printf("\nWrote %s\n", output_file);
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
