#!/usr/bin/env python3
"""Build the reader-facing report with a line-complete rendered note walkthrough."""

from __future__ import annotations

import html
import subprocess
from dataclasses import dataclass
from pathlib import Path

from all_class_lecture import build_all_class_lecture
from case_audit_summaries import CASE_AUDITS
from reader_explanation_overrides import EXPLANATION_OVERRIDES


REPORT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = REPORT_DIR.parents[2]
NOTE_PATH = REPO_ROOT / "experts" / "ToYinkaiYu-20260726.tex"
TEMPLATE_PATH = REPORT_DIR / "report_updated_note_full_enumeration_zh.template.html"
OUTPUT_PATH = REPORT_DIR / "report_updated_note_full_enumeration_zh.html"
CANONICAL_FRAGMENT_PATH = REPORT_DIR / "canonical_afqmc_algorithm_zh.fragment.html"
ENUMERATION_TAIL_PATH = REPORT_DIR / "enumeration_tail_zh.fragment.html"
DETERMINANT_SYMMETRY_BRIDGE_PATH = (
    REPORT_DIR / "determinant_symmetry_bridge_zh.fragment.html"
)


@dataclass(frozen=True)
class Segment:
    key: str
    title: str
    start: int
    end: int
    translation: str
    explanation: str
    collapse_source: bool = False


SEGMENTS = [
    Segment(
        "summary-objects",
        "第一节标题、玻色与费米的统一二次型",
        22,
        50,
        r"""
        <p><em>A short summary for bosonic and fermionic AFQMC</em> 译为
        “玻色与费米 AFQMC 的简短总结”。作者先分别给出玻色和费米的 \(g\)，
        再把两类二次算符都写成 \(h_i=\frac12\chi^TgA_i\chi\)。
        最后一句说：玻色生成元满足复辛代数条件，费米生成元满足复正交代数条件。</p>
        """,
        r"""
        <p>\(\chi\) 是 Nambu 列向量：前 \(N\) 个分量是湮灭算符，后 \(N\) 个分量是产生算符。
        玻色矩阵 \(g=-\Omega\) 满足 \(g^T=-g\) 与 \(g^2=-I\)；费米矩阵
        \(g=\sigma_x\otimes I_N\) 满足 \(g^T=g\) 与 \(g^2=I\)。
        条件 \(gA+A^Tg=0\) 保证 \(gA\) 具有二次算符所需的交换对称性：</p>
        <div class="scroll">\[
          \begin{array}{ll}
          \text{玻色：}&(gA)^T=gA,\\[2pt]
          \text{费米：}&(gA)^T=-gA.
          \end{array}
        \]</div>
        <p>因此玻色 pairing 系数是对称矩阵，费米 pairing 系数是反对称矩阵。
        原文中的 \(sp(2N,\mathbb C)\) 和 \(so(2N,\mathbb C)\) 只是这两条矩阵约束的标准名称；
        读者不需要先掌握李代数术语才能继续阅读。</p>
        """,
    ),
    Segment(
        "summary-weight",
        "对易子与辅助场构型权重",
        51,
        56,
        r"""
        <p>原文第一句说，两个二次算符的对易子仍由矩阵对易子 \([A_1,A_2]\) 表示。
        第二句给出多个时间片相乘后的 Fock-space trace，并把它写成单粒子矩阵乘积的行列式。</p>
        """,
        r"""
        <p>矩阵恒等式的物理作用是把 many-body operator calculation 化成有限维矩阵计算。
        若 \(M=e^{A_1}\cdots e^{A_k}\)，原式的上下号应分开读。这里还要就地
        修正原文漏掉的一个玻色奇偶因子：</p>
        <div class="scroll">\[
          p_{\rm boson}=\bigl[(-1)^N\det(I-M)\bigr]_{\rm op}^{-1/2},\qquad
          p_{\rm fermion}=\bigl[\det(I+M)\bigr]_{\rm op}^{1/2}.
        \]</div>
        <p>一个物理 boson mode 对应一对倒数本征值
        \(\lambda,\lambda^{-1}\)，而
        \((1-\lambda)(1-\lambda^{-1})=-(1-\lambda)^2/\lambda\)。因此
        \(N\) 个物理 boson modes 总共产生 \((-1)^N\)。原文公式仅在 \(N\)
        为偶数时保持原样；这也是当前文章的 paired trace 公式明确限制到偶数
        \(N\) 的原因。下标 “op” 表示平方根由实际有序 Fock operator 固定，
        不是取任意 principal root。平方根还需要指定连续分支；玻色式还要求 Fock trace 收敛，即不能碰到
        \(\det(I-M)=0\) 的 pole。这个公式也说明后面所有 semigroup 条件最终必须控制
        \(e^A\) 及其乘积，而不只是二次型系数 \(gA\)。</p>
        """,
    ),
    Segment(
        "boson-known",
        "玻色列表的前两类：time-reversal symmetry 与 reflection positivity",
        57,
        66,
        r"""
        <p>原文说“玻色有 6 个 passed cases”，随后先列两类已有结构。
        第 1 类是由两个 anti-linear \(Z_2\) symmetries 组成的 time-reversal symmetry；
        第 2 类是 reflection positivity，并特别注明它不是 contraction semigroup。</p>
        """,
        r"""
        <div class="warning">
          <strong>先按三种不同证明路线读这两项。</strong>
          这里的 1) 与 2) 不是后面 Cases 3--16 的前两个
          contraction candidates。1) 调用 Kramers eigenvalue pairing；
          2) 调用 operator-level reflected squares，并额外需要 positive
          cross-reflection coefficient。只有后面的 “Contraction semigroup
          cases” 才固定 \(J_1^TAJ_1=\bar A\) 与
          \(\eta A+A^\dagger\eta\le0\)，再穷举五条离散关系。
          note 把三者连续编号，是为了尝试统一整理已知和候选的无符号机制，
          不是说它们已经由同一个不等式证明。
        </div>

        <h4>先说明 \(J_1\) 和 \(J_2\) 是什么</h4>
        <p>note 到这里第一次写 \(J_1,J_2\)，却没有先定义，确实会让人无法继续读。
        它们都是作用在 \(2N\) 维 Nambu 列向量上的<strong>实正交矩阵</strong>：
        \(J_i^TJ_i=I_{2N}\)。下标 1、2 只表示“第一个”和“第二个”变换；
        它们不是两个新粒子，也不是 Hamiltonian 的两个部分。给定一个复向量 \(v\)，
        相应的 anti-linear transformation 实际作用为</p>
        <div class="scroll">\[
          v\longmapsto J_i\bar v .
        \]</div>
        <p>也就是说，先把向量逐分量复共轭，再左乘 \(J_i\)。
        若用 \(\mathcal K\) 表示逐分量复共轭，这个完整变换才是
        \(J_i\mathcal K\)，而不是 \(J_i\) 单独一个矩阵。因为这里的
        \(J_i\) 都是实矩阵，连续做两次得到</p>
        <div class="scroll">\[
          (J_i\mathcal K)^2v
          =J_i\overline{J_i\bar v}
          =J_i^2v .
        \]</div>
        <p>因此 \(J_i^2=I\) 时，\(J_i\mathcal K\) 在向量上严格平方为恒等；
        \(J_i^2=-I\) 时，平方后得到一个负号，这是 Kramers-type
        anti-linear structure。这里随即出现一个表面矛盾：既然本条的
        \(J_1^2=J_2^2=-I\)，为什么原文仍称它们为两个 \(Z_2\)？</p>

        <h4>“two \(Z_2\) anti-linear symmetries”逐字指什么</h4>
        <p>
        “two” 最直接的意思是：这里提出了两个候选的反线性变换，
        </p>
        <div class="scroll">\[
          \Theta_1=J_1\mathcal K,\qquad
          \Theta_2=J_2\mathcal K .
        \]</div>
        <p>
        它不是说存在一个取两个值的辅助场，也不是说 \(J_1,J_2\)
        是度规中的两个相因子。每个 \(\Theta_i\) 都先复共轭，再做一次
        \(J_i\) 给出的实线性变换。
        </p>
        <p>
        “\(Z_2\)”需要稍加解释。这里
        \(\Theta_i^2=-I\)，所以若把 \(\Theta_i\) 当作作用在单粒子列向量
        上的普通线性算符，它并不是严格平方为 \(+I\) 的二阶算符。
        物理上仍把它称作 \(Z_2\) anti-linear symmetry，是因为这个负号
        对单粒子态的射线只是整体相位；对含有两个场算符的 quadratic
        Hamiltonian，两个场各得到一个负号，乘起来也是 \(+1\)。
        换成更精确的数学说法，\(\Theta_i\) 在单粒子向量上给出
        \(Z_2\) 的 projective representation，而它在 quadratic
        coefficient 上诱导的变换才严格平方为恒等。
        </p>
        <p>
        为了直接看见后一句，暂时把 quadratic form 的完整系数记作
        \(M=gA\)。\(\Theta_i\) 在 \(M\) 上诱导的操作是
        </p>
        <div class="scroll">\[
          M\longmapsto J_i^T\overline M\,J_i .
        \]</div>
        <p>
        “anti-linear”来自 \(M\) 被复共轭。对于本条的实正交 \(J_i\)
        与 \(J_i^2=-I\)，有 \(J_i^T=J_i^{-1}=-J_i\)。因此同一个操作
        连续做两次，结果为
        </p>
        <div class="scroll">\[
          \begin{aligned}
          M
          &\longmapsto J_i^T\overline M J_i\\
          &\longmapsto
          J_i^T\overline{\,J_i^T\overline M J_i\,}J_i\\
          &=(J_i^T)^2M J_i^2
          =(-I)M(-I)=M .
          \end{aligned}
        \]</div>
        <p>
        左右两边的两个负号恰好相消。这就是这里的每一个
        “\(Z_2\)”：它在 quadratic coefficient 上做两次便回到原处。
        因而 \(\Theta_i^2=-I\) 与 “\(Z_2\)”并不矛盾，二者说的是
        同一变换作用在不同对象上的结果。
        </p>
        <p>
        本条还要求 \([J_1,J_2]=0\)。因为 \(J_1,J_2\) 都是实矩阵，
        两个反线性变换在 quadratic coefficient 上诱导的操作也彼此对易。
        若这两个诱导操作确实不同，并且一个允许的 Hamiltonian 同时在二者
        之下不变，那么恒等操作、第一种操作、第二种操作及二者的乘积
        形成 \(Z_2\times Z_2\)。这就是 “two \(Z_2\) anti-linear
        symmetries” 在 quadratic Hamiltonian 层面的准确含义。
        </p>
        <p class="small">
        这一读法与合作者所用半群来源的定义一致：
        <a href="https://arxiv.org/html/1712.09412v3#S4">Wei,
        Semigroup approach to the sign problem in quantum Monte Carlo
        simulations，Sec. IV</a> 先把两种操作明确写成实正交 \(J_1,J_2\)
        与复共轭共同作用在 coefficient matrix \(A\) 上，再分别用于限制
        weight 的实性和构造 contraction metric。
        </p>
        <div class="warning">
          <strong>原文的五条式子还没有规定 \(A\)。</strong>
          它只列了 \(J_i\) 对 \(g\) 的作用、\(J_i^2\) 以及二者的
          对易关系。若 \(J_iK\) 确实是某个具体 quadratic Hamiltonian
          的 anti-linear symmetry，才应另外检查
          \[
          J_i^T\overline{(gA)}J_i=gA .
          \]
          对本条的两个 \(J\)，这会分别变成
          \[
          J_1^TAJ_1=\overline A,\qquad
          J_2^TAJ_2=-\overline A .
          \]
          但是，文章的 number-conserving Kramers slice 一般只满足第一式；
          它对 note 给出的第二个 \(J_2\) 满足的是带 transpose 的另一条
          Nambu 恒等式，下面会逐块算出。因此不能从 “two anti-linear
          symmetries” 这句话直接推断文章的 \(A\) 同时满足上面两式。
          对当前文章而言，\(J_1K\) 是真正施加在物理 annihilation
          operators 上的 Kramers symmetry；\(J_2\) 是把它写进
          particle/hole doubled space 后出现的结构性伴随矩阵。
        </div>
        <p>
        在本文两组分、无配对的物理实现中，还要再区分“两个矩阵操作”
        与“两个独立的物理 time reversal”。后文会具体得到
        \(J_2=(\sigma_x^{\rm Nambu}\otimes I)J_1\)：第二个变换等于
        同一个 physical Kramers transformation 再乘 Nambu
        particle/hole exchange。因此该实现只有一个独立的 physical
        time-reversal symmetry；第二个 \(Z_2\) 来自把它放进
        Nambu doubled coefficient space 后得到的伴随操作。
        </p>

        <h4>三个会反复使用的 \(2\times2\) 实矩阵</h4>
        <p>为看清后面的张量积，把 note 使用的 Pauli matrices 直接写开：</p>
        <div class="scroll">\[
          I_2=\begin{pmatrix}1&0\\0&1\end{pmatrix},\qquad
          \sigma_x=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
          i\sigma_y=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
          \sigma_z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
        \]</div>
        <p>其中 \(\sigma_x^2=\sigma_z^2=I_2\)，而
        \((i\sigma_y)^2=-I_2\)。不同 Pauli matrices 彼此反对易，例如
        \(\sigma_x(i\sigma_y)=-(i\sigma_y)\sigma_x\)。
        为了与文章的两种玻色子直接对齐，下面固定 Nambu 顺序为
        \(\chi=(\hat b,\hat c,\hat b^+,\hat c^+)^T\)。于是张量积的第一个
        \(2\times2\) 因子作用在 particle/hole 空间，第二个因子作用在
        \(b/c\) flavor 空间；若每种 flavor 含多个格点，最后再张量乘 site identity。
        这样每个 Pauli factor 都有明确的物理位置。</p>

        <h4>\(J_i^TgJ_i=\pm g\) 在说什么</h4>
        <p>玻色 \(g\) 已在 1.1 定义。最小的 \(N=1\) 情形是</p>
        <div class="scroll">\[
          g=\begin{pmatrix}0&-1\\1&0\end{pmatrix}=-\,i\sigma_y .
        \]</div>
        <p>\(J_i^TgJ_i=g\) 表示这个基变换保持玻色 canonical commutation
        structure；\(J_i^TgJ_i=-g\) 表示它把该 structure 的符号翻转。
        这条关系只说明 \(J_i\) 如何作用于 \(g\)，还没有说明 \(A\) 是否具有该 symmetry。</p>

        <h4>为什么二次算符的 symmetry 要看 \(gA\)</h4>
        <p>note 的二次算符是 \(h=\frac12\chi^TgA\chi\)，所以系数矩阵是
        \(gA\)，不是 \(A\) 单独。anti-linear transformation 保持这个二次型时，
        要求</p>
        <div class="scroll">\[
          J_i^T(gA)J_i=\overline{gA}=g\bar A .
        \]</div>
        <p>由于 \(J_iJ_i^T=I\)，左边可以不跳步地拆成</p>
        <div class="scroll">\[
          J_i^TgAJ_i
          =J_i^Tg(J_iJ_i^T)AJ_i
          =(J_i^TgJ_i)(J_i^TAJ_i).
        \]</div>
        <p>于是有两种不同情况：</p>
        <div class="scroll">\[
          \begin{array}{c|c}
          J_i^TgJ_i=g & J_i^TAJ_i=\bar A\\[2pt]
          J_i^TgJ_i=-g & J_i^TAJ_i=-\bar A
          \end{array}
        \]</div>
        <p>这正是“\(h\) 的 symmetry 由 \(gA\) 决定，而 \(A\) 自己的条件可能差一个负号”
        的具体内容。不过 note 的前两类只列出 \(J_i\) 与 \(g\) 的离散关系，
        没有在这里写出每个 \(J_i\) 对 \(A\) 的完整条件；不能仅凭这五条关系就假定
        两个 \(J_iK\) 都按同一个公式保持 Hamiltonian。后面的 contraction list
        才明确把 \(J_1^TAJ_1=\bar A\) 写成共同条件。</p>

        <h4>怎样从文章的物理 time reversal 得到 note 的 \(J_1,J_2\)</h4>
        <p><code>main.tex</code> 的 TRS theorem 先在<strong>没有 pairing、粒子数守恒</strong>
        的单粒子空间中定义一个 Kramers antiunitary transformation。
        对文章的两种 flavor，它的作用是</p>
        <div class="scroll">\[
          \Theta\hat b\,\Theta^{-1}=\hat c,\qquad
          \Theta\hat c\,\Theta^{-1}=-\hat b,\qquad
          \Theta i\Theta^{-1}=-i .
        \]</div>
        <p>因此在 \((\hat b,\hat c)^T\) 上，\(\Theta=UK\) 中的 real matrix 是</p>
        <div class="scroll">\[
          U=i\sigma_y=\begin{pmatrix}0&1\\-1&0\end{pmatrix},
          \qquad U^2=-I_2 .
        \]</div>
        <p>把同一个变换写到
        \(\chi=(\hat b,\hat c,\hat b^+,\hat c^+)^T\) 上，matrix 就是</p>
        <div class="scroll">\[
          g=-i\sigma_y\otimes I_2,\qquad
          J_1=I_2\otimes i\sigma_y,\qquad
          J_2=\sigma_x\otimes i\sigma_y .
        \]</div>
        <p>这里 \(J_1K\) 就是文章真正施加的 physical time reversal。
        \(J_2\) 可写成</p>
        <div class="scroll">\[
          J_2=(\sigma_x\otimes I_2)J_1 .
        \]</div>
        <p>前面的 \(\sigma_x\otimes I_2\) 只交换 Nambu 的 particle 与 hole
        两半。因此 note 所说的 “two anti-linear symmetries” 不应理解成体系中
        另有第二个彼此独立的 physical time-reversal operation；在这个 realization
        中，第二个 \(J\) 是 physical Kramers transformation 与 Nambu
        particle-hole doubling 的组合。逐项检查可得</p>
        <div class="scroll">\[
          \begin{aligned}
          J_1^2&=-I_4,&
          J_1^TgJ_1&=g,\\
          J_2^2&=-I_4,&
          J_2^TgJ_2&=-g,\\
          J_1J_2&=J_2J_1.&&
          \end{aligned}
        \]</div>
        <p>这五个等式只核对 note 本段实际写出的 \(J,g\) relations。
        要判断它们如何作用于文章的 Hamiltonian，还要先写出 physical slice。</p>
        <p>文章的单时间片写成
        \(\hat h=\hat{\boldsymbol a}^+B\hat{\boldsymbol a}\)，其中
        \(\hat{\boldsymbol a}=(\hat{\boldsymbol b},\hat{\boldsymbol c})^T\)。
        Kramers condition \(U^\dagger\bar B U=B\) 等价于文章给出的 block form</p>
        <div class="scroll">\[
          B=\begin{pmatrix}
          D&F\\-\bar F&\bar D
          \end{pmatrix}.
        \]</div>
        <p>同一个 number-conserving slice 的 Nambu exponent generator 是</p>
        <div class="scroll">\[
          A=\begin{pmatrix}B&0\\0&-B^T\end{pmatrix}.
        \]</div>
        <p>这一步还包含一个容易漏掉的正规序常数。直接代入 note 的定义，</p>
        <div class="scroll">\[
          \begin{aligned}
          \frac12\chi^TgA\chi
          &=\frac12\left(
          \hat{\boldsymbol a}^{T}B^T\hat{\boldsymbol a}^{+}
          +\hat{\boldsymbol a}^{+T}B\hat{\boldsymbol a}\right)\\
          &=\hat{\boldsymbol a}^{+T}B\hat{\boldsymbol a}
          +\frac12\Tr B .
          \end{aligned}
        \]</div>
        <p>所以若物理 slice 写成
        \(\hat h=\hat{\boldsymbol a}^{+T}B\hat{\boldsymbol a}\)，
        note 的完整表示应取
        \(\xi=-\frac12\Tr B\)。Kramers block form 使
        \(\Tr B=2\operatorname{Re}\Tr D\) 为实数，因此这个标量不会
        重新引入 complex phase。</p>
        <p>现在才把上面的 \(J_1,J_2\) 代入，可以直接算到</p>
        <div class="scroll">\[
          J_1^TAJ_1=\bar A,\qquad
          J_2^TAJ_2=-\bar A^T .
        \]</div>
        <p>第二式多出的 transpose 来自 Nambu particle/hole exchange。
        它再次说明 \(J_2K\) 包含 Nambu doubling relation，不能当成文章额外施加的
        第二个 physical time reversal。</p>
        <p>在 Nambu 空间中，相同条件由 \(J_1K\) 作用到 exponent generator
        \(A\) 上。令
        \(\mathcal B=e^{B_1}\cdots e^{B_L}\)。physical Kramers symmetry
        使 \(\mathcal B\) 的非实 eigenvalues 以
        \(\lambda,\bar\lambda\) 配对，实 eigenvalues 则有偶数重数，所以</p>
        <div class="scroll">\[
          \det(I-\mathcal B)
          =\prod_{\lambda\notin\mathbb R}|1-\lambda|^2
           \prod_{r\in\mathbb R}(1-r)^{\text{even}}\ge0 .
        \]</div>
        <p>这才是 <code>main.tex</code> 中 TRS 消除符号问题的物理机制：
        Kramers partners 让 determinant 的所有潜在负因子成对出现。
        该 theorem 当前只覆盖 number-conserving slices；文章在
        \(\Delta\ne0\) 时没有用它来证明 paired Nambu weight，而是使用下面的 RP theorem。</p>

        <h4>Case 1 中 \(A\) 应满足的完整结构</h4>
        <p>现在可以把 Case 1 从五条离散关系补成一个可实际检查的
        \(A\)-criterion。文章所用的物理条件依次是</p>
        <div class="scroll">\[
          \begin{gathered}
          A=\begin{pmatrix}B&0\\0&-B^T\end{pmatrix},\qquad
          B=\begin{pmatrix}D&F\\-\bar F&\bar D\end{pmatrix},\\
          J_1=I_2\otimes i\sigma_y,\qquad
          J_1^TAJ_1=\bar A,\qquad
          \xi=-\frac12\Tr B\in\mathbb R .
          \end{gathered}
        \]</div>
        <p>第一行先排除 pairing，并写出所有 Kramers-symmetric
        number-conserving generators；\(D\) 和 \(F\) 都可以是任意
        complex matrices。第二行说明这个 block form 正是
        \(J_1K\) invariance，而不是额外假定第二个独立的 physical
        time reversal。note 的第二个矩阵
        \(J_2=\sigma_x\otimes i\sigma_y\) 随后自动满足
        \(J_2^TAJ_2=-\bar A^T\)，但它不再缩小 \(D,F\) 的取值范围。</p>

        <h4>若沿收缩半群流程继续，Case 1 会落到 Case 8 的一个子类</h4>
        <p>time-reversal symmetry 本身允许 \(B\) 和 \(-B\)，所以它没有
        选定“衰减”方向。要让每个时间片还具有可由局部矩阵检查的
        bosonic damping，可以从 Case 1 已有的两个矩阵构造</p>
        <div class="scroll">\[
          -J_2J_1=\sigma_x\otimes I .
        \]</div>
        <p>这个新矩阵的平方为 \(+I\)，保持 \(J_1^2=-I\)，并与 \(J_1\)
        对易；它正是 note Case 8 中负责收缩的 \(J_2\)，而不是
        Case 1 原先平方为 \(-I\) 的第二个矩阵。它与 \(g\) 相乘得到</p>
        <div class="scroll">\[
          (-J_2J_1)g=
          \begin{pmatrix}I&0\\0&-I\end{pmatrix}.
        \]</div>
        <p>将上面的 number-conserving \(A\) 代入完整矩阵不等式，左右两块
        不省略地算成</p>
        <div class="scroll">\[
          \begin{aligned}
          &\bigl[(-J_2J_1)g\bigr]A
          +A^\dagger\bigl[(-J_2J_1)g\bigr]\\
          &\qquad=
          \begin{pmatrix}
          B+B^\dagger&0\\
          0&(B+B^\dagger)^T
          \end{pmatrix}.
          \end{aligned}
        \]</div>
        <p>因此这个交集的局部判据恰好是
        \(B+B^\dagger\le0\)。若严格小于零，每个 one-particle
        slice \(e^B\) 都在通常的 Hilbert-space norm 下收缩；
        若取等号，则该 slice 是 unitary。把 \(B\) 拆成</p>
        <div class="scroll">\[
          B_{\rm reversible}=\frac{B-B^\dagger}{2},\qquad
          B_{\rm damping}=\frac{B+B^\dagger}{2}\le0
        \]</div>
        <p>就得到与后文 maximal subgroup 和 invariant cone 完全对应的两部分。
        用文章的 \(D,F\) 逐块写出，第一部分满足</p>
        <div class="scroll">\[
          B_{\rm reversible}=
          \begin{pmatrix}
          D_{\rm a}&F_{\rm s}\\
          -\bar F_{\rm s}&\bar D_{\rm a}
          \end{pmatrix},\qquad
          D_{\rm a}^\dagger=-D_{\rm a},\quad
          F_{\rm s}^T=F_{\rm s},
        \]</div>
        <p>它生成 Kramers-symmetric unitary propagations。第二部分满足</p>
        <div class="scroll">\[
          B_{\rm damping}=
          \begin{pmatrix}
          D_{\rm h}&F_{\rm a}\\
          -\bar F_{\rm a}&\bar D_{\rm h}
          \end{pmatrix}\le0,\qquad
          D_{\rm h}^\dagger=D_{\rm h},\quad
          F_{\rm a}^T=-F_{\rm a},
        \]</div>
        <p>它提供 one-sided damping。这里
        \(D_{\rm a}=(D-D^\dagger)/2\)、
        \(D_{\rm h}=(D+D^\dagger)/2\)、
        \(F_{\rm s}=(F+F^T)/2\)、
        \(F_{\rm a}=(F-F^T)/2\)，没有引入新的自由度。
        因而 Case 1 的全部 TRS generators 由 Kramers block form 给出；
        其中还能逐 slice 证明收缩与 trace convergence 的部分，正好是
        Case 8 的 \(B+B^\dagger\le0\) 子类。</p>

        <h4>怎样从文章的 physical reflection 得到 note 的 \(J_1\)</h4>
        <p><code>main.tex</code> 把 \(b\) flavor 与 \(c\) flavor 当作 reflection
        的两侧，定义</p>
        <div class="scroll">\[
          \theta(i)=-i,\qquad
          \theta(\hat b_i)=\eta_i\hat c_i,\qquad
          \theta(\hat b_i^+)=\bar\eta_i\hat c_i^+ .
        \]</div>
        <p>这里 \(\theta\) 是 anti-linear operation，所以
        \(\theta(z\hat O)=\bar z\,\theta(\hat O)\)。reflection 还应满足
        \(\theta^2=1\)。把 \(\theta\) 连续作用两次到 \(\hat b_i\) 上，得到</p>
        <div class="scroll">\[
          \theta^2(\hat b_i)
          =\theta(\eta_i\hat c_i)
          =\bar\eta_i\,\theta(\hat c_i)
          =\hat b_i .
        \]</div>
        <p>由于 \(|\eta_i|=1\)，上式要求
        \(\theta(\hat c_i)=\eta_i\hat b_i\)。同理，creation operators 满足
        \(\theta(\hat c_i^+)=\bar\eta_i\hat b_i^+\)。因此在单格点 Nambu
        顺序
        \(\chi_i=(\hat b_i,\hat c_i,\hat b_i^+,\hat c_i^+)^T\) 中，
        physical reflection 的完整 matrix form 是</p>
        <div class="scroll">\[
          \theta:\ \chi_i\longmapsto J_1(\eta_i)\,\bar\chi_i,\qquad
          J_1(\eta_i)=
          \begin{pmatrix}
            0&\eta_i&0&0\\
            \eta_i&0&0&0\\
            0&0&0&\bar\eta_i\\
            0&0&\bar\eta_i&0
          \end{pmatrix}.
        \]</div>
        <p>任意 reflection phase 已经完整地包含在这个 \(J_1(\eta_i)\) 中。
        当 \(\eta_i\) 不是 real number 时，\(J_1(\eta_i)\) 也不是 real
        matrix；anti-linear operation 平方为一的正确检查是</p>
        <div class="scroll">\[
          J_1(\eta_i)\,\overline{J_1(\eta_i)}=I_4 ,
        \]</div>
        <p>而不是把 complex matrix 误写成 \(J_1(\eta_i)^2=I_4\)。
        note 从一开始把 \(J_1,J_2\) 限定为 real orthogonal matrices，
        因而它实际上已经选取了 \(\eta_i=1\) 的 phase convention。</p>

        <h4>为什么 \(\eta_i\) 可以规范固定为 1</h4>
        <p>这一点可以直接在 operators 上验证，不需要先引入额外的群论术语。
        对每个格点同时重新定义两种 flavor 的 phase：</p>
        <div class="scroll">\[
          \hat b_i'
          =e^{\,i\arg(\eta_i)/2}\hat b_i,\qquad
          \hat c_i'
          =e^{\,i\arg(\eta_i)/2}\hat c_i .
        \]</div>
        <p>利用 \(\theta\) 的 anti-linearity，有</p>
        <div class="scroll">\[
          \begin{aligned}
          \theta(\hat b_i')
          &=e^{-i\arg(\eta_i)/2}\eta_i\hat c_i
            =\hat c_i',\\
          \theta(\hat c_i')
          &=e^{-i\arg(\eta_i)/2}\eta_i\hat b_i
            =\hat b_i'.
          \end{aligned}
        \]</div>
        <p>所以 \(\eta_i\) 确实是 flavor basis 的 phase convention。
        改变这一 convention 时，Hamiltonian 中 hopping 或 pairing
        coefficients 的 matrix representation 也要一起变换；物理内容不变。
        文章的 paired example 取
        \(\eta_i=e^{-i\arg\Delta}\)，正是在选择 reflection phase 来抵消 pairing
        amplitude \(\Delta\) 的 phase。换到上面的 primed basis 后，
        reflection phase 为 1，而 pairing coefficient 相应变成 real
        nonnegative number。</p>

        <h4>note 中的 \(J_2\) 不是第二个连续 phase 自由度</h4>
        <p>现在才采用 note 的 real convention \(\eta_i=1\)。在
        \((\hat b,\hat c,\hat b^+,\hat c^+)^T\) 中，两个 matrices 是</p>
        <div class="scroll">\[
          g=-i\sigma_y\otimes I_2,\qquad
          J_1=I_2\otimes\sigma_x,\qquad
          J_2=I_2\otimes i\sigma_y .
        \]</div>
        <p>\(J_1K\) 先 complex conjugate，再交换 \(b,c\)，所以它就是
        physical reflection。要看清 \(J_2\) 多做了什么，只需把两个 matrices
        相乘：</p>
        <div class="scroll">\[
          -J_1J_2
          =I_2\otimes\sigma_z
          =\operatorname{diag}(1,-1,1,-1).
        \]</div>
        <p>右边在 \(b,b^+\) entries 上取 \(+1\)，在 \(c,c^+\) entries
        上取 \(-1\)。它没有交换两侧，只标记哪个 Nambu component 属于
        \(b\) side、哪个属于 \(c\) side。反过来写就是</p>
        <div class="scroll">\[
          J_2=-J_1\bigl(I_2\otimes\sigma_z\bigr).
        \]</div>
        <p>因此 \(J_2K\) 可以理解成 physical reflection \(J_1K\)
        再复合一个 \(c\)-side minus sign。这个 minus sign 是一个离散的
        relative flavor gauge transformation；它不是任意
        \(\eta_i=e^{i\varphi_i}\) 所包含的连续 \(U(1)\) phase。
        任意 \(\eta_i\) 已经由上面的 complex matrix \(J_1(\eta_i)\)
        单独表示，不能把 note 的 \(J_1,J_2\) 当作两个分量，再靠二者组合来生成
        \(\eta_i\)。</p>
        <p>从 reflection geometry 看，\(J_1\) 给出“交换两侧并 complex
        conjugate”，而 \(-J_1J_2\) 给出“哪一侧是 \(b\)，哪一侧是 \(c\)”。
        二者合起来确实把交换操作与左右分区同时编码进 matrices。
        但 <code>main.tex</code> 的 operator formulation 一开始已经写成
        \(\mathcal F_b\otimes\mathcal F_c\)，左右分区是已知的；因此 theorem
        只需要显式写 \(\theta\)，不需要再把 \(J_2\) 当作第二个 physical
        reflection assumption。</p>
        <p>note 把 \(J_2\) 加进来后，得到下面五条离散 relations：</p>
        <div class="scroll">\[
          J_1^2=I_4,\quad J_1^TgJ_1=g,\qquad
          J_2^2=-I_4,\quad J_2^TgJ_2=g,\qquad
          J_1J_2=-J_2J_1 .
        \]</div>
        <p>新增的 <code>experts/RPBAFQMC.tex</code> 给出了这两个 matrices
        的直接来源。它先逐字规定</p>
        <div class="source-quote">
          “Reflection symmetry requires
          \(J_1^TAJ_1=\bar A\). Assume that \(J_2\Omega\) plays the role
          of the metric of the contraction semigroup and the expansion semigroup.”
        </div>
        <p>所以在合作者原本的 construction 中，\(J_1\) 明确负责 physical
        reflection symmetry；作者试图让 \(J_2\) 与 bosonic symplectic
        matrix \(\Omega\) 相乘，构造 \(J_2\Omega\) metric。
        该文件随后用</p>
        <div class="scroll">\[
          J_2^TAJ_2=\bar A
          \quad\text{与}\quad
          J_2^TAJ_2=-\bar A
        \]</div>
        <p>分别挑出作者称为 maximal-subgroup generators 与 cone generators，
        然后声称 reflection-positive coefficient block 的正半定条件可改写成
        contraction part 与 expansion part 的 direct sum。</p>

        <h4>为什么 <code>RPBAFQMC.tex</code> 的 direct-sum 论证不成立</h4>
        <p>用户指出了这一旧论证中的关键错误：contraction 与 expansion blocks
        会混合。把 Hermitian matrix \(J_2\Omega\) 选到正、负本征子空间分开的
        basis 后，一般传播矩阵只能写成</p>
        <div class="scroll">\[
          M_\ell=
          \begin{pmatrix}
            M_{\ell,++}&M_{\ell,+-}\\
            M_{\ell,-+}&M_{\ell,--}
          \end{pmatrix}.
        \]</div>
        <p>若它真是 contraction block 与 expansion block 的 direct sum，
        就必须对每个时间片都有
        \(M_{\ell,+-}=M_{\ell,-+}=0\)，也就是正、负两个子空间分别保持不变。
        reflection positivity 的 coefficient condition 并没有给出这两个
        等式。相邻时间片相乘时，diagonal block 已经含有 cross terms：</p>
        <div class="scroll">\[
          \begin{aligned}
          (M_2M_1)_{++}
          &=M_{2,++}M_{1,++}\\
          &\quad+M_{2,+-}M_{1,-+},\\[2pt]
          (M_2M_1)_{--}
          &=M_{2,-+}M_{1,+-}\\
          &\quad+M_{2,--}M_{1,--}.
          \end{aligned}
        \]</div>
        <p>两个 off-diagonal blocks 也由四类 blocks 共同生成。因此不能把完整
        propagation 分成彼此独立的 contraction semigroup 与 expansion
        semigroup，再分别应用半群闭合性。关系
        \(J_2^TAJ_2=\pm\bar A\) 给出的是 generator 的 linear restrictions，
        并不自动说明 \(J_2\Omega\) 的正、负本征子空间对 \(e^A\) 不变。</p>
        <p>合作者的论文
        <a href="https://arxiv.org/abs/1712.09412">arXiv:1712.09412</a>
        中正确的 contraction-semigroup 语言也支持这一判断。该论文的
        sign-free application 是 fermionic Majorana AFQMC；下面使用的
        matrix definition 与 multiplication identity 本身不依赖 particle
        statistics。固定
        Hermitian metric \(J_2\Omega\) 后，contraction condition
        是对<strong>完整矩阵</strong>施加</p>
        <div class="scroll">\[
          M^\dagger(J_2\Omega)M\le J_2\Omega .
        \]</div>
        <p>其乘法闭合来自完整矩阵恒等式</p>
        <div class="scroll">\[
          \begin{aligned}
          &(M_1M_2)^\dagger(J_2\Omega)(M_1M_2)-J_2\Omega\\
          &\quad=M_2^\dagger
          \left[M_1^\dagger(J_2\Omega)M_1-J_2\Omega\right]M_2\\
          &\qquad+\left[M_2^\dagger(J_2\Omega)M_2-J_2\Omega\right].
          \end{aligned}
        \]</div>
        <p>这里从未要求把 \(M\) 拆成两个不混合的 blocks。
        论文所说 maximal subgroup，是上式取等号的完整 matrices；
        invariant cone 是一组 generators，在 maximal subgroup 的
        conjugation 下仍留在同一个 cone。这个 “invariant” 修饰的是
        generator cone，不是说 \(J_2\Omega\) 的正、负本征子空间分别被
        propagation 保持。论文提到的 polar decomposition 同样是
        “cone part 乘 group part”，不是 “contraction block 直和 expansion
        block”。</p>
        <p>所以 <code>RPBAFQMC.tex</code> 只能帮助我们确认作者当时赋予
        \(J_1,J_2\) 的<strong>预期分工</strong>，不能提供有效的 regularized-weight
        semigroup proof。独立于这一错误，恒等式
        \(-J_1J_2=I_2\otimes\sigma_z\) 仍准确说明 \(J_2\) 相对
        \(J_1\) 多出的 \(b/c\) 分区符号。</p>

        <div class="warning">
          <strong>两个同名的 \(\eta\) 必须分开。</strong>
          <code>main.tex</code> 的 \(\eta_i\) 是
          \(\theta(\hat b_i)=\eta_i\hat c_i\) 中的 scalar phase，
          \(|\eta_i|=1\)。note 后面有时把
          \(\eta=J_2g\) 称为 metric；那个 \(\eta\) 是一个
          \(2N\times2N\) Hermitian matrix。二者没有“一个由另一个生成”的关系。
        </div>

        <h4>Case 2 中 \(A\) 的完整 block structure</h4>
        <p>为了直接对齐 <code>main.tex</code> 的 RP block test，这里改用
        reflected-sector 顺序
        \(\chi=(\hat{\boldsymbol b},\hat{\boldsymbol b}^+,
        \hat{\boldsymbol c},\hat{\boldsymbol c}^+)^T\)。
        若每一侧有 \(M\) 个 modes，则这个顺序中的 bosonic matrix 是</p>
        <div class="scroll">\[
          g=
          \begin{pmatrix}g_0&0\\0&g_0\end{pmatrix},\qquad
          g_0=\begin{pmatrix}0&-I_M\\I_M&0\end{pmatrix}.
        \]</div>
        <p>文章把 Gaussian RP slice 写成</p>
        <div class="scroll">\[
          \hat h=\chi^T
          \underbrace{\begin{pmatrix}
          D&F\\F^T&\bar D
          \end{pmatrix}}_{\displaystyle Q}
          \chi+\xi,\qquad
          F=F^\dagger\succeq0,\quad \xi\in\mathbb R .
        \]</div>
        <p>note 的 convention 则是
        \(\hat h=\frac12\chi^TgA\chi+\xi\)。二者逐项比较得到</p>
        <div class="scroll">\[
          gA=2Q,\qquad
          A=-2gQ
          =-2\begin{pmatrix}
          g_0D&g_0F\\
          g_0F^T&g_0\bar D
          \end{pmatrix}.
        \]</div>
        <p>这是 Case 2 缺失的 \(A\)-structure。严格地说，
        \(gA\) 必须是 symmetric matrix。若原来写下的 \(D\) 含有
        antisymmetric part，那一部分只通过 canonical commutator
        贡献一个 scalar，可以移入 \(\xi\)；因此可先取
        \(D\to(D+D^T)/2\)，再使用上式。这样
        \(gA+A^Tg=0\) 可直接验证。</p>
        <p>在同一顺序中，note 的两个矩阵为</p>
        <div class="scroll">\[
          J_1=\begin{pmatrix}0&I_{2M}\\I_{2M}&0\end{pmatrix},\qquad
          J_2=\begin{pmatrix}0&I_{2M}\\-I_{2M}&0\end{pmatrix}.
        \]</div>
        <p>\(J_1K\) 交换两侧并复共轭，给出 physical reflection；
        \(J_2\) 记录两侧的相对 orientation。把它们代回便得到
        \(J_1^TgJ_1=g\)、\(J_1^2=I\)、
        \(J_2^TgJ_2=g\)、\(J_2^2=-I\) 与
        \(J_1J_2=-J_2J_1\)。但是这五条仍看不见
        \(F\succeq0\)；真正把 reflection symmetry 提升为
        reflection positivity 的正是 \(A\) 中这个 positive
        cross-reflection block。</p>

        <h4>为什么这些 matrices 仍不足以给出 reflection positivity</h4>
        <p>reflection symmetry 与 reflection positivity 是两件不同的事。
        前者只说 \(b\) sector 与 \(c\) sector 互为复共轭；后者还要求每个
        HS-decoupled slice 能整理成</p>
        <div class="scroll">\[
          \hat h=\hat q+\theta(\hat q)
          +\sum_{\mu,\nu}C_{\mu\nu}
          \hat X_\mu\theta(\hat X_\nu),
          \qquad C=C^\dagger\ge0 .
        \]</div>
        <p>正半定 matrix \(C\) 可以分解成平方和，因而每个传播因子最终是
        \(\sum_r\hat R_r\theta(\hat R_r)\) 的极限。这里已经出现一套
        正确的 semigroup proof：两个 reflected sums 相乘时，左右两侧
        operators 彼此对易，所以
        \(R\theta(R)S\theta(S)=RS\theta(RS)\)；任意有限和也因此对乘法
        封闭。左右 Fock spaces 的 trace 给出</p>
        <div class="scroll">\[
          \Tr[\hat R\,\theta(\hat R)]
          =\left|\Tr_{\hat b}\hat R\right|^2\ge0 .
        \]</div>
        <p>这就是文章 RP criterion 的物理内容。对 paired benchmark，
        \(\theta(\hat b_i)=e^{-i\arg\Delta}\hat c_i\)，相位可吸收到 flavor basis 中；
        跨两侧的 pairing coefficient 变成
        \(F=(\Delta\tau|\Delta|/2)I\ge0\)。因此 paired model 的非负权重来自
        operator-level reflection positivity，而不是仅由
        \(J_1^TgJ_1=g,\ J_1^2=I\) 两个矩阵等式推出。
        对 finite bare trace，证明直接来自这个 reflected-square
        multiplicative semigroup。
        <code>experts/RPBAFQMC.tex</code> 曾尝试把 regularized weight
        表成 contraction part 与 expansion part 的 direct sum，但上面的
        block-mixing calculation 否定了这一步。当前得到验证的 RP 结论仍是：
        finite bare trace 由 reflected squares 保证 nonnegative。
        因而“是否有 semigroup proof”的答案是有，只是它不是
        \(J_2g\) 定义的 matrix contraction semigroup。完整推导、固定度规
        contraction 的 no-go calculation，以及它与 TRS/Case 8 的统一关系，
        单列在
        <a href="part_6_case12_semigroups.html">《Case 1/2 的半群证明与统一边界》</a>；
        不能沿用旧文件的 direct-sum assertion。</p>
        """,
    ),
    Segment(
        "boson-contraction-list",
        "玻色 contraction semigroup 的条件与 Cases 3--16",
        67,
        117,
        r"""
        <p>原文先规定所有候选 Case 都满足
        \(J_1^TAJ_1=\bar A\) 和
        \(J_2gA+A^\dagger J_2g\le0\)，然后逐项改变
        \(J_1^TgJ_1=\pm g\)、\(J_1^2=\pm I\)、
        \(J_2^TgJ_2=\pm g\)、\(J_2^2=\pm I\)，以及
        \(J_1,J_2\) 对易或反对易。原文各项的文字判断依次是：
        Case 3 Failed；Case 4 Failed；Case 5 “non-Hermitian case I”；
        Case 6 “non-Hermitian case II”；Case 7 “Yinkai's case”；
        Case 8 “mainly non-Hermitian”；Case 9 与 Case 10 Failed；
        Cases 11--16 全部 Failed。</p>
        """,
        r"""
        <p>
        读到这一标题时，问题才正式切换为本次 \(2^5\) 穷举。
        五个二选一关系只给 \(J_1,J_2\) 分类；本段显示的两条关于 \(A\)
        的公式才决定一个具体时间片是否进入候选 semigroup。程序必须依次做三件事：
        先找满足五条关系的 \(J_1,J_2\)，再解合法 quadratic generator
        \(gA+A^Tg=0\) 与 \(J_1^TAJ_1=\bar A\)，最后检查 contraction
        inequality 是否允许严格小于零。仅完成第一步不等于找到了无符号情形。
        </p>

        <h4>这一列表里 \(J_1\) 与 \(J_2\) 各做什么</h4>
        <p>从这里开始，note 不再要求 \(J_1,J_2\) 都是上一段那种
        “保持 \(gA\) 的 symmetry”。它固定两条共同条件：</p>
        <div class="scroll">\[
          J_1^TAJ_1=\bar A,\qquad
          J_2gA+A^\dagger J_2g\le0 .
        \]</div>
        <p>第一条由 \(J_1\) 负责。因为 \(J_1\) 正交，
        \(J_1^TAJ_1=\bar A\) 等价于 \(AJ_1=J_1\bar A\)。
        若 \(Av=\lambda v\)，先复共轭再使用这个等式：</p>
        <div class="scroll">\[
          \bar A\bar v=\bar\lambda\bar v
          \quad\Longrightarrow\quad
          A(J_1\bar v)=J_1\bar A\bar v
          =\bar\lambda(J_1\bar v).
        \]</div>
        <p>所以 \(J_1\) 把 eigenvalue \(\lambda\) 的 eigenvector
        配到 eigenvalue \(\bar\lambda\) 的 eigenvector。它控制的是复共轭配对。</p>

        <p>第二条由 \(J_2\) 负责。在 note 这 14 个 bosonic candidates 中，
        \(J_2g\) 是 Hermitian matrix，可以作为 note 所说的 metric。
        不等式表示沿 \(A\) 生成的 propagation 不会把这个 metric 增大：</p>
        <div class="scroll">\[
          J_2gA+A^\dagger J_2g\le0
          \quad\Longrightarrow\quad
          (e^A)^\dagger J_2g\,e^A\le J_2g .
        \]</div>
        <p>这一步不是定义后直接跳出的结论。令 \(t\) 从 0 增加到 1，逐项求导：</p>
        <div class="scroll">\[
          \begin{aligned}
          \frac{d}{dt}
          \left(e^{tA^\dagger}J_2g\,e^{tA}\right)
          &=A^\dagger e^{tA^\dagger}J_2g\,e^{tA}
            +e^{tA^\dagger}J_2g\,e^{tA}A\\
          &=e^{tA^\dagger}
            \left(A^\dagger J_2g+J_2gA\right)e^{tA}\le0 .
          \end{aligned}
        \]</div>
        <p>从 \(t=0\) 积到 \(1\) 就得到上一式。这才是
        “contraction”的具体含义。这里 \(J_2\) 的首要作用是构造
        \(J_2g\)，不应与 \(J_1\) 的复共轭配对作用混在一起。</p>

        <h4>本段所说 maximal subgroup 与 invariant cone</h4>
        <p>
        先令 \(\eta=J_2g\)。在本段可能通过的玻色类中，
        \(\eta^\dagger=\eta\) 且 \(\eta^2=I\)。若
        \[
          \eta A+A^\dagger\eta=0,
        \]
        则 \(e^A\) 精确保持 \(\eta\) 不变，这些 \(A\) 生成 maximal subgroup。
        允许小于零的方向来自 invariant cone。对任意一个已经满足共同线性条件的
        \(A\)，定义
        </p>
        <div class="scroll">\[
          \begin{aligned}
          A_{\rm subgroup}
          &=\frac12\left(A-\eta A^\dagger\eta\right),\\
          A_{\rm cone}
          &=\frac12\left(A+\eta A^\dagger\eta\right),\\
          A&=A_{\rm subgroup}+A_{\rm cone}.
          \end{aligned}
        \]</div>
        <p>
        现在不凭名称判断，而是逐项代回。利用
        \(\eta^\dagger=\eta\) 与 \(\eta^2=I\)，第一项给出
        </p>
        <div class="scroll">\[
          \begin{aligned}
          \eta A_{\rm subgroup}
          +A_{\rm subgroup}^\dagger\eta
          &=
          \frac12(\eta A-A^\dagger\eta)
          +\frac12(A^\dagger\eta-\eta A)\\
          &=0 .
          \end{aligned}
        \]</div>
        <p>
        所以第一项确实是 maximal-subgroup generator。第二项则满足
        </p>
        <div class="scroll">\[
          \eta A_{\rm cone}=A_{\rm cone}^\dagger\eta,
          \qquad
          \eta A_{\rm cone}+A_{\rm cone}^\dagger\eta
          =2\eta A_{\rm cone}.
        \]</div>
        <p>
        因而第二项只有在再施加
        \(\eta A_{\rm cone}\le0\) 时才属于 invariant cone；严格小于零
        才使收缩矩阵负定。换言之，原先“第一项给零，第二项给
        半负定”的次序没有写反，原报告的问题是省略了这段使次序可核验的计算。
        </p>
        <p>
        它看起来容易与 note 后面
        \(J_2^TAJ_2=\pm\bar A\) 的正负分支混淆，是因为二者之间还隔着
        \(gA+A^Tg=0\)。在本段的玻色情形，
        \[
          \eta A^\dagger\eta=-J_2^T\bar A J_2 .
        \]
        因而 \(J_2^TAJ_2=+\bar A\) 对应
        \(\eta A^\dagger\eta=-A\)，恰好落入上面的减号
        \(A_{\rm subgroup}\)；而
        \(J_2^TAJ_2=-\bar A\) 对应
        \(\eta A^\dagger\eta=+A\)，落入加号
        \(A_{\rm cone}\)。额外的这个负号正是表面上“像是写反了”的来源。
        </p>
        <p>
        这里分解的是同一个完整矩阵的两种 generator
        components，不是把 particle/hole 或 reflection sectors 拆成互不混合的
        propagation blocks。note 第二、三节的长 block calculations 正是在尝试
        分别写出这两种结构；第 6 节会用完整 Pauli basis 把它们逐类补齐。
        </p>

        <h4>Case 7 的单模例子：每一步都可以手算</h4>
        <p>取单个玻色模，即 Nambu 维数为 2，并采用 note 在第二节给出的
        简化选择</p>
        <div class="scroll">\[
          g=-i\sigma_y
          =\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
          J_1=I_2,\qquad J_2=\sigma_x .
        \]</div>
        <p>这里 \(J_1^TgJ_1=g\)、\(J_1^2=I_2\)；
        \(J_2^TgJ_2=-g\)、\(J_2^2=I_2\)，且 \(J_1,J_2\) 对易。
        \(J_1^TAJ_1=\bar A\) 直接要求 \(A\) 是实矩阵。
        任何实的 \(2\times2\) bosonic generator 都可以写成</p>
        <div class="scroll">\[
          A=\begin{pmatrix}a&b\\c&-a\end{pmatrix},
        \]</div>
        <p>因为代入 \(gA+A^Tg=0\) 后，唯一独立条件就是
        两个 diagonal entries 互为相反数。此时</p>
        <div class="scroll">\[
          J_2g=\sigma_z,\qquad
          J_2gA+A^TJ_2g
          =\begin{pmatrix}
          2a&b-c\\
          b-c&2a
          \end{pmatrix}.
        \]</div>
        <p>例如取 \(a=-\gamma\)、\(b=c=0\)，其中 \(\gamma>0\)，也就是</p>
        <div class="scroll">\[
          A=-\gamma\sigma_z .
        \]</div>
        <p>那么 contraction matrix 恰好是</p>
        <div class="scroll">\[
          J_2gA+A^TJ_2g=-2\gamma I_2<0 .
        \]</div>
        <p>这个例子不是只停留在 matrix inequality。相应二次算符和 bosonic trace 为</p>
        <div class="scroll">\[
          h=-\gamma\left(a^+a+\frac12\right),\qquad
          \Tr e^h=\frac{e^{-\gamma/2}}{1-e^{-\gamma}}>0 .
        \]</div>
        <p>因此读到 Case 7 时，可以把 \(J_1=I_2\) 理解为“要求 \(A\) real”，
        把 \(J_2=\sigma_x\) 理解为“使 \(J_2g=\sigma_z\)，并用它区分
        contracting 与 expanding directions”。高维 Cases 只是把这套计算放进
        更大的 block matrices，并允许 \(J_1^2=-I\) 或不同的 commutation relation。</p>

        <h4>列表里的 Passed/Failed 还缺什么</h4>
        <p>本段的 Passed/Failed 是作者的手算标签；仅找到满足离散关系的
        \(J_1,J_2\)，或仅解出 \(J_1^TAJ_1=\bar A\) 的 linear subspace，
        都还不能证明存在使收缩矩阵负定的生成元。必须继续检查上述 Hermitian matrix
        是否能严格小于零，再检查多个 \(e^A\) 相乘后的完整 Fock trace，
        以及 determinant 平方根的连续取号。</p>
        """,
    ),
    Segment(
        "boson-passed-list",
        "玻色作者版 passed-only 清单",
        118,
        141,
        r"""
        <p>“List passed ones only”译为“只列出通过的情形”。\(1''\) 是
        time-reversal symmetry；\(2''\) 是 reflection positivity，并保留
        “non-contraction semigroup”的说明；\(3''\) 与 \(4''\) 分别是
        “non-Hermitian case I/II”；\(5''\) 是 “Yinkai's case”；
        \(6''\) 是 “mainly non-Hermitian”。它们分别对应前面的两类已有结构
        与 Cases 5--8；新版已经删除原先对应 Case 10 的 \(7''\)。</p>
        """,
        r"""
        <p>这次重新编号很容易造成误读：\(1''\) 和 \(2''\) 不是前面 contraction
        inequality 的通过项；\(3''\)--\(6''\) 才来自该列表。
        与上一版相比，作者已接受 commuting Case 10 为 Failed，所以总数从 7 降为 6。
        本 note 此处没有就地定义 “non-hermitian case”，但新增的
        <code>experts/SGNH.tex</code> 补出了它的物理含义：作者研究的是</p>
        <div class="scroll">\[
          H_K=-H_K^\dagger,\qquad H_U=H_U^\dagger ,
        \]</div>
        <p>也就是 single-body term 为 anti-Hermitian，而 interaction term
        仍为 Hermitian 的 bosonic models。该文件的两组 semigroup conditions
        正好对应这里的 Cases 3 与 4，并给出具体 Hamiltonians：
        第一组取 real antisymmetric hopping matrix；
        第二组使用 \(b,c\) flavors，允许 anti-Hermitian \(B_{11}\) 与
        symmetric \(B_{12}\)，同时取
        \(U(\hat n_b-\hat n_c)^2\)。所以这里的 “non-hermitian”
        主要指 physical single-body Hamiltonian，不是笼统地指任意一个
        displayed block 不等于自己的 Hermitian conjugate。</p>
        <p><code>experts/SGNH.tex</code> 声称这些 models sign-problem-free，
        但当前文件只给出 proof scheme，没有写完 metaplectic 表示中
        determinant 平方根怎样沿连续传播取号，也没有写完 regularization
        的全部步骤。因此这个来源澄清了标签，不能单独替代
        本报告对 complete bosonic weight 的检查。</p>
        """,
    ),
    Segment(
        "fermion-list",
        r"费米候选条件与 Cases \(1'\)--\(10'\)",
        142,
        182,
        r"""
        <p>
        原文标题写 “7 examined cases”，但随后实际编号为
        \(1'\)--\(10'\)。结合后面的 “List independent, passed ones only”
        恰好列出七项，这里的 “7” 应是在说七个独立的通过类，而不是只检查了
        七个候选。\(1'\) 是两个 anti-linear \(Z_2\) symmetries，作者紧接着说
        它只是 semigroup Case \(9'\) 的 special case。\(2'\) 被称为玻色
        reflection positivity 的费米对应物，作者只写“存在但没有用”。
        接着原文给出费米不等式，并列出 \(3'\)--\(10'\)：
        \(3'\) 和 \(4'\) 分别标作 Majorana reflection positivity 与
        time-reversal positivity；\(5'\)--\(9'\) 标为 Passed，
        \(10'\) 标为 Failed。
        </p>
        """,
        r"""
        <h4>先把费米的 contraction semigroup 写成标准形式</h4>
        <p>
        费米部分不能照抄前面的玻色推导。这里
        \[
          g^\dagger=g,\qquad g^2=I,\qquad
          gA+A^Tg=0.
        \]
        为了看清 note 的不等式，只在本小节暂记
        \[
          X=gA .
        \]
        上面的 Lie-algebra condition 立刻给出
        \(X^T=-X\)，所以 \(X\) 正是 quadratic form 的
        complex skew-symmetric coefficient matrix。
        </p>
        <p>
        第一条 anti-linear condition 在 \(X\) 上还会受到
        \(J_1\) 是否翻转 \(g\) 的影响。若把
        \(J_1^TgJ_1=\pm g\) 中实际出现的正负号原样保留，则
        </p>
        <div class="scroll">\[
          J_1^TXJ_1
          =(J_1^TgJ_1)(J_1^TAJ_1)
          =\begin{cases}
          \bar X,&J_1^TgJ_1=+g,\\
          -\bar X,&J_1^TgJ_1=-g.
          \end{cases}
        \]</div>
        <p>
        因此 \(3'\)、\(4'\)、\(7'\)、\(8'\) 在 \(X\) 上是标准的
        fixed-point condition；\(5'\)、\(6'\)、\(9'\)、\(10'\)
        则满足 \(J_1^TXJ_1=-\bar X\)。后四类不能不经说明就直接套用只假定
        \(J_1^TXJ_1=\bar X\) 的已知 Majorana theorem，这正是它们被当作
        新候选研究的原因之一。
        </p>
        <p>
        Cases \(3'\)--\(10'\) 都取
        \(J_2^2=-I\) 与 \(J_2^TgJ_2=-g\)。由于 \(J_2\) 实正交，
        第一式给出 \(J_2^T=-J_2\)；再与第二式合用可得
        </p>
        <div class="scroll">\[
          gJ_2=-J_2g .
        \]</div>
        <p>
        现在令
        \[
          \eta=iJ_2 .
        \]
        这里的 \(i\) 不是装饰。因为 \(J_2\) 是实反对称矩阵，
        </p>
        <div class="scroll">\[
          \eta^\dagger=(-i)J_2^T=iJ_2=\eta,
          \qquad
          \eta^2=(iJ_2)^2=I .
        \]</div>
        <p>
        所以 \(\eta\) 才是 Majorana coefficient space 上的 Hermitian
        indefinite metric。利用 \(X^\dagger=A^\dagger g\) 与
        \(gJ_2=-J_2g\)，note 的第二条逐步变成
        </p>
        <div class="scroll">\[
          \begin{aligned}
          iJ_2gA-iA^\dagger J_2g
          &=iJ_2X+iA^\dagger gJ_2\\
          &=iJ_2X+iX^\dagger J_2\\
          &=\eta X+X^\dagger\eta
          \le0 .
          \end{aligned}
        \]</div>
        <p>
        因此它并不是“把玻色式随意乘一个 \(i\)”；它是把标准
        contraction inequality 写在 skew-symmetric coefficient
        \(X=gA\) 上。对 \(t\ge0\) 求导，
        </p>
        <div class="scroll">\[
          \frac{d}{dt}
          \left(e^{tX^\dagger}\eta e^{tX}\right)
          =
          e^{tX^\dagger}
          \left(X^\dagger\eta+\eta X\right)e^{tX}\le0 ,
        \]</div>
        <p>
        从而
        \[
          (e^X)^\dagger\eta e^X\le\eta .
        \]
        两个这样的传播矩阵相乘仍满足同一不等式，因为
        </p>
        <div class="scroll">\[
          \begin{aligned}
          &(M_1M_2)^\dagger\eta(M_1M_2)-\eta\\
          &\quad =
          M_2^\dagger(M_1^\dagger\eta M_1-\eta)M_2\\
          &\qquad+
          (M_2^\dagger\eta M_2-\eta)\le0 .
          \end{aligned}
        \]</div>
        <p>
        这才是本段标题中 “semigroup” 的内容：每个时间片在同一个
        \(\eta\) 下 contraction，任意有序乘积仍是 contraction。
        </p>

        <h4>费米 maximal subgroup 与 invariant cone</h4>
        <p>
        与玻色部分一样，但现在分解的是 \(X=gA\)。定义
        </p>
        <div class="scroll">\[
          \begin{aligned}
          X_{\rm subgroup}
          &=\frac12\left(X-\eta X^\dagger\eta\right),\\
          X_{\rm cone}
          &=\frac12\left(X+\eta X^\dagger\eta\right).
          \end{aligned}
        \]</div>
        <p>
        直接代回得到
        </p>
        <div class="scroll">\[
          \eta X_{\rm subgroup}
          +X_{\rm subgroup}^\dagger\eta=0,
        \]</div>
        <p>
        所以 \(e^{X_{\rm subgroup}}\) 保持 \(\eta\)，构成 maximal
        subgroup。另一部分满足
        </p>
        <div class="scroll">\[
          \eta X_{\rm cone}=X_{\rm cone}^\dagger\eta,\qquad
          \eta X_{\rm cone}+X_{\rm cone}^\dagger\eta
          =2\eta X_{\rm cone}.
        \]</div>
        <p>
        再要求 \(\eta X_{\rm cone}\le0\)，才从这个线性子空间中选出
        invariant cone。“invariant” 可以用等式直接验证。若
        \(M^\dagger\eta M=\eta\)，并令
        \(X'_{\rm cone}=MX_{\rm cone}M^{-1}\)，则
        \[
        \eta X'_{\rm cone}+(X'_{\rm cone})^\dagger\eta
        =M^{-\dagger}
        (\eta X_{\rm cone}+X_{\rm cone}^\dagger\eta)M^{-1}.
        \]
        右边是对原 Hermitian matrix 的 congruence transformation；
        因此原式半负定时，新式仍半负定。
        </p>

        <div class="warning">
          <strong>Note 仍缺少一个 Nambu--Majorana 记号桥梁。</strong>
          上面的推导严格说明原不等式控制 \(e^X=e^{gA}\)。
          但 note 开头的 canonical propagation 与 trace formula 写的是
          \(e^A\)。在 real Majorana basis 中，skew-symmetric coefficient
          同时就是 canonical generator，所以已知半群定理可以直接使用；
          在当前 complex Nambu basis 中，这两种 matrix role 被 \(g\)
          分开了。要把已知定理完整搬回来，必须写出明确的
          Nambu--Majorana basis transformation，并把 \(A,J_1,J_2,\eta\)
          一起 transport；不能只把 \(X=gA\) 当作与 \(A\) 自动相似。
          因而这些标签准确指出了作者想调用的已知 positivity class，
          但当前 note 尚未就地完成对其 \(e^A\) formula 的证明。
        </div>

        <h4>\(1'\)：为什么 “just a special case of semigroup Case \(9'\)”</h4>
        <p>
        Case \(1'\) 有两个 anti-linear transformations。第一个
        \(J_1\mathcal K\) 满足 \(J_1^2=-I\)，第二个
        \(J_2\mathcal K\) 满足 \(J_2^2=+I\)；二者都翻转 \(g\)，并且对易。
        Case \(9'\) 的五条离散关系正好把这两个 \(J\) 的角色交换：
        semigroup 中负责第一条实性条件的 \(J_1\) 平方为 \(+I\)，
        负责 cone 的 \(J_2\) 平方为 \(-I\)。
        </p>
        <p>
        到这里为止，只能说<strong>五条离散关系</strong>在交换名字后相同。
        要进一步证明 \(1'\) 真是 \(9'\) 的 maximal-subgroup special case，
        还必须核对 \(A\) 的正负分支。先从 \(X=gA\) 上的等号看：
        若 Case \(9'\) 的 cone inequality 饱和，
        </p>
        <div class="scroll">\[
          i(J_2X-\bar XJ_2)=0,
        \]</div>
        <p>
        则 \(J_2X=\bar XJ_2\)。又因 \(J_2^T=-J_2\) 与
        \(J_2^2=-I\)，
        </p>
        <div class="scroll">\[
          J_2^TXJ_2
          =-J_2XJ_2
          =-\bar XJ_2^2
          =\bar X .
        \]</div>
        <p>
        但 Case \(9'\) 中 \(J_2^TgJ_2=-g\)，所以把最后一式换回 \(A\)
        并不是正号，而是
        </p>
        <div class="scroll">\[
          \begin{aligned}
          J_2^TXJ_2=\bar X
          &\Longleftrightarrow
          (J_2^TgJ_2)(J_2^TAJ_2)=g\bar A\\
          &\Longleftrightarrow
          J_2^TAJ_2=-\bar A .
          \end{aligned}
        \]</div>
        <p>
        因此，交换 Case \(1'\) 的两个 \(J\) 后，要成为 Case \(9'\)
        的等号边界，所需的两条 \(A\) 条件应当是：原 Case \(1'\) 的
        \(J_2\) 满足正号 \(J_2^TAJ_2=\bar A\)，而原 Case \(1'\) 的
        \(J_1\) 满足负号 \(J_1^TAJ_1=-\bar A\)。
        </p>
        <div class="warning">
          <strong>Note 本身没有保持这个符号一致。</strong>
          第三节实际手算 Case \(1'\) 时，先取
          \(J_1^TAJ_1=\bar A\)，随后也取
          \(J_2^TAJ_2=\bar A\)。这与上面由 Case \(9'\) 等号严格推出的
          一正一负不相同。因此 “It is just a special case” 目前只在
          五条 \(J,g\) 离散关系的层面成立；若要在 generator 层面成立，
          要么第三节有一处正负号需要改，要么作者还隐含使用了
          \(A\mapsto iA\) 等 convention change。报告不能替作者任选一种。
          这是回复合作者时应直接请他确认的问题。
        </div>
        <p>
        在符号修正并统一后，正确的物理图像才会是：双 symmetry class
        位于 semigroup 的 maximal subgroup；Case \(9'\) 另外允许严格
        cone directions，而这些 directions 一般破坏第二条 symmetry。
        </p>

        <h4>\(2'\)：为什么说费米对应物 “exists but not useful”</h4>
        <p>
        这一句本身没有给 \(J_1,J_2\)、没有给 \(A\) 的 block form，
        也没有给 positivity inequality，所以不能从 note 原文唯一恢复一个
        可穷举的 Case。能够确定的是，作者指向了 bosonic operator
        reflection positivity 的 fermionic analogue。
        </p>
        <p>
        对玻色算符，可以把左右两侧写成带非负系数的 reflected products，
        示意为
        \[
          \sum_\alpha \lambda_\alpha\,
          \hat X_\alpha\,\theta(\hat X_\alpha),
          \qquad \lambda_\alpha\ge0 .
        \]
        费米算符也能这样做，但若 \(\hat X_\alpha\) 含奇数个 fermion
        operators，把左右两侧重新排序会产生负号，所以必须连同固定的
        parity-dependent phase 与 ordering convention 一起定义。
        不能把玻色 reflected square 逐字复制过去。
        </p>
        <p>
        作者没有解释 “not useful”。结合紧接着的 \(3'\) 来看，最自然的
        解释是：这样的 graded fermionic reflection cone 确实存在，
        但它不会提供一个独立于 Majorana reflection positivity 的新分类；
        把 fermions 改写为 Majorana operators 后，真正适合 AFQMC
        multiplication 与 trace 的版本正是 \(3'\)。这是由上下文得到的解释，
        不是 note 已经给出的证明；若要在论文中保留 \(2'\)，仍需让作者明确
        它的 reflection map、fermion-ordering phase 和“无用”的严格含义。
        </p>

        <h4>\(3'\)：Majorana reflection positivity 具体在说什么</h4>
        <p>
        Case \(3'\) 的 \(J_1^2=+I\) 表示一个 reflection-type
        anti-linear involution，\(J_2^2=-I\) 则给出上面的 Hermitian
        metric \(\eta=iJ_2\)。由于 \(\{J_1,J_2\}=0\) 且
        \(\bar\eta=-iJ_2\)，
        \[
        J_1^T\bar\eta J_1
        =-iJ_1^TJ_2J_1=iJ_2=\eta.
        \]
        再用 \(J_1^TXJ_1=\bar X\)，得到
        \[
        J_1^T\overline{(\eta X+X^\dagger\eta)}J_1
        =\eta X+X^\dagger\eta.
        \]
        因此反线性条件与 \(\eta X+X^\dagger\eta\le0\) 可以同时成立。
        </p>
        <p>
        为看见其物理内容，在 real Majorana coefficient space 中可选标准形式
        \[
          J_1=\sigma_x\otimes I,\qquad
          J_2=i\sigma_y\otimes I .
        \]
        这里的 \(i\sigma_y\) 是实矩阵。把 Majorana operators 分成
        reflection 两侧 \(\gamma^{(1)},\gamma^{(2)}\)，允许的
        quadratic form 可以写成
        </p>
        <div class="scroll">\[
          \begin{aligned}
          \gamma^T X\gamma
          ={}&\gamma^{(1)T}B\gamma^{(1)}
          \gamma^{(2)T}\bar B\gamma^{(2)}\\
          &+2i\,\gamma^{(1)T}C\gamma^{(2)},
          \qquad C=C^\dagger,\quad C\ \text{semidefinite}.
          \end{aligned}
        \]</div>
        <p>
        前两项互为 reflection partners。最后一项是跨 reflection plane
        的 coupling；其 Hermitian matrix \(C\) 必须固定取同一半定方向，
        方向的正负取决于虚时间指数采用 \(e^{-\Delta\tau h}\) 还是相反约定。
        将 \(C\) spectral-decompose 为非负 eigenvalues 与 eigenvectors 后，
        cross term 就成为带非负系数的 reflected Majorana pairs 之和。
        因而指数展开中的每一项都落在同一个 graded reflection cone 中。
        </p>
        <p>
        当 \(C=0\) 时，两侧完全解耦且互为复共轭，Gaussian weight
        直接因子化成 \(W\bar W=|W|^2\)。允许 \(C\ne0\) 的 semidefinite
        directions 就是 invariant-cone extension。Majorana reflection
        positivity theorem 说明这个 operator cone 对 multiplication
        封闭，并且其 trace 非负。因此 \(3'\) 不是给 Case 随手加的旧名称；
        它说明该离散关系在正确 Majorana generator convention 中重现了一个
        已有完整 non-negative-trace theorem。参见
        <a href="https://arxiv.org/abs/1601.01994">Wei et al.,
        Majorana Positivity and the Fermion Sign Problem</a>，以及
        <a href="https://arxiv.org/html/1712.09412v3#S5">
        semigroup formulation 的 Majorana-RP block form</a>。
        </p>
        <div class="warning">
          <strong>但这个文献标签不能修复 note 的 Nambu 记号缺口。</strong>
          按 note 原样取
          \[
            g=\sigma_x,\qquad J_1=\sigma_x,\qquad
            J_2=i\sigma_y,\qquad A=iy\sigma_z\quad(y>0),
          \]
          五条 Case \(3'\) 关系、\(gA+A^Tg=0\) 与
          \(J_1^TAJ_1=\bar A\) 全部成立，而且
          \[
            iJ_2gA-iA^\dagger J_2g=-2yI<0 .
          \]
          可是对应的实际 Nambu quadratic operator 为
          \(h=iy(n-\tfrac12)\)，所以
          \[
            \Tr e^h=2\cos\frac y2 .
          \]
          它在 \(y=\pi\) 为零，在 \(y=2\pi\) 等于 \(-2\)。
          这是一条从 \(y=0\) 连续出发的精确反例：note 当前写出的
          literal Nambu conditions 并不保证 non-negative weight。
          它不否定 Majorana reflection positivity theorem；它证明的是
          必须先完成前述 basis transport，不能只沿用 Case 名称。
        </div>

        <h4>\(4'\)：time-reversal positivity 不只是 time-reversal invariance</h4>
        <p>
        Case \(4'\) 与 \(3'\) 的唯一离散差别是 \(J_1^2=-I\)。
        所以 \(J_1\mathcal K\) 不再是 reflection，而是 Kramers-type
        time reversal。对一对 fermion flavors，可写成
        </p>
        <div class="scroll">\[
          T(c_i)=d_i,\qquad
          T(d_i)=-c_i,\qquad
          T(i)=-i .
        \]</div>
        <p>
        \(T^2=-1\) 作用在含奇数个 fermion operators 的对象上，
        但 \(T^2=+1\) 作用在 quadratic Hamiltonian 等 even-parity
        operators 上。maximal-subgroup generators 是普通的
        time-reversal-invariant quadratic forms，例如
        </p>
        <div class="scroll">\[
          h_0=
          \begin{pmatrix}c^+&d^+\end{pmatrix}
          \begin{pmatrix}M&S\\-\bar S&\bar M\end{pmatrix}
          \begin{pmatrix}c\\d\end{pmatrix},
          \qquad T(h_0)=h_0 .
        \]</div>
        <p>
        但 “time-reversal positivity” 比 \(T(h_0)=h_0\) 更强。
        它在所有 time-reversal-even operators 中再选一个有方向的
        convex cone：cone generators 由 annihilation/creation
        operator 与其 Kramers partner 成对组成，例如
        \(\chi T(\chi)\)，而 creation pairs 要带由 fermion ordering
        固定的负号。再乘以 \(e^{h_0}\) 后，这类 operators 对加法和乘法
        仍封闭，并具有非负 trace。
        </p>
        <p>
        在 note 的矩阵语言中，\(J_1\) 定义 Kramers pairing，
        \(J_2\) 与不等式选择上述 cone 的正方向，二者反对易保证相容。
        所以 \(4'\) 的标签不是“只要有 time reversal 就够了”，而是
        “time-reversal-invariant maximal subgroup 加上一个
        time-reversal-paired positive cone”。这一 operator-level
        construction 见
        <a href="https://arxiv.org/html/2510.06226#S2">Wei,
        Time-reversal positivity, Sec. II</a>；它还明确区分了
        \(T^2=-1\) 的 odd sector 与 \(T^2=+1\) 的 even sector。
        </p>
        <p>
        与 \(3'\) 一样，这个已知 operator cone 使用的是正确 transport
        后的 Majorana/time-reversal generator。note 只写下五条
        \(J,g\) relations 和同一个 Nambu minus-sign inequality，
        还没有证明它们等价于该 operator cone。因此 \(4'\) 的标签解释了
        研究动机，不能代替缺失的 Nambu--Majorana derivation。
        </p>

        <h4>\(5'\)--\(10'\) 在这一框架中的位置</h4>
        <p>
        \(3'\) 与 \(4'\) 是两个已有名称的基准类；\(5'\)--\(10'\)
        则逐项改变 \(J_1\) 是否翻转 \(g\)、\(J_1^2\) 的符号以及
        \(J_1,J_2\) 对易或反对易，检查同一个 maximal-subgroup/cone
        construction 中是否仍有使收缩矩阵负定的方向。note 的
        Passed/Failed 在这里首先只表示“存在/不存在负定生成元”，
        不是完整 Fock 权重结论。后文逐个 block 的手算
        和完整穷举会说明哪些 linear spaces 非空；而上面指出的
        Nambu--Majorana propagation bridge 仍是把所有新类升级为完整
        fermionic weight theorem 时必须补上的共同步骤。
        </p>
        """,
    ),
    Segment(
        "fermion-passed-comment",
        "费米 passed-only 清单与第一节 Comment",
        183,
        211,
        r"""
        <p>新版明确写 “List independent, passed ones only”，并把独立费米候选
        编为 \(1'''\)--\(7'''\)：\(1'''\) 是 Majorana reflection positivity；
        \(2'''\) 是 time-reversal positivity；\(3'''\)--\(7'''\) 对应原先
        \(5'\)--\(9'\)。原先单列的两个 anti-linear symmetries 被并入 \(9'\)，
        因此后面所有 triple-prime 编号都前移一位。新版 Comment 只保留三组费米配对：
        \(1'''\) 与 \(5'''\)、\(2'''\) 与 \(6'''\)，以及 \(3'\) 与 \(7'''\)。</p>
        """,
        r"""
        <p>方括号 \([J_1,J_2]=0\) 表示对易，花括号
        \(\{J_1,J_2\}=0\) 表示反对易。前两组
        \(1'''\) 与 \(5'''\)、\(2'''\) 与 \(6'''\) 的其他四条关系相同，
        只改变这一条，因此确实是在检验：
        是否有
        \[
        J_1^T\overline{(\eta A+A^\dagger\eta)}J_1
        =+(\eta A+A^\dagger\eta)
        \]
        或者同一式子的右边带负号。
        但原文第三组逐字写成 \(3'\) 与 \(7'''\)；前者保持 \(g\)，后者翻转 \(g\)，
        所以它们不只差 commutation relation。若作者本意是
        \(3'''\) 与 \(7'''\)，则只需在 \(3'\) 后补两个 prime，才形成同样的受控配对。</p>
        <p>
        作者也把旧版的 “I don't think so” 改成更谨慎的
        “It has to be checked”。完整检查的答案是：<strong>对易或反对易确实会改变
        cone 中是否存在负定生成元</strong>，但必须先说清楚检查的是哪一个
        propagation matrix。
        </p>
        <p>
        若直接采用 note 顶部权重中的 \(e^A\)，并用 Hermitian metric
        \(J_2g\) 做标准 contraction，则数值与解析检查一致给出：
        \(1'''\) 和 \(2'''\) 的反对易版本中，半负定条件会被迫退化为等号；
        \(5'''\) 和 \(6'''\) 的对易版本才允许负定生成元。
        对 \(J_1\) 翻转 \(g\) 的受控配对则相反：
        \(3'''\) 的反对易版本允许负定生成元，而
        \(7'''\) 的对易版本中半负定条件只能取等号。
        </p>
        <p>
        若改用上一节的 Majorana coefficient \(X=gA\) 与 metric
        \(iJ_2\)，已知 Majorana reflection/time-reversal positivity
        theorem 使用的是反对易 \(J_1,J_2\)。这与上一段并不冲突：
        两段控制的是 \(e^X\) 与 \(e^A\) 两个不同的 matrix exponent。
        Note 当前把 Majorana inequality 与 Nambu \(e^A\) weight 写在一起，
        正是为何同一组 “对易还是反对易” 会看似得到相反答案。
        在补出 Nambu--Majorana transformation 之前，不能把两套
        Passed labels 合并成一个结论。
        </p>
        """,
    ),
    Segment(
        "boson-case7",
        "第二节开头与玻色 Case 7",
        212,
        221,
        r"""
        <p>第二节标题译为“新玻色情形的检验”。Case 7 取
        \(J_1^TgJ_1=g\)、\(J_1^2=I\)、
        \(J_2^TgJ_2=-g\)、\(J_2^2=I\)，并令 \(J_1,J_2\) 对易。
        作者先给出一个张量积实现，再指出可用更简单的 \(J_1=I_{2N}\)。
        最后一句说 metric 是 \(\eta=J_2g\)，并把 contraction 称为“physical”。</p>
        """,
        r"""
        <h4>先把张量积放回文章的 \(b,c\) 模型</h4>
        <p>文章有 \(N_s\) 个格点和两种 flavor，因此 note 这里的
        \(N=2N_s\)。采用与前面相同的 Nambu 顺序</p>
        <div class="scroll">\[
          \chi=(\hat{\boldsymbol b},\hat{\boldsymbol c},
          \hat{\boldsymbol b}^+,\hat{\boldsymbol c}^+)^T .
        \]</div>
        <p>Case 7 的第一种选择完整写开就是</p>
        <div class="scroll">\[
          J_1=
          \begin{pmatrix}
          0&I_{N_s}&0&0\\
          I_{N_s}&0&0&0\\
          0&0&0&I_{N_s}\\
          0&0&I_{N_s}&0
          \end{pmatrix},
          \qquad
          J_2=
          \begin{pmatrix}
          0&0&I_{N_s}&0\\
          0&0&0&I_{N_s}\\
          I_{N_s}&0&0&0\\
          0&I_{N_s}&0&0
          \end{pmatrix}.
        \]</div>
        <p>这里的 \(J_1,J_2\) 不是 7 月 19 日报告预先使用的记号。
        那份报告先从物理模型出发，直接发现了两件事：交换 \(b,c\)
        并复共轭会保持每个时间片，而 particle/hole signature matrix
        \(\operatorname{diag}(I,-I)\) 使稳定自由项满足
        \(\eta A_{\rm free}+A_{\rm free}^\dagger\eta<0\)。合作者在读到该证明后，
        才把前一操作写成 \(J_1K\)，并由
        \(\eta=J_2g\) 反推出 \(J_2\)。所以 Case 7 是对那份具体
        pole-free pairing 证明的矩阵化改写，而不是先有五条矩阵式、再碰巧找到
        文章模型。</p>
        <p>\(J_1K\) 先复共轭，再在 particle 和 hole 两部分中分别交换
        \(b,c\)。这正是文章 reflection
        \(\theta(\hat b_i)=\hat c_i,\ \theta(i)=-i\) 在 Nambu coefficients
        上的表示；若 \(\Delta\) 有相位，只需把相应 phase 放入这个 flavor exchange。
        \(J_2\) 则交换 Nambu 的 annihilation 与 creation 两半。它不是新的
        physical operation，而是用来构造 particle/hole signature matrix。</p>
        <p>对上面的 \(J_2\) 和玻色</p>
        <div class="scroll">\[
          g=\begin{pmatrix}0&-I_N\\I_N&0\end{pmatrix},
        \]</div>
        <p>直接做 block multiplication 得到</p>
        <div class="scroll">\[
          J_2g=\begin{pmatrix}I&0\\0&-I\end{pmatrix},
          \qquad (J_2g)^\dagger=J_2g,\qquad (J_2g)^2=I .
        \]</div>
        <p>也就是说，Case 7 的 \(\eta=J_2g\) 恰好是
        \(\operatorname{diag}(I_{2N_s},-I_{2N_s})\)：particle components
        取正号，hole components 取负号。它不是 ordinary positive-definite
        norm，也不是一个新的 observable；它记录 bosonic Bogoliubov dynamics
        中 particle/hole 两半的相反符号。</p>

        <h4>“Yinkai Yu's case” 在这里有一个精确定义</h4>
        <p>按你提供的写作背景，合作者是在阅读 7 月 19 日的
        pole-free pairing 报告后开始写这组 note；旧 note 第一节标题
        “Discovery based on Yinkai's observation” 又在文本内部印证了这个
        来源。因此，原始的 “Yinkai Yu's case” 首先指那份报告中的具体
        双组分配对构造。这个名称最早在矩阵分类中的精确定义出现在旧 note
        <code>experts/ToYinkaiYu.tex</code> 的第一节。原文先给出上面的
        \(J_1,J_2\)，紧接着用 “\(\Longleftrightarrow\)” 写出五条关系：</p>
        <div class="scroll">\[
          J_1^TgJ_1=g,\qquad J_1^2=I,\qquad
          J_2^TgJ_2=-g,\qquad J_2^2=I,\qquad
          [J_1,J_2]=0 .
        \]</div>
        <p>新版 note 把完全相同的五条关系编号为 Case 7，并再次写
        “Yinkai Yu's case”。因此，在需要一个精确数学标签时，本报告把
        <strong>“Yinkai's Case 7” 精确限定为这五条关系所定义的类别</strong>。
        这五条式子逐项都要满足；只共用一个 \(J_2\)，或只得到同一个
        \(J_2g\)，都还不能称为同一个 Case 7。</p>
        <p>判断一个实际辅助场模型时，还要再分两步。首先，对每个时间片的
        传播生成元 \(A\) 检查</p>
        <div class="scroll">\[
          J_1^TAJ_1=\bar A,\qquad
          (J_2g)A+A^\dagger(J_2g)\le0 .
        \]</div>
        <p>前一式使传播行列式具有复共轭成对结构；再配合实且为正的
        正规序标量因子、一个已知权重为正的参考构型和不中断的连续路径，
        才能固定完整权重的符号。后一式保证 \(e^A\) 位于以 \(J_2g\) 为 metric
        的 contraction semigroup。
        其次，若要排除玻色 pole 并把 bare trace 留在收敛分支，还要有
        一个使 \(\eta A+A^\dagger\eta<0\) 的稳定自由项。对本文模型，
        这个负定贡献由稳定的自由
        Hamiltonian 提供，而 \(U_2\) 辅助场满足等号。因而“五条
        \(J_1,J_2\) 关系”“单个 \(A\) 的两条条件”和“零场自由
        Hamiltonian 稳定、grand-canonical 玻色迹有限且为正”是三个
        依次更具体的检查层次，不能彼此替代。</p>

        <h4>为什么这正是 7 月 19 日 pole-free 报告中的结构</h4>
        <p>上面的写作背景和旧 note 的标题
        “Discovery based on Yinkai's observation” 共同确认了这个来源。
        7 月 19 日报告使用 \(g=-\Omega\)，并把同一个 signature matrix 写成
        \(\eta=J_2^{\rm old}\Omega\)，其中
        \(J_2^{\rm old}=-\sigma_x\otimes I_N\)。新版 note 改用
        \(J_2=\sigma_x\otimes I_N\) 并写 \(\eta=J_2g\)。两种写法完全相同：</p>
        <div class="scroll">\[
          J_2^{\rm old}\Omega
          =(-\sigma_x\otimes I_N)\Omega
          =(\sigma_x\otimes I_N)(-\Omega)
          =J_2g .
        \]</div>
        <p>因此 “Yinkai's case” 不是后来硬贴到旧报告上的名称；它就是旧报告
        \(\eta\)-contraction proof 所使用的离散 matrix structure。
        对文章的 \(U_1=0\) paired benchmark，每个时间片有两类传播因子：</p>
        <ol>
          <li>稳定的自由配对 Hamiltonian 使其收缩矩阵负定。若
          \(\epsilon_{\min}-\mu>|\Delta|\)，其 exponent generator \(A\) 满足
          \[
            (J_2g)A+A^\dagger(J_2g)<0,
          \]
          所以 \((e^A)^\dagger(J_2g)e^A-J_2g<0\)，传播矩阵位于
          收缩半群内部。</li>
          <li>\(U_2(\hat n_b-\hat n_c)^2\) 的 real HS field 产生
          \(\exp[i\sum_i\theta_i(\hat n_{b,i}-\hat n_{c,i})]\)。
          它只改变 phase，对相应 \(A\) 满足同一个式子的等号，因此是
          \(J_2g\)-isometry，位于 contraction domain 的边界。</li>
        </ol>
        <p>两类因子都满足 \(J_1^TAJ_1=\bar A\)：交换 \(b,c\) 的同时复共轭，
        会把 \(+i\theta_i\) 与 \(-i\theta_i\) 互换回来；real hopping 和
        reflected pairing 也保持不变。由于 contraction condition 对有序矩阵乘法封闭，
        任意 auxiliary-field history 的完整 Nambu propagation 都严格满足</p>
        <div class="scroll">\[
          \mathcal M^\dagger(J_2g)\mathcal M-(J_2g)<0 .
        \]</div>
        <p>若 \(\mathcal Mv=\lambda v\) 且 \(|\lambda|=1\)，把 \(v\) 代入上式，
        左边会等于零，与严格小于零矛盾。因此完整 propagation 没有单位圆
        eigenvalue，特别没有 \(\lambda=1\)，于是
        \(\det(I-\mathcal M)\ne0\)。这就是旧报告的逐构型 pole-free result。</p>

        <h4>先把 “trace class” 换成可直接检查的物理条件</h4>
        <p>
        玻色 Fock space 允许每个 mode 有 \(0,1,2,\ldots\) 个粒子，
        所以“有限维 matrix 没有 pole”与“把所有 occupation states
        的贡献相加后得到有限结果”不是同一件事。数学上把后一要求称为
        <em>trace class</em>：算符 \(\hat U\) 的所有 singular values
        之和有限，
        \[
          \Tr\sqrt{\hat U^\dagger\hat U}<\infty .
        \]
        这个条件保证 \(\Tr\hat U\) 绝对收敛；改变 Fock basis
        不会改变其值。
        </p>
        <p>
        对本文的稳定 quadratic free Hamiltonian，可以先用逐模
        occupation-number 求和直接验证这件事。稳定条件
        \(\epsilon_{\min}-\mu>|\Delta|\) 允许作 bosonic Bogoliubov
        transformation，把自由项写成
        </p>
        <div class="scroll">\[
          \hat H_0=E_0+\sum_{m=1}^{2N_s}
          \varepsilon_m\,\hat\beta_m^+\hat\beta_m,
          \qquad \varepsilon_m>0 .
        \]</div>
        <p>
        因而一个虚时间步的 bare trace 可以逐个 quasiparticle mode
        求和：
        </p>
        <div class="scroll">\[
          \begin{aligned}
          \Tr e^{-\Delta\tau\hat H_0}
          &=e^{-\Delta\tau E_0}
            \prod_m\sum_{n_m=0}^{\infty}
            e^{-\Delta\tau\varepsilon_m n_m}\\
          &=e^{-\Delta\tau E_0}
            \prod_m\frac1{1-e^{-\Delta\tau\varepsilon_m}}<\infty .
          \end{aligned}
        \]</div>
        <p>
        每个 geometric series 收敛的原因很具体：
        \(\varepsilon_m>0\) 使第 \(n_m\) 个 occupation state
        比前一个多一个因子 \(e^{-\Delta\tau\varepsilon_m}<1\)。
        这就是“高 occupation states 被压低”的完整含义。
        </p>
        <p>
        \(U_2\) 的 HS factor 为
        \[
          \hat V(\phi)=
          \exp\!\left[
          i\sum_i\phi_i(\hat n_{b,i}-\hat n_{c,i})
          \right].
        \]
        指数中的算符是 Hermitian，所以
        \(\hat V(\phi)^\dagger\hat V(\phi)=I\)：它只给 occupation
        states 加 phase，operator norm 等于 1，不会放大任何态。
        一个 trace-class 算符左右乘这种 bounded operator 后仍为
        trace class。这里使用的不是口头判断，而是 trace norm 的
        双边理想不等式
        \[
          \|\hat B\hat T\hat C\|_1
          \le \|\hat B\|\,\|\hat T\|_1\,\|\hat C\|,
        \]
        其中 \(\hat T\) 是 trace class，\(\hat B,\hat C\) 是 bounded
        operators。对 HS phase factors，
        \(\|\hat B\|=\|\hat C\|=1\)。于是 Trotter product 中只要保留稳定的
        \(e^{-\Delta\tau\hat H_0}\) factors，任意有限 HS history 的
        many-body product 都有绝对收敛的 Fock trace。
        </p>

        <h4>contraction、收敛与正号在这里各完成哪一步</h4>
        <p>现在可以把 Case 7 的完整逻辑分成四步，不再用一句术语包办：</p>
        <ol>
          <li><strong>bare trace 存在。</strong>
          上面的 quasiparticle geometric series 与 unitary HS factor
          证明每个 fixed-field many-body product 都是 trace class。</li>
          <li><strong>路径中没有 pole。</strong>
          稳定自由因子严格满足
          \((e^A)^\dagger(J_2g)e^A-J_2g<0\)，HS phase 因子取等号；
          完整有序乘积仍严格小于零，因此不可能有单位圆 eigenvalue，
          特别不可能有 \(\lambda=1\)。</li>
          <li><strong>weight 是 real number。</strong>
          \(J_1K\) 交换 \(b,c\) 并复共轭，逐时间片保持 generator family；
          正实的 Gaussian HS factor 与正规序 scalar 不另添 complex phase。</li>
          <li><strong>real weight 的符号不变。</strong>
          连续 HS configuration space 含零场点。零场 thermal trace 为正；
          weight 又处处有限、非零且连续，所以不能在不先经过零或 pole 的情况下
          从正值变成负值。</li>
        </ol>
        <p>
        这四步给 \(U_1=0\) paired benchmark 一条独立于 RP 的
        sign-free argument。<code>main.tex</code> 的 RP theorem
        则采用另一条路线：它把每个时间片写成 reflected products，
        直接证明 trace 在存在时非负。RP 需要 positive reflected
        coupling；上面的 semigroup 路线需要稳定自由项、同一个
        contraction metric、连通的 auxiliary-field domain 与全程无 pole。
        两套证明的假设不同，不能用其中一套的名称替代另一套的推导。
        </p>

        <p>原文还给出 \(J_1=I_{2N}\) 的简单 representative。
        它只要求 \(A=\bar A\)，适合检查这一组五条矩阵关系；
        但它不再表示文章中实际的 \(b\leftrightarrow c\) reflection。
        因而解释 benchmark 时应使用第一种 \(J_1\)，不能为了矩阵简单而丢掉
        flavor 的物理含义。</p>
        """,
    ),
    Segment(
        "boson-case8-j1",
        r"玻色 Case 8：矩阵选择与 \(J_1^TAJ_1=\bar A\)",
        222,
        292,
        r"""
        <p>Case 8 与 Case 7 的差别是 \(J_1^2=-I\)。
        原文给出 \(J_1,J_2\) 的 Pauli 张量积和 \(4\times4\) block form，
        写出一般玻色生成元 \(A\)，再完整计算 \(J_1^TAJ_1\)。
        “So” 后列出的六条 block relations 是把所得矩阵与 \(\bar A\) 逐块比较的结果。</p>
        """,
        r"""
        <p>一般玻色生成元先由 \(gA+A^Tg=0\) 固定成</p>
        <div class="scroll">\[
          A=\begin{pmatrix}B&C\\D&-B^T\end{pmatrix},
          \qquad C=C^T,\quad D=D^T .
        \]</div>
        <p>原文再把每个 \(N\times N\) block 分成 \(N/2\) 大小的子块。
        例如乘积矩阵的 \((1,1)\) block 是 \(-B_{11}^T\)，而
        \(\bar A\) 的 \((1,1)\) block 是 \(\bar B_{11}\)，故
        \(-B_{11}^T=\bar B_{11}\)，也就是
        \(B_{11}=-B_{11}^\dagger\)。按同样的逐块等式读取其余位置，
        得到原文列出的 \(B_{22},B_{12},C_{11},C_{22},C_{12}\) 关系。
        因此最后显示的 \(A\) 不是新的假设，而是已经解完第一条 anti-linear condition
        后的一般形式。</p>
        <p>先用最小 \(N=2\) 看清这一组 \(J_1,J_2\)。此时
        \(I_{N/2}=1\)，原文的 tensor products 就是普通 \(4\times4\) matrices：</p>
        <div class="scroll">\[
          g=-i\sigma_y\otimes I_2,\qquad
          J_1=(-i\sigma_y)\otimes\sigma_z,\qquad
          J_2=\sigma_x\otimes\sigma_x .
        \]</div>
        <p>\((-i\sigma_y)^2=-I_2\)，故 \(J_1^2=-I_4\)；
        \(J_2^2=I_4\)。\(J_1\) 在两个 tensor factors 上分别与
        \(J_2\) 反对易，两次负号相消，所以 \(J_1J_2=J_2J_1\)。
        同样直接相乘可得 \(J_1^TgJ_1=g\)、
        \(J_2^TgJ_2=-g\)。这说明原文 Case 8 的显式 matrices
        的确实现了标题的五条离散关系。</p>
        """,
        True,
    ),
    Segment(
        "boson-case8-j2",
        r"玻色 Case 8：\(J_2\) 分解、maximal subgroup 与 invariant cone",
        293,
        375,
        r"""
        <p>原文接着计算 \(J_2^TAJ_2=\pm\bar A\)。
        加号对应作者所称的 maximal subgroup generators，减号对应 invariant cone
        generators。作者分别写出两类 block relations 与 \(A\)，最后计算
        \(J_2\Omega A\le0\)，把它等价改写成一个 block matrix 半正定，并以 “Good” 结束。</p>
        """,
        r"""
        <p>因为玻色原文取 \(g=-\Omega\)，所以
        \(J_2\Omega A=-J_2gA\)。对满足
        \(J_2^TAJ_2=-\bar A\) 的生成元，\(J_2gA\) 是 Hermitian，
        故原文的最后一步确实是在施加一个可比较本征值的
        matrix inequality。maximal subgroup 对应等号边界
        \(J_2gA+A^\dagger J_2g=0\)；cone generators 对应离开边界的 Hermitian
        directions。两部分相加才形成完整 semigroup generator。
        这里 \(J_1^2=-I\) 没有妨碍这个不等式。因此 Case 8 的允许
        生成元中确定存在使收缩矩阵负定的方向。</p>
        <p>还可以不用一般 blocks，直接给出 cone 内一点。对刚才的 \(N=2\)
        matrices，</p>
        <div class="scroll">\[
          J_2g=\sigma_z\otimes\sigma_x .
        \]</div>
        <p>取任意 \(\gamma>0\)，令</p>
        <div class="scroll">\[
          A=-\gamma\,\sigma_z\otimes\sigma_x .
        \]</div>
        <p>逐项代入可得</p>
        <div class="scroll">\[
          gA+A^Tg=0,\qquad
          J_1^TAJ_1=\bar A,\qquad
          J_2gA+A^\dagger J_2g=-2\gamma I_4<0 .
        \]</div>
        <p>所以 Case 8 不只是 “cone equations 有非零解”，而是确实有
        使收缩矩阵负定的例子。原文后面的大 block inequality 是这一简单
        representative 向一般 \(N\) 与一般 blocks 的展开。</p>

        <h4>这一步证明了 matrix cone 非空，但还没有证明原 displayed
        metric 的 bare Fock trace 收敛</h4>
        <p>这里必须把同一个 \(A\) 放回第一节定义的物理 quadratic
        operator，而不能只读 matrix inequality。因为
        \(J_2g=\sigma_z\otimes\sigma_x\)，直接相乘得到</p>
        <div class="scroll">\[
          \frac12\hat\chi^TgA\hat\chi
          =-\gamma\,\hat{\boldsymbol a}^{+T}
          \sigma_x\hat{\boldsymbol a},
          \qquad
          \hat{\boldsymbol a}=(\hat a_1,\hat a_2)^T .
        \]</div>
        <p>令
        \(\hat a_\pm=(\hat a_1\pm\hat a_2)/\sqrt2\)，便有</p>
        <div class="scroll">\[
          \frac12\hat\chi^TgA\hat\chi
          =-\gamma\hat n_+ +\gamma\hat n_- .
        \]</div>
        <p>于是 grand-canonical bare trace 中出现</p>
        <div class="scroll">\[
          \left(\sum_{n_+=0}^{\infty}e^{-\gamma n_+}\right)
          \left(\sum_{n_-=0}^{\infty}e^{+\gamma n_-}\right),
        \]</div>
        <p>第二个几何级数发散。这个反例同时满足 Case 8 的五条关系、
        \(J_1^TAJ_1=\bar A\) 与严格 contraction inequality，所以原文
        “Good” 的准确含义只能是<strong>生成元分类通过</strong>。
        它不能单独承担 trace-class 结论。</p>

        <h4>同一个离散 Case 怎样得到可采样的另一组物理矩阵实现</h4>
        <p>Case 8 的五条关系并没有强迫使用上面的 \(J_2\)。当 flavor
        数为偶数时，可以改取</p>
        <div class="scroll">\[
          J_1=I_2\otimes(-i\sigma_y)\otimes I,\qquad
          J_2=\sigma_x\otimes I .
        \]</div>
        <p>这仍满足
        \(J_1^TgJ_1=g\)、\(J_1^2=-I\)、
        \(J_2^TgJ_2=-g\)、\(J_2^2=I\) 与
        \([J_1,J_2]=0\)，但现在</p>
        <div class="scroll">\[
          J_2g=\operatorname{diag}(I,-I).
        \]</div>
        <p>报告在物理 Hamiltonian catalog 中采用的是这一组矩阵。
        稳定自由项提供物理粒子数衰减，
        HS factors 满足等号；完整传播位于物理
        complex-symplectic semigroup 的内部。Potapov--Olshanski
        decomposition 后的正定 damping quadratic form 可由 unitary
        Bogoliubov transformation 对角化为
        \(-\sum_j\epsilon_j(\beta_j^+\beta_j+1/2)\)、
        \(\epsilon_j>0\)，所以 Fock trace norm 是
        \(\prod_j e^{-\epsilon_j/2}/(1-e^{-\epsilon_j})<\infty\)。
        这才把同一个离散 Case 8 完成到 bare-trace-convergent、
        sign-free、pole-free 的物理模型。</p>
        """,
        True,
    ),
    Segment(
        "boson-case3-j1",
        "玻色 Case 3：矩阵选择与第一条约束",
        376,
        437,
        r"""
        <p>Case 3 取 \(J_1^2=I\)，\(J_2^2=I\)，二者反对易。
        作者随后写 “Also a Yin-Kai's case”，再计算
        \(J_1^TAJ_1=\bar A\)，并列出 \(B\)、\(C\)、\(D\) 子块之间的关系。</p>
        """,
        r"""
        <h4>这里的 “Also” 不能按精确定义的 Case 7 来读</h4>
        <p>Case 3 与 Case 7 确实使用同一个</p>
        <div class="scroll">\[
          J_2=\sigma_x\otimes I_N,\qquad
          J_2g=\begin{pmatrix}I_N&0\\0&-I_N\end{pmatrix}.
        \]</div>
        <p>所以二者共用同一个 particle/hole metric。但是它们对
        \(J_1,J_2\) 的要求不同：</p>
        <div class="scroll">\[
          \begin{array}{c|c}
          \text{Case 7}&[J_1,J_2]=0\\
          \text{Case 3}&\{J_1,J_2\}=0
          \end{array}
        \]</div>
        <p>在 note 固定的实 Pauli-product convention 中，同时作保持
        \(g\) 的实换基不会把对易变成反对易。因此 Case 3 不是 Case 7
        在这套枚举中的另一种矩阵写法。若允许给反线性变换乘任意复相位，
        则正确的平方应写成 \(J\bar J\)，五条式子和 metric 也必须一起
        改写；note 没有给出这样的 equivalence。结合本段后面的
        “Not a contraction
        semigroup”，这里最稳妥的读法是：作者把一个从 7 月 19 日原型
        继续尝试出来、并共用同一 \(J_2g\) metric 的候选 representative
        作了来源标记；这句话本身没有宣称它满足 Case 7 的无符号条件。</p>

        <p>这段乘法的作用仍是解线性约束。以 \((1,1)\) block 为例，
        \(-B_{22}^T=\bar B_{11}\) 给出
        \(B_{11}=-B_{22}^\dagger\)；\((1,2)\) block
        \(B_{12}^T=\bar B_{12}\) 给出 \(B_{12}=B_{12}^\dagger\)。
        原文写出的其余四条关系也分别来自相应 block。到这里仅确定了允许的线性子空间，
        尚未施加半负定性。</p>
        <p>为什么它最终与 Case 7 不同，可以先试最自然的负定方向。
        在最小 \(N=2\) realization 中，原文使用</p>
        <div class="scroll">\[
          J_1=(-i\sigma_y)\otimes(-i\sigma_y),\qquad
          J_2=\sigma_x\otimes I_2,\qquad
          J_2g=\sigma_z\otimes I_2 .
        \]</div>
        <p>若暂时不管 \(J_1\)，取
        \(A=-\gamma\,\sigma_z\otimes I_2\) 会使 contraction matrix
        等于 \(-2\gamma I_4\)。但是这一 \(A\) 是实矩阵，而直接相乘给出</p>
        <div class="scroll">\[
          J_1^TAJ_1=-A\ne A=\bar A .
        \]</div>
        <p>也就是说，\(J_2\) 单独允许的最直接 contracting direction 被
        \(J_1\) 条件排除了。这已经预示后面为什么只剩等号边界。</p>
        """,
        True,
    ),
    Segment(
        "boson-case3-j2",
        "玻色 Case 3：subgroup、cone 与 “Not a contraction semigroup”",
        438,
        495,
        r"""
        <p>作者把 \(J_2^TAJ_2=+\bar A\) 解成 maximal subgroup，
        把负号分支解成 convex cone，最后写
        \(J_2gA=(\sigma_z\otimes I_N)A\le0\)，并判断
        “Not a contraction semigroup”。</p>
        """,
        r"""
        <p>关键不是满足 \(J_2^TAJ_2=-\bar A\) 的线性空间是否非零，
        而是其中能否找到
        \(J_2gA+A^\dagger J_2g<0\) 的生成元。下面直接计算这个问题。</p>
        <p>把上一段的观察推广到任意允许 \(A\)。这里不能随意交换
        matrices 的次序。由 \(J_1^TgJ_1=g\) 和
        \(J_1J_1^T=I\)，先得到 \(gJ_1=J_1g\)；由
        \(\{J_1,J_2\}=0\)，再得到
        \(J_1^TJ_2J_1=-J_2\)。因此</p>
        <div class="scroll">\[
          \begin{aligned}
          J_1^T(J_2g)J_1
          &=J_1^TJ_2gJ_1\\
          &=J_1^TJ_2J_1g
            &&\bigl(gJ_1=J_1g\bigr)\\
          &=-J_2g
            &&\bigl(J_1^TJ_2J_1=-J_2\bigr).
          \end{aligned}
        \]</div>
        <p>复共轭 \(J_1^TAJ_1=\bar A\) 还分别给出
        \(J_1^T\bar A J_1=A\) 和
        \(J_1^TA^TJ_1=A^\dagger\)。把这三条已经证明的等式代入完整
        contraction matrix，才得到</p>
        <div class="scroll">\[
          \begin{aligned}
          &J_1^T\overline{\left(J_2gA+A^\dagger J_2g\right)}J_1\\
          &=(J_1^TJ_2gJ_1)(J_1^T\bar A J_1)
          +(J_1^TA^TJ_1)(J_1^TJ_2gJ_1)\\
          &=(-J_2g)A+A^\dagger(-J_2g)\\
          &=-\left(J_2gA+A^\dagger J_2g\right).
          \end{aligned}
        \]</div>
        <p>若
        \(J_2gA+A^\dagger J_2g\le0\)，复共轭和正交基变换保持
        半负定，所以上式左边也 \(\le0\)。利用上式右边得到
        \[
        -(J_2gA+A^\dagger J_2g)\le0
        \quad\Longleftrightarrow\quad
        J_2gA+A^\dagger J_2g\ge0.
        \]
        与原来的半负定条件合并，只能有
        \(J_2gA+A^\dagger J_2g=0\)。这才是 Case 3 对所有 blocks
        的失败证明。</p>
        """,
        True,
    ),
    Segment(
        "boson-case4-j1",
        "玻色 Case 4：二维 block form",
        496,
        535,
        r"""
        <p>Case 4 仍令 \(J_1,J_2\) 反对易，但改成 \(J_1^2=-I\)。
        原文也在所选矩阵后写 “Also a Yin-Kai's case”。
        原文使用 \(2\times2\) block form，计算后得到
        \(B=-B^\dagger\) 与 \(C=-\bar D\)。</p>
        """,
        r"""
        <h4>Case 4 与精确定义的 Case 7 相差两条关系</h4>
        <p>这里仍有
        \(J_2=\sigma_x\otimes I_N\)，所以 \(J_2g\) 与 Case 7 相同；
        但</p>
        <div class="scroll">\[
          \begin{array}{c|cc}
          &J_1^2&J_1,J_2\text{ 的关系}\\ \hline
          \text{Case 7}&+I&[J_1,J_2]=0\\
          \text{Case 4}&-I&\{J_1,J_2\}=0
          \end{array}
        \]</div>
        <p>在 note 的实矩阵 convention 中，平方的正负和对易类型在
        保持 \(g\) 的实换基后都不改变，
        所以 Case 4 也不与 Case 7 等价。这里的 “Also” 至多说明作者
        把它视为从同一个 pole-free pairing 原型继续生成的候选；
        不能据此跳过下面的
        contraction 检查。该检查最终只得到等号边界。</p>

        <p>从原文乘积
        \(\begin{pmatrix}-B^T&-D\\-C&B\end{pmatrix}=\bar A\)
        逐块比较：
        \(-B^T=\bar B\) 等价于 \(B=-B^\dagger\)；
        \(-D=\bar C\) 等价于 \(D=-\bar C\)。
        右下与左下 block 不再提供独立条件。由此得到原文最后一行的 \(A\)。</p>
        <p>最小 \(N=1\) 时可直接取
        \(J_1=-i\sigma_y\)、\(J_2=\sigma_x\)，仍有
        \(J_2g=\sigma_z\)。看似最好的 choice
        \(A=-\gamma\sigma_z\) 产生 \(-2\gamma I_2\)，
        但 \(J_1^TAJ_1=-A\ne\bar A\)。因此把 \(J_1^2\) 从
        \(+I\) 改成 \(-I\) 后，这个反对易类别仍然没有负定生成元。</p>
        """,
        True,
    ),
    Segment(
        "boson-case4-j2",
        "玻色 Case 4：maximal subgroup、cone 与失败判断",
        536,
        564,
        r"""
        <p>原文计算 \(J_2^TAJ_2=\pm\bar A\)，得到 maximal subgroup 中 \(C=0\)，
        convex cone 中 \(B=0\)。随后写出 \(J_2g=\operatorname{diag}(I,-I)\)，
        并判断不存在 contraction semigroup。</p>
        """,
        r"""
        <p>在满足 \(J_2^TAJ_2=-\bar A\) 的部分，
        \[
        A=\begin{pmatrix}0&-\bar C\\C&0\end{pmatrix},\qquad
        J_2gA=\begin{pmatrix}0&-\bar C\\-C&0\end{pmatrix}.
        \]
        本 Case 还有 \(J_1^TgJ_1=g\)、\(\{J_1,J_2\}=0\) 和
        \(J_1^TAJ_1=\bar A\)，所以逐项相乘得到
        \[
        J_1^T\overline{(J_2gA+A^\dagger J_2g)}J_1
        =-(J_2gA+A^\dagger J_2g).
        \]
        假定括号内的矩阵半负定，则左边半负定，因而括号内的负号也半负定；
        这等价于括号内的矩阵半正定。它同时半负定和半正定，只能为零，
        所以 Case 4 不存在负定生成元。</p>
        """,
        True,
    ),
    Segment(
        "boson-case9-j1",
        "玻色 Case 9：两个矩阵实现与第一条约束",
        565,
        629,
        r"""
        <p>Case 9 令 \(J_1^TgJ_1=-g\)、\(J_1^2=I\)，并让 \(J_1,J_2\) 对易。
        作者先指出最简单的 \(J_1=J_2\) 有 sign problem，再给出另一个
        \(4\times4\) block realization，把后者称为 “Also a Yin-Kai's
        case”，并解出 \(J_1^TAJ_1=\bar A\)。</p>
        """,
        r"""
        <h4>Case 9 只与 Case 7 共用 \(J_2\)，第一条关系已经不同</h4>
        <p>第二种 realization 仍取
        \(J_2=\sigma_x\otimes I_N\)，所以它也得到
        \(J_2g=\operatorname{diag}(I_N,-I_N)\)。然而</p>
        <div class="scroll">\[
          \begin{array}{c|c}
          \text{Case 7}&J_1^TgJ_1=+g\\
          \text{Case 9}&J_1^TgJ_1=-g
          \end{array}
        \]</div>
        <p>这个正负号说明 \(J_1\) 是保持还是翻转 bosonic commutation
        form。在 note 固定的实矩阵 convention 中，任何保持玻色对易关系
        的同时实换基都会保留这个正负号，因此不能把 Case 9 变回 Case 7。
        作者在同一段先写
        “there is sign problem”，后面又写 “Also a Yin-Kai's case”，
        也表明后一句不是一个 positivity theorem。它只能理解为
        “由 7 月 19 日原型启发的另一种矩阵组合”这一宽松标注。</p>

        <p>第一种 realization 已提示：只满足五条离散矩阵关系并不自动消除 sign problem，
        还必须限制 \(A\)。第二种 realization 的 block comparison 给出
        \(B_{11},B_{22}\) anti-Hermitian、\(B_{21}=B_{12}^\dagger\)，
        以及 \(D\) 由 \(C\) 的复共轭决定。原文最后显示的是满足全部这些条件的一般 \(A\)。</p>
        """,
        True,
    ),
    Segment(
        "boson-case9-j2",
        "玻色 Case 9：只剩 off-diagonal cone",
        630,
        677,
        r"""
        <p>作者解第二条 \(J_2\) 约束后说：maximal subgroup 令
        \(B_{12}=C_{12}=0\)，convex cone 反而令
        \(B_{11}=B_{22}=C_{11}=C_{22}=0\)。随后写出只含 off-diagonal
        blocks 的 \(A\)，并判断不存在 contraction semigroup。</p>
        """,
        r"""
        <p>这里 \(J_1^TgJ_1=-g\)、\([J_1,J_2]=0\)，并且
        \(\eta=J_2g\)。直接代入得到
        \[
        J_1^T\overline{(\eta A+A^\dagger\eta)}J_1
        =-(\eta A+A^\dagger\eta).
        \]
        若 \(\eta A+A^\dagger\eta\le0\)，左边也半负定，于是
        \(-(\eta A+A^\dagger\eta)\le0\)，即
        \(\eta A+A^\dagger\eta\ge0\)。因此只能有
        \(\eta A+A^\dagger\eta=0\)。这说明满足第二条线性等式的
        off-diagonal \(A\) 虽然存在，却不能给出负定生成元。</p>
        """,
        True,
    ),
    Segment(
        "boson-case10",
        "玻色 Case 10：新版矩阵与失败判断",
        678,
        684,
        r"""
        <p>新版保留 Case 10 的五条离散关系，但把 \(J_2\) 从旧版的
        \(\sigma_x\otimes I_N\) 改为 \(\sigma_z\otimes I_N\)。
        作者仍写 “Also a Yin-Kai's case”，但不再展开旧版的 block
        calculation，并明确改判为 “There's no contraction
        semigroup”。</p>
        """,
        r"""
        <h4>Case 10 揭示 “Also” 所指的矩阵来源</h4>
        <p>先把 Case 7 中已经出现的三个 Nambu matrices 并列：</p>
        <div class="scroll">\[
          \begin{aligned}
          g&=(-i\sigma_y)\otimes I_N,\\
          J_2^{\text{Case 7}}&=\sigma_x\otimes I_N,\\
          J_2^{\text{Case 7}}g&=\sigma_z\otimes I_N .
          \end{aligned}
        \]</div>
        <p>新版 Case 10 恰好把 Case 7 的 metric 拿来当自己的
        \(J_2\)：</p>
        <div class="scroll">\[
          J_2^{\text{Case 10}}
          =\sigma_z\otimes I_N
          =J_2^{\text{Case 7}}g,
          \qquad
          J_2^{\text{Case 10}}g=-\sigma_x\otimes I_N .
        \]</div>
        <p>所以更新后的 Case 10 虽然不再与 Case 7 共用 \(J_2\)，
        却仍直接使用 7 月 19 日原型中的 particle/hole metric。
        这解释了作者为什么在改动 \(J_2\) 后仍保留 “Also”。Cases
        3、4、9 保留 Case 7 的 \(J_2\)；Case 10 则改用 Case 7 的
        \(J_2g\)。这些条目都在重新组合原型中已经出现的矩阵。</p>
        <p>但是 Case 10 还有
        \(J_1^TgJ_1=-g\) 和 \(J_1^2=-I\)，而 Case 7 分别为
        \(+g\) 与 \(+I\)，并且作者在同一句明确写
        “no contraction semigroup”。因此，共用原型中的 building
        blocks 只解释名称的来源，不能推出它与 Case 7 等价，更不能推出
        无符号。note 没有把这种“从原型重新组合”的关系定义成新的
        数学分类。</p>

        <h4>新版 matrices 现在确实满足标题</h4>
        <p>新版选择</p>
        <div class="scroll">\[
          J_1=\sigma_z\otimes(-i\sigma_y)\otimes I_{N/2},
          \qquad
          J_2=\sigma_z\otimes I_N .
        \]</div>
        <p>两个 matrices 的第一个 tensor factor 都是 \(\sigma_z\)，
        而 \(J_2\) 在其余空间上是 identity，因此</p>
        <div class="scroll">\[
          J_1J_2=J_2J_1 .
        \]</div>
        <p>同时可逐项验算</p>
        <div class="scroll">\[
          J_1^TgJ_1=-g,\qquad J_1^2=-I_{2N},\qquad
          J_2^TgJ_2=-g,\qquad J_2^2=I_{2N}.
        \]</div>
        <p>所以新版 representative 与 Case 10 标题一致。旧版
        \(J_2=\sigma_x\otimes I_N\) 会与 \(J_1\) 反对易，实际落入 Case 6；
        新版已经修复上一版报告指出的错配。</p>

        <h4>为什么 commuting Case 10 只能停在边界</h4>
        <p>对任何同时满足 \(J_1^TAJ_1=\bar A\) 的 \(A\)，直接使用
        \(J_1,J_2\) 都翻转 \(g\) 且彼此对易，可得</p>
        <div class="scroll">\[
          J_1^T\overline{\left(J_2gA+A^\dagger J_2g\right)}J_1
          =-\left(J_2gA+A^\dagger J_2g\right).
        \]</div>
        <p>如果 \(J_2gA+A^\dagger J_2g\le0\)，复共轭和正交基变换
        保持半负定，所以上式左边也 \(\le0\)。用上式右边替换左边，得到
        \[
        -(J_2gA+A^\dagger J_2g)\le0
        \quad\Longleftrightarrow\quad
        J_2gA+A^\dagger J_2g\ge0.
        \]
        与原来的半负定条件合并，因而只能</p>
        <div class="scroll">\[
          J_2gA+A^\dagger J_2g=0 .
        \]</div>
        <p>这说明 Case 10 中凡满足半负定条件的生成元都只能满足
        maximal-subgroup 等号，不存在负定生成元。新版的 Failed 判断与本报告的解析分类、Octave
        穷举完全一致。</p>

        <p>用户补充说明 “ToLeiWang4.pdf” 大概是
        <code>experts/RPBAFQMC.tex</code> 的编译稿。这个判断与文件主题吻合：
        该文件确实讨论 BAFQMC reflection positivity、regularized weights，
        并声称存在 contraction/expansion semigroup decomposition。
        这项 decomposition 本身不成立，因为两类 blocks 在一般传播层中混合。
        此外，该文件在
        Supplemental Material 中显式使用的 RP matrices 满足</p>
        <div class="scroll">\[
          J_1^TgJ_1=g,\quad J_1^2=I,\qquad
          J_2^TgJ_2=g,\quad J_2^2=-I,\qquad
          \{J_1,J_2\}=0 ,
        \]</div>
        <p>也就是 note 的 RP Case 2，而不是本段 Case 10 的五条 relations。
        因而该文件只能解释作者为什么在 RP 讨论中引入第二个 \(J_2\)；
        既不能证明其声称的 RP regularization，也不能充当 Case 10 的
        负定收缩证明。上面的 Case 10 等号结论仍然需要保留。</p>
        """,
    ),
    Segment(
        "boson-case11-j1",
        "玻色 Case 11：第一条约束",
        685,
        745,
        r"""
        <p>Case 11 改成 \(J_2^TgJ_2=g\)、\(J_2^2=-I\)，并令
        \(J_1,J_2\) 反对易。作者给出两矩阵，重复 Case 3 型的
        \(J_1^TAJ_1=\bar A\) block calculation。</p>
        """,
        r"""
        <p>原文列出的 relations 与 Case 3 基本相同，因为所选 \(J_1\) 相同。
        需要注意显示的最终 \(A\) 中第 \((4,2)\) block 写成
        \(-\bar C_{22}\)，而由上一行
        \(C_{11}=-\bar D_{22}\) 应回代为 \(-\bar C_{11}\)。
        这是局部抄写不一致，不改变随后“是否存在负定生成元”的结构判断。</p>
        """,
        True,
    ),
    Segment(
        "boson-case11-j2",
        "玻色 Case 11：convex cone 与失败判断",
        746,
        793,
        r"""
        <p>作者计算第二条约束，只写出 convex cone：
        \(B_{11}=B_{22}=0\)、\(C_{11}=C_{22}\)、\(C_{12}=0\)。
        随后给出 \(A\)、写出 \(J_2gA\)，并判断不存在 contraction semigroup。</p>
        """,
        r"""
        <p>本 Case 的 \(J_2^2=-I\)。对任意玻色生成元，
        \(\operatorname{Tr}(J_2gA)=0\)，所以
        \(\operatorname{Tr}(J_2gA+A^\dagger J_2g)=0\)。
        Hermitian matrix 若半负定且 trace 为零，全部 eigenvalues 只能为零。
        因此半负定条件只能取等号，不存在负定生成元；这比逐个 block
        猜测更直接。</p>
        """,
        True,
    ),
    Segment(
        "boson-case12-j1",
        "玻色 Case 12：第一条约束",
        794,
        854,
        r"""
        <p>Case 12 保持 \(J_2^TgJ_2=g\)、\(J_2^2=-I\) 与反对易关系，
        只把 \(J_1^2\) 改成 \(-I\)。作者给出矩阵并解
        \(J_1^TAJ_1=\bar A\)。原文 “We jave” 应为 “We have”。</p>
        """,
        r"""
        <p>逐块比较仍得到 \(B_{11},B_{22}\) anti-Hermitian、
        \(B_{21}=B_{12}^\dagger\)，以及 \(D\) 由 \(C\) 决定。
        与 Case 11 相比，改变的是 \(J_1\) 的 realization，而
        \(J_2^2=-I\) 导致的 trace obstruction 尚未改变。</p>
        """,
        True,
    ),
    Segment(
        "boson-case12-j2",
        "玻色 Case 12：convex cone 与失败判断",
        855,
        902,
        r"""
        <p>作者给出 convex cone 的四条 block relations，写出相应 \(A\) 与
        \(J_2gA\)，然后判断不存在 contraction semigroup。</p>
        """,
        r"""
        <p>原文没有写 maximal subgroup，但这不影响“是否存在负定生成元”这个问题。
        由于 \(J_2^2=-I\)，与 Case 11 相同的 trace argument 迫使任何
        Hermitian seminegative contraction matrix 等于零。因此 Failed
        不是这一组 Pauli matrices 的偶然结果。</p>
        """,
        True,
    ),
    Segment(
        "boson-case13",
        "玻色 Case 13",
        903,
        917,
        r"""
        <p>作者取 \(J_1=\sigma_x\otimes I_N\)、
        \(J_2=-i\sigma_y\otimes I_N\)，给出二者的 block matrices，
        然后写“metric 是 \(-I_N\)，不存在 contraction semigroup”。</p>
        """,
        r"""
        <p>直接相乘得到 \(J_2g=-I_{2N}\)，所以原文的 \(-I_N\)
        是维数上的简写或笔误。若 metric 为负单位阵，标准条件变成
        \(A+A^\dagger\ge0\)，它本身可以定义 ordinary expansion/contraction
        direction；但在玻色 Lie-algebra 与本 Case 的 symmetry constraints 下，
        trace argument 仍排除负定收缩矩阵。
        因此“没有 semigroup”的可靠依据不是 metric 等于常数本身，而是约束后的 trace。</p>
        """,
    ),
    Segment(
        "boson-case14",
        "玻色 Case 14",
        918,
        936,
        r"""
        <p>Case 14 与 Case 13 的 \(J_2\) 相同，改用平方为 \(-I\) 的 \(J_1\)。
        作者写出 \(4\times4\) block realization，并作出同样的 metric 与失败判断。</p>
        """,
        r"""
        <p>这里同样有 \(J_2g=-I_{2N}\)，原文写成 \(-I_N\)。
        改变 \(J_1^2\) 不会解除由 \(J_2^2=-I\) 导致的玻色 trace obstruction，
        所以两项成对失败。</p>
        """,
    ),
    Segment(
        "boson-case15",
        "玻色 Case 15",
        937,
        963,
        r"""
        <p>Case 15 取 \(J_1=I\)，所以 \(A\) 为实矩阵。
        作者计算 \(J_2^TAJ_2=\pm\bar A\)，写出 convex cone 的
        \(B=B^\dagger\)、\(C=\bar D\)，再由 \(J_2g=-I\) 判断失败。</p>
        """,
        r"""
        <p>原文的 \(J_1=I_N\) 应按上下文读作 \(I_{2N}\)。
        \(A=\bar A\) 是 anti-linear condition 的完整内容。
        但 \(J_2^2=-I\) 仍使 contraction matrix trace 为零，
        所以即使 convex-cone linear equations 有解，半负定条件也只能取等号。</p>
        """,
        True,
    ),
    Segment(
        "boson-case16-j1",
        "玻色 Case 16：第一条约束",
        964,
        996,
        r"""
        <p>Case 16 取 \(J_1^TgJ_1=-g\)、\(J_1^2=I\)，
        \(J_2^TgJ_2=g\)、\(J_2^2=-I\)，并让二者对易。
        作者解得 \(B=-B^\dagger\)、\(C=\bar D\)。</p>
        """,
        r"""
        <p>从
        \(\begin{pmatrix}-B^T&D\\C&B\end{pmatrix}=\bar A\)
        逐块比较，左上给出 \(B=-B^\dagger\)，右上给出
        \(D=\bar C\)。这是第一条约束的完整解，尚未涉及 inequality。</p>
        """,
        True,
    ),
    Segment(
        "boson-case16-j2",
        "玻色 Case 16：convex cone 与失败判断",
        997,
        1063,
        r"""
        <p>作者继续计算 \(J_2^TAJ_2=\pm\bar A\)，列出 convex cone 的
        block relations，写出 \(J_2gA\le0\)，最后判断不存在 contraction semigroup。</p>
        """,
        r"""
        <p>最后显示的 matrix inequality 是必要检查，但原文没有给出一个满足严格
        半负定的 block choice。实际上 \(J_2^2=-I\) 再次令其 trace 为零，
        所以半负定只能退化为零。至此第二节手算的所有原文都已覆盖；
        其共同的高成本来自每个 Case 都重复展开 \(4\times4\) block products。</p>
        """,
        True,
    ),
    Segment(
        "fermion-general",
        "第三节标题与一般费米生成元",
        1064,
        1073,
        r"""
        <p>第三节标题译为“新费米情形的检验”。作者先写出一般费米生成元的
        \(4\times4\) block form，并注明 \(C_{11},C_{22},D_{11},D_{22}\)
        都是反对称矩阵。</p>
        """,
        r"""
        <p>费米条件 \((gA)^T=-gA\) 给出</p>
        <div class="scroll">\[
          A=\begin{pmatrix}B&C\\D&-B^T\end{pmatrix},
          \qquad C=-C^T,\quad D=-D^T.
        \]</div>
        <p>再把 \(N\times N\) blocks 拆成 \(N/2\) 子块时，
        off-diagonal positions 必须带原文显示的负号，例如
        \(C_{21}=-C_{12}^T\)。这正是它与玻色 block form 的直接差别。</p>
        """,
    ),
    Segment(
        "fermion-case1-j1",
        r"费米 Case \(1'\)：第一条 anti-linear symmetry",
        1074,
        1124,
        r"""
        <p>作者给出 \(J_1=-i\sigma_y\otimes I_N\) 与
        \(J_2=-i\sigma_y\otimes(-i\sigma_y)\otimes I_{N/2}\)，
        然后计算 \(J_1^TAJ_1=\bar A\)，得到各 \(B\) block
        anti-Hermitian，并写 \(C=-\bar D\)。</p>
        """,
        r"""
        <p>例如 \(-B_{11}^T=\bar B_{11}\) 给出
        \(B_{11}=-B_{11}^\dagger\)，
        \(-B_{21}^T=\bar B_{12}\) 给出
        \(B_{12}=-B_{21}^\dagger\)。
        \(C=-\bar D\) 是对四个 pairing subblocks 的合并写法。
        这些条件说明 \(J_1\mathcal K\) 如何把 particle-hole blocks 配对。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case1-j2",
        r"费米 Case \(1'\)：第二个 anti-linear symmetry 与尚缺的证明",
        1125,
        1173,
        r"""
        <p>作者此处取 \(J_2^TAJ_2=\bar A\)，再解出
        \(B_{11}=-B_{22}^\dagger\)、\(B_{12}=B_{12}^\dagger\)、
        \(C_{11}=C_{22}\)、\(C_{12}=C_{12}^T\)。
        最后三句说：这是 non-Hermitian case；作者尚不知道怎样证明，
        只测试了 \(B_{11}\ne0\) 而其余 blocks 为零的子情形，该测试通过。</p>
        """,
        r"""
        <p>“测试一个只有 \(B_{11}\) 的子空间”只能证明这个子空间没有发现负例，
        不能覆盖一般 \(B_{12},C_{11},C_{12}\)。
        本段仍保留旧文字 “I don't know how to prove it”，但新版第一节已经改称
        \(1'\) 是 \(9'\) 的 special case。两处只有在作者补出 basis change 或
        subspace inclusion 后，才能构成完整论证；本段的 block calculation 自身没有展示该包含关系。
        更重要的是，本报告第 8 节已经给出 \(9'\) 离散关系下的负权重反例，
        所以“属于 \(9'\)”不能自动成为完整 Fock-weight positivity 的证明。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case5-j1",
        r"费米 Case \(5'\)：\(J_1\) 条件与原文矩阵笔误",
        1174,
        1197,
        r"""
        <p>Case \(5'\) 声称 \(J_1=\sigma_z\otimes I_N\)，
        \(J_2=-i\sigma_y\otimes I_N\)。作者随后从
        \(J_1^TAJ_1=\bar A\) 得到 \(B=\bar B\)、
        \(C=-\bar C\)、\(D=-\bar D\)。</p>
        """,
        r"""
        <p>原文显示的 \(J_1\) matrix 写成
        \(\operatorname{diag}(I_N,I_N)\)，但紧接着的乘法使用的是
        \(\operatorname{diag}(I_N,-I_N)=\sigma_z\otimes I_N\)。
        因此显示矩阵是笔误，后续三条 relations 对应声称的 \(\sigma_z\)。
        它们分别说明 \(B\) 为实矩阵，而两个 pairing blocks 为纯虚矩阵。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case5-j2",
        r"费米 Case \(5'\)：subgroup、cone 与 “new kind of positivity”",
        1198,
        1253,
        r"""
        <p>作者计算 \(J_2^TAJ_2=\pm\bar A\)，分别写出 maximal subgroup
        与 convex cone。最后把 \(J_2gA\le0\) 化成
        \(\begin{pmatrix}B&C\\C&B\end{pmatrix}\ge0\)，并说
        “Case \(5'\) 给出一个 semigroup，可能是一种新的 positivity”。</p>
        """,
        r"""
        <p>本段与第一节的显示式不同，但本段反而采用了正确的 Nambu
        metric：\(\eta=J_2g\)。对满足
        \(J_2^TAJ_2=-\bar A\) 的生成元，
        \(A^\dagger\eta=\eta A\)，所以标准生成元条件
        \(\eta A+A^\dagger\eta\le0\) 正好化为
        \(J_2gA\le0\)。完整解析穷举也确认 Case \(5'\) 有 nonempty
        negative-definite region，因此这确实定义了控制 \(e^A\) 的 contraction
        semigroup。</p>
        <p>需要保留的 caveat 是“new”。把 Wei 论文的 canonical
        Majorana-reflection-positive metric 完整变换到本 note 的 Nambu
        convention 后，metric 也变成 \(J_2g\)，而不是 \(iJ_2g\)。
        在最小 canonical block 中，同一 reality subspace 可以用
        Case \(5'\) 的 \(J_1\) 表示；有额外 symmetries 时也可能同时满足
        其他允许负定生成元的标签。所以 Case \(5'\) 的 semigroup 是真的，
        但不能仅凭当前 block form 宣称它是一种新的 positivity。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case9-j1",
        r"费米 Case \(9'\)：第一条约束",
        1254,
        1297,
        r"""
        <p>Case \(9'\) 令 \(J_1,J_2\) 对易。作者给出 diagonal \(J_1\)
        与 off-diagonal \(J_2\)，随后从 \(J_1^TAJ_1=\bar A\)
        判断哪些 blocks 为实、纯虚，或由复共轭保持。</p>
        """,
        r"""
        <p>因为 \(J_1\) 的 diagonal entries 是 \(+1,-1,-1,+1\)，
        conjugation by \(J_1\) 会按行列符号乘积给每个 block 加正负号。
        正号位置要求 block 等于其复共轭，负号位置要求 block 等于其复共轭的相反数。
        原文列出的十条 relations 正是这一逐块规则。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case9-j2",
        r"费米 Case \(9'\)：作者的 Hermitian/cone 分解",
        1298,
        1371,
        r"""
        <p>作者把 \(J_2\) 的加号分支称为 maximal subgroup，并说得到的是
        Hermitian case；负号分支称为 convex cone。最后写出
        \(iJ_2gA\le0\)，但没有另写文字结论。</p>
        """,
        r"""
        <p>左侧虽然标成 \(iJ_2gA\)，但紧接着显示的
        \(-\sigma_z\otimes\sigma_x\) 实际等于 \(J_2g\)；
        真正的 \(iJ_2g\) 还应多一个整体 \(i\)。因此右侧 block
        calculation 应按正确的 \(\eta A=J_2gA\) 读取。</p>
        <p>本 Case 有 \(J_1^TgJ_1=-g\)、\([J_1,J_2]=0\) 和
        \(\eta=J_2g\)，所以
        \[
        J_1^T\overline{(\eta A+A^\dagger\eta)}J_1
        =-(\eta A+A^\dagger\eta).
        \]
        若括号内的矩阵半负定，左边也半负定，故上式推出
        \(-(\eta A+A^\dagger\eta)\le0\)，也就是括号内的矩阵半正定。
        它同时半负定和半正定，只能取零。报告第 8 节还给出满足
        Case \(9'\) relations 的多时间片负权重反例，所以原文的
        Passed 标签不能保留。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case10-j1",
        r"费米 Case \(10'\)：两个 realization 与第一条约束",
        1372,
        1431,
        r"""
        <p>作者先说最简单的 \(J_1=J_2=-i\sigma_y\otimes I_N\)
        有 sign problem；再选择另一个 \(J_2\) 做 block calculation。
        第一条约束给出 \(B_{11},B_{22}\) anti-Hermitian、
        \(B_{12}=-B_{21}^\dagger\)，以及 \(C\) 与 \(D\) 的复共轭关系。</p>
        """,
        r"""
        <p>第一种 realization 再次表明离散关系本身不足以决定 sign。
        第二种 realization 的 \(A\) 是完整 anti-linear constraint subspace；
        它的存在仍不说明 cone 内有使收缩矩阵负定的方向。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case10-j2",
        r"费米 Case \(10'\)：convex cone 与失败判断",
        1432,
        1492,
        r"""
        <p>作者解出 convex cone 中 diagonal \(B,C\) blocks 为零，
        写出 \(iJ_2gA\le0\)，最后说“所以这个 ‘wrong’ case 有 sign problem”。</p>
        """,
        r"""
        <p>这里也有同一个标签问题：原文左侧写 \(iJ_2gA\)，右侧
        \(-\sigma_z\otimes\sigma_z\,A\) 实际是 \(J_2gA\)。
        按正确 metric 读取后，所得 contraction candidate 是纯
        off-diagonal block matrix，非零 eigenvalues 成正负对，因此
        不可能负定。原文用引号写 “wrong”，是在标记这一组
        commutation choice；它不是一个已定义的物理分类名称。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case6-j1",
        r"费米 Case \(6'\)：第一条约束",
        1493,
        1552,
        r"""
        <p>Case \(6'\) 保持 \(J_1^TgJ_1=-g\) 与 \(J_2^TgJ_2=-g\)，
        令二者都平方为 \(-I\) 且反对易。作者计算第一条约束并写出一般 \(A\)。</p>
        """,
        r"""
        <p>所得 relations 与玻色 Case 12 的形式相似，但 pairing blocks 的
        transpose signs 由费米反对称性决定。原文逐块乘法已经把这些负号全部写出，
        因此这里不能直接把玻色结论照搬给费米。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case6-j2",
        r"费米 Case \(6'\)：subgroup、cone 与候选 positivity",
        1553,
        1626,
        r"""
        <p>作者解出 maximal subgroup 和 convex cone，写出
        \(iJ_2gA\le0\)，最后说“Good, a new non-hermitian case.
        Possibly has positivity.”，即“很好，这是新的 non-Hermitian case，
        可能具有 positivity”。</p>
        """,
        r"""
        <p>左侧写成 \(iJ_2gA\)，但右侧
        \(-\sigma_z\otimes\sigma_x\,A\) 实际等于 \(J_2gA\)；
        去掉左侧多出的 \(i\) 后，这正是标准 Nambu contraction cone。
        完整穷举确认它包含负定生成元，乘法封闭性与从正参考点连续延拓
        随后给出完整 Fock-weight positivity。</p>
        <p>不过 “new” 仍不能由这份手算推出。\(J_1^2=-I\) 的 Wei
        Kramers-plus-pairing semigroup 完整换到 Nambu convention 后，
        同样落在 \(J_2g\) 中允许负定生成元的分支；其具体 \(J_1\) label 会随
        complex-fermion basis 和额外 symmetries 改变，不应在没有写出
        transformation 时唯一指定为某一个 case。是否还有超出已知类的
        physical realization，需要另做 basis-equivalence analysis。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case7-input",
        r"费米 Case \(7'\)：实矩阵条件",
        1627,
        1636,
        r"""
        <p>Case \(7'\) 取 \(J_1=I_{2N}\)，
        \(J_2=-i\sigma_y\otimes I_N\)。原文因此写
        \(J_1^TAJ_1=\bar A\)，即 \(A\) 是实矩阵。</p>
        """,
        r"""
        <p>这里没有省略额外 block relations：当 \(J_1=I\) 时，
        第一条 anti-linear condition 的确完整等价于 \(A=\bar A\)。
        费米的一般结构仍要求 \(C,D\) 为反对称矩阵。</p>
        """,
    ),
    Segment(
        "fermion-case7-j2",
        r"费米 Case \(7'\)：subgroup、cone 与 “With positivity”",
        1637,
        1689,
        r"""
        <p>作者计算 \(J_2^TAJ_2=\pm\bar A\)，写出 maximal subgroup 与
        convex cone，随后给出 \(iJ_2gA\le0\)，以 “With positivity” 结束。</p>
        """,
        r"""
        <p>原文左侧写 \(iJ_2gA\)，但右侧的
        \(-\sigma_z A\) 实际等于 \(J_2gA\)，所以左侧多了一个 \(i\)。
        去掉它以后，从第二行到第三行把
        \(-\sigma_z A\) 写成
        \(-\begin{pmatrix}B&C\\-C&B^T\end{pmatrix}\)。
        要把它称为 Hermitian seminegative matrix，还需使用此前的
        \(B=B^\dagger\)、\(C=\bar D\)、费米反对称性与 \(A=\bar A\)。
        这些条件合在一起给出正确的 slice-level cone；完整穷举确认该类
        包含负定生成元。报告后文再证明任意多时间片的乘积仍满足收缩
        不等式，并从一个正参考点连续延拓，从而固定 Fock trace 的正号。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case8-j1",
        r"费米 Case \(8'\)：第一条约束",
        1690,
        1749,
        r"""
        <p>Case \(8'\) 与 Case \(7'\) 有相同的 \(J_2\) 关系和对易关系，
        但令 \(J_1^2=-I\)。作者给出 \(4\times4\) realization，
        计算后列出 \(B,C,D\) 的 block relations，并写出一般 \(A\)。</p>
        """,
        r"""
        <p>例如 \(-B_{22}^T=\bar B_{11}\) 给出
        \(B_{11}=-B_{22}^\dagger\)，而
        \(D_{22}=\bar C_{11}\) 给出 \(C_{11}=\bar D_{22}\)。
        原文其余 relations 同样来自对应位置。由于费米 pairing block
        反对称，\((1,2)\) 与 \((2,1)\) positions 的 transpose signs
        不能从玻色 Case 直接复制。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case8-j2",
        r"费米 Case \(8'\)：subgroup、cone 与 “With positivity”",
        1750,
        1821,
        r"""
        <p>作者给出 maximal subgroup 和 convex cone 的 block forms，
        最后写出 \(iJ_2gA\le0\)，并以 “With positivity” 结束。</p>
        """,
        r"""
        <p>这段是第三节最后一份完整手算。与前几例相同，左侧
        \(iJ_2gA\) 多写了 \(i\)，右侧实际计算的是 \(J_2gA\)。
        按 \(\eta=J_2g\) 读取后，它给出的确是标准 Nambu cone；
        完整穷举确认该类包含负定生成元。原 note 的
        “With positivity” 仍没有证明任意多时间片的乘积继续满足收缩
        不等式，也没有说明怎样从正参考点连续固定 spin trace 的符号。
        本报告后文已经补上这两步，因此 Case \(8'\) 可以保留为
        \(e^A\) contraction class。</p>
        """,
        True,
    ),
    Segment(
        "proofs-empty",
        "第四节 `Proofs`",
        1822,
        1824,
        r"""
        <p>原文最后建立标题 “Proofs”，正文只有一个句点。</p>
        """,
        r"""
        <p>这表示更新 note 尚未写入解析证明。前两节的长 block calculations
        提供了 examples 和 candidate subspaces，但第一节的总分类、Comment、
        semigroup closure 与完整 Fock-weight positivity 都没有在原 note 的
        `Proofs` 节完成。以上已经按原顺序覆盖 note 的每一句正文和每个显示公式。</p>
        """,
    ),
]


def render_latex_fragment(source: str) -> str:
    process = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "html5", "--mathjax"],
        input=source,
        text=True,
        capture_output=True,
        check=True,
    )
    rendered = process.stdout
    for level in range(1, 7):
        rendered = rendered.replace(f"<h{level}", "<h4")
        rendered = rendered.replace(f"</h{level}>", "</h4>")
    return rendered


def validate_coverage(note_lines: list[str]) -> None:
    expected = 22
    for segment in SEGMENTS:
        if segment.start != expected:
            raise RuntimeError(
                f"Note coverage gap or overlap before {segment.key}: "
                f"expected line {expected}, got {segment.start}"
            )
        if segment.end < segment.start:
            raise RuntimeError(f"Invalid range for {segment.key}")
        expected = segment.end + 1
    if expected != 1825:
        raise RuntimeError(f"Note coverage ends at {expected - 1}, expected 1824")
    if len(note_lines) < 1824:
        raise RuntimeError("Updated note is shorter than the audited source")


def build_walkthrough(note_lines: list[str]) -> str:
    blocks: list[str] = []
    for index, segment in enumerate(SEGMENTS, start=1):
        source = "".join(note_lines[segment.start - 1 : segment.end])
        rendered = render_latex_fragment(source)
        open_attribute = "" if segment.collapse_source else " open"
        explanation = EXPLANATION_OVERRIDES.get(segment.key, segment.explanation)
        audit = CASE_AUDITS.get(segment.key, "")
        blocks.append(
            fr"""
            <article class="walkthrough-block" id="note-{html.escape(segment.key)}">
              <h3>1.{index} {html.escape(segment.title)}</h3>
              <details class="note-original"{open_attribute}>
                <summary>note 原文，第 {segment.start}--{segment.end} 行
                {"（完整矩阵推导，点击展开）" if segment.collapse_source else "（完整显示）"}</summary>
                <div class="note-source">{rendered}</div>
              </details>
              <div class="explanation">
                <div class="annotation-label">讲解与补全</div>
                {explanation}
                {audit}
              </div>
            </article>
            """
        )
    return "\n".join(blocks)



def main() -> None:
    note_lines = NOTE_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    validate_coverage(note_lines)
    walkthrough = build_walkthrough(note_lines)
    all_class_lecture = build_all_class_lecture()
    canonical_algorithm = CANONICAL_FRAGMENT_PATH.read_text(encoding="utf-8")
    enumeration_tail = ENUMERATION_TAIL_PATH.read_text(encoding="utf-8")
    determinant_symmetry_bridge = DETERMINANT_SYMMETRY_BRIDGE_PATH.read_text(
        encoding="utf-8"
    )
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    if template.count("{{NOTE_WALKTHROUGH}}") != 1:
        raise RuntimeError("Template must contain exactly one note walkthrough marker")
    if template.count("{{ENUMERATION_TAIL}}") != 1:
        raise RuntimeError("Template must contain exactly one enumeration-tail marker")
    if template.count("{{DETERMINANT_SYMMETRY_BRIDGE}}") != 1:
        raise RuntimeError(
            "Template must contain exactly one determinant-symmetry bridge marker"
        )
    if enumeration_tail.count("{{ALL_CLASS_STRUCTURES}}") != 1:
        raise RuntimeError("Enumeration tail must contain one all-class marker")
    if enumeration_tail.count("{{CANONICAL_ALGORITHM}}") != 1:
        raise RuntimeError("Enumeration tail must contain one canonical marker")
    output = template.replace("{{NOTE_WALKTHROUGH}}", walkthrough)
    output = output.replace(
        "{{DETERMINANT_SYMMETRY_BRIDGE}}", determinant_symmetry_bridge
    )
    output = output.replace("{{ENUMERATION_TAIL}}", enumeration_tail)
    output = output.replace("{{ALL_CLASS_STRUCTURES}}", all_class_lecture)
    output = output.replace("{{CANONICAL_ALGORITHM}}", canonical_algorithm)
    output = "\n".join(line.rstrip() for line in output.splitlines()) + "\n"
    OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(
        f"Wrote {OUTPUT_PATH.name}: {len(SEGMENTS)} note segments, "
        "continuous source coverage lines 22-1824, "
        "64 unified formula-and-model class sheets."
    )


if __name__ == "__main__":
    main()
