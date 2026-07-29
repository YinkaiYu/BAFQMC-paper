"""Render a formula-first, class-specific atlas for all 64 sign classes."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from physical_model_catalog import (
    render_maximal_only_model,
    render_physical_model,
)


REPORT_DIR = Path(__file__).resolve().parents[1]
TENSOR_PATH = REPORT_DIR / "tables" / "tensor_block_structures.csv"
MAXIMAL_PATH = REPORT_DIR / "tables" / "maximal_subgroup_structures.csv"
FULL_PATH = REPORT_DIR / "tables" / "full_64_class_enumeration.csv"


PAULI_TEX = {
    "I": "I_2",
    "X": r"\sigma_x",
    "Y": r"i\sigma_y",
    "Z": r"\sigma_z",
}

PAULI_NUMPY = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, 1], [-1, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex),
}

COEFFICIENT_CONDITIONS = {
    "R_S": (
        r"K_P^T=K_P",
        r"\overline{K_P}=K_P",
        "实对称",
    ),
    "R_A": (
        r"K_P^T=-K_P",
        r"\overline{K_P}=K_P",
        "实反对称",
    ),
    "iR_S": (
        r"K_P^T=K_P",
        r"\overline{K_P}=-K_P",
        "纯虚对称",
    ),
    "iR_A": (
        r"K_P^T=-K_P",
        r"\overline{K_P}=-K_P",
        "纯虚反对称",
    ),
}

BOSON_TRS_CLASS = "s1+_q1-_s2-_q2-_r+"
BOSON_RP_CLASS = "s1+_q1+_s2+_q2-_r-"

# These programs are used only for group-only cards whose five relations do not
# yet prove positivity.  The formulas in each card still choose their generators
# from that card's own P-K_P table.
GROUP_ONLY_RESEARCH_PROGRAMS: dict[
    str, dict[int, tuple[str, str]]
] = {
    "boson": {
        1: (
            "kagome 平带中的受挫 parametric pair-density wave",
            "把格点重复空间取为 kagome 晶格，可同时保留平带 hopping、"
            "有向 bond form factor 与 pairing fluctuation；目标是区分"
            "手性凝聚、pair-density wave 和相对密度序。",
        ),
        3: (
            "单组分三角格玻色子的 pair-current 临界性",
            "最小 Nambu 维数只有 2，因此这是单组分格点模型；格点指标由"
            r" \(K_P\) 承担，可研究三角格上 pair fluctuation 与"
            " loop-current order 是否在同一临界点出现。",
        ),
        6: (
            "全阻挫梯子中的手性配对与 Ising-BKT 分裂",
            "在每个 plaquette 放入 π flux，并让本卡允许的 pairing HS"
            " 方向沿梯子键交替，可检验手性 Ising 转变与相位相干"
            " BKT 转变是否分裂。",
        ),
        7: (
            "kagome 玻色平带的 nematic pair superfluid",
            "选择 kagome 平带 hopping，并让两个不等价键方向使用本卡"
            "允许的 pairing form factors，可研究平带中旋转对称破缺、"
            "pair superfluid 与普通凝聚的竞争。",
        ),
        8: (
            "dice 格子 parametric bosons 的拓扑边界放大",
            "把纯虚反对称系数放在有向 dice-lattice bonds，并把 pairing"
            " 方向置于边界，可研究受相互作用修正的 bosonic BdG 边界模"
            "与稳定性边界。",
        ),
        9: (
            "单组分受挫 Josephson 链的 pair-current multicriticality",
            r"这个 2 维 Nambu 代表不含内部 flavor；把 \(K_P\) 取为受挫"
            "链的邻接与有向键矩阵，可研究 pair ordering、current order"
            " 与 commensurate-incommensurate 转变。",
        ),
        11: (
            "双层 bosonic BdG Chern 平带的相互作用失稳",
            "两物理模可解释为 layer；允许的层间 pairing 与有向 hopping"
            "可形成相反手性的 BdG bands，用来研究相互作用诱导的边界"
            "凝聚和 layer-polarized phase。",
        ),
        12: (
            "π-flux 方格中的 bosonic pair-density-wave 晶体",
            "让实反对称系数编码 π-flux 键取向，并把 pairing form factor"
            "放在有限波矢，可研究 pair-density wave、条纹序与"
            "squeezed superfluid 的相图。",
        ),
        14: (
            "单组分全阻挫格子的 bond-energy-square 玻色模型",
            r"本类只有粒子数守恒通道；取 \(K_P=iS\)、\(S=S^T\) 为"
            " plaquette 上的实对称 bond form factor，"
            r"\(-i\hat h(G_1)\) 就是 Hermitian bond-energy 算符；"
            "它可研究受挫动能涨落诱导的 bond order 与 nematicity。",
        ),
        15: (
            "helical bosonic BdG 平带的 Kramers-paired 边界谱",
            "本卡的 particle-number-conserving 子空间具有 Kramers"
            " determinant 配对；允许的 pairing 方向可用于构造 helical"
            " BdG flat bands，并检验还需什么稳定项才能形成热系综。",
        ),
        16: (
            "受挫双层玻色子的 chiral-pair condensate",
            "把两个最小物理模解释为双层，在三角格上组合层内有向 hopping"
            "与层间 pairing，可研究 chiral single-boson condensate"
            "向 chiral pair condensate 的转变。",
        ),
        18: (
            "quartic pairing projector 驱动的玻色量子磁体",
            "该最小表示没有非零厄米二次 group 方向，却允许厄米算符平方；"
            "把固定粒子数双模单元映射为大自旋，可研究纯四次"
            "pair projector 产生的自旋向列序。",
        ),
        19: (
            "kagome 环交换与 parametric pairing 的竞争网络",
            r"在 kagome 六边形上选择有向 \(K_P\)，并用允许的 pairing"
            " Pauli 方向构造环上集体算符平方，可研究环交换、局域化"
            "magnon analog 与 pair coherence。",
        ),
        20: (
            "单组分 frustrated rotor 的 bond-order 临界点",
            "本类只含粒子数守恒 HS 方向；把纯虚对称系数对应的 Hermitian"
            " 算符取为有限波矢 bond energy，可研究受挫超流中的"
            "bond order、nematicity 与相位刚度。",
        ),
        21: (
            "dice 平带中的多通道 squeezed-boson order",
            "利用本卡同时允许的多个 particle-hole mixing 方向，把"
            "squeezing 放在 dice 平带的不同子晶格，可研究 compact"
            " localized modes、pair coherence 与密度不均匀性。",
        ),
        23: (
            "三角格双模玻色子的 pair-nematic 相",
            "将两个最小物理模解释为 orbital doublet，并令 pairing"
            " form factor 在三条键上按二维表示变换，可研究"
            "pair nematic、手性轨道序与普通凝聚的竞争。",
        ),
        24: (
            "无序图上的 bosonic BdG localization 与 pair glass",
            r"把 \(K_P\) 取为实空间无序图的对称或有向邻接矩阵，可研究"
            "parametric pairing 对 Anderson localization、rare regions"
            " 与玻色 pair-glass crossover 的影响。",
        ),
        26: (
            "合成维度 flux ladder 的相互作用 parametric pump",
            "两个最小物理模可作真实腿与合成腿；周期调制允许的 pairing"
            "方向，可研究 many-body parametric pumping、边缘输运"
            "与手性不稳定性。",
        ),
        27: (
            "moiré 玻色窄带中的 pair crystal 与相干竞争",
            r"令实对称 \(K_P\) 描述长波 moiré hopping，反对称部分描述"
            "valley-current form factor，可研究窄带中的 pair crystal、"
            "fragmented condensation 与 valley coherence。",
        ),
        28: (
            "checkerboard 平带的 squeezed superfluid 与角模",
            "把两个物理模解释为 checkerboard 子晶格，并让 pairing"
            "在正交键上取不同 form factor，可研究晶体对称保护的"
            "bosonic BdG 角态及其相互作用失稳。",
        ),
        29: (
            "受挫环交换玻色子的 pair-fragmented phase",
            "本类没有厄米二次 group 方向，但允许多种厄米集体算符平方；"
            "在共享边的 plaquettes 上使用这些方向，可研究环交换诱导的"
            "fragmentation 与 pair coherence。",
        ),
        31: (
            "四组分 spin-orbital bosons 的非阿贝尔 parametric 网络",
            "最小四个 annihilation modes 可作 spin-orbital quartet；"
            r"本卡丰富的 \(P\)-\(K_P\) 表允许非对易 conversion 与 pairing "
            "通道，可研究 spin-orbital entanglement 和集体拓扑模。",
        ),
        32: (
            "crystalline bosonic BdG 阵列中的 corner squeezing",
            "两个物理模可作晶胞内轨道；让允许的 pairing form factors"
            "在 x、y 边上按反射奇偶性取值，可研究相互作用修正的"
            "higher-order bosonic corner modes。",
        ),
    },
    "fermion": {
        1: (
            "spinless p-wave 平带网络的相互作用 Majorana 模",
            r"最小 Nambu 维数 2，不含自旋 flavor；把格点 \(K_P\) 取为"
            "有向 p-wave bonds，可研究平带 Majorana modes 与"
            " current interaction 的竞争。",
        ),
        2: (
            "checkerboard Chern 窄带中的 loop-current 质量",
            "用实对称系数构造窄带 hopping、实反对称系数构造有向电流，"
            "可研究 interaction-generated Chern mass、轨道磁性与"
            "charge order。",
        ),
        3: (
            "两轨道 Majorana 平带与 pair-density-wave",
            "两个最小物理模可作轨道 doublet；允许的 normal 与 pairing"
            " form factors 可产生近乎平坦的 Majorana band，并研究"
            "pair-density wave 对边界态的重构。",
        ),
        5: (
            "单组分阻挫 Chern 费米子的密度与电流竞争",
            r"本类不需要内部 flavor；把 \(K_P\) 放在 honeycomb 或"
            "checkerboard bonds，可研究 loop-current Chern mass 与"
            "密度序的竞争。",
        ),
        6: (
            "spinless Dirac 节点的 p-wave mass generation",
            "以单组分 honeycomb Dirac cone 为自由度，并用允许的"
            "particle-hole mixing HS 通道耦合 p-wave mass，可研究"
            "相互作用质量生成和拓扑缺陷零模。",
        ),
        8: (
            "particle-hole 对称的 spinless bond-order Dirac 格点",
            "本类只有粒子数守恒通道；其非平凡方向把纯虚对称系数转成"
            " Hermitian density/hopping form factor，适合研究半填充"
            " Dirac 系统的 bond order 与 nematic mass。",
        ),
        9: (
            "多轨道平带的 excitonic 与 pairing 竞争",
            r"把两个最小物理模解释为轨道，并将对称 \(K_P\) 用作窄带"
            r"hybridization、反对称 \(K_P\) 用作电流通道，可研究"
            "excitonic order、pairing 与 flat-band ferromagnetism。",
        ),
        11: (
            "crystalline BdG 格点的高阶 Majorana 角态",
            "允许的轨道混合与 pairing Pauli 方向可按镜面对称组织，"
            "用来研究相互作用对 higher-order topological"
            " superconductors 角态和边界质量的影响。",
        ),
        14: (
            "nodal superconductors 的磁性与配对质量竞争",
            "选择线节点或点节点 BdG hopping，并让本卡允许的"
            "density/pairing form factors 耦合辅助场，可研究节点湮灭、"
            "磁性质量与拓扑配对。",
        ),
        16: (
            "三角格多轨道 pair-density-wave 费米子",
            "把两个物理模作 orbital doublet，在三组有限波矢键上选择"
            "本卡允许的 pairing form factor，可研究 PDW、nematicity"
            "与手性超导。",
        ),
        17: (
            "单组分 Chern 费米子的 interaction-driven orbital order",
            "该 2 维 Nambu 代表不含自旋；用有向格点矩阵构造电流平方，"
            "可研究从 Dirac semimetal 到 orbital Chern insulator 的转变。",
        ),
        18: (
            "spinless Kitaev 网络的相互作用 domain-wall modes",
            "允许的 p-wave Nambu 方向可放在一维网络及其 junctions，"
            "用来研究相互作用驱动的拓扑段、domain-wall Majorana"
            "与无序临界性。",
        ),
        20: (
            "无自旋量子霍尔窄带的 nematic 电流序",
            "本类只有粒子数守恒方向；在 Chern 或 Landau-level-like"
            " 窄带中使用各向异性 bond-current form factors，可研究"
            " nematicity、轨道序与分数量子霍尔竞争。",
        ),
        21: (
            "mixed-parity 拓扑超导体的相互作用相边界",
            "将两个最小物理模解释为反演伙伴轨道，组合允许的 normal"
            " hybridization 与奇偶混合 pairing，可研究拓扑相边界、"
            "nodal arcs 与边界 Majorana modes。",
        ),
        22: (
            "非中心对称 BdG 平带中的 helical-pair instability",
            "本卡同时允许 normal 与 pairing Pauli 方向；在缺少反演的"
            "窄带上选择相应 form factors，可研究 helical pairing、"
            "spinless analog 的 magnetoelectric response 与 PDW。",
        ),
        23: (
            r"moiré 双轨道超导窄带的 charge-\(4e\) 前驱涨落",
            "把两个物理模作 moiré orbitals，并用本卡允许的多个 pairing"
            " quadratures 构造相互作用，可研究普通 pairing、复合"
            r"charge-\(4e\) order 与轨道极化。",
        ),
        26: (
            "单组分 Dirac 格点的 interaction-driven bond mass",
            "本类不引入自旋 flavor；把纯虚对称系数对应的 Hermitian"
            " hopping form factor 放在 honeycomb 或 π-flux bonds 上，"
            "可研究 bond mass、dimerization 与拓扑 domain walls。",
        ),
        28: (
            "晶体对称 Majorana hinge 网络的相互作用质量",
            "两个物理模可作镜面伙伴轨道；按晶体方向组织允许的 pairing"
            "与 current form factors，可研究 hinge/corner Majorana"
            " modes 对相互作用和无序的稳定性。",
        ),
        29: (
            r"平带超导体的 pair fragmentation 与 charge-\(4e\) order",
            "在 kagome 或 moiré flat band 上用本卡允许的两个 pairing"
            " quadratures 构造相互作用，可研究 pair fragmentation、"
            r"charge-\(4e\) coherence 与 PDW。",
        ),
        31: (
            "多轨道非幺正 pairing 与 orbital-current 竞争",
            "两个最小物理模可作轨道 doublet；本卡允许的多组 pairing"
            "和有向 hopping 可构造 nonunitary pairing，研究其与"
            "orbital-current order、Bogoliubov Fermi surfaces 的竞争。",
        ),
    },
}

def sign_rhs(value: str | int, symbol: str) -> str:
    return symbol if int(value) == 1 else f"-{symbol}"


def signed_word(value: str | int, expression: str) -> str:
    return expression if int(value) == 1 else f"-{expression}"


def pauli_word_tex(word: str) -> str:
    return r"\otimes ".join(PAULI_TEX[letter] for letter in word)


def pauli_word_numpy(word: str) -> np.ndarray:
    result = np.array([[1]], dtype=complex)
    for letter in word:
        result = np.kron(result, PAULI_NUMPY[letter])
    return result


def parse_terms(raw_terms: str) -> list[tuple[str, str]]:
    terms: list[tuple[str, str]] = []
    for entry in raw_terms.split(";"):
        if entry:
            word, coefficient_type = entry.split(":")
            terms.append((word, coefficient_type))
    return terms


def coefficient_sample(coefficient_type: str) -> np.ndarray:
    if coefficient_type.endswith("_S"):
        matrix = np.array([[1.0, 0.37], [0.37, -0.21]], dtype=complex)
    else:
        matrix = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    if coefficient_type.startswith("i"):
        matrix *= 1j
    return matrix


def coefficient_equations(
    symbol: str, coefficient_type: str
) -> tuple[str, str]:
    transpose_rhs = symbol if coefficient_type.endswith("_S") else f"-{symbol}"
    conjugation_rhs = (
        symbol if coefficient_type.startswith("R_") else f"-{symbol}"
    )
    return (
        rf"{symbol}^T={transpose_rhs}",
        rf"\overline{{{symbol}}}={conjugation_rhs}",
    )


def coefficient_realization(
    symbol: str, coefficient_type: str, role: str
) -> str:
    base, subscript = symbol.split("_", maxsplit=1)
    entry = rf"{base}_{{{subscript},ij}}"
    reverse_entry = rf"{base}_{{{subscript},ji}}"
    if coefficient_type == "R_S":
        condition = (
            rf"\({entry}\in\mathbb R\) 且 "
            rf"\({entry}={reverse_entry}\)"
        )
        use = "对角元可作局域 form factor，非对角元可作实 hopping 或对称键 form factor"
    elif coefficient_type == "R_A":
        condition = (
            rf"\({entry}\in\mathbb R\) 且 "
            rf"\({entry}=-{reverse_entry}\)"
        )
        use = (
            "它必须作用在至少两个格点或轨道上；给每条有向键指定一个实数，"
            "反向键取相反数"
        )
    elif coefficient_type == "iR_S":
        condition = (
            rf"\({entry}=i s_{{ij}}\)，"
            r"\(s_{ij}=s_{ji}\in\mathbb R\)"
        )
        use = "可表示带固定相位的对称 hopping、conversion 或 pair form factor"
    else:
        condition = (
            rf"\({entry}=i c_{{ij}}\)，"
            r"\(c_{ij}=-c_{ji}\in\mathbb R\)"
        )
        use = "可表示有向 bond current 或带固定相位的反对称 pair form factor"
    return (
        f"为把这个{role}直接放到格点模型中，可取 {condition}；"
        f"{use}。"
    )


def physical_adjoint(
    statistics: str, word: str, coefficient_type: str
) -> str:
    pauli = pauli_word_numpy(word)
    coefficient = coefficient_sample(coefficient_type)
    generator = np.kron(pauli, coefficient)
    internal_dimension = 2 ** (len(word) - 1)
    if statistics == "boson":
        g_small = -PAULI_NUMPY["Y"]
    else:
        g_small = PAULI_NUMPY["X"]
    g = np.kron(np.kron(g_small, np.eye(internal_dimension)), np.eye(2))
    exchange = np.kron(
        np.kron(PAULI_NUMPY["X"], np.eye(internal_dimension)),
        np.eye(2),
    )
    kernel = g @ generator
    adjoint_kernel = exchange @ kernel.conj().T @ exchange
    if np.linalg.norm(adjoint_kernel - kernel) < 1e-10:
        return "Hermitian"
    if np.linalg.norm(adjoint_kernel + kernel) < 1e-10:
        return "anti-Hermitian"
    raise RuntimeError(
        f"Cannot classify physical adjoint: {statistics} {word} "
        f"{coefficient_type}"
    )


def physical_channel(
    statistics: str, word: str, coefficient_type: str
) -> str:
    number_conserving = word[0] in ("I", "Z")
    adjoint = physical_adjoint(statistics, word, coefficient_type)
    if number_conserving and adjoint == "Hermitian":
        return "厄米的粒子数守恒项"
    if number_conserving:
        return (
            r"\(i\) 乘厄米的粒子数守恒项；该厄米算符究竟是 "
            r"density、hopping 还是 current，要把本行 \(P\) 与 "
            r"\(K_P\) 一起代入 \(-i\hat h(P\otimes K_P)\) 判断"
        )
    if adjoint == "Hermitian":
        return "厄米的 pairing 项"
    return r"\(i\) 乘厄米的 pairing 项（pairing-channel HS 方向）"


def coefficient_table(
    raw_terms: str,
    statistics: str,
    *,
    compact: bool = False,
) -> str:
    terms = parse_terms(raw_terms)
    if not terms:
        return "<p>没有非零项。</p>"
    rows = []
    for word, coefficient_type in terms:
        transpose, conjugation, plain_name = COEFFICIENT_CONDITIONS[
            coefficient_type
        ]
        interpretation = physical_channel(
            statistics, word, coefficient_type
        )
        if compact:
            rows.append(
                rf"<tr><td>\({pauli_word_tex(word)}\)</td>"
                rf"<td>\({transpose},\ {conjugation}\)</td></tr>"
            )
        else:
            rows.append(
                rf"<tr><td>\({pauli_word_tex(word)}\)</td>"
                rf"<td>\({transpose}\)</td>"
                rf"<td>\({conjugation}\)</td>"
                rf"<td>{plain_name}</td><td>{interpretation}</td></tr>"
            )
    if compact:
        heading = r"<tr><th>\(P\)</th><th>\(K_P\) 的完整条件</th></tr>"
    else:
        heading = (
            r"<tr><th>\(P\)</th><th>转置</th><th>复共轭</th>"
            "<th>等价说法</th><th>对应二次算符</th></tr>"
        )
    return (
        '<div class="scroll"><table class="coefficient-table"><thead>'
        + heading
        + "</thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def sum_formula(lhs: str, raw_terms: str) -> str:
    words = [word for word, _ in parse_terms(raw_terms)]
    if not words:
        return rf"\[{lhs}=0.\]"
    set_body = r",\, ".join(pauli_word_tex(word) for word in words)
    return rf"""
      \[
        {lhs}=\sum_{{P\in\mathcal P}}P\otimes K_P,\qquad
        \mathcal P=\left\{{{set_body}\right\}} .
      \]
    """


def relation_block(row: dict[str, str], dimension: int) -> str:
    mutual = (
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
          {mutual}.
        \end{{gathered}}
      \]</div>
    """


def summary_relations(row: dict[str, str]) -> str:
    mutual = "[J_1,J_2]=0" if int(row["r"]) == 1 else r"\{J_1,J_2\}=0"
    return (
        rf"\(J_1^TgJ_1={sign_rhs(row['s1'], 'g')}\), "
        rf"\(J_1^2={sign_rhs(row['q1'], 'I')}\); "
        rf"\(J_2^TgJ_2={sign_rhs(row['s2'], 'g')}\), "
        rf"\(J_2^2={sign_rhs(row['q2'], 'I')}\); "
        rf"\({mutual}\)"
    )


def defining_lemmas() -> str:
    return r"""
      <h4>先把 48 个空锥类别一次证明完</h4>
      <p>
        为避免在每张卡片里先写一组候选矩阵、最后又把它们全部排除，
        这里先证明两个判据。推导始终直接使用
        \(J_a^TgJ_a=\pm g\)、\(J_a^2=\pm I\) 以及对易或反对易，
        不再为这五个正负号另取缩写。
      </p>
      <p>
        对 invariant-cone 方向定义
        \[
          H=\eta A_{\mathrm{cone}}
          =H^\dagger,\qquad H<0 .
        \]
        因为 \(J_2\) 是实正交矩阵，
        当 \(J_2^2=I\) 时 \(J_2^T=J_2\)，当
        \(J_2^2=-I\) 时 \(J_2^T=-J_2\)。利用
        \(gA_{\mathrm{cone}}+A_{\mathrm{cone}}^Tg=0\)，逐步得到
        \[
        \begin{aligned}
          \operatorname{Tr}(J_2gA_{\mathrm{cone}})
          &=\operatorname{Tr}\!\left[
             (J_2gA_{\mathrm{cone}})^T\right]\\
          &=\operatorname{Tr}
             (A_{\mathrm{cone}}^Tg^TJ_2^T).
        \end{aligned}
        \]
        最后一行尚未代入玻色或费米的 \(g^T\)。现在分别使用
        \(A_{\mathrm{cone}}^Tg=-gA_{\mathrm{cone}}\) 以及
        \(J_2^T=\pm J_2\)，得到
      </p>
      <div class="scroll">
        <table>
          <thead><tr><th></th><th>\(J_2^2=I\)</th>
          <th>\(J_2^2=-I\)</th></tr></thead>
          <tbody>
            <tr><td>玻色：\(g^T=-g\)</td>
            <td>等式没有迫使迹为零</td>
            <td>\(\operatorname{Tr}H=-\operatorname{Tr}H=0\)</td></tr>
            <tr><td>费米：\(g^T=g\)</td>
            <td>\(\operatorname{Tr}H=-\operatorname{Tr}H=0\)</td>
            <td>等式没有迫使迹为零</td></tr>
          </tbody>
        </table>
      </div>
      <p>
        负定 Hermitian 矩阵的全部本征值都小于零，其迹必小于零。
        因此玻色要有严格 cone 必须取 \(J_2^2=I\)，费米必须取
        \(J_2^2=-I\)。其余 32 类立即被排除。这就是
        <strong>迹阻碍引理</strong>。
      </p>
      <p>
        第二个判据使用 \(J_1\)。先看一个具体例子：若
        \(J_1^TgJ_1=g\)、\(J_2^TgJ_2=g\)，metric 是
        \(\eta=iJ_2g\)。若 \(J_1,J_2\) 反对易，
        \[
        \begin{aligned}
          J_1^T\overline\eta J_1
          &=-iJ_1^TJ_2gJ_1\\
          &=-iJ_1^TJ_2J_1g\\
          &=-i(-J_2)g\\
          &=iJ_2g=\eta .
        \end{aligned}
        \]
        若把反对易改成对易，第三行便少一个负号，最后得到
        \(-\eta\)。其余三种 \(J_1,J_2\) 对 \(g\) 的作用完全类似，
        直接结果是
      </p>
      <div class="scroll">
        <table>
          <thead><tr><th>\(J_1\) 对 \(g\)</th><th>\(J_2\) 对 \(g\)</th>
          <th>Hermitian metric</th><th>使
          \(J_1^T\overline\eta J_1=\eta\) 的关系</th></tr></thead>
          <tbody>
            <tr><td>保持</td><td>保持</td><td>\(iJ_2g\)</td>
            <td>反对易</td></tr>
            <tr><td>保持</td><td>翻转</td><td>\(J_2g\)</td>
            <td>对易</td></tr>
            <tr><td>翻转</td><td>保持</td><td>\(iJ_2g\)</td>
            <td>对易</td></tr>
            <tr><td>翻转</td><td>翻转</td><td>\(J_2g\)</td>
            <td>反对易</td></tr>
          </tbody>
        </table>
      </div>
      <p>
        再利用
        \(J_1^T\overline A_{\mathrm{cone}}J_1=A_{\mathrm{cone}}\)，
        得到
        \[
          J_1^T\overline HJ_1
          =(J_1^T\overline\eta J_1)
           (J_1^T\overline A_{\mathrm{cone}}J_1).
        \]
        表中所列的对易关系使右边等于 \(H\)。若采用另一种对易关系，
        右边等于 \(-H\)：左边仍是负定矩阵，右边却是正定矩阵，矛盾。
        在允许等号的半负定版本中，同一论证只留下 \(H=0\)。
        这就是<strong>\(J_1\) 翻转引理</strong>。
      </p>
      <div class="result">
        <strong>严格锥非空的充要条件。</strong>
        玻色先要 \(J_2^2=I\)，费米先要 \(J_2^2=-I\)。
        在此基础上，\(J_1,J_2\) 若同为保持 \(g\) 或同为翻转 \(g\)，
        二者必须反对易；若一个保持、另一个翻转，二者必须对易。
        这些条件成立时，取
        \(A_{\mathrm{cone}}=-\eta\) 便有
        \[
          \eta A_{\mathrm{cone}}
          +A_{\mathrm{cone}}^\dagger\eta=-2I<0 .
        \]
        而且
        \(gA_{\mathrm{cone}}+A_{\mathrm{cone}}^Tg=0\) 与
        \(J_1^TA_{\mathrm{cone}}J_1=\overline A_{\mathrm{cone}}\)
        也逐项成立。因此这两个条件不仅排除 48 类，也显式证明其余
        16 类确实有严格负定方向。
      </div>
    """


def group_block(row: dict[str, str]) -> str:
    formula = sum_formula(
        r"A_{\mathrm{group}}", row["maximal_terms"]
    )
    table = coefficient_table(
        row["maximal_terms"], row["statistics"]
    )
    return rf"""
      <h4>\(A_{{\mathrm{{group}}}}\)：maximal subgroup 的全部生成元</h4>
      <p>这里的“全部”是指所列最小代表及其
      \(J_a\otimes I_m\) 扩展。生成元同时满足</p>
      <div class="scroll">\[
        \boxed{{
        \begin{{aligned}}
          gA_{{\mathrm{{group}}}}+A_{{\mathrm{{group}}}}^Tg&=0,\\
          J_1^TA_{{\mathrm{{group}}}}J_1
            &=\overline{{A_{{\mathrm{{group}}}}}},\\
          J_2^TA_{{\mathrm{{group}}}}J_2
            &=\overline{{A_{{\mathrm{{group}}}}}},\\
          \eta A_{{\mathrm{{group}}}}
            +A_{{\mathrm{{group}}}}^\dagger\eta&=0 .
        \end{{aligned}}}}
      \]</div>
      {formula}
      {table}
      <p class="small">
        每一行的 \(K_P\) 都是独立的 \(m\times m\) 矩阵。若
        \(m=1\)，满足 \(K_P^T=-K_P\) 的行自动为零；其余行仍可取
        任意满足表中条件的系数。
      </p>
    """


def cone_block(row: dict[str, str], full: dict[str, str]) -> str:
    if not int(row["strict_interior"]):
        if full["status"] == "boundary_only_trace_obstruction":
            reason = (
                r"本类有 \(J_2^2="
                + sign_rhs(row["q2"], "I")
                + r"\)，并满足迹阻碍引理的条件；所以"
                r" \(\operatorname{Tr}(\eta A)=0\) 与"
                r" \(\eta A<0\) 不相容。"
            )
            lemma = "迹阻碍引理"
        else:
            kappa = (
                int(full["tau"])
                * int(row["q2"])
                * int(row["s2"])
                * int(row["s1"])
                * int(row["r"])
            )
            if kappa != -1:
                raise RuntimeError("Unexpected reality-flip sign")
            reason = (
                r"本类逐项给出 "
                r"\(J_1^T\overline{(\eta A)}J_1=-\eta A\)，"
                r"所以一个负定矩阵会被等式送到它的正定相反数。"
            )
            lemma = r"\(J_1\) 翻转引理"
        return rf"""
          <h4>\(A_{{\mathrm{{cone}}}}\)：严格 invariant cone</h4>
          <div class="scope">
            <strong>没有解：</strong>
            \[
              \boxed{{\mathcal C=\varnothing}} .
            \]
            {reason} 因而本卡不再列“尚未施加不等式的候选空间”；
            那个线性空间不是 invariant cone，也不能提供严格收缩。
            本类引用的是前面的<strong>{lemma}</strong>。
          </div>
        """

    formula = sum_formula(
        r"A_{\mathrm{cone}}", row["cone_linear_terms"]
    )
    table = coefficient_table(
        row["cone_linear_terms"], row["statistics"]
    )
    return rf"""
      <h4>\(A_{{\mathrm{{cone}}}}\)：严格 invariant cone 的全部约束</h4>
      <p>这一类通过了两个引理。\(A_{{\mathrm{{cone}}}}\) 必须同时满足</p>
      <div class="scroll">\[
        \boxed{{
        \begin{{aligned}}
          gA_{{\mathrm{{cone}}}}+A_{{\mathrm{{cone}}}}^Tg&=0,\\
          J_1^TA_{{\mathrm{{cone}}}}J_1
            &=\overline{{A_{{\mathrm{{cone}}}}}},\\
          J_2^TA_{{\mathrm{{cone}}}}J_2
            &=-\overline{{A_{{\mathrm{{cone}}}}}},\\
          \eta A_{{\mathrm{{cone}}}}
            -A_{{\mathrm{{cone}}}}^\dagger\eta&=0,\\
          \eta A_{{\mathrm{{cone}}}}
            +A_{{\mathrm{{cone}}}}^\dagger\eta&<0 .
        \end{{aligned}}}}
      \]</div>
      <p>
        第四式说明 \(\eta A_{{\mathrm{{cone}}}}\) 是 Hermitian 矩阵，
        所以最后一式等价于
        \(\eta A_{{\mathrm{{cone}}}}<0\)。先由前四个等式得到
      </p>
      {formula}
      {table}
      <p>
        表中每个 \(K_P\) 的转置与复共轭条件可以逐行写开；负定性却是
        <em>整块矩阵</em>
        \[
          \boxed{{
            \eta\sum_{{P\in\mathcal P}}P\otimes K_P<0}}
        \]
        的条件。不同 \(P\) 项一般不对易，因此不能把这一个矩阵不等式
        错拆成若干互相独立的标量不等式。本类 cone 非空已经由前面的
        充要条件证明；具体 Hamiltonian 应从这张表中选择满足整块负定
        条件且对应厄米算符的方向。
      </p>
    """


def physical_kernel_block(row: dict[str, str]) -> str:
    group_j1 = signed_word(row["s1"], r"\overline{B_{\mathrm{group}}}")
    group_j2 = signed_word(row["s2"], r"\overline{B_{\mathrm{group}}}")
    kernel_type = (
        "复对称" if row["statistics"] == "boson" else "复反对称"
    )
    statistic_name = "玻色" if row["statistics"] == "boson" else "费米"
    if int(row["strict_interior"]):
        cone_j1 = signed_word(
            row["s1"], r"\overline{B_{\mathrm{cone}}}"
        )
        cone_j2 = signed_word(
            -int(row["s2"]), r"\overline{B_{\mathrm{cone}}}"
        )
        table_rows = rf"""
          B_{{\mathrm{{group}}}}
            &{group_j1}&{group_j2}\\
          B_{{\mathrm{{cone}}}}
            &{cone_j1}&{cone_j2}
        """
        consequence = (
            r"group 与 cone 在 \(J_2\) 下相差一个负号；这正是五条关系"
            "能够把等号方向和收缩方向分开的原因。"
        )
    else:
        table_rows = rf"""
          B_{{\mathrm{{group}}}}
            &{group_j1}&{group_j2}
        """
        consequence = (
            r"本类没有 \(A_{\mathrm{cone}}\)，因此这里只列实际存在的 "
            "group kernel，不再展示被不等式排除的形式候选。"
        )
    return rf"""
      <h4>把矩阵条件翻译回二次 Hamiltonian kernel \(B=gA\)</h4>
      <p>
        实际二次算符是
        \(\hat h(A)=\frac12\hat\chi^T(gA)\hat\chi\)，所以物理上应检查
        \(B=gA\)，而不是把 \(A\) 本身误叫做 Hamiltonian matrix。
        本类的符号逐项给出
      </p>
      <div class="scroll">\[
        \begin{{array}}{{c|cc}}
          &J_1^TBJ_1&J_2^TBJ_2\\ \hline
          {table_rows}
        \end{{array}}
      \]</div>
      <p>
        此外 \(B^T={'B' if row["statistics"] == "boson" else '-B'}\)：
        在本报告采用的 Nambu 排序中，本卡的{statistic_name}
        \(B\) 是{kernel_type} kernel。{consequence}
      </p>
    """


def group_antilinear_analysis(row: dict[str, str]) -> tuple[str, list[int]]:
    """Explain the two actual anti-linear actions for a group-only class."""
    paragraphs: list[str] = []
    physical_kramers: list[int] = []
    for index in (1, 2):
        word = row[f"J{index}_word"]
        square = int(row[f"q{index}"])
        kernel_sign = int(row[f"s{index}"])
        matrix = pauli_word_tex(word)
        if kernel_sign == 1:
            equation = (
                rf"J_{index}^TB_{{\mathrm{{group}}}}J_{index}"
                r"=\overline{B_{\mathrm{group}}}"
            )
            if square == -1 and word[0] in ("I", "Z"):
                physical_kramers.append(index)
                meaning = rf"""
                  这个 \(J_{index}\) 的第一个 Pauli 因子是
                  \({PAULI_TEX[word[0]]}\)，所以它不交换 Nambu 的
                  particle 与 hole 两半。限制到 particle-number-conserving
                  generators 后，\(J_{index}\mathcal K\) 直接作用在
                  annihilation operators 上，而且
                  \((J_{index}\mathcal K)^2=-I\)。它因此是一条真正可用于
                  Kramers 配对的 physical time-reversal symmetry。
                """
            elif square == -1:
                meaning = rf"""
                  虽然 \((J_{index}\mathcal K)^2=-I\)，
                  \(J_{index}={matrix}\) 的第一个 Pauli 因子交换 particle
                  与 hole。因此它是 BdG/Nambu 空间中的反线性约束，
                  不是作用在 annihilation operators 内部的普通
                  Kramers time reversal；仅凭这一式不能套用文章的
                  number-conserving determinant 配对证明。
                """
            else:
                meaning = rf"""
                  这里 \((J_{index}\mathcal K)^2=+I\)。它使
                  \(B_{{\mathrm{{group}}}}\) 保持一个反线性 symmetry，
                  但不会产生 Kramers 二重简并；实本征值仍可单独出现。
                """
        else:
            equation = (
                rf"J_{index}^TB_{{\mathrm{{group}}}}J_{index}"
                r"=-\overline{B_{\mathrm{group}}}"
            )
            meaning = rf"""
              右边多出的负号说明 \(J_{index}\mathcal K\) 把
              Hamiltonian kernel 送到其相反数。它是 particle-hole/chiral
              型约束，而不是使同一个 \(B_{{\mathrm{{group}}}}\) 不变的
              time reversal；无论 \(J_{index}^2\) 取什么符号，这一条
              都不能单独给出 Kramers determinant positivity。
            """
        paragraphs.append(
            rf"""
              <li>
                \(J_{index}={matrix}\)：\({equation}\)，并且
                \(J_{index}^2={sign_rhs(square, "I")}\)。{meaning}
              </li>
            """
        )
    return (
        '<ul class="relation-analysis">' + "".join(paragraphs) + "</ul>",
        physical_kramers,
    )


def has_stable_number_conserving_direction(row: dict[str, str]) -> bool:
    """Whether the displayed tensor basis contains a traceful Hermitian free term."""
    traceful_word = "Z" + "I" * (int(row["n"]) - 1)
    return (traceful_word, "R_S") in parse_terms(
        row["maximal_number_conserving_terms"]
    )


def positivity_block(
    row: dict[str, str], maximal: dict[str, str]
) -> str:
    if int(row["strict_interior"]):
        if row["statistics"] == "boson" and row["metric"] == "J2g":
            return r"""
              <p class="result">
                <strong>本类的矩阵生成元形成收缩半群；下方物理代表给出
                grand-canonical 无符号构造。</strong>
                \(A_{\mathrm{group}}\) 满足
                \(\eta A_{\mathrm{group}}
                +A_{\mathrm{group}}^\dagger\eta=0\)，所以它沿着
                \(\eta\)-长度不变的方向传播；\(A_{\mathrm{cone}}\) 满足
                \(\eta A_{\mathrm{cone}}
                +A_{\mathrm{cone}}^\dagger\eta<0\)，所以它使这个长度
                严格减小。由
                \[
                  e^{A_{\mathrm{group}}^\dagger}\eta
                  e^{A_{\mathrm{group}}}=\eta,\qquad
                  e^{A_{\mathrm{cone}}^\dagger}\eta
                  e^{A_{\mathrm{cone}}}<\eta
                \]
                可见，同一 \(J_1,J_2,\eta\) 下这些时间片的有序乘积仍是
                \(\eta\)-收缩矩阵。
              </p>
              <p>
                对玻色问题还要把这个矩阵陈述与物理 Fock 空间中的求迹
                对应起来。单凭任意 Hermitian \(\eta\) 下的严格不等式，
                不能推出物理玻色求迹收敛；\(\eta\) 还必须与
                \((b,b^+)^T\) 的 oscillator representation 相容。
                下方模型没有省略这一步：它采用同一五条关系的物理适配
                代表，使 \(J_2g\) 成为标准 particle/hole signature，
                并含有稳定的厄米自由项。于是每个辅助场构型的 Gaussian
                演化算符都可求迹，传播矩阵不会遇到 bare-trace pole。
                辅助场空间连通，再以零场构型的正权重固定平方根分支，
                得到整个构型空间的非负权重。
              </p>
            """

        if row["statistics"] == "boson" and row["metric"] == "iJ2g":
            return r"""
              <p class="result">
                <strong>本类确实有严格的 \(iJ_2g\)-收缩矩阵锥；下方模型
                的无符号结论采用 canonical fixed-\(N\) 求迹。</strong>
                对本卡的 \(A_{\mathrm{group}}\) 与
                \(A_{\mathrm{cone}}\)，有序传播矩阵保持
                \[
                  \eta=iJ_2g,\qquad
                  \eta A_{\mathrm{group}}
                  +A_{\mathrm{group}}^\dagger\eta=0,\qquad
                  \eta A_{\mathrm{cone}}
                  +A_{\mathrm{cone}}^\dagger\eta<0 .
                \]
                这完整证明了矩阵层面的收缩半群结构。
              </p>
              <p>
                这里不能把“矩阵严格收缩”直接改写成
                grand-canonical 玻色 Fock trace 收敛。例如最小见证
                \(A_{\mathrm{cone}}=-\eta\) 虽满足上面的负定不等式，
                在物理 \((b,b^+)^T\) representation 中却可能只生成
                unitary 演化，高占据数求和并不衰减。下方模型因此固定
                总粒子数 \(N\)，使用
                \[
                  W_N(\phi)=
                  \operatorname{Tr}_{\mathcal H_N}\hat U(\phi).
                \]
                对有限格点，\(\mathcal H_N\) 是有限维空间，求迹必定有限；
                报告再对每个所列模型的 block character 单独证明
                \(W_N(\phi)\geq0\)。所以这里给出的 canonical 无符号结论
                是完整结论，并未借用不成立的 grand-canonical
                trace-class 推论。
              </p>
            """

        base = r"""
          <p class="result">
            <strong>本类由费米收缩半群给出无符号区域。</strong>
            \(A_{\mathrm{group}}\) 产生保持 \(\eta\) 的可逆运动，
            \(A_{\mathrm{cone}}\) 产生真正压入半群内部的运动。任意时间片
            只要由这两类允许方向组成并保持同一 \(J_1,J_2,\eta\)，有序
            乘积仍在同一半群中。相应的费米 Gaussian character
            非负，因此每个辅助场构型的权重非负。费米 Fock space
            本来有限维；与玻色情形不同，这里不需要用严格不等式来压低
            任意大的玻色占据数，也没有 bare-trace 收敛问题。
          </p>
        """
        if row["statistics"] == "fermion" and int(
            maximal["maximal_subgroup_sign_guaranteed"]
        ):
            name = (
                r"Majorana \(\{T^+,T^-\}\)"
                if maximal["mtr_class"] == "Majorana_Tplus_Tminus"
                else r"Kramers \(\{T^-,T^-\}\)"
            )
            base += rf"""
              <p>
                对本类的等号边界还能作一个独立校验：把两条反线性变换
                搬到实 Majorana 基底后，平方与相互关系正好是
                {name} 类。因此纯 \(A_{{\mathrm{{group}}}}\) 时间片的费米
                trace 已经非负；加入本类 \(A_{{\mathrm{{cone}}}}\) 后则可
                同时使用半群论证。
              </p>
            """
        return base

    anti_linear_text, physical_kramers = group_antilinear_analysis(row)

    if row["statistics"] == "boson":
        result = r"""
          <h4>这两个 \(J\) 对本类 \(gA\) 的实际正性含义</h4>
        """ + anti_linear_text
        if physical_kramers:
            indices = ", ".join(rf"\(J_{index}\mathcal K\)" for index in physical_kramers)
            note_case = (
                r"""
                  本卡的五个离散正负号正是 note 的玻色
                  time-reversal Case 1；其中
                  \(J_1\mathcal K\) 是文章所用的 physical Kramers
                  transformation，\(J_2\) 是它与 Nambu
                  particle/hole exchange 的组合。需要同时记住，本节
                  的 group 卡还额外要求
                  \(J_2^TA_{\mathrm{group}}J_2
                  =\overline{A_{\mathrm{group}}}\)，而文章的一般 TRS
                  slice 满足的是
                  \(J_2^TAJ_2=-\overline A^{\,T}\)。所以“离散正负号
                  相同”不等于“允许的 \(A\) 完全相同”；本卡只是文章
                  TRS 条件与当前 group 等式的更小交集。
                """
                if row["class_id"] == BOSON_TRS_CLASS
                else r"""
                  note 没有把这张交集卡另起一个 time-reversal 编号，
                  但卡片施加的第二条约束只会缩小允许的 generators，
                  不会破坏这里已经存在的 physical Kramers symmetry。
                """
            )
            if has_stable_number_conserving_direction(row):
                stable_text = rf"""
                  本卡的 \(P\)-\(K_P\) 表还包含
                  \[
                    A_0=-\kappa\,
                    {pauli_word_tex("Z" + "I" * (int(row["n"]) - 1))}
                    \otimes I_m,\qquad \kappa>0 .
                  \]
                  它对应正的 one-particle energy
                  \(\kappa\sum_i b_i^+b_i\)，使零场传播的全部本征值模
                  小于 1。因此本卡确有 bare trace 有限的
                  grand-canonical 参考构型；在与 pole 不相交的连通
                  区域中，Kramers determinant 配对给出正权重。
                """
            else:
                stable_text = r"""
                  但本卡所列最小代表还有一个必须就地说明的限制：表中的
                  particle-number-conserving 厄米 one-particle
                  generators 全部无迹。任意这类时间片的 particle block
                  \(D_\ell\) 因而满足
                  \[
                    \operatorname{Tr}D_\ell=0,\qquad
                    |\det e^{D_\ell}|=e^{\operatorname{ReTr}D_\ell}=1 .
                  \]
                  有序乘积 \(\mathcal B\) 仍有
                  \(|\det\mathcal B|=1\)。若它的所有本征值都满足
                  \(|\lambda|<1\)，则
                  \(|\det\mathcal B|=\prod_\lambda|\lambda|<1\)，与前式
                  矛盾。因此这个最小代表虽然有 Kramers determinant
                  配对，却没有只靠本卡 number-conserving group
                  generators 构成的、bare trace 有限的
                  grand-canonical 热分支。要得到可模拟模型，必须换用
                  同一五符号类的物理适配表示并重新求 \(A\) 交集，或再
                  加一条与原 \(J_1,J_2\) 同时相容的稳定方向。
                """
            result += rf"""
              <p class="result">
                <strong>本卡的 particle-number-conserving group 子空间
                具有 Kramers determinant 配对。</strong>
                可直接使用 {indices}。对任意由这些
                number-conserving generators 构成的传播矩阵
                \(\mathcal B\)，非实本征值成
                \((\lambda,\overline\lambda)\) 对，实本征值具有偶数
                重数，所以
                \[
                  \det(I-\mathcal B)=
                  \prod_{{\lambda\notin\mathbb R}}|1-\lambda|^2
                  \prod_{{\lambda\in\mathbb R}}
                  (1-\lambda)^{{\mathrm{{even}}}}\geq0 .
                \]
                {note_case}
              </p>
              <p>{stable_text}</p>
            """
        else:
            result += r"""
              <p class="scope">
                <strong>因此，本卡原有的两条反线性约束没有给出
                number-conserving Kramers positivity。</strong>
                上面的结论来自本卡实际 \(J_1,J_2\) 对 \(gA\) 的作用，
                不是根据类别名称猜测。若另加一条保持 annihilation
                子空间、平方为 \(-I\) 的 physical time reversal，
                必须把它作为第三个明确矩阵写出并重新求交集。
              </p>
            """
        if row["class_id"] == BOSON_RP_CLASS:
            result += r"""
              <p class="result">
                <strong>本卡同时是 note 所称的 reflection-positivity
                离散类别。</strong>
                \(J_1^2=+I\)、\(J_2^2=-I\) 与
                \(J_1J_2=-J_2J_1\) 给出一对 reflected sectors 的代数
                骨架。对于含 pairing 的模型，还要在本卡 group algebra
                内逐块检查跨反射系数
                \(F=F^\dagger\succeq0\)。满足这条附加条件时，有限
                bare trace 可写成 reflected operator squares 的和，
                因而非负；这一 RP 证明允许 pairing，不依赖上一段只适用
                于 particle-number-conserving slices 的 Kramers 证明。
              </p>
            """
        return result

    if row["statistics"] == "fermion" and int(
        maximal["maximal_subgroup_sign_guaranteed"]
    ):
        name = (
            r"Majorana \(\{T^+,T^-\}\)"
            if maximal["mtr_class"] == "Majorana_Tplus_Tminus"
            else r"Kramers \(\{T^-,T^-\}\)"
        )
        return rf"""
          <h4>这两个 \(J\) 对本类 \(gA\) 的实际正性含义</h4>
          {anti_linear_text}
          <p class="result">
            <strong>本类只有 maximal subgroup，但已经是完整的费米
            无符号类。</strong>
            把本卡列出的 \(J_1,J_2\) 变到实 Majorana 基底后，直接得到
            \[
              T_1^2={sign_rhs(maximal["majorana_q1"], "I")},\qquad
              T_2^2={sign_rhs(maximal["majorana_q2"], "I")},\qquad
              T_1T_2={signed_word(maximal["majorana_r"], "T_2T_1")}.
            \]
            这正是 {name}，不是另加的一套 Kramers 模板。它使 Gaussian
            trace 分解成实平方或一对共轭因子的乘积。因此任意
            \(A_{{\mathrm{{group}}}}\) 时间片的有序乘积都有非负权重；
            费米 Hilbert space 有限，所以不需要
            \(A_{{\mathrm{{cone}}}}\) 来排除 bare-trace pole。
          </p>
        """

    negative_count = int(maximal["random_negative_count"])
    subgroup_dimension = int(maximal["maximal_subgroup_dimension"])
    if negative_count:
        numerical_check = rf"""
          对本卡最小代表，从完整
          \(A_{{\mathrm{{group}}}}\) 基底随机组成 600 组有序传播后，
          已找到 {negative_count} 组负 Fock trace；最小值为
          \({float(maximal["random_min_real_weight"]):.6g}\)。
          一个负例已经足以排除“本卡五条关系保证任意 group product
          非负”这一命题。
        """
    elif subgroup_dimension == 0:
        numerical_check = r"""
          本卡最小代表在 \(m=1\) 时
          \(A_{\mathrm{group}}=0\)，所以只有恒等传播，正权重是平凡的。
          当 \(m\geq2\) 时，\(K_P^T=-K_P\) 的行可以变成非零；这时必须
          使用上面的完整 \(P\)-\(K_P\) 表重新判断，不能把最小表示的
          平凡结果外推到所有重数。
        """
    else:
        numerical_check = rf"""
          本卡最小代表的 600 组随机乘积没有出现负值，但这不是正性证明：
          其 Majorana 反线性 pair 不属于两个已知的非负类，而且随机抽样
          不能覆盖整个连续 group。卡片因此只保留精确代数结论。
        """
    mtr_description = {
        "commuting_pair_not_generic": (
            "两条 Majorana 反线性变换彼此对易"
        ),
        "Tplus_Tplus_not_generic": (
            r"两条 Majorana 反线性变换彼此反对易，但二者平方都为 \(+I\)"
        ),
    }[maximal["mtr_class"]]
    positive_pair_names = (
        r"Majorana \(\{T^+,T^-\}\) 或 Kramers "
        r"\(\{T^-,T^-\}\)"
    )
    return rf"""
      <h4>这两个 \(J\) 对本类 \(gA\) 的实际正性含义</h4>
      {anti_linear_text}
      <p>
        在实 Majorana 基底中，本卡两条反线性变换满足
        \[
          T_1^2={sign_rhs(maximal["majorana_q1"], "I")},\qquad
          T_2^2={sign_rhs(maximal["majorana_q2"], "I")},\qquad
          T_1T_2={signed_word(maximal["majorana_r"], "T_2T_1")}.
        \]
        也就是说，{mtr_description}；它不等于
        {positive_pair_names} 的一般正性类。{numerical_check}
      </p>
      <p class="scope">
        因此本卡五条关系精确确定了 group algebra，却没有给出整个
        group 的费米无符号定理。一个具体 Hamiltonian 仍可在该
        algebra 内取更小的共轭分块、Majorana-RP 或 physical Kramers
        子空间；那是对本卡 \(P\)-\(K_P\) 系数的附加限制，必须明确写出。
      </p>
    """


def strict_model_key(row: dict[str, str]) -> str:
    prefix = "B" if row["statistics"] == "boson" else "F"
    s1 = "+" if int(row["s1"]) == 1 else "-"
    q1 = "+" if int(row["q1"]) == 1 else "-"
    return f"{prefix}-{row['metric']}-s1{s1}q1{q1}"


def boson_special_model(row: dict[str, str]) -> str:
    if row["class_id"] != BOSON_RP_CLASS:
        raise RuntimeError("boson_special_model is reserved for the RP card")
    return r"""
      <section class="model-example">
        <p class="model-title"><strong>该类自身可证明无符号的物理模型：
        带反射配对的阻挫双层玻色模型</strong></p>
        <p>
          令 \(b_i\) 与 \(c_i\) 位于一对被 reflection 交换的层，取
          \[
          \begin{aligned}
            H_0={}&\sum_{ij}\!\left[
              b_i^+D_{ij}b_j+c_i^+\overline D_{ij}c_j\right]\\
              &+\sum_{ij}\!\left[
              b_iF_{ij}c_j+b_i^+F_{ij}c_j^+\right],
              \qquad F=F^\dagger\succeq0 ,
          \end{aligned}
          \]
          并加入可写成
          \(\sum_{\mu\nu}C_{\mu\nu}X_\mu\theta(X_\nu)\)、
          \(C\succeq0\) 的 reflected density 或 bond interactions。
          \(D\) 可包含三角或 kagome 格子的复 hopping 与无序，
          \(F\) 则是层间 pair injection 或 parametric coupling。
          在 reflected-sector Nambu 排序中，固定场 slice 的 kernel 为
          \[
            B_\ell=
            \begin{pmatrix}
              D_\ell&F_\ell\\
              F_\ell^T&\overline D_\ell
            \end{pmatrix},
            \qquad F_\ell=F_\ell^\dagger\succeq0 .
          \]
          本卡的 \(J_1,J_2\) 等式负责产生这对 reflected sectors；
          \(F_\ell\succeq0\) 是不能从五个正负号中省略的 RP 条件。
        </p>
        <p>
          该模型适合研究阻挫平带上的 pair condensation、层间
          squeezed phases 与密度序竞争。它允许真正的 pairing，因此
          不是把 number-conserving TRS 模型重复换名。
        </p>
      </section>
    """


def representative_probe_model(
    row: dict[str, str], number: int
) -> str:
    terms = parse_terms(row["maximal_terms"])
    hermitian = [
        term for term in terms
        if physical_adjoint(row["statistics"], *term) == "Hermitian"
    ]
    antihermitian = [
        term for term in terms
        if physical_adjoint(row["statistics"], *term) == "anti-Hermitian"
    ]
    internal_modes = 2 ** (int(row["n"]) - 1)
    mode_text = (
        "一个物理模，不含内部 flavor"
        if internal_modes == 1
        else f"{internal_modes} 个 annihilation modes"
    )
    stable_word = "Z" + "I" * (int(row["n"]) - 1)
    stable_term = (
        (stable_word, "R_S")
        if (stable_word, "R_S") in hermitian
        else None
    )
    hermitian_number_conserving = [
        term for term in hermitian if term[0][0] in ("I", "Z")
    ]
    free_term = stable_term or (
        hermitian_number_conserving[0]
        if hermitian_number_conserving
        else (hermitian[0] if hermitian else None)
    )
    antihermitian_pairing = [
        term for term in antihermitian if term[0][0] in ("X", "Y")
    ]
    hermitian_pairing = [
        term for term in hermitian if term[0][0] in ("X", "Y")
    ]
    hermitian_pairing_not_free = [
        term for term in hermitian_pairing if term != free_term
    ]
    antihermitian_nontrivial = [
        term
        for term in antihermitian
        if any(letter != "I" for letter in term[0])
    ]
    hermitian_interactions = [
        term for term in hermitian if term != free_term
    ]
    interaction_term = (
        antihermitian_pairing[0]
        if antihermitian_pairing
        else (
            hermitian_pairing_not_free[0]
            if hermitian_pairing_not_free
            else (
                hermitian_pairing[0]
                if hermitian_pairing
                else (
                    antihermitian_nontrivial[0]
                    if antihermitian_nontrivial
                    else (
                        antihermitian[0]
                        if antihermitian
                        else (
                            hermitian_interactions[0]
                            if hermitian_interactions
                            else free_term
                        )
                    )
                )
            )
        )
    )

    if free_term is None:
        free_construction = r"""
          <p>
            本卡完整 \(A_{\mathrm{group}}\) 表中没有使
            \(\hat h(A)\) Hermitian 的非零方向。因此这个最小表示不能
            在不离开本卡 group algebra 的前提下写出二次自由
            Hamiltonian；它只能提供下面的 quartic HS 通道。扩大
            \(m\) 只会让表中的 \(K_P\) 变大，不会改变这一厄米性结论。
          </p>
        """
    else:
        free_word, free_type = free_term
        free_transpose, free_conjugation = coefficient_equations(
            "K_0", free_type
        )
        free_realization = coefficient_realization(
            "K_0", free_type, "自由项"
        )
        if stable_term is not None:
            stability = r"""
              这一行含有 one-particle identity component。取
              \(K_0=\kappa I_m\)、\(\kappa>0\)，并选择正号
              \(\hat H_0=\hat h(G_0)\)，即可得到单粒子矩阵迹非零的
              正能量参考项。
            """
        elif row["statistics"] == "boson":
            stability = r"""
              这给出合法的厄米二次项，但该行的 one-particle trace
              为零，所以它本身不能作为玻色 grand-canonical
              稳定参考项。
            """
        else:
            stability = r"""
              这给出合法的厄米二次项。费米 Fock 空间在有限格点上是
              有限维的，所以 one-particle trace 是否为零不承担
              bare-trace 收敛条件。
            """
        free_construction = rf"""
          <p>
            本卡可直接选取
            \[
              G_0={pauli_word_tex(free_word)}\otimes K_0,\qquad
              {free_transpose},\qquad {free_conjugation} .
            \]
            因为 \(\hat h(G_0)=\frac12\hat\chi^TgG_0\hat\chi\)
            是 Hermitian，\(\hat H_0=u_0\hat h(G_0)\) 是本卡实际允许的
            二次自由项，虚时间生成元为
            \(A_0=-\Delta\tau u_0G_0\in A_{{\mathrm{{group}}}}\)。
            {stability}
            {free_realization}
          </p>
        """

    if interaction_term is None:
        interaction_construction = (
            r"<p>本卡最小表示没有非零 HS interaction direction。</p>"
        )
    else:
        interaction_word, interaction_type = interaction_term
        interaction_transpose, interaction_conjugation = (
            coefficient_equations("K_1", interaction_type)
        )
        interaction_realization = coefficient_realization(
            "K_1", interaction_type, "相互作用通道"
        )
        interaction_matrix = pauli_word_tex(interaction_word)
        if physical_adjoint(
            row["statistics"], interaction_word, interaction_type
        ) == "anti-Hermitian":
            interaction_construction = rf"""
              <p>
                选取
                \[
                  G_1={interaction_matrix}\otimes K_1,\qquad
                  {interaction_transpose},\qquad
                  {interaction_conjugation} .
                \]
                这时 \(\hat X=-i\hat h(G_1)\) 是 Hermitian。厄米相互作用
                \[
                  \hat H_{{\mathrm{{int}}}}=+\frac U2\hat X^2,\qquad U>0
                \]
                具有正 Gaussian HS identity
                \[
                  e^{{-\Delta\tau U\hat X^2/2}}
                  \propto\int d\phi\,e^{{-\phi^2/2}}
                  e^{{\sqrt{{\Delta\tau U}}\phi\,\hat h(G_1)}} ,
                \]
                所以每个场值的生成元
                \(A_{{\mathrm{{HS}}}}(\phi)
                =\sqrt{{\Delta\tau U}}\phi\,G_1\) 都确实属于本卡列出的
                \(A_{{\mathrm{{group}}}}\) 中。
                {interaction_realization}
              </p>
            """
        else:
            interaction_construction = rf"""
              <p>
                选取
                \[
                  G_1={interaction_matrix}\otimes K_1,\qquad
                  {interaction_transpose},\qquad
                  {interaction_conjugation} .
                \]
                此时 \(\hat X=\hat h(G_1)\) 是 Hermitian。吸引相互作用
                \[
                  \hat H_{{\mathrm{{int}}}}=-\frac U2\hat X^2,\qquad U>0
                \]
                可用实 Gaussian 场分解，逐场生成元同样是
                \(A_{{\mathrm{{HS}}}}(\phi)
                =\sqrt{{\Delta\tau U}}\phi\,G_1
                \in A_{{\mathrm{{group}}}}\)。
                {interaction_realization}
              </p>
            """

    number_conserving = any(word[0] in ("I", "Z") for word, _ in terms)
    pairing = any(word[0] in ("X", "Y") for word, _ in terms)
    try:
        research_title, research_target = GROUP_ONLY_RESEARCH_PROGRAMS[
            row["statistics"]
        ][number]
    except KeyError as error:
        raise RuntimeError(
            f"Missing group-only research program for "
            f"{row['statistics']} card {number:02d}"
        ) from error
    channel_text = (
        "粒子数守恒与 pairing"
        if number_conserving and pairing
        else ("粒子数守恒" if number_conserving else "pairing")
    )
    return rf"""
      <section class="model-example">
        <p class="model-title"><strong>由本类实际
        \(A_{{\mathrm{{group}}}}\) 得到的研究模型：
        {research_title}</strong></p>
        <p>
          这个最小表示的物理内容是：{mode_text}。后面的 \(K_P\)
          承担格点或轨道
          重复指标；这里不为统一格式额外添加 \(\sigma\) 标记的 flavor。
          上表显示它允许 {channel_text} 通道。
        </p>
        {free_construction}
        {interaction_construction}
        <p>
          <strong>这个模型值得研究的物理问题。</strong>
          {research_target}
          这些二次项和 HS 方向都来自本卡的明确行，不是额外套入的
          flavor 模板。由于前面的逐类分析尚未给出整个
          \(A_{{\mathrm{{group}}}}\) 的非负定理，这里得到的是
          <strong>厄米、对称性兼容、但尚待再加正性条件的研究模型</strong>；
          不能把“生成元属于本类”直接改写为“已经无符号”。
        </p>
      </section>
    """


def physical_model(
    row: dict[str, str], maximal: dict[str, str], number: int
) -> str:
    if int(row["strict_interior"]):
        return render_physical_model(strict_model_key(row))
    if (
        row["statistics"] == "boson"
        and row["class_id"] == BOSON_RP_CLASS
    ):
        return boson_special_model(row)
    if row["statistics"] == "fermion" and int(
        maximal["maximal_subgroup_sign_guaranteed"]
    ):
        return render_maximal_only_model(row["class_id"])
    return representative_probe_model(row, number)


def number_conserving_block(row: dict[str, str]) -> str:
    group_terms = row["maximal_number_conserving_terms"]
    group_formula = sum_formula(
        r"A_{\mathrm{group}}^{(N)}", group_terms
    )
    group_table = coefficient_table(
        group_terms, row["statistics"], compact=True
    )
    if int(row["strict_interior"]):
        cone_formula = sum_formula(
            r"A_{\mathrm{cone}}^{(N)}",
            row["cone_number_conserving_terms"],
        )
        cone_table = coefficient_table(
            row["cone_number_conserving_terms"],
            row["statistics"],
            compact=True,
        )
        cone_content = rf"""
          <p>\(A_{{\mathrm{{cone}}}}^{{(N)}}\) 的等式解为</p>
          {cone_formula}
          {cone_table}
          <p>它仍必须整体满足
          \(\eta A_{{\mathrm{{cone}}}}^{{(N)}}<0\)。若表为空，则这个代表的
          严格方向只能含 pairing；不能从完整 cone 非空推断
          number-conserving cone 也非空。</p>
        """
    else:
        cone_content = (
            r"<p>本类严格 \(A_{\mathrm{cone}}\) 已由上面的引理排除，"
            "所以 number-conserving 子空间中同样没有严格 cone 解。</p>"
        )
    return rf"""
      <details>
        <summary>只看 particle-number-conserving 子空间</summary>
        <p>\(A_{{\mathrm{{group}}}}^{{(N)}}\) 的全部项为</p>
        {group_formula}
        {group_table}
        {cone_content}
      </details>
    """


def case_card(
    row: dict[str, str],
    maximal: dict[str, str],
    full: dict[str, str],
    number: int,
) -> str:
    statistic_name = "玻色" if row["statistics"] == "boson" else "费米"
    dimension = 2 ** int(row["n"])
    if int(row["strict_interior"]):
        cone_label = (
            rf"\(A_{{\mathrm{{cone}}}}\neq\varnothing\)，"
            rf"metric={row['metric']}"
        )
    elif row["statistics"] == "boson" and row["class_id"] == BOSON_RP_CLASS:
        cone_label = "group-only；玻色 RP 骨架与稳定 Kramers 子空间"
    elif row["statistics"] == "boson":
        _, physical_kramers = group_antilinear_analysis(row)
        if physical_kramers and has_stable_number_conserving_direction(row):
            cone_label = "group-only；Kramers determinant 配对与稳定方向"
        elif physical_kramers:
            cone_label = "group-only；Kramers determinant 配对，但本代表无稳定方向"
        else:
            cone_label = "group-only；五条关系本身无正性定理"
    elif row["statistics"] == "fermion" and int(
        maximal["maximal_subgroup_sign_guaranteed"]
    ):
        cone_label = "group-only；费米 MTR 正性"
    else:
        cone_label = "group-only；五条关系本身无正性定理"
    card_id = f"class-{row['statistics']}-{number:02d}"
    return rf"""
      <details class="all-class-card" id="{card_id}">
        <summary>
          {statistic_name} {number:02d}：{summary_relations(row)}；
          最小 Nambu 维数 {dimension}；{cone_label}
        </summary>
        <div class="all-class-body tex2jax_ignore">
          <h4>五条关系与本卡采用的最小代表</h4>
          {relation_block(row, dimension)}
          <p>
            Pauli word 的第一个因子始终是 Nambu particle/hole 空间。
            若总维数为 2，就只有一个 annihilation mode，并没有隐藏的
            内部 flavor。后续因子才是这个最小代表真正需要的内部空间；
            \(K_P\) 则作用在额外的 \(m\) 维格点、轨道或 flavor
            重复空间。
          </p>
          {group_block(row)}
          {cone_block(row, full)}
          {physical_kernel_block(row)}
          {positivity_block(row, maximal)}
          {physical_model(row, maximal, number)}
          {number_conserving_block(row)}
        </div>
      </details>
    """


def representation_answer() -> str:
    return r"""
      <h4>固定一组 \(J_1,J_2\) 会不会漏掉允许的 \(A\)</h4>
      <p>
        先回答“某一五符号类别有没有严格收缩方向”。前面的两个引理只用
        \(J_1,J_2\) 的五个正负号，完全没有使用某个 Pauli word。
        因而，同一类别换成另一组矩阵表示，不会把空 cone 变成非空，也
        不会把非空 cone 变成空。16 个严格类的数目不会因代表选择改变。
      </p>
      <p>
        但“允许的 \(A\) 一共有多少个独立方向”确实依赖表示。原因很具体：
        五个正负号没有记录 \(J_1,J_2\) 的共同本征子空间各重复了多少次。
        程序用同一个费米 all-plus 类的三个 8 维表示作过直接比较：
      </p>
      <div class="scroll">
        <table>
          <thead><tr><th>8 维表示</th>
          <th>满足全部 group 等式的实维数</th>
          <th>满足 cone 等式、尚未施加负定条件的实维数</th></tr></thead>
          <tbody>
            <tr><td>重数平衡的 Pauli 表示</td><td>12</td><td>16</td></tr>
            <tr><td>第一种不平衡重数</td><td>12</td><td>16</td></tr>
            <tr><td>第二种不平衡重数</td><td>21</td><td>7</td></tr>
          </tbody>
        </table>
      </div>
      <p>
        因此每张卡的 \(P\)–\(K_P\) 表是对“卡上所列最小代表以及
        \(J_a\otimes I_m\) 扩展”的完整答案，不是假称覆盖同一五符号
        类的全部不等价表示。若实际模型给出另一组 \(J_1,J_2\)，就应把
        它们直接代入卡片所写的四组等式重新求解。两组表示若只差一个
        保持 \(g\) 的 basis change，允许的 \(A\) 只是相似变换，不会
        漏解；只有共同子空间的重数真正不同，解空间维数才会改变。
      </p>
    """


def minimal_dimension_proof() -> str:
    return r"""
      <h4>最小维数怎样读：2、4、8 分别意味着什么</h4>
      <p>
        维数 2 的 Nambu spinor 是 \((a,a^+)^T\)，只含一个物理模。
        维数 4 才需要两个 annihilation modes；维数 8 需要四个。
        因此卡片写“最小维数 2”时，后面的模型不会为了统一格式再强行
        加一个内部 \(\sigma\) 自由度。
      </p>
      <div class="scroll">
        <table>
          <thead><tr><th></th><th>2 维即可</th><th>最小为 4 维</th>
          <th>最小为 8 维</th></tr></thead>
          <tbody>
            <tr><td>玻色 32 类</td><td>7</td><td>24</td><td>1</td></tr>
            <tr><td>费米 32 类</td><td>11</td><td>20</td><td>1</td></tr>
          </tbody>
        </table>
      </div>
      <p>
        2 维的检查可以直接做完。玻色取
        \(g=-i\sigma_y\)：\(I\) 保持 \(g\) 且平方为 \(I\)，
        \(\sigma_x,\sigma_z\) 翻转 \(g\) 且平方为 \(I\)，
        \(i\sigma_y\) 保持 \(g\) 且平方为 \(-I\)。费米取
        \(g=\sigma_x\)：\(I,\sigma_x\) 保持 \(g\) 且平方为 \(I\)，
        \(\sigma_z\) 翻转 \(g\) 且平方为 \(I\)，
        \(i\sigma_y\) 翻转 \(g\) 且平方为 \(-I\)。
        将这些可能逐对组合并检查二者对易或反对易，就得到上表的
        7 类与 11 类。其余类别至少需要 4 维。
      </p>
      <p>
        两个 Pauli 因子的所有乘积已经给出玻色另外 24 类和费米另外
        20 类。只剩各一个例外：
      </p>
      <div class="scroll">\[
        \begin{array}{c|ccccc|cc}
        &J_1^TgJ_1&J_1^2&J_2^TgJ_2&J_2^2&J_1J_2
        &J_1&J_2\\ \hline
        \text{玻色}&-g&-I&-g&-I&+J_2J_1&XIY&XXY\\
        \text{费米}&+g&-I&+g&-I&-J_2J_1&IIY&IYX
        \end{array}
      \]</div>
      <details>
        <summary>为什么这两个例外确实不能压到 4 维</summary>
        <p>
          玻色情形中，\(J_1,J_2\) 对易且都平方为 \(-I\)。令
          \(K=J_1J_2\)，则 \(K^2=I\)，空间分成 \(K=+1\) 与
          \(K=-1\) 两部分。两个部分彼此不由 \(g\) 配对，每一部分都
          必须单独带一个非退化的玻色 Nambu 结构。与此同时 \(J_1\)
          在每一部分都平方为 \(-I\) 并翻转 \(g\)。在二维实空间中，
          “翻转 \(g\)”的矩阵行列式为 \(-1\)，而“平方为 \(-I\)”
          的矩阵行列式为 \(+1\)，二者矛盾；所以每一部分至少 4 维，
          两部分合计至少 8 维。
        </p>
        <p>
          费米情形中，\(J_1,J_2\) 反对易且都平方为 \(-I\)。从任一
          向量 \(v\) 出发，\(v,J_1v,J_2v,J_1J_2v\) 构成一个四元组；
          反对易关系保证四者不能出现非平凡实线性关系。两条矩阵又都
          保持 \(g\)，所以这个四元组的四个 \(g\)-norm 同号。标准
          4 维费米 Nambu metric 有两个正方向、两个负方向，容不下一个
          四个方向全同号的组；8 维的四正、四负才可由一个正组与一个
          负组实现。
        </p>
      </details>
    """


def atlas_guide() -> str:
    return r"""
      <div class="note">
        <strong>64 张卡片不再与另一个“16 类清单”重复。</strong>
        每张卡依次给出：最小 \(J_1,J_2\)；满足全部等式的
        \(A_{\mathrm{group}}\)；若存在则给出真正满足严格不等式的
        \(A_{\mathrm{cone}}\)；\(B=gA\) 的物理对称性；该类自身能够
        证明的正性；最后才是与实际矩阵方向相连的物理模型。
      </div>
      <p>
        图 1 是这些卡片的目录式“周期表”。每格的 B/F 编号与下方卡片
        编号一致；\(d=2,4,8\) 是最小 Nambu 维数；C(J) 与 C(iJ)
        表示两种 metric 下的严格 contraction cone；Kdet(N) 表示卡片所列
        代表的 particle-number-conserving group 子空间具有 Kramers
        determinant 配对，是否另有稳定热分支要看卡片中的 trace 检查；
        RP、MTR 分别表示 reflection positivity 与费米
        Majorana-time-reversal 正性，G 表示目前只得到 maximal
        subgroup。格子底部同时
        标出空 cone 是被迹引理还是 \(J_1\) 翻转引理排除。
      </p>
    """


def lazy_mathjax_script() -> str:
    return r"""
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
    if not (
        len(tensor_rows) == len(maximal_rows) == len(full_rows) == 64
    ):
        raise RuntimeError("Expected 64 rows in every classification table")

    blocks = [
        atlas_guide(),
        lazy_mathjax_script(),
        defining_lemmas(),
        representation_answer(),
        minimal_dimension_proof(),
    ]
    for statistic, title in (
        ("boson", "玻色 32 类"),
        ("fermion", "费米 32 类"),
    ):
        blocks.append(f"<h4>{title}</h4>")
        number = 0
        for row in tensor_rows:
            if row["statistics"] != statistic:
                continue
            number += 1
            key = (row["statistics"], row["class_id"])
            blocks.append(
                case_card(
                    row,
                    maximal_rows[key],
                    full_rows[key],
                    number,
                )
            )
        if number != 32:
            raise RuntimeError(f"Expected 32 {statistic} rows, found {number}")

    blocks.append(
        r"""
        <p class="small">
          机器可读结果：
          <a href="tables/full_64_class_enumeration.csv">五符号、metric、
          最小维数与两个阻碍判据</a>；
          <a href="tables/tensor_block_structures.csv">每类
          \(P\otimes K_P\) 的完整等式解</a>；
          <a href="tables/maximal_subgroup_structures.csv">费米 MTR
          分类与数值抽样复核</a>；
          <a href="tables/nonpauli_realization_dependence.csv">同类不等价
          表示的维数对照</a>。
        </p>
        """
    )
    result = "\n".join(blocks)
    forbidden = (
        r"A_{\rm max}",
        r"A_{\max}",
        r"A_{\rm cone,lin}",
        r"A_{\rm cone}",
        "COMPONENT_COUNT",
        "MODEL_TITLE",
    )
    for marker in forbidden:
        if marker in result:
            raise RuntimeError(f"Forbidden or unresolved marker: {marker}")
    return result
