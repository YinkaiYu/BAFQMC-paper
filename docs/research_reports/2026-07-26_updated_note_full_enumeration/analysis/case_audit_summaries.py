"""Local correctness summaries appended to the note walkthrough."""

from __future__ import annotations


CASE_AUDITS: dict[str, str] = {
    "boson-contraction-list": r"""
      <div class="note">
        <strong>这一总表逐项核对后的结论。</strong>
        对本报告为 \(J_2g\) 四类选取的具体矩阵实现，
        \(\eta=J_2g\) 直接等于标准 physical particle/hole metric
        \(\operatorname{diag}(I,-I)\)。因此 physical metaplectic
        representation 对相应 symplectic Olshanski semigroup 的延拓
        可以使用 Howe、Hilgert 与 Neeb 的已有结果。
        “存在负定生成元”不只是在说某个矩阵例子。若每个时间片传播矩阵
        \(M_\ell\) 都满足
        \(M_\ell^\dagger\eta M_\ell-\eta\le0\)，而且每个完整构型中
        至少有一个时间片满足严格不等式，那么完整传播矩阵满足
        \(M^\dagger\eta M-\eta<0\)。由于这里的 \(\eta\) 正是标准物理
        particle/hole metric，且 metaplectic extension 适用，此时
        bosonic Fock operator 是 trace class，也就是
        \(\operatorname{Tr}\sqrt{\hat U^\dagger\hat U}<\infty\)，
        对所有玻色高占据态的贡献取绝对值后求和仍收敛；\(+1\) pole
        也被排除。\(J_1\) 使完整权重为实后，
        连通 Gaussian field space 与正的零场 trace 把全部构型固定在
        同一个正号上。因此，对报告已经明确构造且满足上述逐时间片条件的
        HS 模型，结论是完整的“无符号且无极点”。
        <div class="scroll">
          <table>
            <thead><tr><th>case</th><th>核对结果</th><th>对原标签的判断</th></tr></thead>
            <tbody>
              <tr><td>3</td><td>\(J_1^T\overline{(\eta A+A^\dagger\eta)}J_1=-(\eta A+A^\dagger\eta)\)，故半负定只能为零</td><td>Failed 正确</td></tr>
              <tr><td>4</td><td>\(J_1^T\overline{(\eta A+A^\dagger\eta)}J_1=-(\eta A+A^\dagger\eta)\)，故半负定只能为零</td><td>Failed 正确</td></tr>
              <tr><td>5</td><td>允许的 \(A\) 中有 \(\eta A+A^\dagger\eta<0\) 的解</td><td>报告构造的 HS 模型逐构型无符号、无 pole；note 未在后文手算</td></tr>
              <tr><td>6</td><td>允许的 \(A\) 中有 \(\eta A+A^\dagger\eta<0\) 的解</td><td>报告构造的 HS 模型逐构型无符号、无 pole；note 未在后文手算</td></tr>
              <tr><td>7</td><td>允许的 \(A\) 中有 \(\eta A+A^\dagger\eta<0\) 的解</td><td>报告构造的 HS 模型逐构型无符号、无 pole</td></tr>
              <tr><td>8</td><td>允许的 \(A\) 中有 \(\eta A+A^\dagger\eta<0\) 的解</td><td>报告构造的 HS 模型逐构型无符号、无 pole</td></tr>
              <tr><td>9</td><td>\(J_1^T\overline{(\eta A+A^\dagger\eta)}J_1=-(\eta A+A^\dagger\eta)\)，故半负定只能为零</td><td>Failed 正确</td></tr>
              <tr><td>10</td><td>\(J_1^T\overline{(\eta A+A^\dagger\eta)}J_1=-(\eta A+A^\dagger\eta)\)，故半负定只能为零</td><td>Failed 正确</td></tr>
              <tr><td>11</td><td>\(\Tr(\eta A+A^\dagger\eta)=0\)，故半负定只能为零</td><td>Failed 正确</td></tr>
              <tr><td>12</td><td>\(\Tr(\eta A+A^\dagger\eta)=0\)，故半负定只能为零</td><td>Failed 正确</td></tr>
              <tr><td>13</td><td>\(\Tr(\eta A+A^\dagger\eta)=0\)，故半负定只能为零</td><td>Failed 正确</td></tr>
              <tr><td>14</td><td>\(\Tr(\eta A+A^\dagger\eta)=0\)，故半负定只能为零</td><td>Failed 正确</td></tr>
              <tr><td>15</td><td>\(\Tr(\eta A+A^\dagger\eta)=0\)，故半负定只能为零</td><td>Failed 正确</td></tr>
              <tr><td>16</td><td>\(\Tr(\eta A+A^\dagger\eta)=0\)，故半负定只能为零</td><td>Failed 正确</td></tr>
            </tbody>
          </table>
        </div>
        因此第一节保留 Cases 5--8，并证明其余收缩类别中不存在负定生成元；
        这一生成元分类正确。原文把 Case 5 的编号写进数学模式
        <code>$5)</code>，只是排版不一致，不影响五条关系。
      </div>
    """,
    "boson-passed-list": r"""
      <div class="note">
        <strong>passed-only 清单的核对结论。</strong>
        该清单的六项计数与更新后的第一节一致，但它混合了三种不同证据：
        TRS、operator-level reflection positivity，以及 Cases 5--8
        中允许负定生成元的四个 contraction classes。因而“六项通过”
        不能解读成由同一个半群不等式证明的六个类别。
      </div>
    """,
    "fermion-list": r"""
      <div class="note">
        <strong>费米总表逐项核对后的结论。</strong>
        原文先说 “7 examined cases”，随后实际列出 \(1'\)--\(10'\)；
        这里的 7 只能理解为作者随后认为“独立且通过”的数目，不是候选
        case 数。这是一处文字计数不清，不是矩阵计算。
        <div class="scroll">
          <table>
            <thead><tr><th>case</th><th>按直接控制 \(e^A\) 的检查</th><th>对原说明的判断</th></tr></thead>
            <tbody>
              <tr><td>\(1'\)</td><td>交换两个 \(J\) 的职责后，落在 \(9'\) 的等号部分</td><td>“special case”在线性约束层面正确；非负权重仍未证明</td></tr>
              <tr><td>\(2'\)</td><td>没有给矩阵或不等式，无法穷举</td><td>“exists but not useful”证据不足</td></tr>
              <tr><td>\(3'\)</td><td>\(J_2gA+A^\dagger J_2g\leq0\) 只能取等号</td><td>名称来自 Majorana RP；当前 Nambu 条件未完成该定理的换基</td></tr>
              <tr><td>\(4'\)</td><td>同样只能取等号</td><td>名称来自 time-reversal positivity；当前 Nambu 条件未完成该定理的换基</td></tr>
              <tr><td>\(5'\)</td><td>存在负定生成元</td><td>按修正后的 \(e^A\) contraction，完整 semigroup sign-free</td></tr>
              <tr><td>\(6'\)</td><td>存在负定生成元</td><td>按修正后的 \(e^A\) contraction，完整 semigroup sign-free</td></tr>
              <tr><td>\(7'\)</td><td>存在负定生成元</td><td>按修正后的 \(e^A\) contraction，完整 semigroup sign-free</td></tr>
              <tr><td>\(8'\)</td><td>存在负定生成元</td><td>按修正后的 \(e^A\) contraction，完整 semigroup sign-free</td></tr>
              <tr><td>\(9'\)</td><td>半负定只能取等号，并有负权重反例</td><td>Passed 错误</td></tr>
              <tr><td>\(10'\)</td><td>半负定只能取等号</td><td>无负定生成元这一判断正确；不能据此断言所有模型都有 sign problem</td></tr>
            </tbody>
          </table>
        </div>
        第一节写的
        \(iJ_2gA-iA^\dagger J_2g\leq0\) 与顶部的 \(e^A\) trace
        formula 不对齐。后面的手算表明作者实际想用的是
        \(\eta=J_2g\) 和
        \(J_2gA+A^\dagger J_2g\leq0\)：Case \(5'\) 左右都这样写，
        Cases \(6'\)--\(10'\) 的右侧也都实际乘了 \(J_2g\)，只是左侧
        标签多了 \(i\)。这不是 Wei 的 Majorana 论文出错，而是本 note
        在 Majorana 与 Nambu conventions 之间少做了一次完整换基。
        对修正后的 Cases \(5'\)--\(8'\)，费米 Fock space 有限。
        对满足 \(M^\dagger\eta M-\eta<0\) 的传播矩阵，\(-1\)
        不是本征值，所以权重不为零；\(J_1\) 使权重为实，连续性和
        一个已知正的参考传播矩阵固定其正号。对只满足
        \(M^\dagger\eta M-\eta\le0\) 的传播矩阵，乘
        \(e^{\epsilon A_0}\) 后得到严格收缩矩阵，再令
        \(\epsilon\to0^+\)，权重得到非负极限。因此这里可以直接使用
        Wei 的 semigroup continuity argument，结论是完整 sign-free
        semigroup。
      </div>
    """,
    "fermion-passed-comment": r"""
      <div class="result">
        <strong>第一节 Comment 的明确答案。</strong>
        commutator/anti-commutator 确实影响结论。本组取
        \(\eta=J_2g\)。当
        \(J_1^T\bar\eta J_1=+\eta\) 时，
        \[
        J_1^T\overline{(\eta A+A^\dagger\eta)}J_1
        =\eta A+A^\dagger\eta,
        \]
        半负定条件与 \(J_1\) 相容；Cases \(5'\)--\(8'\) 的穷举
        进一步找到负定生成元。当
        \(J_1^T\bar\eta J_1=-\eta\) 时，
        \[
        J_1^T\overline{(\eta A+A^\dagger\eta)}J_1
        =-(\eta A+A^\dagger\eta).
        \]
        若原矩阵半负定，左边也半负定，所以上式又推出原矩阵半正定；
        二者合起来只能有
        \(\eta A+A^\dagger\eta=0\)。这发生在 Cases
        \(3',4',9',10'\)。原文写的 “\(3'\) 与 \(7'''\)”
        还同时改变了 \(J_1^TgJ_1\) 的符号；若作者本意是只比较
        对易关系，较可能应写 “\(3'''\) 与 \(7'''\)”。
      </div>
    """,
    "boson-case7": r"""
      <div class="result">
        <strong>Case 7 核对结论：正确。</strong>
        原文给出的 \(J_1,J_2\) 满足标题中的五条关系；
        \(\eta=J_2g\) 是 Hermitian involution；允许的生成元中存在
        \(\eta A+A^\dagger\eta<0\) 的解。这里没有发现影响计算的局部
        typo。
        对报告中对应的 relative-density HS model，固定 number-damping
        factor 严格收缩，而任意正负的 Gaussian HS field factor 都满足
        等号。若 \(M_1\) 严格、\(M_2\) 半收缩，则
        \[
        (M_1M_2)^\dagger\eta(M_1M_2)-\eta
        =M_2^\dagger(M_1^\dagger\eta M_1-\eta)M_2
        +(M_2^\dagger\eta M_2-\eta)<0 .
        \]
        所以任意时空场构型的完整乘积都严格收缩。这里直接有
        \(J_2g=\operatorname{diag}(I,-I)\)，完整传播位于标准
        symplectic Olshanski semigroup 的严格内部；已有 metaplectic
        extension 与 interior trace-class theorem 因而适用。
        对应 Fock operator 是 trace class，并且 \(M\) 没有
        \(+1\) eigenvalue。零场权重为
        \(\prod_j(1-e^{-\beta\epsilon_j})^{-1}>0\)；\(J_1\) 使权重为实，
        连通的实 Gaussian field space 又不允许它在没有 zero/pole 时换号。
        因此该 explicit HS model 的最终结论就是
        <strong>bare trace 对所有构型收敛、权重恒正、没有 determinant
        pole</strong>。
      </div>
    """,
    "boson-case8-j1": r"""
      <div class="result">
        <strong>Case 8 第一部分核对结论：正确。</strong>
        显示的 \(J_1,J_2\) 实现了五条离散关系；逐块比较
        \(J_1^TAJ_1=\bar A\) 得到的线性条件与直接矩阵乘法一致。
        本段没有发现需要改动数学结果的 typo。
      </div>
    """,
    "boson-case8-j2": r"""
      <div class="result">
        <strong>Case 8 第二部分核对结论：生成元分类正确；note 原式采用的
        度规与本报告物理模型采用的另一组矩阵实现必须分开。</strong>
        maximal-subgroup 等号部分和 invariant-cone 线性部分的分工正确；
        穷举确认允许的生成元中存在负定解，例如正文给出的
        \(A=-\gamma\,\sigma_z\otimes\sigma_x\)。原文最后的 “Good”
        因而正确表示“受 \(J_1,J_2\) 约束的生成元空间确实进入了
        \(J_2g\)-contraction semigroup 的内部”。
        但对 note 原式采用的
        \(J_2g=\sigma_z\otimes\sigma_x\)，这个最简单的负定解对应
        \[
          \frac12\chi^TgA\chi
          =-\gamma\,\boldsymbol a^{+T}\sigma_x\boldsymbol a .
        \]
        \(\sigma_x\) 的两个 eigenvalues 为 \(+1,-1\)，所以一个
        occupation-number 几何级数含 \(e^{+\gamma n}\) 并发散。
        因此 “Good” 本身还不是对 note 原式度规的
        grand-canonical trace-class 证明。
        <br><br>
        报告给出的双组分 relative-density HS model 使用同一离散 Case
        的另一组矩阵实现，并含固定的严格粒子数衰减项；
        场因子位于 maximal subgroup。利用 Case 7 核对框中逐项写出的
        乘积恒等式，任意多时间片的完整 \(M\) 都严格收缩。
        这里用于物理模型的是穷举表中的另一组矩阵实现，
        它直接满足
        \(\eta=J_2g=\operatorname{diag}(I,-I)\)；不需要假定 note
        显示的任意 \(J_2g\) 都能由 physical mode transformation
        化成标准形式。标准 metaplectic extension 给出 trace-class
        Fock operator，并排除 \(+1\) pole。权重由 \(J_1\)
        保证为实，并由连通场域和正零场 trace 固定为正。
        因此本报告的 explicit Case 8 HS path 同样是
        <strong>无符号、无极点且 bare trace 收敛</strong>。
      </div>
    """,
    "boson-case3-j1": r"""
      <div class="note">
        <strong>Case 3 第一部分核对结论：分块代数正确。</strong>
        原文的 \(J_1,J_2\) 和 \(J_1^TAJ_1=\bar A\) 分块条件可由直接乘法复现。
        这里与 Case 7 共用
        \(J_2=\sigma_x\otimes I_N\)，所以也共用
        \(J_2g=\operatorname{diag}(I_N,-I_N)\)；不同之处是
        \(\{J_1,J_2\}=0\)。
      </div>
    """,
    "boson-case3-j2": r"""
      <div class="result">
        <strong>Case 3 第二部分核对结论：Failed 正确。</strong>
        invariant-cone 的线性方程可以有非零解，但在同时施加
        \(J_1^TAJ_1=\bar A\) 后，任何半负定收缩矩阵都被迫为零。
        所以这里的失败不是“找不到任何 \(A\)”，而是找不到使
        \(\eta A+A^\dagger\eta<0\) 的 \(A\)。
      </div>
    """,
    "boson-case4-j1": r"""
      <div class="note">
        <strong>Case 4 第一部分核对结论：分块条件正确。</strong>
        \(B=-B^\dagger\)、\(C=-\bar D\) 与直接逐块比较一致。
        这里也与 Case 7 共用
        \(J_2=\sigma_x\otimes I_N\) 和
        \(J_2g=\operatorname{diag}(I_N,-I_N)\)。Case 4 的
        \(J_1^2=-I\)，并且 \(J_1,J_2\) 反对易。
      </div>
    """,
    "boson-case4-j2": r"""
      <div class="result">
        <strong>Case 4 第二部分核对结论：Failed 正确。</strong>
        本类满足
        \(J_1^T\overline{(\eta A+A^\dagger\eta)}J_1
        =-(\eta A+A^\dagger\eta)\)。若括号内的矩阵半负定，左边也
        半负定，所以上式又给出括号内的矩阵半正定；因此它只能为零。
        原文“没有 contraction semigroup”更准确地应读成：
        这个受约束类别没有进入收缩半群内部的生成元，但仍有等号部分。
      </div>
    """,
    "boson-case9-j1": r"""
      <div class="note">
        <strong>Case 9 第一部分核对结论：分块代数正确。</strong>
        第二个 matrix realization 和随后的 \(J_1\) 线性条件可由直接乘法复现。
        第二个 realization 仍取
        \(J_2=\sigma_x\otimes I_N\)，因而
        \(J_2g=\operatorname{diag}(I_N,-I_N)\)；与 Case 7 的差别是
        \(J_1^TgJ_1=-g\)。
      </div>
    """,
    "boson-case9-j2": r"""
      <div class="result">
        <strong>Case 9 第二部分核对结论：Failed 正确。</strong>
        本类同样满足
        \(J_1^T\overline{(\eta A+A^\dagger\eta)}J_1
        =-(\eta A+A^\dagger\eta)\)。因此半负定条件同时推出半正定条件，
        只能退化为等号。原文正确识别了失败，但应保留 maximal-subgroup
        等号部分，不能把它表述成完全没有任何半群元素。
      </div>
    """,
    "boson-case10": r"""
      <div class="result">
        <strong>Case 10 核对结论：新版已改正确。</strong>
        更新后的 \(J_1,J_2\) 确实对易并满足标题中的其余四条关系，而且
        \(J_1^T\overline{(\eta A+A^\dagger\eta)}J_1
        =-(\eta A+A^\dagger\eta)\)。故半负定条件同时推出半正定条件，
        只能取等号，Failed 正确。旧版使用
        \(J_2=\sigma_x\otimes I\) 时实际落入另一个对易类型；新版删除
        那段旧 block calculation 是必要修正。
        本条的 “Also a Yin-Kai's case” 与 Cases 3、4、9 的矩阵对应
        不同：
        \[
          J_2=\sigma_z\otimes I_N
          =J_2^{\mathrm{Case\ 7}}g,\qquad
          J_2g=-\sigma_x\otimes I_N .
        \]
        即本条把 Case 7 的对角度规矩阵放在了新的 \(J_2\) 位置。
      </div>
    """,
    "boson-case11-j1": r"""
      <div class="correction">
        <strong>Case 11 第一部分核对结论：有一处回代 typo。</strong>
        原文上一行给出的关系要求最终 \(A\) 的 \((4,2)\) 子块为
        \(-\bar C_{11}\)，显示式却写成 \(-\bar C_{22}\)。
        其余 \(J_1\) 线性关系与直接乘法一致；这个局部错误不改变
        后面的 trace obstruction。
      </div>
    """,
    "boson-case11-j2": r"""
      <div class="result">
        <strong>Case 11 第二部分核对结论：Failed 正确。</strong>
        因 \(J_2^2=-I\)，
        \(\Tr(\eta A+A^\dagger\eta)=0\)。若本征值为
        \(\lambda_j\le0\)，则
        \(\sum_j\lambda_j=0\) 迫使每个 \(\lambda_j=0\)。
        因此不存在负定生成元，原文的最终判断正确。
      </div>
    """,
    "boson-case12-j1": r"""
      <div class="correction">
        <strong>Case 12 第一部分核对结论：数学正确，英文有 typo。</strong>
        “We jave” 应为 “We have”。逐块得到的 \(J_1\) 约束与直接乘法一致；
        该拼写错误不影响公式。
      </div>
    """,
    "boson-case12-j2": r"""
      <div class="result">
        <strong>Case 12 第二部分核对结论：Failed 正确。</strong>
        与 Case 11 相同，\(J_2^2=-I\) 给出
        \(\Tr(\eta A+A^\dagger\eta)=0\)。半负定使所有本征值
        \(\lambda_j\le0\)，而 \(\sum_j\lambda_j=0\)，所以每个
        \(\lambda_j=0\)。原文虽未列 maximal subgroup，失败结论仍成立。
      </div>
    """,
    "boson-case13": r"""
      <div class="correction">
        <strong>Case 13 核对结论：结论正确，拼写和 metric 维数各有一处 typo。</strong>
        “metrix” 应为 “metric”；
        直接相乘得到 \(J_2g=-I_{2N}\)，不是原文写的 \(-I_N\)。
        在全部生成元约束下仍有
        \(\Tr(\eta A+A^\dagger\eta)=\sum_j\lambda_j=0\)；半负定要求
        \(\lambda_j\le0\)，所以每个 \(\lambda_j=0\)，
        所以 Failed 不受这个维数 typo 影响。
      </div>
    """,
    "boson-case14": r"""
      <div class="correction">
        <strong>Case 14 核对结论：结论正确，沿用了同一组 typo。</strong>
        “metrix” 应为 “metric”，且 metric 应为 \(-I_{2N}\)。
        改变 \(J_1^2\) 不会解除 \(J_2^2=-I\) 给出的
        \(\Tr(\eta A+A^\dagger\eta)=0\)。半负定时所有本征值不大于零，
        本征值总和为零便迫使它们全为零，因此 Failed 正确。
      </div>
    """,
    "boson-case15": r"""
      <div class="correction">
        <strong>Case 15 核对结论：结论正确，两处 identity 的维数少写了一倍。</strong>
        \(J_1\) 作用在完整 Nambu 空间，应写 \(I_{2N}\)，不是 \(I_N\)。
        同样，\(J_2g=-I_{2N}\)，不是原文最后一行的 \(-I_N\)。
        \(A=\bar A\) 和 cone 线性关系可以保留；但仍有
        \(\Tr(\eta A+A^\dagger\eta)=\sum_j\lambda_j=0\)。
        若 \(\lambda_j\le0\)，只能全部为零，
        所以 Failed 正确。
      </div>
    """,
    "boson-case16-j1": r"""
      <div class="result">
        <strong>Case 16 第一部分核对结论：正确。</strong>
        \(B=-B^\dagger\)、\(D=\bar C\) 与
        \(J_1^TAJ_1=\bar A\) 的逐块比较一致，本段没有发现影响公式的 typo。
      </div>
    """,
    "boson-case16-j2": r"""
      <div class="result">
        <strong>Case 16 第二部分核对结论：Failed 正确。</strong>
        \(J_2^2=-I\) 再次给出
        \(\Tr(\eta A+A^\dagger\eta)=\sum_j\lambda_j=0\)。
        半负定要求每个 \(\lambda_j\le0\)，所以只能全部为零。
        原文写出的 cone 线性空间非空并不与这个失败结论矛盾。
      </div>
    """,
    "fermion-general": r"""
      <div class="result">
        <strong>一般费米分块核对结论：正确。</strong>
        \(C=-C^T\)、\(D=-D^T\) 以及进一步拆成 \(N/2\) 子块时的转置负号
        都来自 \((gA)^T=-gA\)，可以直接复现。
      </div>
    """,
    "fermion-case1-j1": r"""
      <div class="result">
        <strong>费米 Case \(1'\) 第一部分核对结论：分块代数正确。</strong>
        \(B\) blocks 的 anti-Hermitian relations 和 \(C=-\bar D\)
        与直接矩阵乘法一致；这一步只解出了第一个 anti-linear symmetry，
        尚未证明权重非负。
      </div>
    """,
    "fermion-case1-j2": r"""
      <div class="warning">
        <strong>费米 Case \(1'\) 第二部分核对结论：分块计算正确，但作者的疑问不能由该测试解决。</strong>
        “I don't know how to prove it for this case yet” 准确说明了
        作者在这里尚未证明什么：
        只令 \(B_{11}\neq0\) 的测试覆盖了一个很小的子空间，不能推出一般
        \(B_{12},C_{11},C_{12}\) 的结论。交换 \(J_1,J_2\) 的职责后，
        本段的两个正号条件确实等于 \(9'\) 的 reality condition 加
        maximal-subgroup 等号条件，所以 “special case” 在线性约束层面成立。
        但 \(9'\) 的等号部分本身不能阻止传播穿过 determinant zero；
        \(9'\) 还有明确负权重反例。因此这个包含关系不能替作者完成
        Case \(1'\) 的 positivity proof。现有证据既不能证明整个 Case
        \(1'\) 无符号，也不能证明它一定有符号问题。
      </div>
    """,
    "fermion-case5-j1": r"""
      <div class="correction">
        <strong>费米 Case \(5'\) 第一部分核对结论：关系正确，显示矩阵有 typo。</strong>
        \(J_1=\sigma_z\otimes I_N\) 应显示为
        \(\operatorname{diag}(I_N,-I_N)\)；原文却排成
        \(\operatorname{diag}(I_N,I_N)\)。后续乘法实际使用了正确的
        \(\sigma_z\)，所以 \(B\) 实、\(C,D\) 纯虚的结论可以保留。
      </div>
    """,
    "fermion-case5-j2": r"""
      <div class="note">
        <strong>费米 Case \(5'\) 第二部分核对结论：完整 semigroup positivity 正确，“new” 尚未证明。</strong>
        本段正确使用 \(\eta=J_2g\)，并且穷举确认存在
        \(\eta A+A^\dagger\eta<0\) 的生成元。因此 “gives a semigroup”
        不只是矩阵乘法闭合：费米 Fock space 有限；满足
        \(M^\dagger\eta M-\eta<0\) 的传播矩阵没有 \(-1\)
        本征值；\(J_1\) 使 spin trace 为实。对只满足半负定条件的传播矩阵，
        乘 \(e^{\epsilon A_0}\) 后再令 \(\epsilon\to0^+\)，便从
        严格收缩矩阵的正权重得到非负极限。因此整个半群的权重非负。
        它是否是一种新的 positivity 不能由 block form 决定，因为
        已知 Majorana semigroups 完整换到 Nambu basis 后也进入
        \(J_2g\) 分支；还必须做 basis-equivalence 和物理模型比较。
      </div>
    """,
    "fermion-case9-j1": r"""
      <div class="result">
        <strong>费米 Case \(9'\) 第一部分核对结论：线性分块条件正确。</strong>
        实、纯虚和复共轭 block 的分配与 diagonal \(J_1\) 的直接作用一致。
        这一步只给出允许的线性空间，不能单独支持 Passed。
      </div>
    """,
    "fermion-case9-j2": r"""
      <div class="correction">
        <strong>费米 Case \(9'\) 第二部分核对结论：左侧多写了 \(i\)，cone 的最终 \(A\) 还少了一个负号；Passed 不成立。</strong>
        右侧实际矩阵是 \(J_2gA\)，所以应按
        \(\eta=J_2g\) 检查。原文给出
        \(C_{11}=\bar D_{22}\)，而 \(J_1\) 条件又使
        \(C_{11}=-\bar C_{11}\)，所以 cone 矩阵的 \((4,2)\) block
        应为 \(\bar C_{11}=-C_{11}\)，不是显示式中的 \(C_{11}\)。
        修正这些局部符号后，本类仍满足
        \(J_1^T\overline{(\eta A+A^\dagger\eta)}J_1
        =-(\eta A+A^\dagger\eta)\)。因此半负定同时推出半正定，
        只能取等号，不存在负定生成元；
        报告中的三时间片例子还给出负的完整费米 determinant。因此原文
        第一节的 Passed 标签不能保留。
      </div>
    """,
    "fermion-case10-j1": r"""
      <div class="result">
        <strong>费米 Case \(10'\) 第一部分核对结论：线性分块条件正确。</strong>
        两个 realization 都满足所列离散关系；第二个 realization 的
        \(J_1\) 约束可由直接乘法复现。它们的存在不意味着 cone 中有负定点。
      </div>
    """,
    "fermion-case10-j2": r"""
      <div class="correction">
        <strong>费米 Case \(10'\) 第二部分核对结论：左侧多写了 \(i\)，cone 的 displayed \(A\) 还有两处回代错误。</strong>
        右侧 prefactor 实际是 \(J_2g\)。按正确 metric 读取后，
        \(J_1^T\overline{(\eta A+A^\dagger\eta)}J_1
        =-(\eta A+A^\dagger\eta)\)，所以半负定同时推出半正定，
        只能取等号。由上一行
        \(B_{12}=-B_{21}^\dagger\) 回代，\((2,1)\) block 应为
        \(-B_{12}^\dagger\)，不是 \(+B_{12}^\dagger\)；
        相应的 \((3,4)\) block 应为 \(+\bar B_{12}\)，不是原文的
        \(-\bar B_{21}\)。作者最后判断存在 sign problem
        说得过强；这里得到的只是本类没有负定生成元，不能单凭一个
        充分判据失效就证明每个允许 Hamiltonian 都有符号问题。
      </div>
    """,
    "fermion-case6-j1": r"""
      <div class="result">
        <strong>费米 Case \(6'\) 第一部分核对结论：分块代数正确。</strong>
        各个 block signs 与费米 pairing 的反对称性一致。原文使用的
        <code>\dag</code> 是可渲染的 dagger 记号，不应误判为数学 typo。
      </div>
    """,
    "fermion-case6-j2": r"""
      <div class="correction">
        <strong>费米 Case \(6'\) 第二部分核对结论：左侧多写了 \(i\)，maximal-subgroup 矩阵的两个 block 符号也写错；cone 结论通过。</strong>
        右侧实际计算的是 \(J_2gA\)。采用
        \(\eta=J_2g\) 后，穷举确认该类包含负定生成元。原文
        maximal-subgroup 矩阵的 \((3,3)\) 与 \((4,4)\) blocks
        都应为 \(-B_{11}^T\)，不是 \(+B_{11}^T\)；这两个 typo
        不进入随后写出的 cone 矩阵。因此
        “Possibly has positivity” 可以加强为确定的 semigroup
        positivity：费米 Fock space 有限；严格不等式排除 \(-1\)
        本征值；只满足半负定条件的传播矩阵可乘
        \(e^{\epsilon A_0}\) 后在 \(\epsilon\to0^+\) 时取非负极限。
        这三步给出所有 semigroup elements 的非负权重。
        “new non-Hermitian case” 是否代表文献中新的 positivity
        仍需 basis-equivalence 和具体 Hamiltonian 检验。
      </div>
    """,
    "fermion-case7-input": r"""
      <div class="result">
        <strong>费米 Case \(7'\) 第一部分核对结论：正确。</strong>
        \(J_1=I\) 的确使 \(J_1^TAJ_1=\bar A\) 等价于 \(A=\bar A\)；
        没有被省略的额外 \(J_1\) block 条件。
      </div>
    """,
    "fermion-case7-j2": r"""
      <div class="correction">
        <strong>费米 Case \(7'\) 第二部分核对结论：左侧多写了 \(i\)，修正后存在负定生成元。</strong>
        右侧实际是 \(J_2gA\)。按 \(\eta=J_2g\) 读取后，cone 的
        Hermiticity 和半负定条件正确，穷举也找到负定点。原文
        “With positivity” 没有写证明，但结论可以就地补完：半群乘积
        保持 \(M^\dagger\eta M-\eta\le0\)；严格不等式排除
        \(-1\) 本征值；\(J_1\) 使有限维 fermion trace 为实。
        对任一只满足半负定条件的传播矩阵，乘
        \(e^{\epsilon A_0}\) 后得到严格收缩矩阵，再令
        \(\epsilon\to0^+\)，便得到非负权重。因此这是完整的
        sign-free contraction semigroup。
      </div>
    """,
    "fermion-case8-j1": r"""
      <div class="correction">
        <strong>费米 Case \(8'\) 第一部分核对结论：列出的独立关系正确，但回代成最终 \(A\) 时交换了 \(C_{11}\) 与 \(C_{22}\)。</strong>
        由 \(C_{11}=\bar D_{22}\)、\(C_{22}=\bar D_{11}\) 应得
        \(D_{11}=\bar C_{22}\)、\(D_{22}=\bar C_{11}\)。所以最终
        \(A\) 的 \((3,1)\) block 应为 \(\bar C_{22}\)，
        \((4,2)\) block 应为 \(\bar C_{11}\)；原文正好写反。
        原文的 <code>D_{12}^{\dag}</code> 与
        <code>D_{12}^{\dagger}</code> 都表示 Hermitian conjugation；
        这不是 typo。其余独立 block relations 与直接乘法及费米反对称
        pairing 条件一致。
      </div>
    """,
    "fermion-case8-j2": r"""
      <div class="correction">
        <strong>费米 Case \(8'\) 第二部分核对结论：左侧多写了 \(i\)；maximal-subgroup 矩阵继承了上一段的两个符号错误，但 cone 结论通过。</strong>
        右侧实际是 \(J_2gA\)。采用正确 metric 后，穷举确认本类包含
        \(\eta A+A^\dagger\eta<0\) 的解。在 maximal-subgroup
        displayed \(A\) 中，\((3,1)\) 应为 \(-\bar C_{11}\)，
        \((4,2)\) 应为 \(+\bar C_{11}\)；原文符号相反。
        cone 中 \(C_{22}=C_{11}\)，所以上一段交换 \(C_{11},C_{22}\)
        的 typo 在 cone 矩阵中恰好消失。原文 “With positivity”
        只表达作者的判断，没有写出证明。正确证明与 Case \(7'\)
        相同：乘法保持半负定不等式；严格不等式排除 \(-1\) 本征值；
        \(J_1\) 使权重为实；只满足半负定条件的传播矩阵可用
        \(e^{\epsilon A_0}\) 在 \(\epsilon\to0^+\) 时逼近。四步合在一起，
        给出完整的非负 fermion Fock trace。
      </div>
    """,
    "proofs-empty": r"""
      <div class="warning">
        <strong>Proofs 节核对结论：原 note 没有完成证明。</strong>
        一个句点不能承接前面的 Passed/Failed、new positivity 或
        “With positivity” 等判断。本报告现已把缺失的层次分开补完：
        修正后的 fermion Cases \(5'\)--\(8'\) 是完整 sign-free
        semigroups；boson Cases 5--8 中，报告给出的四个具体 HS 模型
        每个时间片满足半负定条件，每个完整构型至少含一个满足严格
        不等式的固定因子；这些模型使用
        \(\eta=J_2g=\operatorname{diag}(I,-I)\)，故标准 symplectic
        Olshanski semigroup 的 metaplectic extension 适用。
        对每个构型，相应 Fock operator 都是 trace class，也就是
        对所有玻色高占据态的贡献取绝对值后求和仍收敛；权重恒正且无
        pole。新增 bosonic \(iJ_2g\)
        四类则证明了两件不同的事：取 \(\eta=iJ_2g\) 后，确实存在同时满足
        \(gA+A^Tg=0\)、\(J_1^TAJ_1=\bar A\) 和
        \(\eta A+A^\dagger\eta<0\) 的 \(A\)；但一般 BdG
        principal-block calculation 同时证明，这个
        \(\eta=iJ_2g\) 收缩方向与稳定的 grand-canonical Hermitian
        boson Hamiltonian 不相容，pairing 不能消除该阻碍。因此依赖该
        invariant cone 的四个模型改在 fixed-\(N\) sector 中直接证明
        character 逐构型严格为正。这个 no-go 不排除同一五符号类别的
        maximal-subgroup 子空间再满足额外 Kramers/RP 条件；报告已为
        四类都另行构造这种 grand-canonical、bare-trace 收敛的子类。
      </div>
    """,
}
