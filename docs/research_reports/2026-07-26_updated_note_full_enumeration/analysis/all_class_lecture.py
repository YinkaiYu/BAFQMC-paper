"""Render the explicit canonical tensor-family structures for all 64 classes."""

from __future__ import annotations

import csv
import html
from pathlib import Path

from physical_model_catalog import (
    MAXIMAL_ONLY_MODEL_CATALOG,
    MODEL_CATALOG,
    render_maximal_only_model,
    render_physical_model,
)


REPORT_DIR = Path(__file__).resolve().parents[1]
TENSOR_PATH = REPORT_DIR / "tables" / "tensor_block_structures.csv"
MAXIMAL_PATH = REPORT_DIR / "tables" / "maximal_subgroup_structures.csv"
FULL_PATH = REPORT_DIR / "tables" / "full_64_class_enumeration.csv"
STRICT_PATH = REPORT_DIR / "tables" / "strict_generator_structures.csv"
COMPLETION_PATH = (
    REPORT_DIR / "tables" / "positive_completion_representatives.csv"
)


PAULI_TEX = {
    "I": "I_2",
    "X": r"\sigma_x",
    "Y": r"i\sigma_y",
    "Z": r"\sigma_z",
}

COEFFICIENT_TEXT = {
    "R_S": r"任意实对称 \(m\times m\) 矩阵",
    "R_A": r"任意实反对称 \(m\times m\) 矩阵",
    "iR_S": r"\(i\) 乘任意实对称 \(m\times m\) 矩阵",
    "iR_A": r"\(i\) 乘任意实反对称 \(m\times m\) 矩阵",
}


def sign_rhs(value: str, symbol: str) -> str:
    return symbol if int(value) == 1 else f"-{symbol}"


def pauli_word_tex(word: str) -> str:
    return r" \otimes ".join(PAULI_TEX[letter] for letter in word)


def term_rows(raw_terms: str) -> str:
    terms = [entry for entry in raw_terms.split(";") if entry]
    if not terms:
        return '<tr><td colspan="2">只有零矩阵</td></tr>'
    rows = []
    for entry in terms:
        word, coefficient_type = entry.split(":")
        rows.append(
            "<tr>"
            f"<td>\\({pauli_word_tex(word)}\\)</td>"
            f"<td>{COEFFICIENT_TEXT[coefficient_type]}</td>"
            "</tr>"
        )
    return "".join(rows)


def relation_block(row: dict[str, str], dimension: int) -> str:
    relative = (
        r"[J_1,J_2]=0" if int(row["r"]) == 1 else r"\{J_1,J_2\}=0"
    )
    return rf"""
      <div class="scroll">\[
        \begin{{gathered}}
        J_1^TgJ_1={sign_rhs(row["s1"], "g")},\qquad
        J_1^2={sign_rhs(row["q1"], f"I_{{{dimension}}}")},\\
        J_2^TgJ_2={sign_rhs(row["s2"], "g")},\qquad
        J_2^2={sign_rhs(row["q2"], f"I_{{{dimension}}}")},\qquad
        {relative}.
        \end{{gathered}}
      \]</div>
    """


def cone_verdict(
    tensor: dict[str, str], full: dict[str, str], dimension: int
) -> str:
    if int(tensor["strict_interior"]):
        return rf"""
          <p class="result">
            <strong>这一类确实容许严格收缩。</strong>
            上表列出施加不等式以前的完整线性空间；真正用于收缩的
            invariant cone 是其中进一步满足
            \[
              \eta A+A^\dagger\eta\leq0
            \]
            的矩阵。对当前代表以及它的任意重数扩展，都可取
            \[
              A=-\eta,\qquad
              \eta A+A^\dagger\eta=-2I_{{{dimension}m}}<0 .
            \]
            这里的 \(A=-\eta\) 是用来证明负定点存在的试探矩阵，
            不是预先指定的物理自由 Hamiltonian；这一区别在 64 张卡片
            以前的推导中会完整说明。
          </p>
        """

    if full["status"] == "boundary_only_trace_obstruction":
        return r"""
          <p class="scope">
            <strong>这一类的 invariant cone 只有 \(A=0\)。</strong>
            上面的“cone 线性空间”仍可能列出许多矩阵，因为它只解了
            \(\eta A=A^\dagger\eta\)。令 \(H=\eta A\)，则 \(H=H^\dagger\)。
            本类的 \(J_2^2\) 符号使李代数条件给出
            \[
              \operatorname{Tr}H
              =-\operatorname{Tr}H=0 .
            \]
            若再要求 \(H\leq0\)，它的全部实本征值都不大于零而总和为零，
            因此每个本征值只能为零，即 \(H=0\)。由于 \(\eta\) 可逆，
            最终只有 \(A=0\)。因此实际 invariant cone 仅含 \(A=0\)，
            半群中没有非零收缩生成元；上表的非零项只是尚未施加半负定
            条件的候选，不能任取一个当作收缩方向。
          </p>
        """

    return r"""
      <p class="scope">
        <strong>这一类的 invariant cone 只有 \(A=0\)。</strong>
        令 \(H=\eta A=H^\dagger\)。把
        \(J_1^TAJ_1=\overline A\) 与本类五条关系逐项代入，得到
        \[
          J_1^THJ_1=-\overline H .
        \]
        若 \(H\leq0\)，左边是半负定矩阵；但右边是
        \(-\overline H\geq0\)。同一个矩阵同时半负定和半正定，只能为零。
        因此 \(H=0\)，进而 \(A=0\)。上表的“cone 线性空间”只是施加
        半负定以前的候选空间；施加 \(H\leq0\) 后只剩 \(A=0\)。
      </p>
    """


def maximal_verdict(
    tensor: dict[str, str], maximal: dict[str, str]
) -> str:
    if tensor["statistics"] == "fermion":
        if int(maximal["maximal_subgroup_sign_guaranteed"]):
            mtr_name = (
                r"Majorana \(\{T^+,T^-\}\) 类"
                if maximal["mtr_class"] == "Majorana_Tplus_Tminus"
                else r"Kramers \(\{T^-,T^-\}\) 类"
            )
            extra = (
                "这一行同时容许严格收缩生成元。"
                if int(tensor["strict_interior"])
                else
                "这一行的半负定条件只能取等号；无符号结论完全来自 "
                "maximal subgroup 上的两条反线性对称。"
            )
            return rf"""
              <p class="result">
                <strong>费米 maximal subgroup 逐构型无符号。</strong>
                把 Nambu 矩阵变到实 Majorana 基底后，这对反线性对称属于
                {mtr_name}。这是已证明的两种基本 Majorana-time-reversal
                正性类别之一，所以由等号生成元指数化并有序相乘所得的
                传播矩阵，其 Fock trace 都非负。{extra}
              </p>
            """
        negative_count = int(maximal["random_negative_count"])
        trials = int(maximal["random_trials"])
        evidence = ""
        if trials and negative_count:
            evidence = (
                f"规范最小代表的精确 Fock-space 扫描在 {trials} 个"
                f"随机有序乘积中找到 {negative_count} 个负权重。"
            )
        else:
            evidence = (
                "这个最小代表的等号代数可能退化为零维；其他表示重数下仍需"
                "重新检查，五条关系本身不给出正性定理。"
            )
        return f"""
          <p class="warning">
            <strong>费米 maximal subgroup 不具有一般正性保证。</strong>
            变到 Majorana 基底后，这两个反线性变换不属于
            “一个平方为正、一个平方为负”或“两个都平方为负”的
            反对易正性类别。
            {evidence}
          </p>
        """

    return r"""
      <p class="note">
        <strong>玻色 maximal subgroup 要再检查物理正性结构。</strong>
        本卡片列出的等号生成元虽然满足
        \(gA+A^Tg=0\)、两条 \(J_1,J_2\) 反线性约束以及
        \(\eta A+A^\dagger\eta=0\)，这些矩阵条件仍不会自动保证
        bosonic Fock trace 非负。若其中一个反线性变换在 annihilation
        单粒子空间上是真正的 \(\Theta^2=-I\) time reversal，则
        Kramers pairing 可使 \(\det(I-\mathcal B)\geq0\)。另一条路线是
        要求每个 Fock-space 因子属于反射正 cone，即能写成
        \[
          \sum_\alpha X_\alpha\,\theta(X_\alpha)
        \]
        的形式，其中系数非负，且 \(\theta\) 把一个 flavor sector
        反射到另一个 sector 并作复共轭；这时 reflection positivity
        可使有限的 bare trace 非负。两种检查都需要实际 Hamiltonian、
        HS 分解与玻色迹收敛条件，不能只看本卡片的五个正负号。
      </p>
    """


def strict_class_name(row: dict[str, str]) -> str:
    prefix = "B" if row["statistics"] == "boson" else "F"
    first_sign = "+" if int(row["s1"]) == 1 else "-"
    square_sign = "+" if int(row["q1"]) == 1 else "-"
    return f"{prefix}-{row['metric']}-s1{first_sign}q1{square_sign}"


def native_physical_model_for_class(
    tensor: dict[str, str],
    maximal: dict[str, str],
    selected_strict_rows: dict[str, dict[str, str]],
) -> str:
    if int(tensor["strict_interior"]):
        class_name = strict_class_name(tensor)
        if class_name not in MODEL_CATALOG or class_name not in selected_strict_rows:
            raise RuntimeError(f"Missing strict physical model for {class_name}")
        selected = selected_strict_rows[class_name]
        expected = (
            tensor["statistics"],
            tensor["metric"],
            tensor["s1"],
            tensor["q1"],
            tensor["s2"],
            tensor["q2"],
            tensor["r"],
        )
        actual = (
            selected["statistics"],
            selected["metric"],
            selected["s1"],
            selected["q1"],
            selected["s2"],
            selected["q2"],
            selected["r"],
        )
        if expected != actual:
            raise RuntimeError(
                f"Physical representative mismatch for {class_name}: "
                f"{expected} != {actual}"
            )
        same_representative = (
            tensor["J1_word"] == selected["J1_word"]
            and tensor["J2_word"] == selected["J2_word"]
        )
        if same_representative:
            representative_note = (
                "下面的物理模型直接使用本卡片上方的规范代表。"
            )
        else:
            representative_note = rf"""
              上方系数表使用自动找到的最短规范代表。为了让 Hamiltonian
              的厄米性和物理自由度更直观，下面改用同一五条关系类别中的
              \[
                J_1={pauli_word_tex(selected["J1_word"])},\qquad
                J_2={pauli_word_tex(selected["J2_word"])} .
              \]
              Octave 已重新核对这组矩阵的五条关系、全部生成元条件和 HS
              时间片；模型不是把上方规范代表的 \(A\) 表逐字照搬。
            """
        return (
            '<div class="note"><strong>本类的物理实现采用哪组代表。</strong>'
            f"{representative_note}</div>"
            + render_physical_model(class_name)
        )

    if (
        tensor["statistics"] == "fermion"
        and int(maximal["maximal_subgroup_sign_guaranteed"])
    ):
        class_id = tensor["class_id"]
        if class_id not in MAXIMAL_ONLY_MODEL_CATALOG:
            raise RuntimeError(f"Missing maximal-only model for {class_id}")
        return render_maximal_only_model(class_id)

    return ""


def completion_model_for_class(
    tensor: dict[str, str],
    completion: dict[str, str],
) -> str:
    expected = (
        tensor["statistics"],
        tensor["class_id"],
        tensor["s1"],
        tensor["q1"],
        tensor["s2"],
        tensor["q2"],
        tensor["r"],
    )
    actual = (
        completion["statistics"],
        completion["class_id"],
        completion["s1"],
        completion["q1"],
        completion["s2"],
        completion["q2"],
        completion["r"],
    )
    if expected != actual:
        raise RuntimeError(
            f"Positive-completion mismatch: {expected} != {actual}"
        )

    n = int(completion["n"])
    statistic_name = "玻色" if tensor["statistics"] == "boson" else "费米"
    operator = "b" if tensor["statistics"] == "boson" else "c"
    orbital_text = (
        "不需要额外复制轨道"
        if n == 2
        else "还需要两个等价轨道，第三个 Pauli 因子作用在轨道空间"
    )
    metric = (
        r"\eta=J_2g"
        if completion["metric"] == "J2g"
        else r"\eta=iJ_2g"
    )
    j1_tex = pauli_word_tex(completion["J1_word"])
    j2_tex = pauli_word_tex(completion["J2_word"])
    nambu_free = (
        r"\sigma_z\otimes I_2"
        if n == 2
        else r"\sigma_z\otimes I_2\otimes I_2"
    )
    nambu_field = (
        r"\sigma_z\otimes\sigma_z"
        if n == 2
        else r"\sigma_z\otimes\sigma_z\otimes I_2"
    )
    kramers = (
        r"I_2\otimes(i\sigma_y)"
        if n == 2
        else r"I_2\otimes(i\sigma_y)\otimes I_2"
    )

    if tensor["statistics"] == "boson":
        positivity = r"""
          <p class="result">
            <strong>玻色 bare trace 收敛、没有 pole，而且权重严格为正。</strong>
            令 \(\kappa_{\min}>0\) 是 \(K\) 的最小本征值。自由传播因子
            的二范数不大于
            \(e^{-\Delta\tau\kappa_{\min}}\)，而 HS 因子是 unitary，
            因为它的 one-particle 指数是 \(i\) 乘 Hermitian matrix。
            对完整 \(L\) 个时间片使用
            \(\|M_1M_2\|_2\leq\|M_1\|_2\|M_2\|_2\)，得到
            \[
              \|\mathcal B(\phi)\|_2
              \leq e^{-L\Delta\tau\kappa_{\min}}
              =e^{-\beta\kappa_{\min}}<1 .
            \]
            所以 \(\mathcal B(\phi)\) 的每个本征值都严格位于单位圆内。
            普通 Fock-space 求和收敛，
            \(\det[I-\mathcal B(\phi)]\neq0\)，整个实辅助场空间中没有
            determinant pole。额外 Kramers symmetry 使
            \(\mathcal B\) 的非实本征值成共轭对，并使每个实本征值具有
            偶数代数重数。每对非实本征值贡献
            \((1-\lambda)(1-\overline\lambda)=|1-\lambda|^2>0\)；
            一个重数为 \(2m_\lambda\) 的实本征值贡献
            \((1-\lambda)^{2m_\lambda}>0\)。因此
            \[
              W_{\rm B}(\phi)
              =\det[I-\mathcal B(\phi)]^{-1}>0 .
            \]
          </p>
          <p>
            同一模型也满足文章的 operator reflection positivity。
            令 \(\theta\) 交换 \(\uparrow,\downarrow\) 并把
            \(i\) 变为 \(-i\)。自由项是 \(q+\theta(q)\)，HS 项则是
            \[
              i\phi O_i
              =i\phi\sum_o n_{i\uparrow o}
               +\theta\!\left(i\phi\sum_o n_{i\uparrow o}\right).
            \]
            因而每个时间片因子都是 reflected squares 的乘法闭合集合
            中的元素。Kramers 证明从 determinant 本征值配对得到正号；
            reflection-positive 证明直接从 Fock-space trace 得到非负；
            上面的范数估计另外保证这个 trace 确实是收敛的 bare trace。
          </p>
        """
        research_target = r"""
          \(K\) 可取三角、kagome 或其他受阻挫格点的实 hopping matrix，
          再把 chemical potential 选在最低单粒子能量以下，使 \(K>0\)。
          该模型可研究受阻挫双组分玻色子的 flavor-density ordering、
          flat-band condensation 与 collective orbital fluctuations；
          它不是为了填表而加入的零维例子。
        """
    else:
        positivity = r"""
          <p class="result">
            <strong>费米逐构型无符号证明。</strong>
            费米 Fock space 有限，不需要收缩不等式来保证 trace 收敛。
            额外反线性变换
            \(\Theta=(i\sigma_y)\mathcal K\) 满足
            \(\Theta^2=-I\)，且每个 one-particle 时间片满足
            \(U^\dagger\overline{B_\ell}U=B_\ell\)。因此完整传播矩阵
            \(\mathcal B\) 的非实本征值成共轭对，实本征值具有偶数重数，
            \[
              W_{\rm F}(\phi)=\det[I+\mathcal B(\phi)]
              =\prod_{\{\lambda,\overline\lambda\}}
                    |1+\lambda|^2
               \prod_{\lambda\in\mathbb R}
                    (1+\lambda)^{2m_\lambda}\geq0 .
            \]
            第一个乘积对每一对非实共轭本征值只取一次。
            这包括只满足 maximal-subgroup 等号的传播，也允许个别辅助场
            构型具有零权重。
          </p>
        """
        research_target = r"""
          \(K\) 可取 kagome、pyrochlore slab 或 moiré-inspired
          frustrated flat-band hopping。正的 \(O_i^2\) 在费米算符中
          包含 inter-flavor attraction，可用于研究 flat-band pairing、
          BCS--BEC crossover 与多轨道 collective order。这个 Kramers
          子类本身采用已知正性机制；它在这里证明当前五符号类别与一个
          可实际模拟的相互作用模型有非空交集。
        """

    return rf"""
      <section class="model-example positive-completion">
        <p class="model-title">
          <strong>本类施加附加 Kramers 条件后的物理模型：
          受阻挫多轨道双组分{statistic_name}模型</strong>
        </p>
        <p>
          这里不是声称本卡片允许的全部 \(A\) 都自动无符号，而是把它们
          进一步限制到一个已经有严格正性证明的非空子空间。在同一五符号
          类别中，Octave 找到如下可扩展的 \(J_1,J_2\) 实现；随后再施加
          本段后面写出的 physical \(T\)-Kramers 条件：
          \[
            J_1={j1_tex},\qquad J_2={j2_tex},\qquad {metric}.
          \]
          第一个 Pauli 因子是 Nambu 空间，第二个作用在
          \(\uparrow,\downarrow\) 两个物理组分上；{orbital_text}。
          这组代表可以不同于卡片上方用来列完整 \(A\) 结构的最短代表，
          但五个正负号逐项相同。
        </p>
        <p>
          用 \({operator}_{{i\alpha o}}\) 表示格点 \(i\)、组分
          \(\alpha=\uparrow,\downarrow\)、轨道 \(o\) 上的湮灭算符，
          定义
          \[
          \begin{{aligned}}
            O_i&=\sum_o
              \left(n_{{i\uparrow o}}-n_{{i\downarrow o}}\right),\\
            H&=\sum_{{ij,\alpha,o}}
              {operator}_{{i\alpha o}}^+K_{{ij}}
              {operator}_{{j\alpha o}}
              +\frac U2\sum_i O_i^2,
              \qquad K=K^T>0,\quad U>0 .
          \end{{aligned}}
          \]
          这是厄米 Hamiltonian。若当前代表只有两个 Pauli 因子，
          轨道求和只含一个 \(o\)；若有三个因子，则含两个轨道。
        </p>
        <p>
          对每个格点使用正 Gaussian 测度
          \[
            e^{{-\Delta\tau UO_i^2/2}}
            =\int\frac{{d\phi_i}}{{\sqrt{{2\pi}}}}\,
             e^{{-\phi_i^2/2}}
             e^{{\,i\sqrt{{\Delta\tau U}}\phi_iO_i}} .
          \]
          令 \(F_i=|i\rangle\langle i|\)。相应 Nambu 生成元是
          \[
          \begin{{aligned}}
            A_0&=-\Delta\tau\,
              ({nambu_free})\otimes K,\\
            A_{{\rm HS}}(\phi)&=
              i\sqrt{{\Delta\tau U}}\sum_i\phi_i\,
              ({nambu_field})\otimes F_i .
          \end{{aligned}}
          \]
          Octave 对这两个生成元逐项验证
          \[
          \begin{{gathered}}
            gA_0+A_0^Tg=0,\qquad
            gA_{{\rm HS}}+A_{{\rm HS}}^Tg=0,\\
            J_a^TA_0J_a=\overline{{A_0}},\qquad
            J_a^TA_{{\rm HS}}J_a=\overline{{A_{{\rm HS}}}}
            \quad(a=1,2),\\
            \eta A_0+A_0^\dagger\eta=0,\qquad
            \eta A_{{\rm HS}}+A_{{\rm HS}}^\dagger\eta=0 .
          \end{{gathered}}
          \]
          所以自由项和 HS 项都确实属于当前类别的 maximal subgroup；
          不是只满足额外 Kramers symmetry、却已经脱离本卡片的模型。
        </p>
        <p>
          用来证明权重非负的附加物理 time reversal 是
          \[
            T={kramers},\qquad \Theta=T\mathcal K,\qquad T^2=-I ,
          \]
          其中 \(\mathcal K\) 只表示逐分量复共轭。这个 \(\Theta\)
          是对物理 realization 额外施加的正性要求。某些类别中 \(T\)
          恰好可以选成 \(J_1\) 或 \(J_2\)；另一些类别中它是第三个
          anti-linear symmetry。无论哪一种，都要另外确认它作用在真实
          flavor 空间、逐时间片保持 \(A_0,A_{{\rm HS}}\)，而不能只从
          五个正负号推断。
        </p>
        {positivity}
        <p><strong>值得研究的格点实现。</strong>{research_target}</p>
      </section>
    """


def case_card(
    tensor: dict[str, str],
    maximal: dict[str, str],
    full: dict[str, str],
    completion: dict[str, str],
    selected_strict_rows: dict[str, dict[str, str]],
    number: int,
) -> str:
    statistic_name = "玻色" if tensor["statistics"] == "boson" else "费米"
    base_dimension = 2 ** int(tensor["n"])
    metric = (
        r"\eta=J_2g" if tensor["metric"] == "J2g" else r"\eta=iJ_2g"
    )
    number_max = term_rows(tensor["maximal_number_conserving_terms"])
    number_cone = term_rows(tensor["cone_number_conserving_terms"])
    strict_label = (
        "有负定生成元"
        if int(tensor["strict_interior"])
        else "半负定条件只能取等号"
    )
    card_id = f"all-class-{tensor['statistics']}-{number:02d}"
    return rf"""
      <details class="all-class-card" id="{card_id}">
        <summary>
          {statistic_name} {number:02d}：{strict_label}；
          规范代表 \(J_1={pauli_word_tex(tensor["J1_word"])}\)，
          \(J_2={pauli_word_tex(tensor["J2_word"])}\)
        </summary>
        <div class="all-class-body">
          <h4>五条关系、度规与可扩展代表</h4>
          {relation_block(tensor, base_dimension)}
          <p>
            这一卡片固定
            \(J_1=J_{{1,0}}\otimes I_m\)、
            \(J_2=J_{{2,0}}\otimes I_m\) 和
            \(g=g_0\otimes I_m\)，其中上方写出的 Pauli word 就是
            \(J_{{1,0}},J_{{2,0}}\)，\(m\) 可容纳格点、轨道或其他重复自由度。
            使用的 Hermitian 度规是 \({metric}\)。
          </p>

          <h4>Maximal subgroup 生成元 \(A\) 的最终结构</h4>
          <p>
            \(A\) 恰好是下表各行“Pauli 因子 \(\otimes\) 系数矩阵”的任意
            实线性组合；不同表行的系数矩阵彼此独立。表中已经同时解完
            \(gA+A^Tg=0\)、\(J_1^TAJ_1=\overline A\) 和
            \(\eta A+A^\dagger\eta=0\)，不再附带未写出的 block 条件。
          </p>
          <div class="scroll"><table>
            <thead><tr><th>Pauli 因子</th><th>允许的 \(m\times m\) 系数</th></tr></thead>
            <tbody>{term_rows(tensor["maximal_terms"])}</tbody>
          </table></div>
          <p class="small">
            实维数：
            <code>{html.escape(tensor["maximal_dimension_formula"])}</code>。
          </p>

          <h4>施加半负定条件前的 invariant-cone 线性空间</h4>
          <p>
            下表已经同时解完
            \(gA+A^Tg=0\)、\(J_1^TAJ_1=\overline A\) 和
            \(\eta A-A^\dagger\eta=0\)。它给出施加半负定条件以前的完整
            线性空间。
          </p>
          <div class="scroll"><table>
            <thead><tr><th>Pauli 因子</th><th>允许的 \(m\times m\) 系数</th></tr></thead>
            <tbody>{term_rows(tensor["cone_linear_terms"])}</tbody>
          </table></div>
          <p class="small">
            实维数：
            <code>{html.escape(tensor["cone_dimension_formula"])}</code>。
          </p>
          {cone_verdict(tensor, full, base_dimension)}
          {maximal_verdict(tensor, maximal)}
          {native_physical_model_for_class(
              tensor, maximal, selected_strict_rows
          )}
          {completion_model_for_class(tensor, completion)}

          <details>
            <summary>只看 particle-number-conserving 子空间</summary>
            <p><strong>Maximal subgroup：</strong></p>
            <div class="scroll"><table>
              <thead><tr><th>Pauli 因子</th><th>允许的系数</th></tr></thead>
              <tbody>{number_max}</tbody>
            </table></div>
            <p><strong>Invariant-cone 线性空间：</strong></p>
            <div class="scroll"><table>
              <thead><tr><th>Pauli 因子</th><th>允许的系数</th></tr></thead>
              <tbody>{number_cone}</tbody>
            </table></div>
          </details>
        </div>
      </details>
    """


def build_all_class_lecture() -> str:
    tensor_rows = list(csv.DictReader(TENSOR_PATH.open(encoding="utf-8")))
    maximal_rows = {
        (row["statistics"], row["class_id"]): row
        for row in csv.DictReader(MAXIMAL_PATH.open(encoding="utf-8"))
    }
    full_rows = {
        (row["statistics"], row["class_id"]): row
        for row in csv.DictReader(FULL_PATH.open(encoding="utf-8"))
    }
    selected_strict_rows = {
        row["class_name"]: row
        for row in csv.DictReader(STRICT_PATH.open(encoding="utf-8"))
    }
    completion_rows = {
        (row["statistics"], row["class_id"]): row
        for row in csv.DictReader(COMPLETION_PATH.open(encoding="utf-8"))
    }
    if (
        len(tensor_rows) != 64
        or len(maximal_rows) != 64
        or len(full_rows) != 64
        or len(completion_rows) != 64
        or len(selected_strict_rows) != 16
    ):
        raise RuntimeError("Expected 64 rows in each classification table")

    intro = r"""
      <div class="note">
        <strong>本节给出的“一般 \(A\)”有明确范围。</strong>
        每类先选一组最小 Pauli 代表 \(J_{1,0},J_{2,0}\)，再用
        \(J_{1,0}\otimes I_m,J_{2,0}\otimes I_m\) 扩展到任意重数 \(m\)。
        对这个完整张量族，下列系数表是必要且充分的，不是若干示例基底。
        若实际问题使用不等价的 \(J_1,J_2\) 共同本征子空间重数，则应把实际
        矩阵代入三组线性方程重新求核，不能照抄本节维数。
      </div>
      <div class="result">
        <strong>物理模型怎样放进 64 类清单。</strong>
        先只使用每类原有的 BdG 条件 \(gA+A^Tg=0\)、两条
        \(J_1,J_2\) 反线性约束以及相应的 subgroup/cone 条件，8 个玻色
        严格收缩类、8 个费米严格收缩类以及 4 个费米
        maximal-subgroup 类已有逐构型正性证明。
        这 20 类会先给出针对本类允许空间设计的模型。但这不等于其余
        44 类没有无符号子类。对全部 64 类，本报告又要求 \(A\) 同时满足
        一个物理 Kramers symmetry；玻色情况还让同一模型满足 operator
        reflection positivity。Octave 在每一类都找到非空交集，并验证
        自由项和 HS 项仍属于该类的 maximal subgroup。因此下面 64 张
        卡片都会就地写出至少一个厄米相互作用模型、HS 分解、时间片生成元
        和非负证明，同时明确区分“本类原有条件已足以证明所写模型逐构型
        非负”与“必须再限制到附加 Kramers/RP 子空间后，所写模型才有
        正性证明”。
      </div>
      <p class="scope">
        <strong>这里“没有遗漏”的准确范围。</strong>
        本节对五条关系的 64 个离散类别是完整穷举；对附加正性条件，
        系统检查了本报告已有严格证明的 contraction semigroup、费米
        Majorana-time-reversal、physical Kramers TRS 和 operator
        reflection positivity。还可以人为加入更多晶格、轨道或内部群
        对称性，它们形成无穷多种进一步子空间，不可能仅用五个正负号列成
        有限清单。因此本节不声称列尽宇宙中每一种特殊 Hamiltonian；
        它给出的可核对结论是：所有 64 类都至少与上述标准正性机制之一
        有非空交集，而每个交集的 \(J_1,J_2,A_0,A_{\rm HS}\) 和物理模型
        都已明确写出。
      </p>
      <h4>对“五条关系本身不够”的类别怎样继续筛选</h4>
      <p>
        对每一组五个正负号，先求所有同时满足
        \[
          gA+A^Tg=0,\qquad
          J_1^TAJ_1=\overline A,\qquad
          J_2^TAJ_2=\overline A
        \]
        的生成元。五条关系只规定 \(J_1,J_2\) 彼此怎样作用，并不保证
        这个生成元空间中的每个有序乘积都有非负 Fock trace。因此筛选
        不能在“半负定方向为空”或“随机乘积出现负权重”处停止，而要继续
        求它与已证明正性条件的交集。
      </p>
      <p>
        本报告使用的附加 Kramers 条件是指定一个作用在物理
        \(\uparrow,\downarrow\) 组分上的实正交矩阵 \(T\)，使每个自由项
        和每个 HS 生成元逐项满足
        \[
          T^2=-I,\qquad T^TA_\ell T=\overline{A_\ell}.
        \]
        程序保留原来的两条 \(J\)-constraints，再施加这一条 physical
        Kramers equation，求相应线性空间的交集。在部分类别中 \(T\)
        恰好等于某个 \(J_a\)，此时矩阵方程本身重复；新增信息是把这个
        \(J_a\) 识别为作用在真实 flavor doublet 上的 physical time
        reversal，并同时检查 Hamiltonian、HS 分解与玻色迹收敛。在其余
        类别中，\(T\) 是额外的第三个 symmetry。只有当这个交集含有满足
        厄米性与稳定性要求的自由项，并且存在正测度 HS 分解，使每个场值
        的生成元都留在交集中时，才得到该五符号类别中的一个
        Kramers-positive 子类。下面给出的共同模型会逐项完成这些检查。
      </p>
      <div class="scroll"><table>
        <thead>
          <tr>
            <th>筛选层次</th>
            <th>玻色 32 类</th>
            <th>费米 32 类</th>
            <th>这一行实际证明什么</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>原有 contraction / 两条反线性正性条件</td>
            <td>8 类有本类的收缩路径与正参考模型</td>
            <td>12 类属于已证明的 Majorana/Kramers 正性类别</td>
            <td>在写明的生成元、稳定性和 HS 条件下，不需要新增
            physical Kramers symmetry</td>
          </tr>
          <tr>
            <td>再与 physical Kramers 条件取交集</td>
            <td>32/32 类的交集都非空</td>
            <td>32/32 类的交集都非空</td>
            <td>仅凭五条离散关系不能对全类证明正性的类别，仍可在与附加
            physical Kramers 条件的交集中找到可模拟的无符号子空间</td>
          </tr>
          <tr>
            <td>玻色侧再检查 operator reflection positivity</td>
            <td>玻色 32 类中逐类构造的同一批 Kramers 模型也都可写成
            flavor-reflected pairs</td>
            <td>不用于这一列费米证明</td>
            <td>在 bare trace 已由 \(K>0\) 保证收敛后，给出另一条独立
            的非负证明</td>
          </tr>
        </tbody>
      </table></div>
      <p>
        程序还对每一行组成了三个非对易时间片，而不只检查单个
        generator。测试取
        \(K=\left(\begin{smallmatrix}1.4&0.25\\0.25&1.1\end{smallmatrix}\right)>0\)
        和六个正负混合的实 HS 场值。64 行都得到
        \(\|\mathcal B\|_2=0.561998570940<1\)，Kramers residual 为零。
        单轨道与双轨道玻色权重分别为
        \(12.797599651208\) 与 \(163.778556832601\)；相应费米权重分别为
        \(4.707424163557\) 与 \(22.159842255645\)，全部严格为正。
        这些数值不是正性证明的替代品；它们用来检查从内部 Pauli
        generators 到实际有序传播矩阵的实现没有漏掉转置、复共轭或乘法
        次序。
      </p>
      <p>
        所以“原五条关系不足”在本报告中只表示不能对该类允许的全部
        \(A\) 作统一正性断言；它不再被当成停止研究的判据。下面每张
        卡片先说明原条件能否独立定论，再就地写出附加筛选后留下的
        \(J_1,J_2,T,A_0,A_{\rm HS}\) 与 Hamiltonian。
      </p>
      <p>
        先把两个常用名称准确地固定下来。满足
        \[
          M^\dagger\eta M=\eta
        \]
        的有限传播矩阵 \(M\)，在同时保留本类 \(g,J_1,J_2\) 约束的
        传播矩阵中，构成相应 contraction semigroup 的 maximal
        subgroup；其无穷小生成元 \(A\) 满足
        \(\eta A+A^\dagger\eta=0\)。与之配套的 invariant cone 是满足
        \[
          \eta A=A^\dagger\eta,\qquad \eta A\leq0
        \]
        的生成元集合；用 maximal subgroup 的传播矩阵对其中的生成元作
        共轭变换，结果仍留在这个集合中。报告后面所谓“求 subgroup 和
        cone 的 \(A\) 结构”，分别是求前一个群的无穷小生成元以及后一个
        生成元集合，并不是把传播矩阵与生成元混为同一对象。
      </p>
      <h4>为什么枚举时先试 \(A=-\eta\)：它回答的是哪一个问题</h4>
      <p>
        前面的线性方程先找出 maximal subgroup：其中的生成元满足
        \[
          \eta A+A^\dagger\eta=0 .
        \]
        沿这些方向演化时，有限矩阵 \(e^A\) 保持
        \(v^\dagger\eta v\)，所以正、反方向都允许。若要从这个 group
        扩充为还含严格收缩元素的 contraction semigroup，还要问是否
        存在另一个合法的二次生成元，使
        \[
          \eta A=A^\dagger\eta,\qquad \eta A<0 .
        \]
        第一式说 \(\eta A\) 是 Hermitian；第二式说它的每个本征值都
        小于零。二式合起来立即给出
        \[
          \eta A+A^\dagger\eta=2\eta A<0 .
        \]
        因此枚举中的问题不是“物理自由项是否必须等于某个特殊矩阵”，而是
        “满足五条 \(J_1,J_2\) 关系的矩阵空间中，究竟有没有至少一个这样
        的负定方向”。
      </p>
      <p>
        选择 \(A=-\eta\) 并不是猜出来的。令
        \[
          P=-\eta A .
        \]
        因为 \(\eta A=A^\dagger\eta\)，矩阵 \(P\) 是 Hermitian；严格
        收缩条件 \(\eta A<0\) 又正好等价于 \(P>0\)。反过来，只要取一个
        positive-definite \(P\)，就可写
        \[
          A=-\eta P ,
        \]
        并得到 \(\eta A=-P<0\)。在所有这种候选中，\(P=I\) 不偏向任何
        基底方向，也不引入待调参数，所以最先检查它；这一步立即给出
        \(A=-\eta\)。
      </p>
      <p>
        本报告已经把 \(\eta\) 的相因子选到
        \(\eta^\dagger=\eta\) 且 \(\eta^2=I\)。于是最直接的试探矩阵是
        \[
          A=-\eta .
        \]
        它首先自动满足 invariant-cone 的 Hermiticity 条件：
        \[
          \begin{aligned}
          \eta A&=\eta(-\eta)=-I,\\
          A^\dagger\eta&=(-\eta)^\dagger\eta=-I .
          \end{aligned}
        \]
        因而
        \[
          \eta A+A^\dagger\eta=-2I<0 .
        \]
        这就是选择 \(-\eta\) 的全部动机：左乘一次 \(\eta\) 后，它恰好
        变成各方向都为 \(-1\) 的普通单位矩阵，不需要猜参数，也不需要做
        数值优化。它证明受约束的生成元集合确实包含满足
        \(\eta A+A^\dagger\eta<0\) 的方向。
      </p>
      <h4>但 \(A=-\eta\) 还必须是合法的玻色或费米二次生成元</h4>
      <p>
        上一步只检查了收缩不等式，还没有检查
        \(gA+A^Tg=0\)。因为 \(J_2\) 是实正交矩阵，
        \(J_2^2=+I\) 时 \(J_2^T=J_2\)，而
        \(J_2^2=-I\) 时 \(J_2^T=-J_2\)。另一方面，
        \(J_2^TgJ_2=g\) 等价于 \(J_2g=gJ_2\)，
        \(J_2^TgJ_2=-g\) 等价于 \(J_2g=-gJ_2\)。
      </p>
      <p>
        对玻色子，\(g^T=-g\) 且 \(g^2=-I\)。若
        \(J_2^2=+I\)，把 \(A=-J_2g\) 或
        \(A=-iJ_2g\) 代入后，两项逐项相消：
        \[
        \begin{array}{c|cc}
        &gA&A^Tg\\ \hline
        J_2g=gJ_2&+\hbox{同一相因子}\,J_2&
                         -\hbox{同一相因子}\,J_2\\
        J_2g=-gJ_2&-\hbox{同一相因子}\,J_2&
                         +\hbox{同一相因子}\,J_2
        \end{array}
        \]
        所以两种 \(J_2^TgJ_2=\pm g\) 都有
        \(gA+A^Tg=0\)。若改成 \(J_2^2=-I\)，
        \(J_2^T\) 多出的负号使两项相加而非相消，非零的
        \(A=-\eta\) 便不再是玻色辛生成元。
      </p>
      <p>
        对费米子，\(g^T=g\) 且 \(g^2=I\)。现在恰好需要
        \(J_2^2=-I\)，因为 \(J_2^T=-J_2\) 提供相消所需的负号：
        \[
        \begin{array}{c|cc}
        &gA&A^Tg\\ \hline
        J_2g=gJ_2&-\hbox{同一相因子}\,J_2&
                         +\hbox{同一相因子}\,J_2\\
        J_2g=-gJ_2&+\hbox{同一相因子}\,J_2&
                         -\hbox{同一相因子}\,J_2 .
        \end{array}
        \]
        若改成 \(J_2^2=+I\)，两项也会相加。因此
        \[
          \boxed{J_2^2=+I\quad\text{（玻色）}},\qquad
          \boxed{J_2^2=-I\quad\text{（费米）}}
        \]
        正是 \(A=-\eta\) 还能满足二次生成元条件的必要条件。
      </p>
      <h4>最后检查 \(J_1\) 的反线性对称</h4>
      <p>
        还剩 \(J_1^TAJ_1=\overline A\)。在上面允许的
        \(J_2^2\) 下，若 \(J_2^TgJ_2=-g\)，Hermitian 度规是
        \(\eta=J_2g\)；若 \(J_2^TgJ_2=g\)，Hermitian 度规是
        \(\eta=iJ_2g\)。直接代入四种可能，得到下表：
      </p>
      <div class="scroll"><table>
        <thead>
          <tr>
            <th>\(J_1\) 与 \(g\)</th>
            <th>\(J_2\) 与 \(g\)</th>
            <th>使用的 \(\eta\)</th>
            <th>\(J_1,J_2\) 必须满足</th>
            <th>\(J_1^TJ_2gJ_1\)</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>\(J_1^TgJ_1=g\)</td><td>\(J_2^TgJ_2=g\)</td>
          <td>\(iJ_2g\)</td><td>\(\{J_1,J_2\}=0\)</td><td>\(-J_2g\)</td></tr>
          <tr><td>\(J_1^TgJ_1=g\)</td><td>\(J_2^TgJ_2=-g\)</td>
          <td>\(J_2g\)</td><td>\([J_1,J_2]=0\)</td><td>\(+J_2g\)</td></tr>
          <tr><td>\(J_1^TgJ_1=-g\)</td><td>\(J_2^TgJ_2=g\)</td>
          <td>\(iJ_2g\)</td><td>\([J_1,J_2]=0\)</td><td>\(-J_2g\)</td></tr>
          <tr><td>\(J_1^TgJ_1=-g\)</td><td>\(J_2^TgJ_2=-g\)</td>
          <td>\(J_2g\)</td><td>\(\{J_1,J_2\}=0\)</td><td>\(+J_2g\)</td></tr>
        </tbody>
      </table></div>
      <p>
        例如第一行的 \(A=-iJ_2g\)。由
        \(J_1^TgJ_1=g\) 和 \(J_1J_2=-J_2J_1\)，逐项得到
        \[
          J_1^TAJ_1
          =-iJ_1^TJ_2gJ_1
          =+iJ_2g
          =\overline{-iJ_2g}
          =\overline A .
        \]
        第二、四行的 \(A=-J_2g\) 是实矩阵，表中最后一列为
        \(+J_2g\)，所以同样得到 \(J_1^TAJ_1=A=\overline A\)；
        第三行与第一行相同，复共轭恰好补上 \(i\) 的负号。
        整个计算没有使用 \(J_1^2=+I\) 还是 \(-I\)，所以这两种选择
        都保留。最终玻色和费米各有八类允许这个负定试探矩阵。
      </p>
      <div class="warning">
        <strong>现在可以准确回答“为什么讨论 \(A=-\eta\)”。</strong>
        它用来在解析层面区分“半负定条件只能取等号”和“存在严格收缩
        方向”，从而避免为 64 类分别做一次半定规划。它没有规定辅助场必须沿
        \(-\eta\)，也没有规定固定自由项必须沿 \(-\eta\)。实际模型只需
        每个时间片生成元都可写成 maximal-subgroup 李代数生成元与
        invariant-cone 收缩生成元之和，并让总和满足半负定条件；
        负定部分可以来自固定自由项，也可以来自对所有允许场值都保持
        半负定的 HS 通道。
      </div>
      <p>
        对标准玻色 Nambu 度规
        \(\eta=\operatorname{diag}(I,-I)\)，\(A=-\eta\) 对应
        \[
          \frac12\chi^TgA\chi
          =-\sum_j\left(a_j^+a_j+\frac12\right),
        \]
        的确压低每个 mode 的高占据态，可作为稳定的 imaginary-time
        damping。对一般 \(J_2g\) 或 \(iJ_2g\)，同一个矩阵可能对应
        squeezing、某些 modes 的放大，或只在固定总粒子数空间中有界。
        因此每个物理模型仍须单独检查 Hamiltonian 的厄米性、稳定性、
        HS 测度和 bare trace；本报告后面的模型不把这张代数证书当作
        物理结论的替代品。
      </p>
      <h4>为什么五条离散关系足以判定代数上是否存在严格收缩生成元，却
      不足以给出一般权重正性或全部 \(A\) 的结构</h4>
      <p>
        对任意实现，只要
        \(J_2^2\) 的符号和 \(J_1,J_2\) 的相对关系满足本报告前面推导的
        两个条件，取试探矩阵 \(A=-\eta\) 就逐项满足
        \[
          gA+A^Tg=0,\qquad
          J_1^TAJ_1=\overline A,\qquad
          \eta A+A^\dagger\eta=-2I<0 .
        \]
        Octave 对 8568 组不同 Pauli 实现做了交叉检查，其中 2184 组属于
        这 16 个玻色/费米有负定方向的类，全部通过。因此换代表不会漏掉
        “哪一类有负定方向”这一结论。这里的“足以”只指严格收缩生成元的
        存在性，不是 Fock 权重正性。
      </p>
      <p>
        但五条关系没有记录共同本征子空间的重数。一个同维反例是费米全正号类。
        在 \(g=\operatorname{diag}(I_4,-I_4)\) 的 basis 中，下面两组
        \(J_1,J_2\) 都平方为 \(I_8\)，都与 \(g\) 及彼此对易：
        \[
        \begin{aligned}
        J_1^{(a)}&=\operatorname{diag}(1,1,-1,-1,1,1,-1,-1),\\
        J_2^{(a)}&=\operatorname{diag}(1,-1,1,-1,1,-1,1,-1),\\
        J_1^{(b)}&=\operatorname{diag}(1,1,1,1,1,1,1,-1),\\
        J_2^{(b)}&=\operatorname{diag}(1,1,1,1,1,1,-1,-1).
        \end{aligned}
        \]
        直接对完整复 \(8\times8\) 矩阵空间求实线性核，第一组的 maximal
        subgroup 为 12 维、cone 线性空间为 16 维；第二组分别为 21 维和
        7 维。故最小代表不会漏符号类，却可能漏掉另一种表示重数允许的
        \(A\)。复现数据见
        <a href="tables/nonpauli_realization_dependence.csv">nonpauli_realization_dependence.csv</a>。
      </p>
      <h4>四种系数说明</h4>
      <div class="scroll"><table>
        <thead><tr><th>表中说明</th><th>独立实参数数目</th></tr></thead>
        <tbody>
          <tr><td>任意实对称 \(m\times m\) 矩阵</td><td>\(m(m+1)/2\)</td></tr>
          <tr><td>任意实反对称 \(m\times m\) 矩阵</td><td>\(m(m-1)/2\)</td></tr>
          <tr><td>\(i\) 乘任意实对称矩阵</td><td>\(m(m+1)/2\)</td></tr>
          <tr><td>\(i\) 乘任意实反对称矩阵</td><td>\(m(m-1)/2\)</td></tr>
        </tbody>
      </table></div>
    """

    blocks = [intro]
    for statistic in ("boson", "fermion"):
        statistic_name = "玻色 32 类" if statistic == "boson" else "费米 32 类"
        blocks.append(f"<h4>{statistic_name}</h4>")
        class_rows = [row for row in tensor_rows if row["statistics"] == statistic]
        for number, tensor in enumerate(class_rows, start=1):
            key = (statistic, tensor["class_id"])
            blocks.append(
                case_card(
                    tensor,
                    maximal_rows[key],
                    full_rows[key],
                    completion_rows[key],
                    selected_strict_rows,
                    number,
                )
            )
    return "\n".join(blocks)
