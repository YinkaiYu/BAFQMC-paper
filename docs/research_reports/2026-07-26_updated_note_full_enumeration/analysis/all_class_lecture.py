"""Render one non-redundant, formula-first atlas for all 64 sign classes."""

from __future__ import annotations

import csv
from pathlib import Path


REPORT_DIR = Path(__file__).resolve().parents[1]
TENSOR_PATH = REPORT_DIR / "tables" / "tensor_block_structures.csv"
MAXIMAL_PATH = REPORT_DIR / "tables" / "maximal_subgroup_structures.csv"
FULL_PATH = REPORT_DIR / "tables" / "full_64_class_enumeration.csv"
COMPLETION_PATH = REPORT_DIR / "tables" / "positive_completion_representatives.csv"


PAULI_TEX = {
    "I": "I_2",
    "X": r"\sigma_x",
    "Y": r"i\sigma_y",
    "Z": r"\sigma_z",
}


BOSON_TARGETS = (
    {
        "title": "三角格子手性凝聚与有限温手性转变",
        "lattice": (
            r"\(\epsilon_{\mathcal L}\) 取三角格子上具有 "
            r"\(\pm K\) 简并最低点的实阻挫 hopping，并整体平移到正定"
        ),
        "interaction": (
            r"\(V_{ij}=U\delta_{ij}+v[\cos(K\!\cdot r_i)"
            r"\cos(K\!\cdot r_j)+\sin(K\!\cdot r_i)"
            r"\sin(K\!\cdot r_j)]\succeq0\)，其中 \(U,v\geq0\)。"
            r"后两项是两个显式的正半定有限波矢通道"
        ),
        "why": (
            "实阻挫色散本身允许凝聚态自发选择手性；有限波矢相互作用又能"
            "与相对密度序竞争。它可回答手性 Ising 与相位相干 BKT 转变"
            "是否分裂。该相互作用不直接产生总密度 Mott gap，所以这里"
            "研究的是通向 chiral Mott 问题的可计算双组分对应模型，不能"
            "把它预先称为 chiral Mott insulator。"
        ),
        "links": (
            '<a href="https://arxiv.org/abs/1308.3237">三角格子 chiral '
            "Mott 工作</a>；"
            '<a href="https://arxiv.org/abs/1207.1725">全阻挫 '
            "Bose-Hubbard 的 loop-current Mott 工作</a>"
        ),
    },
    {
        "title": "三角格子相对密度超固体与多波矢竞争序",
        "lattice": (
            r"\(\epsilon_{\mathcal L}\) 取正 hopping 的三角格子阻挫能带"
        ),
        "interaction": (
            r"\(V_{ij}=U\delta_{ij}+v\cos[K\!\cdot(r_i-r_j)]\)"
            r"并取 \(U,v\) 使其本征值非负，从而增强 \(K\) 点的"
            r"相对密度涨落"
        ),
        "why": (
            "它可直接测量手性凝聚、相对密度波和二者共存的有限温区域。"
            "这不是把已知 hard-core 模型口头换名；这里是一个可由 "
            "Gaussian HS 严格实现的 soft-core、平衡固定粒子数模型。"
        ),
        "links": (
            '<a href="https://arxiv.org/abs/0809.1667">三角格子阻挫 '
            "hard-core boson 超固体</a>；"
            '<a href="https://arxiv.org/abs/2309.03193">阻挫 extended '
            "Bose-Hubbard 与 DQCP</a>"
        ),
    },
    {
        "title": "kagome 平带玻色子的阻挫凝聚与相对密度序",
        "lattice": (
            r"\(\epsilon_{\mathcal L}\) 取 kagome 最近邻实 hopping，"
            r"并允许弱的实远邻 hopping 调节平带宽度"
        ),
        "interaction": (
            r"\(V=U I+V_1 L_{\rm kagome}\succeq0\)，"
            r"其中 \(L_{\rm kagome}\) 是正半定的格点图 Laplacian"
        ),
        "why": (
            "平带放大相互作用效应，受阻挫最低能态又具有宏观简并；"
            "该模型可无偏地区分 order-by-disorder、相对密度晶体与"
            "多波矢凝聚。"
        ),
        "links": (
            '<a href="https://arxiv.org/abs/1207.4795">kagome 阻挫玻色'
            "超流</a>；"
            '<a href="https://arxiv.org/abs/2005.10810">相互作用平带'
            "玻色子的拓扑束缚态</a>"
        ),
    },
    {
        "title": "全阻挫梯子与二维阵列中的热手性相变",
        "lattice": (
            r"\(\epsilon_{\mathcal L}\) 取每个 plaquette 含 \(\pi\) "
            r"flux 的实 \(\pm t\) hopping；可从双腿梯子扩展到二维阵列"
        ),
        "interaction": r"\(V=U I\succeq0\)",
        "why": (
            "这一选择直接产生 staggered loop-current 自由度，适合计算"
            "手性 Ising 转变与相位相干 BKT 转变是否分裂。平衡 canonical "
            "实现避免了玻色总密度方向的 grand-canonical 稳定性问题。"
        ),
        "links": (
            '<a href="https://arxiv.org/abs/1207.1725">全阻挫 '
            "Bose-Hubbard 的 chiral Mott 相</a>；"
            '<a href="https://arxiv.org/abs/2603.04498">三角梯子的'
            "手性与 pair superfluidity</a>"
        ),
    },
)


FERMION_TARGETS = (
    {
        "title": "kagome/moire-inspired 平带中的强耦合配对与赝能隙",
        "lattice": (
            r"\(\epsilon_{\mathcal L}\) 取 kagome 或多轨道窄带的实 hopping，"
            r"并允许保持 Kramers 对称的带间混合"
        ),
        "interaction": (
            r"\(V\succeq0\) 取短程；对费米子，\(Q_i^2\) 包含"
            r"反平行组分之间的吸引"
        ),
        "why": (
            "窄带使配对能标不再由小费米面控制，可研究超导、预成对玻色"
            "流体、赝能隙和 BCS--BEC crossover。"
        ),
        "links": (
            '<a href="https://arxiv.org/abs/2111.10018">moire 平带的'
            "超导与 bosonic fluid</a>"
        ),
    },
    {
        "title": "两轨道窄带中的诱导配对与相对相位集体模",
        "lattice": (
            r"\(\epsilon_{\mathcal L}\) 取两条近简并窄带，并加入实的弱轨道杂化"
        ),
        "interaction": (
            r"\(Q_i=\sum_{o=1}^{2}(n_{i\uparrow o}-n_{i\downarrow o})\)，"
            r"\(V=U I\succeq0\)"
        ),
        "why": (
            "弱杂化的两条窄带可以分别形成强度不同的配对关联，并通过"
            "相互作用彼此诱导。该模型可直接测量两个轨道的 pair "
            "susceptibility、超流刚度以及两个凝聚分量之间的相对相位"
            "关联，从而研究轨道选择性赝能隙和 Leggett-type 集体模。"
        ),
        "links": (
            '<a href="https://arxiv.org/abs/1212.2727">双层 attractive '
            "Hubbard 中的诱导配对与杂化竞争</a>"
        ),
    },
    {
        "title": "受阻挫 Dirac 能带中的超导量子临界性",
        "lattice": (
            r"\(\epsilon_{\mathcal L}\) 取带交错 \(\pi\) flux 的三角格子"
            r"实 hopping，使半填充能带在两个 Dirac 点接触"
        ),
        "interaction": r"\(V=U I+V_1L_{\mathcal L}\succeq0\)",
        "why": (
            "Dirac 低能态密度使相互作用驱动的配对转变存在有限临界耦合，"
            "适合高精度提取临界指数，并检查 superconducting、density "
            "和多轨道序之间是否出现扩大对称性。"
        ),
        "links": (
            '<a href="https://arxiv.org/abs/1803.02001">三角格子 '
            r"\(\pi\)-flux attractive Hubbard 的 chiral-XY "
            "量子临界性</a>"
        ),
    },
    {
        "title": "无序受阻挫平带中的配对、局域化与热输运",
        "lattice": (
            r"\(\epsilon_{\mathcal L}=\epsilon_{\rm fr}+W_{\rm dis}\)，其中实无序势"
            r"对两个 Kramers 组分完全相同"
        ),
        "interaction": r"\(V\succeq0\) 取局域或有限程",
        "why": (
            "同一无符号算法可同时处理窄带、几何阻挫和无序，因而可区分"
            "谱隙、相位刚度与局域化尺度，而不必依赖解析延拓以外的"
            "小系统方法。"
        ),
        "links": (
            '<a href="https://arxiv.org/abs/2111.10018">平带配对与'
            "有限温 bosonic-fluid 区域</a>"
        ),
    },
)


def sign_rhs(value: str, symbol: str) -> str:
    return symbol if int(value) == 1 else f"-{symbol}"


def pauli_word_tex(word: str) -> str:
    # TeX control words consume following letters, so keep a separator after
    # \otimes (otherwise strings such as \otimesI become unknown commands).
    return r"\otimes ".join(PAULI_TEX[letter] for letter in word)


def coefficient_tex(word: str, coefficient_type: str) -> str:
    subscript = rf"\mathrm{{{word}}}"
    if coefficient_type == "R_S":
        return rf"S_{{{subscript}}}"
    if coefficient_type == "R_A":
        return rf"R_{{{subscript}}}"
    if coefficient_type == "iR_S":
        return rf"iS_{{{subscript}}}"
    if coefficient_type == "iR_A":
        return rf"iR_{{{subscript}}}"
    raise ValueError(f"Unknown coefficient type: {coefficient_type}")


def parse_terms(raw_terms: str) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for entry in raw_terms.split(";"):
        if entry:
            word, coefficient_type = entry.split(":")
            parsed.append((word, coefficient_type))
    return parsed


def expanded_formula(raw_terms: str, lhs: str) -> str:
    terms = parse_terms(raw_terms)
    if not terms:
        return rf'<div class="scroll">\[{lhs}=0.\]</div>'

    rendered = [
        rf"{pauli_word_tex(word)}\otimes "
        rf"{coefficient_tex(word, coefficient_type)}"
        for word, coefficient_type in terms
    ]
    lines = []
    for index in range(0, len(rendered), 2):
        chunk = " + ".join(rendered[index : index + 2])
        if index == 0:
            lines.append(rf"{lhs}&={chunk}")
        else:
            lines.append(rf"&\quad +{chunk}")
    body = r"\\".join(lines)

    return rf"""
      <div class="scroll">\[
        \begin{{aligned}}
          {body}.
        \end{{aligned}}
      \]</div>
    """


def relation_block(row: dict[str, str], dimension: int) -> str:
    relative = (
        r"J_1J_2=J_2J_1" if int(row["r"]) == 1
        else r"J_1J_2=-J_2J_1"
    )
    metric = r"J_2g" if row["metric"] == "J2g" else r"iJ_2g"
    return rf"""
      <div class="scroll">\[
        \begin{{gathered}}
          J_1={pauli_word_tex(row["J1_word"])},\qquad
          J_2={pauli_word_tex(row["J2_word"])},\qquad
          \eta={metric},\\
          J_1^TgJ_1={sign_rhs(row["s1"], "g")},\qquad
          J_1^2={sign_rhs(row["q1"], f"I_{{{dimension}}}")},\\
          J_2^TgJ_2={sign_rhs(row["s2"], "g")},\qquad
          J_2^2={sign_rhs(row["q2"], f"I_{{{dimension}}}")},\qquad
          {relative}.
        \end{{gathered}}
      \]</div>
    """


def summary_relations(row: dict[str, str], dimension: int) -> str:
    relative = (
        r"[J_1,J_2]=0" if int(row["r"]) == 1
        else r"\{J_1,J_2\}=0"
    )
    return (
        rf"\(J_1^TgJ_1={sign_rhs(row['s1'], 'g')}\), "
        rf"\(J_1^2={sign_rhs(row['q1'], f'I_{{{dimension}}}')}\); "
        rf"\(J_2^TgJ_2={sign_rhs(row['s2'], 'g')}\), "
        rf"\(J_2^2={sign_rhs(row['q2'], f'I_{{{dimension}}}')}\); "
        rf"\({relative}\)"
    )


def cone_result(tensor: dict[str, str], full: dict[str, str]) -> str:
    if int(tensor["strict_interior"]):
        return r"""
          <div class="result">
            <strong>真正的 invariant cone 非空。</strong>
            上式中的系数不能任取；最终集合是
            \[
              \mathcal C
              =\{A_{\rm cone,lin}:\eta A_{\rm cone,lin}\leq0\},
            \]
            并且其中确有满足
            \(\eta A_{\rm cone,lin}<0\) 的点。程序用一个简单试探矩阵
            检查非空性；它不被当作本类物理 Hamiltonian。
          </div>
        """
    if full["status"] == "boundary_only_trace_obstruction":
        reason = r"""
          这里 \(\operatorname{Tr}(\eta A_{\rm cone,lin})=0\)。
          若再有 \(\eta A_{\rm cone,lin}\leq0\)，它的全部本征值
          不大于零而总和为零，只能全部等于零。
        """
    else:
        reason = r"""
          这里第一条反线性约束给出
          \(J_1^T\overline{\eta A_{\rm cone,lin}}J_1
          =-\eta A_{\rm cone,lin}\)。若左边半负定，右边便要求同一
          Hermitian 矩阵同时半正定。
        """
    template = r"""
      <div class="scope">
        <strong>施加不等式后只剩零矩阵。</strong>
        \[
          \mathcal C
          =\{A_{\rm cone,lin}:\eta A_{\rm cone,lin}\leq0\}
          =\{0\}.
        \]
        REASON
      </div>
    """
    return template.replace("REASON", reason)


def algebraic_positivity(
    tensor: dict[str, str], maximal: dict[str, str]
) -> str:
    if tensor["statistics"] == "fermion" and int(
        maximal["maximal_subgroup_sign_guaranteed"]
    ):
        name = (
            r"Majorana \(\{T^+,T^-\}\)"
            if maximal["mtr_class"] == "Majorana_Tplus_Tminus"
            else r"Kramers \(\{T^-,T^-\}\)"
        )
        template = r"""
          <p class="result">
            <strong>本类原有的两条反线性对称已经给出费米正性。</strong>
            变到实 Majorana 基底后，它属于 MTR_NAME 类。因而
            \(A_{\max}\) 生成的全部有序乘积具有非负 Fock trace；
            若 invariant cone 非空，它与这些等号方向合在一起仍保持
            同一个正性定理。
          </p>
        """
        return template.replace("MTR_NAME", name)
    if int(tensor["strict_interior"]):
        return r"""
          <p>
            五条关系允许非零收缩方向。它首先是一个完整的生成元分类；
            对玻色模型还要在具体 Fock 表示中检查迹收敛，对费米模型则
            可直接结合有限维 Fock trace。下面选择的格点模型另外具有
            physical Kramers symmetry，所以其逐构型正性不依赖任何
            未说明的猜测。
          </p>
        """
    return r"""
      <p>
        本类的五条关系确定了上面的 \(A_{\max}\)，但 invariant cone
        只有零矩阵。下面不把这一点误读为“本类没有无符号模型”，而是
        明确加入一个作用在真实双组分上的 Kramers symmetry；Octave
        同时验证该物理子空间仍满足本类原来的两条 \(J\)-constraints。
      </p>
    """


def physical_model(
    tensor: dict[str, str],
    maximal: dict[str, str],
    completion: dict[str, str],
    number: int,
) -> str:
    statistic = tensor["statistics"]
    is_boson = statistic == "boson"
    target = (
        BOSON_TARGETS[(number - 1) % len(BOSON_TARGETS)]
        if is_boson
        else FERMION_TARGETS[(number - 1) % len(FERMION_TARGETS)]
    )
    operator = "b" if is_boson else "c"
    component_count = 2 ** (int(completion["n"]) - 1)
    orbital_count = component_count // 2
    orbital_text = (
        "每格点两个物理组分，不需要轨道复制"
        if orbital_count == 1
        else "每格点两个 Kramers 组分和两个轨道"
    )
    ensemble = (
        r"""
          玻色的高密度研究采用平衡 canonical ensemble
          \(N_\uparrow=N_\downarrow=N\)。固定辅助场后，上、下两个
          flavor blocks 互为复共轭，所以
          \[
            W_{N,N}(\phi)
            =\operatorname{Tr}_{N}\mathcal B_\uparrow(\phi)\,
             \overline{\operatorname{Tr}_{N}\mathcal B_\uparrow(\phi)}
            =\left|\operatorname{Tr}_{N}
             \mathcal B_\uparrow(\phi)\right|^2\geq0.
          \]
          每个固定粒子数 Hilbert space 有限，因而没有 bare-trace pole。
          若改做 grand-canonical，只需再取
          \(\epsilon_{\mathcal L}>0\)。若共有 \(L_\tau\) 个时间片，
          每个 HS 因子的 2-norm 都是 1，而
          \[
            \left\|\mathcal B_\uparrow(\phi)\right\|_2
            \leq
            \prod_{\ell=1}^{L_\tau}
            \left\|e^{-\Delta\tau\epsilon_{\mathcal L}}\right\|_2
            =
            e^{-\beta\lambda_{\min}(\epsilon_{\mathcal L})}<1 .
          \]
          因而 \(I-\mathcal B_\uparrow\) 和
          \(I-\mathcal B_\downarrow\) 都可逆，并且
          \[
            W_{\rm GC}(\phi)
            =\frac{1}{
              \det[I-\mathcal B_\uparrow(\phi)]\,
              \det[I-\mathcal B_\downarrow(\phi)]}
            =\frac{1}{
              |\det[I-\mathcal B_\uparrow(\phi)]|^2}>0 .
          \]
          这同时证明 bare trace 收敛、没有 pole 和权重为正。
        """
        if is_boson
        else r"""
          费米 Fock space 本来就是有限维。反线性变换
          \(\Theta=(i\sigma_y)_{\uparrow\downarrow}\mathcal K\)
          满足 \(\Theta^2=-I\)，并逐时间片保持传播矩阵。因此
          \[
            W_{\rm F}(\phi)=\det[I+\mathcal B(\phi)]\geq0.
          \]
          具体地，若
          \(\mathcal Bv=\lambda v\)，Kramers symmetry 给出
          \(\mathcal B(\Theta v)=\overline\lambda(\Theta v)\)。
          非实本征值因此成 \(\lambda,\overline\lambda\) 对；实本征值
          的本征空间则因 \(\Theta^2=-I\) 至少二重简并。于是行列式由
          \(|1+\lambda|^2\) 或 \((1+\lambda)^2\) 这样的非负因子相乘
          得到。
          本类若已经属于 Majorana/Kramers 基本正性类，这个模型是其
          一个物理子空间；其余类别则把 \(\Theta\) 作为额外的第三条
          physical symmetry。
        """
    )
    j1_model = pauli_word_tex(completion["J1_word"])
    j2_model = pauli_word_tex(completion["J2_word"])
    metric = r"J_2g" if completion["metric"] == "J2g" else r"iJ_2g"
    mtr_note = ""
    if statistic == "fermion" and int(maximal["maximal_subgroup_sign_guaranteed"]):
        mtr_note = (
            "本类自身已有 Majorana-time-reversal 正性；这里仍选用同一个"
            "可扩展格点模型，便于把代数类别直接变成研究项目。"
        )

    template = r"""
      <section class="model-example">
        <p class="model-title">
          <strong>本类建议优先计算的模型：MODEL_TITLE</strong>
        </p>
        <p>
          用 \(OPERATOR_{i\sigma o}\) 表示格点 \(i\)、组分
          \(\sigma=\uparrow,\downarrow\)、轨道 \(o\) 上的算符，定义
          \[
          \begin{aligned}
            Q_i&=\sum_o(n_{i\uparrow o}-n_{i\downarrow o}),\\
            H_{\mathcal L}
            &=\sum_{ij,\sigma,o}
              OPERATOR_{i\sigma o}^+
              (\epsilon_{\mathcal L})_{ij}
              OPERATOR_{j\sigma o}
              +\frac12\sum_{ij}Q_iV_{ij}Q_j,
              \qquad V=V^T\succeq0 .
          \end{aligned}
          \]
          这里LATTICE；INTERACTION。这是厄米 Hamiltonian。当前类别的
          具体实现有COMPONENT_COUNT维 annihilation-operator space，
          也就是ORBITAL_TEXT。
        </p>
        <p>
          将 \(V=LL^T\) 后，每个时间片使用正 Gaussian 测度
          \[
            e^{-\frac{\Delta\tau}2Q^TVQ}
            =\int\frac{d^r\phi}{(2\pi)^{r/2}}\,
             e^{-\phi^T\phi/2}\,
             e^{\,i\sqrt{\Delta\tau}\,\phi^TL^TQ} .
          \]
          在“Nambu、真实双组分、轨道、格点”的 tensor-factor 顺序下，
          这两个时间片生成元直接写成
          \[
          \begin{aligned}
            A_{\rm free}
            &=-\Delta\tau\,\sigma_z\otimes I_2
              \otimes I_{\rm orb}\otimes\epsilon_{\mathcal L},\\
            A_{\rm HS}(\phi)
            &=i\sigma_z\otimes\sigma_z\otimes I_{\rm orb}
              \otimes
              \operatorname{diag}\!\left(
                \sqrt{\Delta\tau}\,L\phi\right).
          \end{aligned}
          \]
          \(I_{\rm orb}\) 作用在轨道空间；没有轨道复制时它就是标量 1。
          对这个物理子空间可取
          \[
            J_1^{\rm model}=J1_MODEL\otimes I_{\mathcal L},\qquad
            J_2^{\rm model}=J2_MODEL\otimes I_{\mathcal L},\qquad
            \eta^{\rm model}=METRIC\otimes I_{\mathcal L}.
          \]
          它与卡片顶部的最小代表具有完全相同的五个正负号，但未必是同一个
          表示。程序先逐项验证一个格点上的自由项基本生成元和相对密度
          基本生成元满足两条 \(J\)-constraints。由于 \(J_1,J_2\)
          不作用在格点重复空间，把前者张量乘任意实对称
          \(\epsilon_{\mathcal L}\)，把后者张量乘 \(L\) 的任一实列向量，
          仍满足相同等式；这就覆盖了上式的每个自由项和每个
          \(L^TQ\) 辅助场方向。physical Kramers symmetry 把 \(i\)
          和 \(Q\) 同时变号。MTR_NOTE
        </p>
        <div class="result">
          <strong>逐构型权重。</strong>
          ENSEMBLE
        </div>
        <p>
          <strong>为什么值得算。</strong>WHY
          相关物理背景见 LINKS。链接中的原模型未必满足本报告
          的 HS 条件；本卡给出的 \(H_{\mathcal L}\) 是为保留目标现象而
          构造的可计算对应模型，报告不会把二者混称为同一个 Hamiltonian。
        </p>
      </section>
    """
    replacements = {
        "MODEL_TITLE": target["title"],
        "OPERATOR": operator,
        "LATTICE": target["lattice"],
        "INTERACTION": target["interaction"],
        "COMPONENT_COUNT": str(component_count),
        "ORBITAL_TEXT": orbital_text,
        "J1_MODEL": j1_model,
        "J2_MODEL": j2_model,
        "METRIC": metric,
        "MTR_NOTE": mtr_note,
        "ENSEMBLE": ensemble,
        "WHY": target["why"],
        "LINKS": target["links"],
    }
    for marker, value in sorted(
        replacements.items(), key=lambda item: len(item[0]), reverse=True
    ):
        template = template.replace(marker, value)
    return template


def case_card(
    tensor: dict[str, str],
    maximal: dict[str, str],
    full: dict[str, str],
    completion: dict[str, str],
    number: int,
) -> str:
    statistic_name = "玻色" if tensor["statistics"] == "boson" else "费米"
    dimension = 2 ** int(tensor["n"])
    cone_label = "invariant cone 非空" if int(tensor["strict_interior"]) else "只有 maximal subgroup"
    card_id = f"class-{tensor['statistics']}-{number:02d}"
    template = r"""
      <details class="all-class-card" id="{card_id}">
        <summary>
          STATISTIC NUMBER：CLASS_ID；
          最小 Nambu 维数 DIMENSION；CONE_LABEL
        </summary>
        <div class="all-class-body tex2jax_ignore">
          <h4>五条关系与最小代表</h4>
          RELATION_BLOCK
          <p>
            上式是本类别目前最短的 Pauli-word 实现。将它扩展为
            \(J_a\otimes I_m\) 后，下列公式对任意 \(m\) 都必要且充分。
            每个 Pauli word 的第一个因子是 Nambu particle/hole 空间，
            后面的 Pauli 因子是最小内部空间；最后显式写出的
            \(\otimes S_P\) 或 \(\otimes R_P\) 作用在格点、轨道等
            \(m\) 维重复空间。
            每个 \(S_P\) 是独立的实对称 \(m\times m\) 矩阵，
            每个 \(R_P\) 是独立的实反对称 \(m\times m\) 矩阵：
            \[
              S_P^T=S_P,\qquad R_P^T=-R_P .
            \]
          </p>

          <h4>Maximal subgroup 的全部生成元</h4>
          MAXIMAL_FORMULA

          <h4>Invariant cone 的全部 block 约束</h4>
          <p>
            先解等式
            \(gA+A^Tg=0\)、\(J_1^TAJ_1=\overline A\) 和
            \(\eta A=A^\dagger\eta\)，得到
          </p>
          CONE_FORMULA
          CONE_RESULT
          ALGEBRAIC_POSITIVITY
          PHYSICAL_MODEL

          <details>
            <summary>只保留 particle-number-conserving 生成元</summary>
            NUMBER_MAX_FORMULA
            NUMBER_CONE_FORMULA
          </details>
        </div>
      </details>
    """
    replacements = {
        "{card_id}": card_id,
        "STATISTIC": statistic_name,
        "NUMBER": f"{number:02d}",
        "CLASS_ID": summary_relations(tensor, dimension),
        "DIMENSION": str(dimension),
        "CONE_LABEL": cone_label,
        "RELATION_BLOCK": relation_block(tensor, dimension),
        "MAXIMAL_FORMULA": expanded_formula(
            tensor["maximal_terms"], r"A_{\rm max}"
        ),
        "CONE_FORMULA": expanded_formula(
            tensor["cone_linear_terms"], r"A_{\rm cone,lin}"
        ),
        "CONE_RESULT": cone_result(tensor, full),
        "ALGEBRAIC_POSITIVITY": algebraic_positivity(tensor, maximal),
        "PHYSICAL_MODEL": physical_model(
            tensor, maximal, completion, number
        ),
        "NUMBER_MAX_FORMULA": expanded_formula(
            tensor["maximal_number_conserving_terms"],
            r"A_{\rm max}^{(N)}",
        ),
        "NUMBER_CONE_FORMULA": expanded_formula(
            tensor["cone_number_conserving_terms"],
            r"A_{\rm cone,lin}^{(N)}",
        ),
    }
    for marker, value in sorted(
        replacements.items(), key=lambda item: len(item[0]), reverse=True
    ):
        template = template.replace(marker, value)
    return template


def representation_answer() -> str:
    return r"""
      <h4>固定一组 \(J_1,J_2\) 会不会漏掉 \(A\)</h4>
      <p>
        这个问题必须分成两层回答。第一层只问五个正负号所标记的类别是否
        存在非零收缩方向。把
        \(H=\eta A=H^\dagger\) 代入五条关系后，右边只可能得到
        \[
          J_1^T\overline HJ_1=H
          \quad\text{或}\quad
          J_1^T\overline HJ_1=-H .
        \]
        若得到第二式，\(H\leq0\) 会同时推出 \(H\geq0\)，所以只有
        \(H=0\)。再结合 \(J_2^2\) 是否迫使
        \(\operatorname{Tr}H=0\)，便能判定负定点是否可能存在。
        这些步骤只含五条关系右边的正负号，不含所选 Pauli word。因此
        换一个同类别的代表，不会把“cone 非空”变成“cone 为空”，也不会
        产生第 17 个通过类别。
      </p>
      <p>
        第二层问的是全部允许 \(A\) 的线性空间。这里答案不同：五个正负号
        没有记录 \(J_1,J_2\) 的各个共同子空间分别出现多少次，所以它们
        不能唯一决定 \(A\) 的维数。程序在同一个费米 all-plus 类、同为
        8 维的三种表示中得到
        \[
        \begin{array}{c|cc}
          &\dim A_{\max}&\dim A_{\rm cone,lin}\\ \hline
          \text{balanced Pauli 表示}&12&16\\
          \text{第一种不均匀重数表示}&12&16\\
          \text{第二种不均匀重数表示}&21&7
        \end{array}
        \]
        。因此，顶部公式完整描述的是所列最小代表及其
        \(J_a\otimes I_m\) 扩展；它不是同一五符号类别所有不等价表示的
        并集。给定一个具体物理问题中的 \(J_1,J_2\) 后，正确做法仍是把
        实际矩阵代入三组线性方程重新求解。若两组代表仅由保持 \(g\) 的
        basis change 相连，则两个 \(A\) 空间只差同一个 similarity
        transformation，不会漏解；真正会改变空间的是不等价的重数组合。
      </p>
    """


def minimal_dimension_proof() -> str:
    return r"""
      <h4>为什么绝大多数类别只需 2 维或 4 维，而各有一类必须 8 维</h4>
      <p>
        这里沿用 note 的共同前提：\(J_1,J_2\) 都是实正交矩阵。
        整体乘以 \(-1\) 不改变相应的反线性变换，所以
        \(J_2=\pm J_1\) 不算第二条独立约束。修正程序后，单位阵被允许
        作为其中一个矩阵。
      </p>
      <p>
        先看 2 维。玻色取 \(g=-i\sigma_y\)，费米取
        \(g=\sigma_x\)。把所有 \(2\times2\) 实正交矩阵代入
        \(J^TgJ=\pm g\) 与 \(J^2=\pm I\)，在保持 \(g\) 的 basis
        change 和无关的整体负号下，只剩下
        \[
        \begin{array}{c|c|cc}
          &J&J^TgJ&J^2\\ \hline
          \text{玻色}&I&g&I\\
          &\sigma_x\ \text{或}\ \sigma_z&-g&I\\
          &i\sigma_y&g&-I\\ \hline
          \text{费米}&I\ \text{或}\ \sigma_x&g&I\\
          &\sigma_z&-g&I\\
          &i\sigma_y&-g&-I
        \end{array}
        \]
        。例如，玻色的 \(g\) 是二维有向面积形式，所以一个正交矩阵
        保持还是翻转 \(g\)，正好由它是 rotation 还是 reflection
        决定。平方为 \(-I\) 的二维实正交矩阵只能是
        \(\pm i\sigma_y\)。两个 reflection 的轴本来可以连续转动，
        但再要求二者对易或反对易后，相对夹角只能取离散值，分别可用
        \(\sigma_x,\sigma_z\) 表示。因此上表不是只检查四个 Pauli
        矩阵得到的猜测，而是二维实正交解的完整分类。
      </p>
      <p>
        把上表中两个彼此独立的矩阵逐对组合，玻色有 7 个类别能在 2 维
        实现，费米有 11 个。其余类别不可能是 2 维。程序随后给出：
        玻色另有 24 类、费米另有 20 类可由两个 Pauli 因子在 4 维
        实现。只有下面两类仍需要三个 Pauli 因子：
        \[
        \begin{array}{c|ccccc|cc}
        &J_1^TgJ_1&J_1^2&J_2^TgJ_2&J_2^2&J_1J_2
        &J_1&J_2\\ \hline
        \text{玻色}&-g&-I&-g&-I&+J_2J_1&XIY&XXY\\
        \text{费米}&+g&-I&+g&-I&-J_2J_1&IIY&IYX
        \end{array}
        \]
      </p>
      <p>
        玻色例中令 \(K=J_1J_2\)。由于两者对易且都平方为 \(-I\)，
        \(K^2=I\)。排除 \(J_2=\pm J_1\) 后，\(K\) 的 \(+1\) 与
        \(-1\) 子空间都非空。若 \(Kx=x\)、\(Ky=-y\)，则
        \[
          g(x,y)=g(Kx,Ky)=-g(x,y)=0 .
        \]
        两个子空间因此彼此 \(g\)-正交；总空间上的 \(g\) 非退化，
        所以 \(g\) 在每个子空间上的限制也非退化。\(J_1\) 与 \(K\)
        对易，因而还分别保持这两个子空间。
      </p>
      <p>
        在任一 \(2d\) 维子空间中，\(J_1\) 翻转 \(g\)。任意这样的
        anti-symplectic matrix 都可写成“标准的
        \(\operatorname{diag}(I_d,-I_d)\) 反射”乘一个 determinant
        为 1 的 symplectic matrix，所以
        \(\det J_1=(-1)^d\)。另一方面，\(J_1^2=-I\) 使它的本征值
        成 \(\pm i\) 对，从而
        \(\det J_1=+1\)。所以 \(d\) 必须为偶数，每个非空子空间至少
        4 维；两个子空间合起来至少 8 维。
      </p>
      <p>
        费米例中 \(J_1,J_2\) 是两个反对易、平方为 \(-I\) 且保持
        \(g\) 的矩阵。取一个满足 \(g(v,v)\neq0\) 的向量 \(v\)。
        \(v,J_1v,J_2v,J_1J_2v\) 必须线性独立：若一个非零实线性组合
        使它们相加为零，相应的非零 quaternion
        \(a+bJ_1+cJ_2+dJ_1J_2\) 有逆矩阵，会反推出 \(v=0\)。
      </p>
      <p>
        又因为 \(J_1^TgJ_1=g\) 与 \(J_1^2=-I\)，
        \[
          g(J_1x,y)=-g(x,J_1y),
        \]
        \(J_2\) 也满足同一式子。逐项代入便得到上面四个向量彼此
        \(g\)-正交，并且它们的 \(g\)-长度都等于 \(g(v,v)\)。
        所以这个 4 维组上的 \(g\) 要么全正，要么全负；正、负惯性指数
        都必须是 4 的倍数。4 维费米 Nambu metric
        \(g=\sigma_x\otimes I_2\) 的 signature 是 \((2,2)\)，不可能
        容纳这两个反对易 complex structures。8 维时 signature
        为 \((4,4)\)，一个正组加一个负组正好可以实现，所以最小维数是
        8。
      </p>
      <p class="result">
        <strong>因此三个 Pauli 因子并非普遍需要。</strong>
        64 类中有 62 类的最小维数已经由“二维完整分类给出的下界”和
        “显式 2 维或 4 维矩阵给出的上界”同时确定；上述两个 8 维例外
        还有单独的解析下界。因此，8 维结果不是程序恰好没有找到更短
        写法。
      </p>
    """


def shared_model_theorem() -> str:
    return r"""
      <h4>逐类物理模型采用的共同 HS 结构</h4>
      <p>
        为了让每个类别都对应一个可运行而非零维的 Hamiltonian，下面的
        卡片使用同一类可扩展格点结构，但分别选择三角、kagome、Dirac、
        全阻挫或多轨道窄带。每个模型都有两个真实物理组分
        \(\uparrow,\downarrow\)，必要时再有两个轨道。相互作用只要求
        一个实对称正半定矩阵 \(V\)，因此可逐个本征通道做 Gaussian
        HS 分解。
      </p>
      <p>
        这套构造同时回答“为何换代表会改变模型空间”。每张卡顶部的
        \(J_1,J_2\) 是列出全部 \(A\) 所用的最小代表；模型段落另列
        \(J_1^{\rm model},J_2^{\rm model}\)，它们是同一五符号类别中
        与 physical Kramers doublet 相容的代表。后者有时需要四个
        annihilation modes，但这不表示五条关系本身的最小维数是 8。
        它只是所选格点模型包含两个组分和轨道的物理代价。
      </p>
      <p>
        五个正负号是对一组 \(J_1,J_2\) 的分类，不是 Hamiltonian
        彼此排斥的标签。同一个对称性较高的 Hamiltonian 可以同时找到
        多组 \(J_1,J_2\)，因而出现在多张卡中。下面逐卡重复写出模型，
        是为了给出每个类别的具体矩阵嵌入和逐构型证明；这不应被解释为
        64 个互不等价的新正性机制。各卡轮换选择不同的重要物理问题，
        也不会把仅仅换了一组 \(J_1,J_2\) 的同一 Hamiltonian 冒充成
        新模型。
      </p>
      <p>
        高占据数玻色相优先在
        \(N_\uparrow=N_\downarrow\) 的 canonical ensemble 计算，此时
        固定场权重是两个 canonical characters 的绝对值平方。费米侧
        则直接使用 Kramers determinant。这样，每张卡都同时给出
        Hamiltonian、正测度 HS、类别嵌入和逐构型非负公式，而不是只列
        “可能研究某种相”的题目。
      </p>
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
    completion_rows = {
        (row["statistics"], row["class_id"]): row
        for row in csv.DictReader(COMPLETION_PATH.open(encoding="utf-8"))
    }
    if not (
        len(tensor_rows)
        == len(maximal_rows)
        == len(full_rows)
        == len(completion_rows)
        == 64
    ):
        raise RuntimeError("Expected 64 rows in every classification table")

    blocks = [
        r"""
        <div class="note">
          <strong>本节只列一次每个类别。</strong>
          原来的“64 类”“16 个 cone 非空类”“物理模型”和“64 行总表”
          已合并。以下每张卡固定采用同一顺序：五条关系、最小代表、
          \(A_{\max}\) 的完整公式、invariant cone 的完整公式、正性结论、
          以及一个有明确 HS 分解的研究模型。CSV 总表只作为下载数据保留，
          不再在正文重复渲染。
        </div>
        """,
        r"""
        <script>
          document.addEventListener("DOMContentLoaded", () => {
            const typesetCard = async (card) => {
              if (!card.open) return;
              const body = card.querySelector(".all-class-body");
              if (!body || body.dataset.mathTypeset) return;
              body.dataset.mathTypeset = "pending";
              body.classList.remove("tex2jax_ignore");
              body.classList.add("tex2jax_process");
              try {
                await window.MathJax.startup.promise;
                await window.MathJax.typesetPromise([body]);
                body.dataset.mathTypeset = "done";
              } catch (error) {
                body.dataset.mathTypeset = "";
                console.error("MathJax card typesetting failed", error);
              }
            };
            document.querySelectorAll("details.all-class-card").forEach(
              (card) => {
                card.addEventListener("toggle", () => typesetCard(card));
                typesetCard(card);
              }
            );
          });
        </script>
        """,
        representation_answer(),
        minimal_dimension_proof(),
        shared_model_theorem(),
    ]
    for statistic, title in (
        ("boson", "玻色 32 类"),
        ("fermion", "费米 32 类"),
    ):
        blocks.append(f"<h4>{title}</h4>")
        number = 0
        for tensor in tensor_rows:
            if tensor["statistics"] != statistic:
                continue
            number += 1
            key = (tensor["statistics"], tensor["class_id"])
            blocks.append(
                case_card(
                    tensor,
                    maximal_rows[key],
                    full_rows[key],
                    completion_rows[key],
                    number,
                )
            )
        if number != 32:
            raise RuntimeError(f"Expected 32 {statistic} rows, found {number}")

    blocks.append(
        r"""
        <p class="small">
          机器可读结果：
          <a href="tables/full_64_class_enumeration.csv">五符号与最小维数</a>，
          <a href="tables/tensor_block_structures.csv">全部显式生成元公式</a>，
          <a href="tables/maximal_subgroup_structures.csv">费米 MTR 分类</a>，
          <a href="tables/nonpauli_realization_dependence.csv">同类不等价表示的
          维数对照</a>。
        </p>
        """
    )
    result = "\n".join(blocks)
    unresolved_markers = (
        "MAXIMAL_FORMULA",
        "CONE_FORMULA",
        "PHYSICAL_MODEL",
        "NUMBER_MAX_FORMULA",
        "NUMBER_CONE_FORMULA",
        "MODEL_TITLE",
        "J1_MODEL",
        "J2_MODEL",
        "MTR_NOTE",
    )
    for marker in unresolved_markers:
        if marker in result:
            raise RuntimeError(f"Unresolved report marker: {marker}")
    return result
