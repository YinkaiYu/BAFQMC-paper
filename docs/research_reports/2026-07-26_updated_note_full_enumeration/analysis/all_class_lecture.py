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
HALF_POWER_PATH = (
    REPORT_DIR / "tables" / "half_power_symmetry_64_classes.csv"
)
LOW_DIMENSIONAL_REPRESENTATIONS_PATH = (
    REPORT_DIR / "tables" / "real_representation_orbits_le4.csv"
)
BOSON_PHYSICAL_REPRESENTATIONS_PATH = (
    REPORT_DIR
    / "tables"
    / "bosonic_physical_representation_suborbits_le4.csv"
)


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
    ),
    "R_A": (
        r"K_P^T=-K_P",
        r"\overline{K_P}=K_P",
    ),
    "iR_S": (
        r"K_P^T=K_P",
        r"\overline{K_P}=-K_P",
    ),
    "iR_A": (
        r"K_P^T=-K_P",
        r"\overline{K_P}=-K_P",
    ),
}

BOSON_TRS_CLASS = "s1+_q1-_s2-_q2-_r+"
BOSON_RP_CLASS = "s1+_q1+_s2+_q2-_r-"
BOSON_KRAMERS_MIN_DIMENSION = {
    "s1+_q1-_s2+_q2-_r-": 8,
    BOSON_TRS_CLASS: 4,
    "s1-_q1-_s2+_q2-_r+": 4,
    "s1-_q1-_s2-_q2-_r-": 8,
}

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


def phased_word_label_tex(label: str) -> str:
    if label.startswith("-i"):
        return "-i" + pauli_word_tex(label[2:])
    if label.startswith("i"):
        return "i" + pauli_word_tex(label[1:])
    if label.startswith("-"):
        return "-" + pauli_word_tex(label[1:])
    return pauli_word_tex(label)


def pauli_word_numpy(word: str) -> np.ndarray:
    result = np.array([[1]], dtype=complex)
    for letter in word:
        result = np.kron(result, PAULI_NUMPY[letter])
    return result


def pauli_matrix_decomposition(matrix: np.ndarray) -> tuple[complex, str]:
    """Return coefficient and real-Pauli word for a single Pauli product."""
    n = int(round(np.log2(matrix.shape[0])))
    for letters in np.ndindex(*(4,) * n):
        word = "".join("IXYZ"[index] for index in letters)
        basis = pauli_word_numpy(word)
        coefficient = np.vdot(basis, matrix) / np.vdot(basis, basis)
        if np.linalg.norm(matrix - coefficient * basis) < 1e-10:
            for allowed in (1, -1, 1j, -1j):
                if abs(coefficient - allowed) < 1e-10:
                    return complex(allowed), word
    raise RuntimeError("Matrix is not a single real-Pauli word up to phase")


def phased_pauli_tex(coefficient: complex, word: str) -> str:
    # ``Y`` denotes the real matrix i sigma_y in the enumeration basis.  Eta
    # and eta A are usually clearer in the conventional complex Pauli basis.
    coefficient *= 1j ** word.count("Y")
    coefficient = min(
        (complex(1), complex(-1), complex(1j), complex(-1j)),
        key=lambda allowed: abs(coefficient - allowed),
    )
    conventional = {
        "I": "I_2",
        "X": r"\sigma_x",
        "Y": r"\sigma_y",
        "Z": r"\sigma_z",
    }
    body = r"\otimes ".join(conventional[letter] for letter in word)
    prefixes = {
        complex(1): "",
        complex(-1): "-",
        complex(1j): "i",
        complex(-1j): "-i",
    }
    return prefixes[complex(coefficient)] + body


def metric_matrix_and_tex(row: dict[str, str]) -> tuple[np.ndarray, str]:
    n = int(row["n"])
    identity = np.eye(2 ** (n - 1), dtype=complex)
    g = np.kron(
        -PAULI_NUMPY["Y"]
        if row["statistics"] == "boson"
        else PAULI_NUMPY["X"],
        identity,
    )
    eta = pauli_word_numpy(row["J2_word"]) @ g
    if row["metric"] == "iJ2g":
        eta = 1j * eta
    coefficient, word = pauli_matrix_decomposition(eta)
    return eta, phased_pauli_tex(coefficient, word)


def explicit_eta_product(
    row: dict[str, str], raw_terms: str
) -> str:
    eta, _ = metric_matrix_and_tex(row)
    pieces: list[str] = []
    for word, _ in parse_terms(raw_terms):
        coefficient, product_word = pauli_matrix_decomposition(
            eta @ pauli_word_numpy(word)
        )
        matrix_tex = phased_pauli_tex(coefficient, product_word)
        pieces.append(
            rf"{matrix_tex}\otimes K_{{{pauli_word_tex(word)}}}"
        )
    if not pieces:
        return "0"
    expression = pieces[0]
    for piece in pieces[1:]:
        expression += piece if piece.startswith("-") else f"+{piece}"
    return expression


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


def coefficient_kernel_tex(word: str) -> str:
    internal_word = word[1:]
    if not internal_word or set(internal_word) == {"I"}:
        return r"K_P"
    return rf"{pauli_word_tex(internal_word)}\otimes K_P"


def explicit_quadratic_operator(statistics: str, word: str) -> str:
    kernel = coefficient_kernel_tex(word)
    nambu = word[0]
    if statistics == "boson":
        if nambu == "I":
            return (
                rf"\(\displaystyle\sum_{{ij}}b_i^+"
                rf"({kernel})_{{ij}}b_j\)"
            )
        if nambu == "Z":
            return (
                rf"\(\displaystyle\sum_{{ij}}b_i^+"
                rf"({kernel})_{{ij}}b_j"
                rf"+\frac12\operatorname{{Tr}}({kernel})\)"
            )
        if nambu == "X":
            return (
                rf"\(\displaystyle\frac12\left["
                rf"\boldsymbol b^{{+T}}({kernel})\boldsymbol b^+"
                rf"-\boldsymbol b^T({kernel})\boldsymbol b\right]\)"
            )
        return (
            rf"\(\displaystyle\frac12\left["
            rf"\boldsymbol b^{{+T}}({kernel})\boldsymbol b^+"
            rf"+\boldsymbol b^T({kernel})\boldsymbol b\right]\)"
        )
    if nambu == "I":
        return (
            rf"\(\displaystyle\sum_{{ij}}c_i^+"
            rf"({kernel})_{{ij}}c_j\)"
        )
    if nambu == "Z":
        return (
            rf"\(\displaystyle\sum_{{ij}}c_i^+"
            rf"({kernel})_{{ij}}c_j"
            rf"-\frac12\operatorname{{Tr}}({kernel})\)"
        )
    if nambu == "X":
        return (
            rf"\(\displaystyle\frac12\left["
            rf"\boldsymbol c^T({kernel})\boldsymbol c"
            rf"+\boldsymbol c^{{+T}}({kernel})\boldsymbol c^+\right]\)"
        )
    return (
        rf"\(\displaystyle\frac12\left["
        rf"-\boldsymbol c^T({kernel})\boldsymbol c"
        rf"+\boldsymbol c^{{+T}}({kernel})\boldsymbol c^+\right]\)"
    )


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
        transpose, conjugation = COEFFICIENT_CONDITIONS[coefficient_type]
        operator = explicit_quadratic_operator(statistics, word)
        adjoint = physical_adjoint(statistics, word, coefficient_type)
        adjoint_text = (
            "该式本身为 Hermitian"
            if adjoint == "Hermitian"
            else r"\(-i\hat h\) 为 Hermitian"
        )
        if compact:
            rows.append(
                rf"<tr><td>\({pauli_word_tex(word)}\)</td>"
                rf"<td>\({transpose},\ {conjugation}\)</td>"
                rf"<td>{operator}</td></tr>"
            )
        else:
            rows.append(
                rf"<tr><td>\({pauli_word_tex(word)}\)</td>"
                rf"<td>\({transpose}\)</td>"
                rf"<td>\({conjugation}\)</td>"
                rf"<td>{operator}<br><span class='small'>{adjoint_text}</span>"
                rf"</td></tr>"
            )
    if compact:
        heading = (
            r"<tr><th>\(P\)</th><th>\(K_P\) 的完整条件</th>"
            r"<th>\(\hat h(P\otimes K_P)\)</th></tr>"
        )
    else:
        heading = (
            r"<tr><th>\(P\)</th><th>转置</th><th>复共轭</th>"
            r"<th>具体二次算符 \(\hat h(P\otimes K_P)\)</th></tr>"
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
    _, explicit_metric = metric_matrix_and_tex(row)
    return rf"""
      <div class="scroll">\[
        \begin{{gathered}}
          J_1={pauli_word_tex(row["J1_word"])},\qquad
          J_2={pauli_word_tex(row["J2_word"])},\qquad
          \eta={metric}={explicit_metric},\\
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


def group_block(row: dict[str, str]) -> str:
    formula = sum_formula(
        r"A_{\mathrm{group}}", row["maximal_terms"]
    )
    table = coefficient_table(
        row["maximal_terms"], row["statistics"]
    )
    return rf"""
      <h4>\(A_{{\mathrm{{group}}}}\)：本卡顶部代表的完整解</h4>
      <p>
      这一组公式解的是卡片顶部明确写出的 \(J_1,J_2\)，以及
      \(J_a\otimes I_m\) 的格点或轨道重复。其他二维、四维实现另列在本卡
      后面的可折叠表中。当前代表的生成元同时满足
      </p>
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
        任意满足表中条件的系数。表中 \(\boldsymbol b\) 或
        \(\boldsymbol c\) 包含 Pauli word 除第一个 Nambu 因子以外的内部
        指标以及 \(m\) 维重复指标；因此最后一列已经是可直接写进
        Hamiltonian 的算符，而不是“normal/pairing”标签。
      </p>
    """


def cone_block(row: dict[str, str], full: dict[str, str]) -> str:
    if not int(row["strict_interior"]):
        if full["status"] == "boundary_only_trace_obstruction":
            reason = (
                r"本类有 \(J_2^2="
                + sign_rhs(row["q2"], "I")
                + r"\)。由 <a href='#lemma-1'>引理1</a>，"
                r" \(\operatorname{Tr}(\eta A)=0\) 与"
                r" \(\eta A<0\) 不相容。"
            )
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
                r"由 <a href='#lemma-2'>引理2</a>，本类逐项给出 "
                r"\(J_1^T\overline{(\eta A)}J_1=-\eta A\)，"
                r"所以一个负定矩阵会被等式送到它的正定相反数。"
            )
        return rf"""
          <h4>\(A_{{\mathrm{{cone}}}}\)：严格 invariant cone</h4>
          <div class="scope">
            <strong>没有解：</strong>
            \[
              \boxed{{
                \nexists\,A_{{\mathrm{{cone}}}}\ \text{{同时满足本卡全部等式与 }}
                \eta A_{{\mathrm{{cone}}}}
                +A_{{\mathrm{{cone}}}}^\dagger\eta<0
              }} .
            \]
            {reason} 因而本卡不再列“尚未施加不等式的候选空间”；
            那个线性空间不是 invariant cone，也不能提供严格收缩。
          </div>
        """

    _, explicit_metric = metric_matrix_and_tex(row)
    explicit_product = explicit_eta_product(
        row, row["cone_linear_terms"]
    )
    formula = sum_formula(
        r"A_{\mathrm{cone}}", row["cone_linear_terms"]
    )
    table = coefficient_table(
        row["cone_linear_terms"], row["statistics"]
    )
    return rf"""
      <h4>\(A_{{\mathrm{{cone}}}}\)：严格 invariant cone 的全部约束</h4>
      <p>
      这一类满足<a href="#lemma-1">引理1</a>和
      <a href="#lemma-2">引理2</a>留下的条件。
      \(A_{{\mathrm{{cone}}}}\) 必须同时满足
      </p>
      <div class="scroll">\[
        \boxed{{
        \begin{{aligned}}
          gA_{{\mathrm{{cone}}}}+A_{{\mathrm{{cone}}}}^Tg&=0,\\
          J_1^TA_{{\mathrm{{cone}}}}J_1
            &=\overline{{A_{{\mathrm{{cone}}}}}},\\
          J_2^TA_{{\mathrm{{cone}}}}J_2
            &=-\overline{{A_{{\mathrm{{cone}}}}}},\\
          \eta A_{{\mathrm{{cone}}}}
            +A_{{\mathrm{{cone}}}}^\dagger\eta&<0 .
        \end{{aligned}}}}
      \]</div>
      <p>
        前三式已经保证 \(\eta A_{{\mathrm{{cone}}}}\) 是 Hermitian 矩阵，
        所以最后一式等价于
        \(\eta A_{{\mathrm{{cone}}}}<0\)。先由前三个等式得到
      </p>
      {formula}
      {table}
      <p>
        表中每个 \(K_P\) 的转置与复共轭条件可以逐行写开；负定性却是
        <em>整块矩阵</em>
        \[
          \eta={explicit_metric},\qquad
          \boxed{{
            \eta A_{{\mathrm{{cone}}}}
            ={explicit_product}<0}} .
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
            r"本类没有满足严格负定不等式的 \(A_{\mathrm{cone}}\)，"
            r"所以这里只列实际存在的 group kernel。"
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


def generalized_antilinear_is_physical(
    row: dict[str, str],
) -> tuple[bool, tuple[bool, bool]]:
    """Check whether transformed creation operators remain conjugates."""
    dimension = 2 ** int(row["n"])
    exchange = np.kron(
        PAULI_NUMPY["X"], np.eye(dimension // 2, dtype=complex)
    )
    checks: list[bool] = []
    for index in (1, 2):
        matrix = pauli_word_numpy(row[f"J{index}_word"])
        generalized = (
            matrix if int(row[f"s{index}"]) == 1 else 1j * matrix
        )
        checks.append(
            np.linalg.norm(
                exchange @ generalized.conj() @ exchange - generalized
            )
            < 1e-10
        )
    return all(checks), (checks[0], checks[1])


def group_antilinear_analysis(row: dict[str, str]) -> tuple[str, str]:
    """Write the generalized time-reversal algebra directly in Nambu space."""
    items: list[str] = []
    _, physical_checks = generalized_antilinear_is_physical(row)
    for index in (1, 2):
        word = row[f"J{index}_word"]
        square = int(row[f"q{index}"])
        action_on_g = int(row[f"s{index}"])
        matrix = pauli_word_tex(word)
        generalized_matrix = matrix if action_on_g == 1 else f"i{matrix}"
        raw_kernel_sign = "" if action_on_g == 1 else "-"
        phase_explanation = (
            r"\(U_" + str(index) + rf"=J_{index}\)"
            if action_on_g == 1
            else (
                r"\(U_" + str(index) + rf"=iJ_{index}\)；左右两个 "
                r"\(i\) 抵消 \(J_" + str(index)
                + r"\) 翻转 \(g\) 与 \(B\) 的负号"
            )
        )
        if row["statistics"] == "fermion":
            physical_check = (
                r"费米 Nambu 共轭矩阵就是 \(C=g\)；上式的 "
                r"\(U_" + str(index)
                + r"^TgU_" + str(index)
                + r"=g\) 已同时保证 "
                r"\(C\overline U_" + str(index)
                + r"C=U_" + str(index) + r"\)"
            )
        elif physical_checks[index - 1]:
            physical_check = (
                r"直接代入 \(C=\sigma_x^{\rm Nambu}\otimes I\) 还得到 "
                r"\(C\overline U_" + str(index)
                + r"C=U_" + str(index)
                + r"\)。所以若 \(b\) 变换为某个 annihilation/creation "
                r"线性组合，矩阵的第二半恰好是这个组合的 Hermitian "
                r"conjugate"
            )
        else:
            physical_check = (
                r"但是直接代入 \(C=\sigma_x^{\rm Nambu}\otimes I\) 得到 "
                r"\(C\overline U_" + str(index)
                + r"C\ne U_" + str(index)
                + r"\)。因此这张卡顶部的代表只在暂时把 creation 与 "
                r"annihilation 看成独立分量时保持 canonical matrix，不能把 "
                r"\(\Theta_" + str(index)
                + r"\) 当作物理玻色 Fock 空间上的反幺正时间反演"
            )
        items.append(
            rf"""
              <li>
                原始矩阵 \(J_{index}={matrix}\) 满足
                \[
                  J_{index}^TgJ_{index}
                    ={sign_rhs(action_on_g, "g")},\qquad
                  J_{index}^T\overline{{B_{{\mathrm{{group}}}}}}J_{index}
                    ={raw_kernel_sign}B_{{\mathrm{{group}}}} .
                \]
                定义 \(U_{index}={generalized_matrix}\) 和
                \(\Theta_{index}=U_{index}\mathcal K\) 后，
                \[
                  U_{index}^TgU_{index}=g,\qquad
                  U_{index}^T\overline{{B_{{\mathrm{{group}}}}}}U_{index}
                  =B_{{\mathrm{{group}}}},\qquad
                  \Theta_{index}^2={sign_rhs(square, "I")}.
                \]
                {phase_explanation}。{physical_check}。
              </li>
            """
        )
    generalized_mutual = (
        int(row["r"]) * int(row["s1"]) * int(row["s2"])
    )
    if generalized_mutual == -1:
        if sorted((int(row["q1"]), int(row["q2"]))) == [-1, 1]:
            theorem_class = "conjugate_subsystems"
            theorem_text = (
                r"二者反对易，且一个平方为 \(+I\)、另一个平方为 \(-I\)；"
                r"第 7 卷第 3 节从实际有序算符证明这种组合产生两个"
                r"互为复共轭的 bosonic Fock 或 fermionic Majorana 分块"
            )
        elif int(row["q1"]) == int(row["q2"]) == -1:
            theorem_class = "kramers_pair"
            theorem_text = (
                r"二者反对易且都平方为 \(-I\)；只要两者还满足物理 Nambu "
                r"条件 \(C\overline U_aC=U_a\)，第 7 卷第 4 节的 "
                r"Kramers 时间反演定理便直接证明实际 half-power 非负"
            )
        else:
            theorem_class = "none"
            theorem_text = (
                r"二者反对易但都平方为 \(+I\)；这组 symmetry 本身没有"
                r"普适非负定理"
            )
    else:
        theorem_class = "none"
        theorem_text = (
            r"二者彼此对易；这组 symmetry 本身没有普适非负定理"
        )
    mutual_rhs = (
        r"-\Theta_2\Theta_1"
        if generalized_mutual == -1
        else r"\Theta_2\Theta_1"
    )
    return (
        rf"""
          <ul class="relation-analysis">{"".join(items)}</ul>
          <p>
            对本卡由矩阵关系得到的两条候选时间反演变换，
            \[
              \Theta_1\Theta_2={mutual_rhs}.
            \]
            {theorem_text}。
          </p>
        """,
        theorem_class,
    )


def has_stable_number_conserving_direction(row: dict[str, str]) -> bool:
    """Whether the displayed tensor basis contains a traceful Hermitian free term."""
    traceful_word = "Z" + "I" * (int(row["n"]) - 1)
    return (traceful_word, "R_S") in parse_terms(
        row["maximal_number_conserving_terms"]
    )


def group_only_positivity(
    row: dict[str, str],
    anti_linear_text: str,
    theorem_class: str,
    physical_orbit_rows: list[dict[str, str]],
) -> str:
    heading = (
        r"<h4>由本卡 \(J_1,J_2\) 得到的两条候选时间反演变换</h4>"
    )
    if row["statistics"] == "boson":
        displayed_physical, _ = generalized_antilinear_is_physical(row)
        if displayed_physical:
            physical_gate = (
                "本卡顶部代表已经通过物理 Nambu 共轭检查。"
            )
        elif physical_orbit_rows:
            physical_dimensions = ", ".join(
                str(value)
                for value in sorted(
                    {int(item["matrix_dimension"]) for item in physical_orbit_rows}
                )
            )
            physical_gate = (
                "本卡顶部代表没有通过物理 Nambu 共轭检查，不能直接用于"
                "下面的 Fock-space 证明；但是卡片末尾列出的 "
                f"{len(physical_orbit_rows)} 个物理子轨道通过了检查，"
                f"其 Nambu 维数为 {physical_dimensions}。"
                "下面的结论只用于那些物理子轨道。"
            )
        else:
            physical_gate = (
                "二维和四维内没有通过物理 Nambu 共轭检查的表示；"
                "下面的代数关系在这两个维数内不能提升成玻色 Fock-space "
                "正性定理。"
            )
        if theorem_class == "conjugate_subsystems":
            special = (
                r"""
                <p>
                  这正是 note 的 bosonic reflection-positivity Case 2。
                  上式证明 maximal-subgroup boundary 已经是两个 reflected
                  Fock traces 的模平方。若加入跨两个 sectors 的 coupling，
                  还必须要求其 coefficient matrix 半正定；这条附加条件把
                  group boundary 扩展成 reflection-positive semigroup。
                </p>
                """
                if row["class_id"] == BOSON_RP_CLASS
                else ""
            )
            return rf"""
              {heading}
              {anti_linear_text}
              <p class="result">
                <strong>一条 symmetry 平方为 \(+I\)、另一条平方为
                \(-I\) 且二者反对易时，可得到模平方权重。</strong>
                {physical_gate}
                令 \(P=\Theta_1\Theta_2\)，并把平方为 \(+I\) 的那条
                symmetry 记为 \(\Theta_+\)。由
                \(P^2=I\)、\([P,\hat h_\ell]=0\) 与
                \(\Theta_+P\Theta_+^{{-1}}=-P\)，每个时间片精确分解为
                \[
                  \hat h_\ell=\hat h_{{\ell,+}}+\hat h_{{\ell,-}},
                  \qquad
                  [\hat h_{{\ell,+}},\hat h_{{m,-}}]=0 .
                \]
                由于两条 symmetry 已通过 physical Nambu 检查，\(P\) 的
                两个本征子空间各自包含成套的 annihilation 与 creation
                operators，并构成两个独立 bosonic Fock sectors。因此
                \[
                  W=
                  \operatorname{{Tr}}_+\widehat{{\mathcal U}}_+\,
                  \operatorname{{Tr}}_-\widehat{{\mathcal U}}_-
                  =
                  \left|\operatorname{{Tr}}_+
                  \widehat{{\mathcal U}}_+\right|^2\ge0 .
                \]
                这个算符恒等式直接固定实际 metaplectic half-power，并允许
                原 \(b,b^+\) basis 中有 pairing。若
                {len(physical_orbit_rows)} 个物理子轨道的计数为零，这一段
                只是条件定理，不是本卡的无符号结论。
              </p>
              {special}
            """
        if theorem_class == "kramers_pair":
            minimum_dimension = BOSON_KRAMERS_MIN_DIMENSION[row["class_id"]]
            if minimum_dimension == 8:
                outer = (
                    r"I_2^{\rm Nambu}"
                    if int(row["s1"]) == 1
                    else r"z^{\rm Nambu}"
                )
                physical_representation = rf"""
                  <p>
                    二维和四维的完整枚举没有本类的物理表示，但这并不构成
                    任意维数的 no-go。八维反例可显式写成
                    \[
                      \epsilon=\begin{{pmatrix}}0&1\\-1&0\end{{pmatrix}},
                      \qquad z=\begin{{pmatrix}}1&0\\0&-1\end{{pmatrix}},
                      \qquad
                      u_1=\epsilon\otimes I_2,\quad
                      u_2=z\otimes\epsilon,
                    \]
                    \[
                      J_1={outer}\otimes u_1,\qquad
                      J_2={outer}\otimes u_2.
                    \]
                    按本卡的 \(s_a\) 取
                    \(U_a=J_a\) 或 \(U_a=iJ_a\)，直接相乘可验证
                    \[
                      U_a^TgU_a=g,\quad C\overline U_aC=U_a,\quad
                      U_a\overline U_a=-I,\quad
                      U_1\overline U_2=-U_2\overline U_1.
                    \]
                    对这两个八维表示，\(Q=U_1\overline U_2\) 的 \(+i\)
                    子空间为四维，而且
                    \[
                      \operatorname{{spec}}
                      \left(\eta_0|_{{V_+}}\right)=\{{-1,-1,+1,+1\}}.
                    \]
                    它恰好展示了旧判据漏掉的情形：限制矩阵并非正定，但
                    负方向数 \(n_-=2\) 是偶数，所以 Kramers 公式中的
                    \((-1)^{{n_-}}\) 仍等于 \(+1\)。
                    因而本类的最小物理 Nambu 维数是 8，而不是“任意维都
                    不可能”。
                  </p>
                """
            else:
                physical_representation = rf"""
                  <p>
                    {physical_gate}二维完整枚举没有物理表示，四维子轨道
                    已给出具体矩阵，因此本类的最小物理 Nambu 维数是
                    {minimum_dimension}。
                  </p>
                """
            special = (
                r"""
                本卡正是 note 的 bosonic time-reversal Case 1。main.tex
                的 particle-number-conserving Kramers 证明是它在普通
                annihilation basis 中的一种实现；上面的推导只使用物理
                Nambu 条件与两条时间反演关系，所以也允许逐层
                \(A_{\mathrm{group}}\) 含有 pairing。
                """
                if row["class_id"] == BOSON_TRS_CLASS
                else (
                    r"本卡与 note Case 1 具有同一个 \((-,-)\) 时间反演代数；"
                    r"区别只在 \(J_a\) 对 \(g\) 的原始作用以及实现它所需的"
                    rf"最小 Nambu 维数 {minimum_dimension}。"
                )
            )
            return rf"""
              {heading}
              {anti_linear_text}
              <p class="result">
                <strong>两条物理时间反演对称性都平方为 \(-I\) 且彼此
                反对易，已经足以证明玻色 half-power 权重非负；不需要再
                要求某个子空间上的 commutator matrix 正定。</strong>
              </p>
              {physical_representation}
              <p>
                令
                \[
                  Q=U_1\overline U_2,\qquad
                  V_+=\ker(Q-iI),\qquad
                  K_\ell=A_\ell|_{{V_+}},\qquad
                  \mathcal B=\prod_\ell e^{{K_\ell}} .
                \]
                再令 \(n_-\) 为物理 Nambu commutator matrix
                \(\eta_0=\operatorname{{diag}}(I,-I)\) 限制在 \(V_+\)
                后的负本征值数。收敛区域内的 Fock trace，以及收敛区域外
                与它唯一相接的亚纯延拓，都可写成
                \[
                  W_{{\mathrm B}}^{{\rm an}}
                  =(-1)^{{n_-}}
                  \frac{{\exp[\frac12\sum_\ell
                  \operatorname{{Tr}}K_\ell]}}
                  {{\det(I-\mathcal B)}} .
                \]
                \(\Theta_1\) 保持 \(V_+\) 和 \(\eta_0\)，并满足
                \(\Theta_1^2=-I\)。因此 \(V_+\) 中每个负方向都有线性
                独立、同样为负的 Kramers partner，故 \(n_-\) 必为偶数。
                同一时间反演还使 \(\operatorname{{Tr}}K_\ell\) 为实数，
                并使 \(\det(I-\mathcal B)\ge0\)。所以除
                \(\det(I-\mathcal B)=0\) 的 pole 外，
                \[
                  \boxed{{W_{{\mathrm B}}^{{\rm an}}>0}} .
                \]
                这里没有选择 square-root branch；Kramers 偶重数已经把
                可能的符号成对抵消。{special}
              </p>
            """
        return rf"""
          {heading}
          {anti_linear_text}
          <p class="scope">
            <strong>本卡原始两条时间反演对称性尚未单独固定实际玻色 Fock
            权重的平方根符号。</strong>
            若为本类构造具体模型，还可另外施加 physical Kramers symmetry
            或 operator reflection positivity，但那是模型的附加条件，
            不是本五条关系已经推出的结论。
          </p>
        """

    if theorem_class in ("conjugate_subsystems", "kramers_pair"):
        if theorem_class == "conjugate_subsystems":
            theorem_description = (
                r"一条平方为 \(+I\)、一条平方为 \(-I\) 且二者反对易"
            )
            proof = r"""
              令 \(P=\Theta_1\Theta_2\)，则
              \(P^2=I\) 且 \(P\) 的两个本征子空间不混合。
              平方为 \(+I\) 的时间反演对称性交换两部分。若物理复费米
              模数为偶数，每边的 Majorana operators 都可两两组成普通复费米
              模，所以
              \[
                W_{\mathrm F}
                =\operatorname{Tr}_+\widehat{\mathcal U}_+\,
                 \operatorname{Tr}_-\widehat{\mathcal U}_-
                =\left|\operatorname{Tr}_+
                 \widehat{\mathcal U}_+\right|^2\ge0 .
              \]
              若物理复费米模数为奇数，每个分块含奇数条 Majorana
              directions，不能单独定义普通 Fock trace。此时加入一个完全
              解耦的辅助复费米模，并把它的两条 Majoranas 分到两边；扩充后
              系统的 trace 是原 trace 的两倍，而且
              \[
                2W_{\mathrm F}
                  =\left|\operatorname{Tr}_{+,\mathrm{extended}}
                    \widehat{\mathcal U}_{+,\mathrm{extended}}\right|^2\ge0.
              \]
              因而奇数模与偶数模都得到实际 \(W_{\mathrm F}\ge0\)。这是
              operator-level factorization，不要求粒子数守恒，也不丢失
              fermion Spin double-cover 的符号。
            """
        else:
            theorem_description = (
                r"两条都平方为 \(-I\) 且二者反对易"
            )
            proof = r"""
              令 \(Q=\Theta_1\Theta_2\)，则 \(Q^2=-I\)。
              \(Q\) 的 \(+i\) 子空间定义 emergent conserved fermions，
              其中任一 \(\Theta_a\) 平方为 \(-I\)。若
              \(\mathcal B=\prod_\ell e^{K_\ell}\) 是该 annihilation
              subspace 上的传播矩阵，Kramers pairing 给出
              \[
                \det(I+\mathcal B)=
                \prod_{\lambda\notin\mathbb R}|1+\lambda|^2
                \prod_{r\in\mathbb R}(1+r)^{{2m_r}}\ge0 .
              \]
              同一 symmetry 使每个 \(\operatorname{Tr}K_\ell\) 为实数，
              因而实际 half-power 已精确还原为
              \[
                W_{\mathrm F}
                  =e^{-\frac12\sum_\ell\operatorname{Tr}K_\ell}
                    \det(I+\mathcal B)\ge0 .
              \]
              conserved particle structure 由 \(Q\) 定义，所以原 Nambu
              basis 仍可含 pairing；这里没有遗留 Spin square-root 符号。
            """
        return rf"""
          {heading}
          {anti_linear_text}
          <p class="result">
            <strong>本类虽然只有 maximal subgroup，但
            {theorem_description}，所以已有完整的费米无符号证明。</strong>
            {proof}
          </p>
        """

    all_plus_class = "s1+_q1+_s2+_q2+_r+"
    if row["class_id"] == all_plus_class:
        return rf"""
          {heading}
          {anti_linear_text}
          <p>
            两条平方为 \(+I\) 且彼此对易的时间反演对称性，对任意
            \(A_{{\mathrm{{group}}}}\) 没有普适的双时间反演正性定理。
            不过，本类至少
            含有下面两个可以直接证明的无符号子群；它们都来自本类实际
            \(J_1,J_2\) 约束，而不是额外套用 Kramers 条件。
          </p>
          <p>
            <strong>第一，compact \(SO(m)\) 子群。</strong>取
            \[
              g=\sigma_x^{{\rm Nambu}}\otimes I_m,\qquad
              J_1=I,\qquad J_2=\sigma_x^{{\rm Nambu}}\otimes I_m,
            \]
            以及
            \[
              A_\ell=I_2^{{\rm Nambu}}\otimes k_\ell,\qquad
              k_\ell\in\mathbb R^{{m\times m}},\quad k_\ell^T=-k_\ell .
            \]
            三个 group 等式逐项成立。粒子子空间中的传播为
            \(M=\prod_\ell e^{{k_\ell}}\in SO(m)\)。其非实本征值成
            \(e^{{i\theta}},e^{{-i\theta}}\) 对；因为
            \(\det M=1\)，本征值 \(-1\) 的重数为偶数。因此
            \[
              \det(I+M)
              =\prod_\theta|1+e^{{i\theta}}|^2\ge0 .
            \]
            对应的 Hermitian current 是
            \(\hat L=-i\,c^+kc\)。相互作用
            \(+\frac U2\hat L^2\) 的实 Gaussian HS exponent 正好产生
            \(c^+kc\)，所以这是可直接实现的 interacting AFQMC 子类。
          </p>
          <p>
            <strong>第二，split \(O(n,n)\) 子群。</strong>令
            \[
              \Gamma=\operatorname{{diag}}(I_n,-I_n),\qquad
              J_1=I,\qquad
              J_2=\sigma_x^{{\rm Nambu}}\otimes\Gamma,
            \]
            并取
            \[
              A_\ell=
              \begin{{pmatrix}}a_\ell&0\\0&-a_\ell^T\end{{pmatrix}},
              \qquad a_\ell\in\mathbb R^{{2n\times2n}} .
            \]
            逐块计算给出
            \[
              J_2^TA_\ell J_2=A_\ell
              \quad\Longleftrightarrow\quad
              a_\ell^T\Gamma+\Gamma a_\ell=0 .
            \]
            上式取迹还给出 \(\operatorname{{Tr}}a_\ell=0\)，所以 Nambu
            normal-ordering scalar 恰为 1。因而
            \(M=\prod_\ell e^{{a_\ell}}\) 位于与恒等矩阵相连的
            \(O(n,n)\) 分支，split-orthogonal determinant theorem 给出
            \[
              \boxed{{W_{{\mathrm F}}=\det(I+M)\ge0}} .
            \]
            这条定理覆盖的是本类明确写出的 particle-number-conserving
            子空间，而不是同类任意 pairing direction。它说明二维最小
            代表不能代表整个类别。这一 split-\(O\) 结果是已有
            split-orthogonal/semigroup 定理在统一 Nambu 五关系框架中的
            嵌入；新的作用是让它与同类其余 \(A\) 方向直接比较。
          </p>
        """

    return rf"""
      {heading}
      {anti_linear_text}
      <p class="scope">
        <strong>本卡的两条时间反演对称性不形成
        \((+,-)\) 或 \((-,-)\) 反对易 pair，所以五条关系本身不能固定
        实际 Nambu half-power。</strong>
        仍可在本卡的 \(P\otimes K_P\) 表内施加更强的
        split-orthogonal、reflection-positive 或额外
        时间反演约束；这些是本类的无符号子空间，而不是对
        整个 maximal subgroup 的结论。
      </p>
    """


def strict_semigroup_positivity(row: dict[str, str]) -> str:
    """Explain the strict-cone route without invoking A_group TRS theorems."""
    if row["statistics"] == "boson" and row["metric"] == "J2g":
        return r"""
          <section class="semigroup-positivity">
            <p class="result">
              <strong>本卡通过 strict cone 筛选；正性证明走收缩半群与
              连通正分支，不走双时间反演 half-power 定理。</strong>
              对本卡下方明确构造、并已逐时间片核对收缩不等式的物理模型，
              \(\eta=J_2g\) 与 bosonic particle/hole Fock
              representation 相容。它的每个完整辅助场传播都满足
              \[
                M(\phi)^\dagger\eta M(\phi)-\eta<0 .
              \]
            </p>
            <p>
              乘法封闭性保证任意多个不对易时间片的有序积仍在同一个
              strict contraction semigroup 内。物理 oscillator
              representation 在这个内部给出 trace-class Gaussian
              operator，因此 bare trace 收敛；严格不等式还排除
              \(M(\phi)\) 的 \(+1\) 本征值，所以玻色 determinant
              不会遇到 pole。\(J_1\) 条件使完整权重为实，实辅助场空间
              连通，稳定零场的权重为正。沿任意辅助场路径，实际有序
              Fock operator 连续携带同一个 metaplectic lift，且权重既
              不发散也不经过零。因此所有构型保持同一个正分支。
            </p>
            <p>
              这里没有从最终传播矩阵重新选择平方根，也没有计算一个
              独立的 double-cover 符号。正号完全由“strict contraction、
              正参考点、连通路径”固定。第 6.4 节给出含 pairing 与一般
              不对易时间片乘积的 trace-class 推导。
            </p>
          </section>
        """

    if row["statistics"] == "boson":
        return r"""
          <section class="semigroup-positivity">
            <p class="result">
              <strong>本卡通过 strict cone 的矩阵筛选，metric 为
              \(\eta=iJ_2g\)。</strong>
              本卡的 \(A_{\mathrm{group}}\) 与
              \(A_{\mathrm{cone}}\) 给出了一个可构造的矩阵收缩半群：
              其中存在使
              \(\eta A_{\mathrm{cone}}
              +A_{\mathrm{cone}}^\dagger\eta<0\) 的方向。
              这正是 Octave 穷举要寻找的对象，而不是一组 half-power
              时间反演对称性。
            </p>
            <p>
              对实正交 \(J_2\)，第 6.4 节的一般 Hermitian BdG 推导证明：
              稳定 Hermitian 零场生成元不能同时位于同一个严格
              \(iJ_2g\) 锥。这只排除了把通常稳定零场直接作为该矩阵半群
              正参考点的做法，不是对所有 grand-canonical 实现的 no-go。
            </p>
            <p>
              本卡下方的 number-conserving 实现含无界 Gaussian 双曲场，
              所以 \(\sup_\phi\|\mathcal B(\phi)\|_2=\infty\)，不存在一个
              对全部构型有效的固定 fugacity。它改在固定总粒子数空间
              求迹，并另外用正 reciprocal spectrum 证明每个 character
              严格为正。若另一个实现具有有界或离散 HS support，并满足
              \(z\sup_\phi\|\mathcal B(\phi)\|_2<1\)，则足够负的化学势仍可
              给出 grand-canonical 正权重；完整 ensemble 条件和算法见
              <a href="part_8_canonical_projector_algorithms.html">
              固定粒子数算法卷</a>。
            </p>
          </section>
        """

    return r"""
      <section class="semigroup-positivity">
        <p class="result">
          <strong>本卡通过 strict cone 筛选，并由费米收缩半群固定
          全部辅助场权重的非负号。</strong>
          对本卡下方明确构造、并已逐时间片核对收缩不等式的物理模型，
          每个完整构型都满足
          \[
            M(\phi)^\dagger\eta M(\phi)-\eta<0 .
          \]
          这个不等式对时间片乘法封闭，并排除 \(M(\phi)\) 的
          \(-1\) 本征值；因此实际 fermionic Spin trace 不会经过零。
        </p>
        <p>
          费米 Fock space 有限维，所以没有玻色 bare-trace 收敛问题。
          \(J_1\) 条件使权重为实；连通辅助场空间中的每个构型都可连到
          一个正参考构型。实际有序 Fock operator 沿路径连续，自动保留
          正确的 Spin lift。权重既不为零，就不能改变符号。只有等号边界
          的构型可由 \(e^{\epsilon A_{\mathrm{cone}}}\)、
          \(\epsilon\to0^+\) 从内部逼近，因此其权重是非负极限。
        </p>
        <p>
          这条证明不需要判断本卡的两条候选时间反演变换是否构成
          \((+,-)\) 或 \((-,-)\) pair；那是第 7 卷研究的另一条正性
          路线。
        </p>
      </section>
    """


def positivity_block(
    row: dict[str, str],
    physical_orbit_rows: list[dict[str, str]],
) -> str:
    if int(row["strict_interior"]):
        return strict_semigroup_positivity(row)

    anti_linear_text, theorem_class = group_antilinear_analysis(row)
    group_result = group_only_positivity(
        row,
        anti_linear_text,
        theorem_class,
        physical_orbit_rows,
    )
    return rf"""
      <section class="half-power-positivity">
        <p class="scope">
          <strong>本卡的 strict \(A_{{\mathrm{{cone}}}}\) 为空，不能用
          本卷的收缩半群内部证明。</strong>
          因而下面才启动独立的时间反演对称性补充筛选。完整的算符级定理见
          <a href="part_7_determinant_symmetry_groups.html">
          Gaussian 权重的对称性正性理论卷</a>。
        </p>
        <h4>只含 \(A_{{\mathrm{{group}}}}\) 的有序时间序列</h4>
        {group_result}
      </section>
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


def fermion_all_plus_model() -> str:
    return r"""
      <section class="model-example">
        <p class="model-title"><strong>本类已经严格无符号的两个
        Hermitian interacting models</strong></p>
        <p>
          <strong>受挫图上的 loop-current-square fermions。</strong>
          对任意实反对称 one-particle matrices
          \(k_\mu^T=-k_\mu\)，定义 Hermitian currents
          \[
            \hat L_\mu=-i\sum_{ij}c_i^+(k_\mu)_{ij}c_j ,
          \]
          并考虑
          \[
            \hat H_{\rm current}
            =\frac12\sum_\mu U_\mu\hat L_\mu^2,
            \qquad U_\mu>0 .
          \]
          每个 \(k_\mu\) 可取为三角、kagome 或 moiré 图上的局域
          loop-current pattern；不同 \(k_\mu\) 不必彼此对易。逐项使用
          \[
            e^{-\Delta\tau U_\mu\hat L_\mu^2/2}
            \propto\int d\phi_\mu\,e^{-\phi_\mu^2/2}
            e^{\,\sqrt{\Delta\tau U_\mu}\phi_\mu\,c^+k_\mu c}
          \]
          后，HS generator 是
          \(A_{\rm HS}=I_2^{\rm Nambu}\otimes k_\mu\)，正是上文
          compact-\(SO(m)\) 方向。任意时空场构型给出
          \(M\in SO(m)\)，所以
          \[
            \det(I+M)
            =\prod_{\operatorname{Im}\lambda>0}|1+\lambda|^2
             \prod_{r=\pm1}(1+r)^{n_r}\ge0 .
          \]
          第一项遍历非实共轭本征值对，\(n_r\) 是实本征值
          \(r=\pm1\) 的重数；若出现 \(-1\)，权重为零，否则每个因子均
          为正。这里没有加入 chemical potential，因为
          \(\mu I\notin\mathfrak{so}(m)\)，加入它会离开本卡所证明的
          compact-\(SO(m)\) maximal-subgroup 子空间。这个模型可直接研究
          受挫平带中自发 loop-current、轨道磁性与电荷序的竞争；它不要求
          bipartite lattice。
        </p>
        <p>
          <strong>二分格点 spinless \(t\!-\!V\) 的 hopping-channel
          CT-AFQMC。</strong>把全部 A-sublattice sites 排在 B sites
          之前，令
          \(\Gamma=\operatorname{diag}(I_A,-I_B)\)。取实对称、只连接
          两个子晶格的 \(K\)，并考虑
          \[
            \hat H=\sum_{ij}c_i^+K_{ij}c_j+
            \sum_{\langle ij\rangle}
            \left[V\hat n_i\hat n_j-\frac V2(\hat n_i+\hat n_j)-\Gamma_0\right],
            \qquad V,\Gamma_0>0 .
          \]
          对每条 A--B bond，令
          \(\hat o_{ij}=c_i^+c_j+c_j^+c_i\)。由于
          \(\hat o_{ij}^2=\hat n_i+\hat n_j-2\hat n_i\hat n_j\)，有精确
          分解
          \[
            -\hat v_{ij}
            =\frac{\Gamma_0}{2}\sum_{\sigma=\pm1}
              e^{\sigma\lambda\hat o_{ij}},
            \qquad
            \cosh\lambda=1+\frac{V}{2\Gamma_0}.
          \]
          自由传播与每个 bond vertex 的 one-particle generators 都满足
          \[
            a^T\Gamma+\Gamma a=0 .
          \]
          因此每个 CT configuration 的有序乘积属于
          \(O^{++}(n,n)\)，上文的 split-orthogonal theorem 逐构型给出
          \(\det(I+M)\ge0\)。取 honeycomb、\(\pi\)-flux square 或带
          boundary defects 的 bipartite Dirac lattice，可研究
          semimetal--charge-order criticality、缺陷束缚态与长程
          opposite-sublattice interactions。这个模型是已有
          split-orthogonal 方法的代表；这里的新信息是它在五关系全正类
          的完整四维表示与 \(A_{\rm group}\) 表中的确切位置。
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
    if (
        row["statistics"] == "fermion"
        and row["class_id"] == "s1+_q1+_s2+_q2+_r+"
    ):
        return fermion_all_plus_model()
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


def parse_integer_matrix(raw: str) -> np.ndarray:
    rows = [
        [int(entry) for entry in row.split()]
        for row in raw.split("|")
        if row
    ]
    matrix = np.asarray(rows, dtype=int)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise RuntimeError(f"Invalid serialized square matrix: {raw}")
    return matrix


def signed_permutation_matrix(raw: str) -> np.ndarray:
    entries = [int(entry) for entry in raw.strip("[]").split()]
    matrix = np.zeros((len(entries), len(entries)), dtype=int)
    for column, entry in enumerate(entries):
        matrix[abs(entry) - 1, column] = 1 if entry > 0 else -1
    return matrix


def integer_matrix_tex(matrix: np.ndarray) -> str:
    rows = [
        "&".join(str(int(value)) for value in row)
        for row in np.asarray(matrix)
    ]
    return (
        r"\begin{pmatrix}"
        + r"\\".join(rows)
        + r"\end{pmatrix}"
    )


def pauli_decomposition_tex(matrix: np.ndarray) -> str:
    """Write a real 2x2 or 4x4 matrix in the real Pauli tensor basis."""
    dimension = matrix.shape[0]
    if dimension not in (2, 4) or matrix.shape != (dimension, dimension):
        return integer_matrix_tex(matrix)
    words = list(PAULI_NUMPY)
    if dimension == 4:
        words = [left + right for left in words for right in words]
    basis = [pauli_word_numpy(word).real for word in words]
    coefficients, residuals, _, _ = np.linalg.lstsq(
        np.column_stack([item.reshape(-1) for item in basis]),
        matrix.reshape(-1),
        rcond=None,
    )
    if residuals.size and residuals[0] > 1e-18:
        return integer_matrix_tex(matrix)
    denominator = 2 if any(
        abs(value * 2 - round(value * 2)) < 1e-10
        and abs(value - round(value)) >= 1e-10
        for value in coefficients
    ) else 1
    terms: list[tuple[int, str]] = []
    for value, word in zip(coefficients, words):
        numerator = int(round(value * denominator))
        if numerator:
            terms.append((numerator, pauli_word_tex(word)))
    if not terms:
        return "0"
    pieces: list[str] = []
    for index, (numerator, word_tex) in enumerate(terms):
        sign = "-" if numerator < 0 else "+"
        magnitude = abs(numerator)
        term = word_tex if magnitude == 1 else rf"{magnitude}{word_tex}"
        if index == 0:
            pieces.append(("-" if numerator < 0 else "") + term)
        else:
            pieces.append(rf"\,{sign}\,{term}")
    expression = "".join(pieces)
    if denominator == 2:
        return rf"\frac12\left({expression}\right)"
    return expression


def phased_matrix_tex(phase: str, matrix: np.ndarray) -> str:
    prefix = "" if phase == "1" else "i"
    return prefix + integer_matrix_tex(matrix)


def parse_orbit_terms(raw: str) -> list[tuple[str, np.ndarray]]:
    terms: list[tuple[str, np.ndarray]] = []
    for entry in raw.split(";"):
        if not entry:
            continue
        coefficient_type, serialized_matrix = entry.split("@", 1)
        terms.append(
            (coefficient_type, parse_integer_matrix(serialized_matrix))
        )
    return terms


def canonical_g_matrix(statistics: str, dimension: int) -> np.ndarray:
    nambu_metric = (
        -PAULI_NUMPY["Y"]
        if statistics == "boson"
        else PAULI_NUMPY["X"]
    )
    return np.kron(
        nambu_metric, np.eye(dimension // 2, dtype=complex)
    )


def orbit_literal_span(
    terms: list[tuple[str, np.ndarray]],
) -> str:
    entries: list[str] = []
    for coefficient_type, matrix in terms:
        if coefficient_type == "R_S":
            entries.append(integer_matrix_tex(matrix))
        elif coefficient_type == "iR_S":
            entries.append("i" + integer_matrix_tex(matrix))
    if not entries:
        return r"\{0\}"
    return (
        r"\operatorname{span}_{\mathbb R}\left\{"
        + r",\, ".join(entries)
        + r"\right\}"
    )


def orbit_dimension_formula(
    terms: list[tuple[str, np.ndarray]],
) -> str:
    symmetric_count = sum(
        coefficient_type in ("R_S", "iR_S")
        for coefficient_type, _ in terms
    )
    antisymmetric_count = len(terms) - symmetric_count
    return (
        rf"{symmetric_count}\frac{{m(m+1)}}2"
        rf"+{antisymmetric_count}\frac{{m(m-1)}}2"
    )


def orbit_operator_tex(
    statistics: str,
    matrix: np.ndarray,
    coefficient_index: int,
) -> str:
    dimension = matrix.shape[0]
    half = dimension // 2
    kernel = np.real_if_close(
        canonical_g_matrix(statistics, dimension) @ matrix
    ).astype(int)
    blocks = (
        kernel[:half, :half],
        kernel[:half, half:],
        kernel[half:, :half],
        kernel[half:, half:],
    )
    operator = "b" if statistics == "boson" else "c"
    block_tex = [integer_matrix_tex(block) for block in blocks]
    coefficient = rf"K_{coefficient_index}"
    return rf"""
      \(\displaystyle \frac12\Big[
      \boldsymbol {operator}^T({block_tex[0]}\otimes {coefficient})
      \boldsymbol {operator}
      +\boldsymbol {operator}^T({block_tex[1]}\otimes {coefficient})
      \boldsymbol {operator}^+
      +\boldsymbol {operator}^{{+T}}({block_tex[2]}\otimes {coefficient})
      \boldsymbol {operator}
      +\boldsymbol {operator}^{{+T}}({block_tex[3]}\otimes {coefficient})
      \boldsymbol {operator}^+\Big]\)
    """


def orbit_terms_table(
    statistics: str,
    terms: list[tuple[str, np.ndarray]],
) -> str:
    if not terms:
        return "<p>没有非零方向。</p>"
    rows: list[str] = []
    for index, (coefficient_type, matrix) in enumerate(terms, 1):
        transpose, conjugation = COEFFICIENT_CONDITIONS[coefficient_type]
        rows.append(
            "<tr>"
            rf"<td>\(P_{index}={integer_matrix_tex(matrix)}\)</td>"
            rf"<td>\({transpose.replace('K_P', f'K_{index}')}\)</td>"
            rf"<td>\({conjugation.replace('K_P', f'K_{index}')}\)</td>"
            f"<td>{orbit_operator_tex(statistics, matrix, index)}</td></tr>"
        )
    return (
        '<div class="scroll"><table class="coefficient-table"><thead>'
        r"<tr><th>\(P_\alpha\)</th><th>转置</th><th>复共轭</th>"
        r"<th>具体二次算符 \(\hat h(P_\alpha\otimes K_\alpha)\)</th>"
        "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def orbit_sum_formula(
    lhs: str, terms: list[tuple[str, np.ndarray]]
) -> str:
    if not terms:
        return rf"\[{lhs}=0.\]"
    return rf"""
      \[
        {lhs}=\sum_{{\alpha=1}}^{{{len(terms)}}}
        P_\alpha\otimes K_\alpha .
      \]
    """


def orbit_cone_lmi(
    orbit: dict[str, str],
    terms: list[tuple[str, np.ndarray]],
) -> str:
    phase = orbit["eta_phase"]
    eta_base = parse_integer_matrix(orbit["eta_matrix"])
    pieces = [
        rf"{phased_matrix_tex(phase, eta_base @ matrix)}"
        rf"\otimes K_{index}"
        for index, (_, matrix) in enumerate(terms, 1)
    ]
    return "+".join(pieces) if pieces else "0"


def orbit_pair_list(raw_pairs: str) -> str:
    rendered: list[str] = []
    for pair in raw_pairs.split(";"):
        first, second = pair.split("/", 1)
        rendered.append(
            rf"\left({integer_matrix_tex(signed_permutation_matrix(first))},"
            rf"{integer_matrix_tex(signed_permutation_matrix(second))}\right)"
        )
    return r",\quad ".join(rendered)


def orbit_sheet(
    row: dict[str, str],
    orbit: dict[str, str],
    full: dict[str, str],
    *,
    physical_suborbit: bool = False,
) -> str:
    dimension = int(orbit["matrix_dimension"])
    first = signed_permutation_matrix(orbit["representative_J1"])
    second = signed_permutation_matrix(orbit["representative_J2"])
    eta_base = parse_integer_matrix(orbit["eta_matrix"])
    eta = phased_matrix_tex(orbit["eta_phase"], eta_base)
    group_terms = parse_orbit_terms(orbit["group_terms"])
    cone_terms = parse_orbit_terms(orbit["cone_terms"])
    independence = (
        "两条时间反演约束彼此独立"
        if int(orbit["distinct_J1_J2"])
        else r"\(J_1=J_2\)，所以这里只提供一条独立时间反演约束"
    )
    if physical_suborbit:
        orbit_id = orbit["physical_orbit_id"]
        orbit_kind = "玻色物理表示子轨道"
        j1_under_c = sign_rhs(row["s1"], r"J_1")
        j2_under_c = sign_rhs(row["s2"], r"J_2")
        physical_u1 = r"J_1" if int(row["s1"]) == 1 else r"iJ_1"
        physical_u2 = r"J_2" if int(row["s2"]) == 1 else r"iJ_2"
        physicality = (
            r"本轨道的每个代表都满足 "
            rf"\(CJ_1C={j1_under_c},\ CJ_2C={j2_under_c}\)。"
            rf"因此具体应取 \(U_1={physical_u1}\)、"
            rf"\(U_2={physical_u2}\)；它们满足 "
            r"\(C\overline U_aC=U_a\)，从而保持 "
            r"\(\chi^\dagger=\chi^TC\)"
        )
    else:
        orbit_id = orbit["orbit_id"]
        orbit_kind = "代数表示轨道"
        physicality = (
            r"本轨道只按保持 \(g\) 的换基合并；玻色情形能否作为同一 "
            r"Fock representation 的物理换基，必须再看本卡后面的物理子表"
            if row["statistics"] == "boson"
            else (
                r"费米情形 \(C=g\)，所以保持 \(g\) 已同时保持物理 "
                r"creation 是相应 annihilation 的 Hermitian conjugate"
            )
        )
    group_formula = orbit_sum_formula(
        r"A_{\mathrm{group}}", group_terms
    )
    group_table = orbit_terms_table(row["statistics"], group_terms)
    if int(row["strict_interior"]):
        cone_formula = orbit_sum_formula(
            r"A_{\mathrm{cone}}", cone_terms
        )
        cone_table = orbit_terms_table(row["statistics"], cone_terms)
        cone_content = rf"""
          <p>
            \(A_{{\mathrm{{cone}}}}\) 必须满足本卡前面列出的四个等式。
            对这个表示，它们的完整解为
          </p>
          {cone_formula}
          {cone_table}
          <p>
            继续施加严格不等式时，必须把具体
            \(\eta={eta}\) 代入整块矩阵：
            \[
              \boxed{{\eta A_{{\mathrm{{cone}}}}
              ={orbit_cone_lmi(orbit, cone_terms)}<0}} .
            \]
            不能把这一个整块负定条件拆成各个 \(K_\alpha\) 分别为负。
          </p>
        """
    else:
        lemma_id = (
            "lemma-1"
            if full["status"] == "boundary_only_trace_obstruction"
            else "lemma-2"
        )
        lemma_number = "1" if lemma_id == "lemma-1" else "2"
        cone_content = rf"""
          <p>
            对这一整个五关系类别，
            <a href="#{lemma_id}">引理{lemma_number}</a>已经证明
            \[
              \boxed{{
                \nexists\,A_{{\mathrm{{cone}}}}\ \text{{同时满足全部等式与 }}
                \eta A_{{\mathrm{{cone}}}}
                +A_{{\mathrm{{cone}}}}^\dagger\eta<0
              }} .
            \]
            因此这里不列只满足 cone 等式、却不可能满足严格负定不等式的
            线性候选。
          </p>
        """
    return rf"""
      <section class="orbit-sheet">
        <h5>{dimension} 维，{orbit_kind} {orbit_id}</h5>
        <p>
          取
          \[
            J_1={integer_matrix_tex(first)},\qquad
            J_2={integer_matrix_tex(second)},\qquad
            \eta={eta}.
          \]
          {independence}；{physicality}。这个表示轨道含
          {orbit["orbit_size"]} 组 signed-permutation 标准代表。
        </p>
        <details>
          <summary>展开同一轨道内的全部标准代表</summary>
          <div class="scroll">\[
            {orbit_pair_list(orbit["all_pairs"])}
          \]</div>
        </details>
        <p>
          不额外张量格点或轨道重复空间，即 \(m=1\) 时，
          \(A_{{\mathrm{{group}}}}\) 的全部独立实方向为
          \[
            A_{{\mathrm{{group}}}}^{{({dimension})}}
            \in {orbit_literal_span(group_terms)} .
          \]
          张量任意 \(m\) 维重复空间后，独立实参数数目为
          \[
            \dim_{{\mathbb R}}A_{{\mathrm{{group}}}}
            ={orbit_dimension_formula(group_terms)},
          \]
          完整矩阵结构如下。
        </p>
        {group_formula}
        {group_table}
        {cone_content}
      </section>
    """


def low_dimensional_representation_block(
    row: dict[str, str],
    orbit_rows: list[dict[str, str]],
    physical_orbit_rows: list[dict[str, str]],
    full: dict[str, str],
) -> str:
    by_dimension = {
        dimension: [
            orbit
            for orbit in orbit_rows
            if int(orbit["matrix_dimension"]) == dimension
        ]
        for dimension in (2, 4)
    }
    blocks: list[str] = []
    for dimension in (2, 4):
        if by_dimension[dimension]:
            blocks.extend(
                orbit_sheet(row, orbit, full)
                for orbit in by_dimension[dimension]
            )
        else:
            blocks.append(
                rf"""
                <p>
                  <strong>{dimension} 维：</strong>不存在满足这五条关系的
                  实正交表示。
                </p>
                """
            )
    physical_blocks: list[str] = []
    if row["statistics"] == "boson":
        physical_by_dimension = {
            dimension: [
                orbit
                for orbit in physical_orbit_rows
                if int(orbit["matrix_dimension"]) == dimension
            ]
            for dimension in (2, 4)
        }
        for dimension in (2, 4):
            if physical_by_dimension[dimension]:
                physical_blocks.extend(
                    orbit_sheet(
                        row,
                        orbit,
                        full,
                        physical_suborbit=True,
                    )
                    for orbit in physical_by_dimension[dimension]
                )
            else:
                physical_blocks.append(
                    rf"""
                    <p>
                      <strong>{dimension} 维：</strong>本类没有同时保持
                      \(g\) 与物理 Nambu 共轭矩阵 \(C\) 的表示。
                    </p>
                    """
                )
        physical_section = (
            r"""
            <details class="basis-audit physical-suborbits">
              <summary>只看可直接实现为玻色 Hamiltonian 的物理表示</summary>
              <p>
                这里不再按任意保持 \(g\) 的矩阵合并，而是同时要求换基
                保持
                \[
                  C=\sigma_x^{\mathrm{Nambu}}\otimes I,\qquad
                  \chi^\dagger=\chi^TC .
                \]
                因此下面每一个 \(J_1,J_2\) 都能提升为物理 Fock 空间的
                generalized time-reversal transformation；列出的
                \(A_{\mathrm{group}}\) 与 \(A_{\mathrm{cone}}\) 才可直接
                用于构造玻色 Hamiltonian。
              </p>
            """
            + "".join(physical_blocks)
            + "</details>"
        )
    else:
        physical_section = ""
    return r"""
      <details class="basis-audit low-dimensional-representations">
        <summary>二维和四维内全部实正交表示及其 \(A\) 独立方向</summary>
        <p>
          三个实正交矩阵 \(g,J_1,J_2\) 两两对易或反对易，平方又都等于
          \(\pm I\)。任何矩阵乘积都能把顺序整理为
          \[
            \pm g^aJ_1^bJ_2^c,\qquad a,b,c\in\{0,1\},
          \]
          所以它们生成的有限群至多有 16 个元素。有限群的实正交表示可
          分解成互相正交、不能再分的小块。由这些平方与对易关系得到的
          实矩阵代数，只可能由
          \(\mathbb R,\mathbb C,M_2(\mathbb R),\mathbb H\) 或
          \(M_2(\mathbb C)\) 型小块组成；每一种小块都能用
          \(I_2,\sigma_x,i\sigma_y,\sigma_z\) 的 signed-permutation
          矩阵实现。因此，穷举全部 signed-permutation 矩阵及其正交
          直和，确实覆盖二维、四维的全部实正交表示，不再局限于单个
          Pauli tensor word。
        </p>
        <p>
          程序用八个迹
          \[
            \operatorname{Tr}(g^aJ_1^bJ_2^c),
            \qquad a,b,c\in\{0,1\},
          \]
          区分这些有限群表示，再用
          \[
            S^TS=I,\qquad S^TgS=g,\qquad
            J_a'=S^{-1}J_aS
          \]
          的显式换基矩阵核对等价性。这里同时保留
          \(J_1=J_2\) 的轨道：它只有一条独立时间反演约束，却允许更大的
          \(A\) 空间，删除它反而会漏掉模型。
        </p>
        <p>
          每个轨道先给出 \(m=1\) 时全部独立方向，再给出
          \(\sum_\alpha P_\alpha\otimes K_\alpha\) 的任意重复空间解、
          每个 \(K_\alpha\) 的转置与复共轭条件、具体二次算符，以及
          代入该轨道实际 \(\eta\) 后的 cone 不等式。玻色轨道还逐项标明
          时间反演变换后，creation component 是否仍是相应 annihilation
          component 的 Hermitian conjugate。
        </p>
    """ + "".join(blocks) + physical_section + r"""
      </details>
    """


def compact_representative_block(row: dict[str, str]) -> str:
    """Render the chosen Pauli representative without repeating the five signs."""
    metric = r"J_2g" if row["metric"] == "J2g" else r"iJ_2g"
    _, explicit_metric = metric_matrix_and_tex(row)
    return rf"""
      <div class="scroll compact-representative">\[
        J_1={pauli_word_tex(row["J1_word"])},\qquad
        J_2={pauli_word_tex(row["J2_word"])},\qquad
        \eta={metric}={explicit_metric}.
      \]</div>
    """


def compact_group_block(row: dict[str, str]) -> str:
    return rf"""
      <section class="compact-generator">
        <h4>最大子群生成元</h4>
        <div class="scroll">\[
          \begin{{gathered}}
            gA_{{\mathrm{{group}}}}+A_{{\mathrm{{group}}}}^Tg=0,\\
            J_1^TA_{{\mathrm{{group}}}}J_1
              =\overline{{A_{{\mathrm{{group}}}}}},\qquad
            J_2^TA_{{\mathrm{{group}}}}J_2
              =\overline{{A_{{\mathrm{{group}}}}}},\\
            \eta A_{{\mathrm{{group}}}}
              +A_{{\mathrm{{group}}}}^\dagger\eta=0.
          \end{{gathered}}
        \]</div>
        {sum_formula(r"A_{\mathrm{group}}", row["maximal_terms"])}
        {coefficient_table(
            row["maximal_terms"], row["statistics"], compact=True
        )}
      </section>
    """


def compact_cone_block(
    row: dict[str, str], full: dict[str, str]
) -> str:
    if not int(row["strict_interior"]):
        lemma_id = (
            "lemma-1"
            if full["status"] == "boundary_only_trace_obstruction"
            else "lemma-2"
        )
        lemma_number = "1" if lemma_id == "lemma-1" else "2"
        return rf"""
          <section class="compact-generator">
            <h4>收缩锥生成元</h4>
            <p class="scope">
              <a href="#{lemma_id}">引理{lemma_number}</a>给出
              \[
                \boxed{{\nexists\,A_{{\mathrm{{cone}}}}:\quad
                \eta A_{{\mathrm{{cone}}}}
                +A_{{\mathrm{{cone}}}}^\dagger\eta<0}}.
              \]
            </p>
          </section>
        """

    _, explicit_metric = metric_matrix_and_tex(row)
    return rf"""
      <section class="compact-generator">
        <h4>收缩锥生成元</h4>
        <div class="scroll">\[
          \begin{{gathered}}
            gA_{{\mathrm{{cone}}}}+A_{{\mathrm{{cone}}}}^Tg=0,\\
            J_1^TA_{{\mathrm{{cone}}}}J_1
              =\overline{{A_{{\mathrm{{cone}}}}}},\qquad
            J_2^TA_{{\mathrm{{cone}}}}J_2
              =-\overline{{A_{{\mathrm{{cone}}}}}},\\
            \eta A_{{\mathrm{{cone}}}}
              +A_{{\mathrm{{cone}}}}^\dagger\eta<0.
          \end{{gathered}}
        \]</div>
        {sum_formula(r"A_{\mathrm{cone}}", row["cone_linear_terms"])}
        {coefficient_table(
            row["cone_linear_terms"], row["statistics"], compact=True
        )}
        <div class="scroll">\[
          \eta={explicit_metric},\qquad
          \boxed{{\eta A_{{\mathrm{{cone}}}}
          ={explicit_eta_product(row, row["cone_linear_terms"])}<0}}.
        \]</div>
      </section>
    """


def compact_orbit_terms_table(
    terms: list[tuple[str, np.ndarray]],
) -> str:
    if not terms:
        return "<p>没有非零方向。</p>"
    rows: list[str] = []
    for index, (coefficient_type, matrix) in enumerate(terms, 1):
        transpose, conjugation = COEFFICIENT_CONDITIONS[coefficient_type]
        rows.append(
            rf"<tr><td>\(P_{index}={integer_matrix_tex(matrix)}\)</td>"
            rf"<td>\({transpose.replace('K_P', f'K_{index}')},\ "
            rf"{conjugation.replace('K_P', f'K_{index}')}\)</td></tr>"
        )
    return (
        '<div class="scroll"><table class="coefficient-table">'
        r"<thead><tr><th>\(P_\alpha\)</th>"
        r"<th>\(K_\alpha\) 的条件</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def compact_orbit_sheet(
    row: dict[str, str],
    orbit: dict[str, str],
) -> str:
    first = signed_permutation_matrix(orbit["representative_J1"])
    second = signed_permutation_matrix(orbit["representative_J2"])
    eta = phased_matrix_tex(
        orbit["eta_phase"], parse_integer_matrix(orbit["eta_matrix"])
    )
    group_terms = parse_orbit_terms(orbit["group_terms"])
    cone_terms = parse_orbit_terms(orbit["cone_terms"])
    if int(row["strict_interior"]):
        cone = rf"""
          <h6>\(A_{{\mathrm{{cone}}}}\)</h6>
          {orbit_sum_formula(r"A_{\mathrm{cone}}", cone_terms)}
          {compact_orbit_terms_table(cone_terms)}
          <div class="scroll">\[
            \boxed{{\eta A_{{\mathrm{{cone}}}}
              ={orbit_cone_lmi(orbit, cone_terms)}<0}}.
          \]</div>
        """
    else:
        cone = r"""
          <h6>\(A_{\mathrm{cone}}\)</h6>
          <p>严格不等式 \(\eta A_{\mathrm{cone}}<0\) 没有解。</p>
        """
    return rf"""
      <section class="orbit-sheet compact-orbit-sheet">
        <div class="scroll">\[
          J_1={pauli_decomposition_tex(first)},\qquad
          J_2={pauli_decomposition_tex(second)},\qquad
          \eta={eta}.
        \]</div>
        <h6>\(A_{{\mathrm{{group}}}}\)</h6>
        {orbit_sum_formula(r"A_{\mathrm{group}}", group_terms)}
        {compact_orbit_terms_table(group_terms)}
        {cone}
      </section>
    """


def compact_low_dimensional_block(
    row: dict[str, str],
    orbit_rows: list[dict[str, str]],
) -> str:
    blocks: list[str] = []
    for dimension in (2, 4):
        rows = [
            orbit
            for orbit in orbit_rows
            if int(orbit["matrix_dimension"]) == dimension
        ]
        blocks.append(rf"<h5>{dimension} 维</h5>")
        if rows:
            blocks.extend(compact_orbit_sheet(row, orbit) for orbit in rows)
        else:
            blocks.append("<p>没有这种维数的实正交表示。</p>")
    return r"""
      <details class="basis-audit low-dimensional-representations">
        <summary>同一类别中可能新增 \(A\) 方向的二维、四维表示</summary>
    """ + "".join(blocks) + "</details>"


def compact_positivity_result(
    row: dict[str, str], symmetry: dict[str, str]
) -> str:
    statements: list[str] = []
    if int(row["strict_interior"]):
        metric = r"J_2g" if row["metric"] == "J2g" else r"iJ_2g"
        statements.append(
            rf"<strong>收缩半群：</strong>\(A_{{\mathrm{{cone}}}}\) 非空，"
            rf"度规为 \(\eta={metric}\)。\(A_{{\mathrm{{group}}}}\) "
            r"给出等号方向，满足 \(\eta A_{\mathrm{cone}}<0\) 的方向"
            r"把传播送入收缩半群。"
        )
    else:
        statements.append(
            r"<strong>只有最大子群：</strong>"
            r"\(A_{\mathrm{cone}}\) 为空，不能由本卷的收缩半群路线定号。"
        )

    if int(row["strict_interior"]):
        return '<div class="compact-status"><p>' + statements[0] + "</p></div>"

    mechanism = symmetry["group_half_power_mechanism"]
    if mechanism == "conjugate_subsystems":
        sign = "-" if row["statistics"] == "boson" else "+"
        power = "^{-1}" if row["statistics"] == "boson" else ""
        physical = (
            "在满足物理 Nambu 共轭条件的表示中，"
            if row["statistics"] == "boson"
            else ""
        )
        statements.append(
            rf"<strong>时间反演正性：</strong>{physical}"
            r"两条时间反演对称性把传播分成 \(M_+\) 与"
            r" \(\overline{M_+}\) 两块，"
            rf"\(W=|\det(I{sign}M_+)|{power}\ge0\)。"
            r"这条结论作用于上面 \(A_{\mathrm{group}}\) 的逐层序列。"
        )
    elif mechanism == "kramers_pair":
        formula = (
            r"W=\sqrt{\det M_+}/\det(I-M_+)>0"
            if row["statistics"] == "boson"
            else r"W=\det(I+M_+)/\sqrt{\det M_+}\ge0"
        )
        physical = (
            "在满足物理 Nambu 共轭条件的表示中，"
            if row["statistics"] == "boson"
            else ""
        )
        statements.append(
            rf"<strong>时间反演正性：</strong>{physical}"
            r"两条平方为 \(-I\) 且彼此反对易的时间反演对称性给出 "
            rf"Kramers 配对；\(M_+\) 是一个独立分块上的传播矩阵，"
            rf"\({formula}\)。"
            r"这条结论作用于上面 \(A_{\mathrm{group}}\) 的逐层序列。"
        )
    elif not int(row["strict_interior"]):
        statements.append(
            r"<strong>时间反演筛选：</strong>这五条关系本身尚不足以证明"
            r"全部 \(A_{\mathrm{group}}\) 序列的权重非负。"
        )
    return '<div class="compact-status"><p>' + "</p><p>".join(
        statements
    ) + "</p></div>"


def compact_summary_relations(row: dict[str, str]) -> str:
    mutual = (
        r"J_1J_2=J_2J_1"
        if int(row["r"]) == 1
        else r"J_1J_2=-J_2J_1"
    )
    return rf"""
      <span class="compact-relations">
        <span>\(J_1^TgJ_1={sign_rhs(row["s1"], "g")}\)</span>
        <span>\(J_1^2={sign_rhs(row["q1"], "I")}\)</span>
        <span>\(J_2^TgJ_2={sign_rhs(row["s2"], "g")}\)</span>
        <span>\(J_2^2={sign_rhs(row["q2"], "I")}\)</span>
        <span>\({mutual}\)</span>
      </span>
    """


def compact_summary_status(
    row: dict[str, str], symmetry: dict[str, str]
) -> str:
    dimension = 2 ** int(row["n"])
    if int(row["strict_interior"]):
        metric = r"J_2g" if row["metric"] == "J2g" else r"iJ_2g"
        semigroup = rf"收缩半群：\(\eta={metric}\)"
        semigroup_class = "semigroup-yes"
    else:
        semigroup = "收缩半群：无"
        semigroup_class = "semigroup-no"
    if symmetry["group_half_power_mechanism"] in (
        "conjugate_subsystems",
        "kramers_pair",
    ):
        time_reversal = "时间反演：非负"
        time_reversal_class = "time-reversal-yes"
    else:
        time_reversal = "时间反演：本类不足以定号"
        time_reversal_class = "time-reversal-no"
    return rf"""
      <span class="compact-card-status">
        <span>最小维数：{dimension}</span>
        <span class="{semigroup_class}">{semigroup}</span>
        <span class="{time_reversal_class}">{time_reversal}</span>
      </span>
    """


def case_card(
    row: dict[str, str],
    full: dict[str, str],
    orbit_rows: list[dict[str, str]],
    number: int,
    symmetry: dict[str, str],
) -> str:
    card_id = f"class-{row['statistics']}-{number:02d}"
    return rf"""
      <details class="all-class-card" id="{card_id}">
        <summary>
          {compact_summary_relations(row)}
          {compact_summary_status(row, symmetry)}
        </summary>
        <div class="all-class-body tex2jax_ignore">
          {compact_representative_block(row)}
          {compact_positivity_result(row, symmetry)}
          {compact_group_block(row)}
          {compact_cone_block(row, full)}
          {compact_low_dimensional_block(row, orbit_rows)}
        </div>
      </details>
    """


def representation_answer() -> str:
    return r"""
      <h4>为什么每一类还要继续枚举二维和四维表示</h4>
      <p>
        “由五条正负关系定义的某一类别有没有严格收缩方向”只由
        <a href="#lemma-1">引理1</a>和
        <a href="#lemma-2">引理2</a>决定。这两个证明只用
        \(J_1,J_2\) 的五个正负号，完全没有使用某个 Pauli word。
        因此，同一类别换成另一组矩阵表示，不会把空 cone 变成非空，也
        不会把非空 cone 变成空。16 个严格类的数目不会因代表选择改变。
      </p>
      <p>
        “允许哪些具体 \(A\)”却必须知道 \(J_1,J_2\) 的矩阵本身。
        若一个保持 \(g\) 的实正交矩阵 \(S\) 把两组表示联系为
      </p>
      <div class="scroll">\[
        S^TgS=g,\qquad
        J_a'=S^{-1}J_aS,\qquad
        A'=S^{-1}AS ,
      \]</div>
      <p>
        那么两组 \(A\) 只是同一解空间的换坐标。若不存在这样的 \(S\)，
        五个正负号相同也可能允许不同的 \(A\) 方向。这里的差别不是一个
        新假设。它只表示同一个有限群可在四维空间中由不同的小块直和而成：
        某些选择把更多向量放在 \(J_1=+1\) 的子空间，另一些选择把更多
        向量放在 \(J_1=-1\) 的子空间；与 \(J_2\) 联合后，允许的矩阵元
        位置自然不同。
      </p>
      <p>
        为了不漏掉这些方向，程序不再只遍历单个 Pauli words，而是遍历
        二维与四维的全部 signed-permutation matrices，包括它们的可约
        直和表示。按保持 \(g\) 的实正交换基合并后，结果为
        \[
          \begin{array}{c|cc|c}
          &d=2&d=4&\text{合计}\\ \hline
          \text{玻色}&10&50&60\\
          \text{费米}&16&73&89
          \end{array}
        \]
        这里包含 \(J_1=\pm J_2\) 的表示，因为我们要保留全部允许
        \(A\) 方向。若要求两条 symmetry 确实不同，则相应数目是玻色
        \(7+44\)、费米 \(12+65\)，共 128 个。每张类别卡末尾同时列出
        二维和四维结果，即使该类最小表示已经是二维。
      </p>
      <p>
        单-Pauli 搜索真正漏掉的例子集中在四维费米全正类。例如把费米
        \(g\) 写成 \(\operatorname{diag}(1,1,-1,-1)\)，取
        \[
          J_1=\operatorname{diag}(1,1,1,-1),\qquad
          J_2=\operatorname{diag}(1,-1,1,1),
        \]
        二者满足五个正号且彼此对易，但
        \(\operatorname{Tr}J_1=\operatorname{Tr}J_2=2\)；四维单 Pauli
        word 的迹的绝对值只能是 0 或 4，所以单-Pauli 表不可能包含它。
        新枚举已经把它以及同类其余可约表示全部纳入。
      </p>
      <p>
        对玻色 Hamiltonian 还要做第二层区分。记
        \(C=\sigma_x^{\mathrm{Nambu}}\otimes I\)，物理 Nambu 算符满足
        \(\chi^\dagger=\chi^TC\)。一个只保持 \(g\) 的换基矩阵未必也
        保持 \(C\)，所以“代数上等价”不必等于“同一个玻色 Fock
        representation 中物理等价”。本报告另用
        \[
          S^TgS=g,\qquad S^TCS=C
        \]
        重新细分玻色物理轨道，并只从这些物理轨道构造 Hamiltonian。
        因此，149 个代数轨道负责证明没有漏掉矩阵解；玻色物理子表负责
        保证 \(b^+\) 仍是 \(b\) 的 Hermitian conjugate。两种表承担
        不同任务。
      </p>
    """


def minimal_dimension_proof() -> str:
    return r"""
      <h4>五条代数关系的最小维数怎样读</h4>
      <p>
        下表先只问实正交矩阵 \(g,J_1,J_2\) 实现五条关系需要多大维数。
        若玻色代表还通过 \(C\overline U_aC=U_a\)，维数 2 才可解释为
        \((a,a^+)^T\) 的一个物理模，维数 4 对应两个模，维数 8 对应
        四个模。B12、B32 正好说明两种维数不能混写：五条代数关系四维
        已有解，但物理 Nambu 表示到八维才首次出现。
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
          必须单独带一个可逆、没有零方向的玻色 Nambu 结构。与此同时
          \(J_1\)
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
      <style>
        details.all-class-card > summary {
          font-size: 1.08rem;
          line-height: 1.75;
          padding: 0.7rem 0.8rem;
        }
        .compact-relations {
          display: inline-flex;
          flex-wrap: wrap;
          gap: 0.2rem 1rem;
          vertical-align: top;
        }
        .compact-relations > span { white-space: nowrap; }
        .compact-card-status {
          display: flex;
          flex-wrap: wrap;
          gap: 0.35rem 0.5rem;
          margin: 0.45rem 0 0 1.35rem;
        }
        .compact-card-status > span {
          border: 1px solid #aab4af;
          border-radius: 4px;
          padding: 0.08rem 0.45rem;
          font-size: 0.92rem;
          font-weight: 600;
          white-space: nowrap;
        }
        .compact-card-status .semigroup-yes,
        .compact-card-status .time-reversal-yes {
          border-color: #50816c;
          color: #245943;
          background: #f0f7f3;
        }
        .compact-card-status .semigroup-no,
        .compact-card-status .time-reversal-no {
          color: #535c58;
          background: #f5f6f5;
        }
        .compact-representative { font-size: 1.02rem; }
        .compact-status {
          border-left: 4px solid #2f6f57;
          padding: 0.15rem 0.8rem;
          margin: 0.8rem 0 1rem;
        }
        .compact-status p { margin: 0.45rem 0; }
        .compact-generator { margin: 1rem 0 1.25rem; }
        .compact-generator h4 { margin-bottom: 0.35rem; }
        .compact-generator .coefficient-table,
        .compact-orbit-sheet .coefficient-table { font-size: 1rem; }
        .compact-orbit-sheet {
          border-top: 1px solid #c9d0cc;
          padding-top: 0.7rem;
          margin-top: 0.9rem;
        }
        .compact-orbit-sheet h6 {
          font-size: 1rem;
          margin: 0.55rem 0 0.1rem;
        }
      </style>
      <div class="note">
        <strong>64 类的阅读顺序。</strong>
        先看五条关系，再看 \(A_{\mathrm{cone}}\) 是否非空。非空者形成
        以所列 \(\eta\) 为度规的收缩半群；为空者只有最大子群。随后一行
        单独说明原有两条时间反演对称性是否还能证明
        \(A_{\mathrm{group}}\) 序列非负。展开卡片即可查到完整的
        \(A_{\mathrm{group}}\) 与 \(A_{\mathrm{cone}}\) 解。
      </div>
      <div class="derivation">
        <p>
          收缩锥卡片不再把
          \(\eta A_{\mathrm{cone}}-A_{\mathrm{cone}}^\dagger\eta=0\)
          列作独立条件。取 \(\eta=\alpha J_2g\)，其中
          \(\alpha=1\) 或 \(i\)。由
          \(J_2^TA_{\mathrm{cone}}J_2=-\overline{A_{\mathrm{cone}}}\)、
          \(gA_{\mathrm{cone}}+A_{\mathrm{cone}}^Tg=0\)、
          \(J_2^T=J_2^{-1}\) 可直接得到
        </p>
        <div class="scroll">\[
          A_{\mathrm{cone}}^\dagger\eta
          =-\alpha J_2^TA_{\mathrm{cone}}^TJ_2^2g
          =\alpha J_2gA_{\mathrm{cone}}
          =\eta A_{\mathrm{cone}}.
        \]</div>
        <p>
          因而 \(\eta A_{\mathrm{cone}}\) 自动是 Hermitian 矩阵，唯一还要
          施加的不等式就是
          \(\eta A_{\mathrm{cone}}+A_{\mathrm{cone}}^\dagger\eta<0\)，
          等价地写成 \(\eta A_{\mathrm{cone}}<0\)。
        </p>
      </div>
      <div class="note">
        <strong>为什么仍要检查同一类的其他低维表示。</strong>
        卡片顶部的 Pauli 代表以及任意系数矩阵 \(K_P\)，已经包含该代表的
        任意份相同拷贝，但没有自动包含由不同小块组成的可约表示。后者有时
        确实改变允许的 \(A\) 空间。例如五条关系右侧全取正号的四维费米
        类，其不同表示给出
        \(\dim A_{\mathrm{group}}=6,3,2\) 三种结果。
        因此只保留一组代表会漏掉生成元方向。每张卡末尾只把不等价表示列
        一次，并将 \(J_1,J_2\) 写成
        \(I_2,\sigma_x,i\sigma_y,\sigma_z\) 的张量组合；读者无需再从
        展开的整数矩阵辨认其结构。
      </div>
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
    symmetry_rows = {
        (row["statistics"], row["class_id"]): row
        for row in csv.DictReader(HALF_POWER_PATH.open(encoding="utf-8"))
    }
    orbit_rows_by_class: dict[
        tuple[str, str], list[dict[str, str]]
    ] = {}
    for orbit in csv.DictReader(
        LOW_DIMENSIONAL_REPRESENTATIONS_PATH.open(encoding="utf-8")
    ):
        orbit_rows_by_class.setdefault(
            (orbit["statistics"], orbit["class_id"]), []
        ).append(orbit)
    if not (
        len(tensor_rows)
        == len(maximal_rows)
        == len(full_rows)
        == len(symmetry_rows)
        == 64
    ):
        raise RuntimeError("Expected 64 rows in every classification table")

    blocks = [
        atlas_guide(),
        lazy_mathjax_script(),
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
                    full_rows[key],
                    orbit_rows_by_class.get(key, []),
                    number,
                    symmetry_rows[key],
                )
            )
        if number != 32:
            raise RuntimeError(f"Expected 32 {statistic} rows, found {number}")

    blocks.append(
        r"""
        <p class="small">
          机器可读结果：
          <a href="tables/full_64_class_enumeration.csv">五条正负关系、度规、
          最小维数与两个阻碍判据</a>；
          <a href="tables/tensor_block_structures.csv">每类
          \(P\otimes K_P\) 的完整等式解</a>；
          <a href="tables/maximal_subgroup_structures.csv">每类
          最大子群线性空间与数值残差</a>；
          <a href="tables/half_power_symmetry_64_classes.csv">64 类实际
          Spin/metaplectic half-power 的算符级正性结论</a>；
          <a href="tables/nonpauli_realization_dependence.csv">同类不等价
          表示的维数对照</a>；
          <a href="tables/real_representation_orbits_le4.csv">二维与四维
          149 个完整实正交表示轨道及其 \(A\) 基底</a>；
          <a href="tables/bosonic_physical_representation_suborbits_le4.csv">
          同时保持 \(g\) 与物理 Nambu 共轭关系的玻色表示轨道</a>。
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
