#!/usr/bin/env python3
"""Build the reader-facing report with a line-complete rendered note walkthrough."""

from __future__ import annotations

import csv
import html
import subprocess
from dataclasses import dataclass
from pathlib import Path


REPORT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = REPORT_DIR.parents[2]
NOTE_PATH = REPO_ROOT / "experts" / "ToYinkaiYu-20260726.tex"
TEMPLATE_PATH = REPORT_DIR / "report_updated_note_full_enumeration_zh.template.html"
OUTPUT_PATH = REPORT_DIR / "report_updated_note_full_enumeration_zh.html"
TABLE_PATH = REPORT_DIR / "tables" / "full_64_class_enumeration.csv"


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
        若 \(M=e^{A_1}\cdots e^{A_k}\)，原式的上下号应分开读：</p>
        <div class="scroll">\[
          p_{\rm boson}=\det(I-M)^{-1/2},\qquad
          p_{\rm fermion}=\det(I+M)^{1/2}.
        \]</div>
        <p>平方根还需要指定连续分支；玻色式还要求 Fock trace 收敛，即不能碰到
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
        <p>因此 \(J_i^2=I\) 时变换严格平方为恒等；\(J_i^2=-I\) 时，
        平方后得到一个负号，这是 Kramers-type anti-linear structure。
        note 把两者都放在 “anti-linear \(Z_2\)” 的宽泛说法下，读者真正需要检查的
        是紧邻公式明确写出的 \(J_i^2=I\) 还是 \(-I\)。</p>

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
        <p>忽略由 normal ordering 单独处理的 scalar，同一个 number-conserving
        slice 的 Nambu exponent generator 是</p>
        <div class="scroll">\[
          A=\begin{pmatrix}B&0\\0&-B^T\end{pmatrix}.
        \]</div>
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

        <h4>怎样从文章的 physical reflection 得到 note 的 \(J_1\)</h4>
        <p><code>main.tex</code> 把两种 flavor 当作 reflection 的两侧，定义</p>
        <div class="scroll">\[
          \theta(i)=-i,\qquad
          \theta(\hat b_i)=\eta_i\hat c_i,\qquad
          \theta(\hat b_i^+)=\bar\eta_i\hat c_i^+ .
        \]</div>
        <p>先取最简单的 \(\eta_i=1\)。在
        \((\hat b,\hat c,\hat b^+,\hat c^+)^T\) 中，交换两侧并复共轭正是</p>
        <div class="scroll">\[
          g=-i\sigma_y\otimes I_2,\qquad
          J_1=I_2\otimes\sigma_x,\qquad
          J_2=I_2\otimes i\sigma_y .
        \]</div>
        <p>其中 \(J_1K\) 对应文章的 physical reflection；\(J_2\) 是在同一个
        两侧空间中选取的另一个 real matrix，用来把这一 reflection structure
        补成 note 所列的五条离散关系。它不是 <code>main.tex</code> 的 RP theorem
        额外要求的一项物理对称性。矩阵上确有</p>
        <div class="scroll">\[
          J_1^2=I_4,\quad J_1^TgJ_1=g,\qquad
          J_2^2=-I_4,\quad J_2^TgJ_2=g,\qquad
          J_1J_2=-J_2J_1 .
        \]</div>
        <p>但是 reflection symmetry 与 reflection positivity 仍是两件不同的事。
        前者只说 \(b\) sector 与 \(c\) sector 互为复共轭；后者还要求每个
        HS-decoupled slice 能整理成</p>
        <div class="scroll">\[
          \hat h=\hat q+\theta(\hat q)
          +\sum_{\mu,\nu}C_{\mu\nu}
          \hat X_\mu\theta(\hat X_\nu),
          \qquad C=C^\dagger\ge0 .
        \]</div>
        <p>正半定 matrix \(C\) 可以分解成平方和，因而每个传播因子最终是
        \(\sum_r\hat R_r\theta(\hat R_r)\) 的极限。左右 Fock spaces 的 trace
        随即成对为</p>
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
        这也解释了 note 为什么把 RP 标成 “non-contraction semigroup”：
        它通过 reflected squares 证明 trace 非负，不通过下一段的
        \(J_2g\)-contraction inequality。</p>
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

        <h4>Case 7 的一模例子：每一步都可以手算</h4>
        <p>取一个玻色 mode，即 Nambu dimension 为 2，并采用 note 在第二节给出的
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
        都还不能证明存在 strict contraction。必须继续检查上述 Hermitian matrix
        是否能严格小于零，再检查多个 \(e^A\) 相乘后的完整 Fock trace 与
        square-root branch。</p>
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
        此外，原文没有定义“non-hermitian case”究竟指 \(A\)、\(gA\)、哪一个 block，
        还是对应的 many-body Hamiltonian。因此读到这个标签时，应以紧邻的矩阵关系为准，
        不能把标签本身当作证明。</p>
        """,
    ),
    Segment(
        "fermion-list",
        r"费米候选条件与 Cases \(1'\)--\(10'\)",
        142,
        182,
        r"""
        <p>原文说已经检查了 7 个独立费米情形。\(1'\) 是两个 anti-linear \(Z_2\)
        symmetries；新版不再把它算作独立类，而说明它只是 semigroup Case \(9'\)
        的 special case。\(2'\) 是玻色
        reflection positivity 的费米对应物，作者写“存在但没有用”。
        接着原文提出另一条 contraction inequality，并列出 \(3'\)--\(10'\)：
        \(3'\) 和 \(4'\) 分别被命名为 Majorana reflection positivity 与
        time-reversal positivity；\(5'\)、\(6'\)、\(7'\)、\(8'\)、\(9'\)
        逐项标为 Passed，\(10'\) 标为 Failed。</p>
        """,
        r"""
        <p>这里的不等式必须保持原样阅读：</p>
        <div class="scroll">\[
          iJ_2gA-iA^\dagger J_2g\le0 .
        \]</div>
        <p>它不是把玻色式简单换一个整体 \(i\)，因为第二项前的符号也改变了。
        若令 \(\eta=iJ_2g\)，标准 propagation contraction 应为</p>
        <div class="scroll">\[
          \eta A+A^\dagger\eta
          =iJ_2gA+iA^\dagger J_2g ,
        \]</div>
        <p>而不是原文中的减号。因此这一节写下的是一个不同的 Hermitian
        matrix inequality；它是否足以控制当前 Nambu basis 中的 \(e^A\)，
        需要单独证明，不能从“contraction semigroup cases”这个标题直接推出。</p>
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
        只改变这一条，因此确实能独立检验：
        anti-linear condition \(J_1^TAJ_1=\bar A\) 作用到
        contraction inequality 后，究竟把同一个半负定方向保留下来，还是把它变成相反方向。
        但原文第三组逐字写成 \(3'\) 与 \(7'''\)；前者保持 \(g\)，后者翻转 \(g\)，
        所以它们不只差 commutation relation。若作者本意是
        \(3'''\) 与 \(7'''\)，则只需在 \(3'\) 后补两个 prime，才形成同样的受控配对。</p>
        <p>
        作者也把旧版的 “I don't think so” 改成更谨慎的
        “It has to be checked”。这里先按新版保留问题；答案应在完成后续计算并明确
        contraction matrix 后再给出。</p>
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

        <h4>为什么这正是 7 月 19 日 pole-free 报告中的结构</h4>
        <p>旧报告使用 \(g=-\Omega\)，并把同一个 signature matrix 写成
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
          <li>严格稳定的自由配对 Hamiltonian 产生虚时间衰减。若
          \(\epsilon_{\min}-\mu>|\Delta|\)，其 exponent generator \(A\) 满足
          \[
            (J_2g)A+A^\dagger(J_2g)<0,
          \]
          所以 \(e^A\) 是 strict contraction。</li>
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

        <h4>它与文章 RP criterion 分别证明什么</h4>
        <p>在这个 benchmark 中，两套结构同时成立，但分工不同：</p>
        <ul>
          <li><strong>main.tex 的 RP theorem：</strong>利用
          \(b\leftrightarrow c\) 的 reflected-square decomposition 和正半定
          pairing coefficient，证明固定构型的 operator trace 在存在时非负。</li>
          <li><strong>Yinkai's-case contraction：</strong>利用稳定自由衰减与
          \(U_2\) 纯相位，证明固定构型的 trace denominator 不会出现 pole。</li>
        </ul>
        <p>所以它目前不应被宣传为替代 RP 的第三种 sign-positivity mechanism。
        对本文配对模型，它补上的是 RP theorem 中 “whenever the trace is finite”
        这项条件的一个具体、严格保证。若以后找到一个不满足现有 TRS/RP、
        却能从 Case 7 semigroup 单独推出 real positive weight 的 physical
        HS model，那才会形成文章分类之外的新 sign-free territory。</p>

        <p>原文还给出 \(J_1=I_{2N}\) 的简单 representative。
        它只要求 \(A=\bar A\)，适合检查这一抽象 relations class；
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
        \(J_2\Omega A=-J_2gA\)。在 cone 子空间上，
        \(J_2gA\) 是 Hermitian，故原文的最后一步确实是在施加一个可比较本征值的
        matrix inequality。maximal subgroup 对应等号边界
        \(J_2gA+A^\dagger J_2g=0\)；cone generators 对应离开边界的 Hermitian
        directions。两部分相加才形成完整 semigroup generator。
        这里 \(J_1^2=-I\) 没有妨碍 inequality，Case 8 因而给出了一个真正的候选
        strict contraction family。</p>
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
        strict contraction point。原文后面的大 block inequality 是这一简单
        representative 向一般 \(N\) 与一般 blocks 的展开。</p>
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
        作者称它也是 “Yin-Kai's case”，随后像 Case 8 一样计算
        \(J_1^TAJ_1=\bar A\)，并列出 \(B\)、\(C\)、\(D\) 子块之间的关系。</p>
        """,
        r"""
        <p>这段乘法的作用仍是解线性约束。以 \((1,1)\) block 为例，
        \(-B_{22}^T=\bar B_{11}\) 给出
        \(B_{11}=-B_{22}^\dagger\)；\((1,2)\) block
        \(B_{12}^T=\bar B_{12}\) 给出 \(B_{12}=B_{12}^\dagger\)。
        原文写出的其余四条关系也分别来自相应 block。到这里仅确定了允许的线性子空间，
        尚未施加半负定性。</p>
        <p>为什么它最终与 Case 7 不同，可以先试最自然的 strict direction。
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
        <p>关键不是 cone 线性子空间是否非零，而是该子空间内能否找到严格半负定的
        \(J_2gA+A^\dagger J_2g\)。Case 3 的 anti-linear condition
        会把这个 Hermitian matrix 变成其相反数。若一个允许的 \(A\) 令它半负定，
        对称变换后的同一 \(A\) 又要求它半正定，因此只能等于零。
        原文的 Failed 判断与这一局部现象一致；显示的 block calculation 给出了
        “只剩边界”的坐标形式。</p>
        <p>把上一段的观察推广到任意允许 \(A\)。用本 Case 的
        \(\{J_1,J_2\}=0\)、
        \(J_1^TgJ_1=g\) 和 \(J_1^TAJ_1=\bar A\) 逐项移动 matrices，
        得到</p>
        <div class="scroll">\[
          J_1^T\overline{\left(J_2gA+A^\dagger J_2g\right)}J_1
          =-\left(J_2gA+A^\dagger J_2g\right).
        \]</div>
        <p>左边与 \(J_2gA+A^\dagger J_2g\) 的 eigenvalues 相同，
        右边却把 eigenvalues 全部变号。若这个 matrix 半负定，它便同时半正定，
        故只能等于零。这才是 Case 3 对所有 blocks 的失败证明。</p>
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
        原文使用 \(2\times2\) block form，计算后得到
        \(B=-B^\dagger\) 与 \(C=-\bar D\)。</p>
        """,
        r"""
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
        \(+I\) 改成 \(-I\) 并没有救回这个 anti-commuting branch。</p>
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
        <p>在 cone 分支 \(A=\begin{pmatrix}0&-\bar C\\C&0\end{pmatrix}\) 中，
        \(J_2gA=\begin{pmatrix}0&-\bar C\\-C&0\end{pmatrix}\) 的谱关于零成对出现。
        除非所有本征值都为零，它不可能整体半负定。
        因此这个非零线性方向不能形成 strict cone；原文的结论有直接的 spectral
        interpretation。</p>
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
        \(4\times4\) block realization，并解出 \(J_1^TAJ_1=\bar A\)。</p>
        """,
        r"""
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
        <p>这个 cone matrix 具有把两个子空间互换的 off-diagonal form。
        与 Case 4 一样，其 Hermitian contraction matrix 的非零本征值成
        \(\lambda,-\lambda\) 对出现，所以只有零矩阵能半负定。
        这解释了为什么“cone 分支非空”仍然不够。</p>
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
        作者不再展开旧版的 block calculation，并明确改判为
        “There's no contraction semigroup”。</p>
        """,
        r"""
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
        <p>左边由复共轭和正交 basis change 得到，保留 Hermitian matrix 的
        eigenvalue signs；右边却把所有 signs 翻转。如果
        \(J_2gA+A^\dagger J_2g\le0\)，同一个 matrix 也必须半正定，
        因而只能</p>
        <div class="scroll">\[
          J_2gA+A^\dagger J_2g=0 .
        \]</div>
        <p>这说明 Case 10 只有 maximal-subgroup boundary，没有 strict
        contraction interior。新版的 Failed 判断与本报告的解析分类、Octave
        穷举完全一致。</p>

        <p>原文最后引用 “ToLeiWang4.pdf”，但当前仓库中没有该文件。
        因此本报告不能核对其中的具体推导；上面的直接矩阵证明不依赖该外部文件。</p>
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
        这是局部抄写不一致，不改变随后“能否有 strict contraction”的结构判断。</p>
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
        因此不存在 strict interior；这比逐个 block 猜测更直接。</p>
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
        <p>原文没有写 maximal subgroup，但这不影响 strict-cone question。
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
        trace argument 仍排除 strict seminegative interior。
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
        所以即使 convex-cone linear equations 有解，也没有 strict interior。</p>
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
        r"费米 Case \(1'\)：第二个 anti-linear symmetry 与其证据范围",
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
        subspace inclusion 后才构成完整论证；本段的 block calculation 自身没有展示该包含关系。
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
        <p>这里的 block inequality 确实是一个明确的 Hermitian semidefinite
        condition；但它还没有证明当前 Nambu propagation 的 Fock trace 非负。
        特别是第一节为费米写的不等式含
        \(iJ_2gA-iA^\dagger J_2g\)，而本段实际检查的是 \(J_2gA\)。
        两者不是同一条件，所以“new positivity”在原 note 中仍是研究猜想。</p>
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
        <p>这段完成了线性分解和一个 slice-level inequality，
        但仍需核对它是否等于第一节声称的
        \(iJ_2gA-iA^\dagger J_2g\le0\)，以及它是否控制
        \(e^A\)。原文没有进行这两步，因此第一节给 \(9'\) 的 Passed
        标签并未在这里升级成完整 weight proof。</p>
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
        它的存在仍不说明 cone 内有严格半负定方向。</p>
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
        <p>所得 contraction candidate 是纯 off-diagonal block matrix，
        非零 eigenvalues 成正负对，因此不能 strict seminegative。
        原文用引号写 “wrong”，是在标记这一组 commutation choice；
        它不是一个已定义的物理分类名称。</p>
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
        <p>“Possibly”准确反映了证据层次：block inequality 找到了候选 cone，
        但还没有把它连接到完整 Fock trace。原文也没有证明不同时间片相乘后
        square-root branch 始终保持非负，因此这仍是生成元层面的候选结果。</p>
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
        <p>原文从第二行到第三行把
        \(-\sigma_z A\) 写成
        \(-\begin{pmatrix}B&C\\-C&B^T\end{pmatrix}\)。
        要把它称为 Hermitian seminegative matrix，还需使用此前的
        \(B=B^\dagger\)、\(C=\bar D\)、费米反对称性与 \(A=\bar A\)。
        这些条件合在一起给出 slice-level cone；完整 weight statement
        仍需 propagation 与 branch proof。</p>
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
        <p>这段是第三节最后一份完整手算。它说明某些 block choices 可以令
        显示的 matrix seminegative，但没有证明该 inequality 与第一节公式完全一致，
        也没有证明多时间片 Fock trace 的符号。因而 “With positivity”
        最稳妥的直译是“具有这里所写的 matrix positivity”，不能自动扩张成
        “AFQMC weight 已被证明无符号”。</p>
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
                {segment.explanation}
              </div>
            </article>
            """
        )
    return "\n".join(blocks)


def relation(sign: str, target: str) -> str:
    positive = int(sign) == 1
    if target == "j1g":
        return r"\(J_1^TgJ_1=" + (r"g\)" if positive else r"-g\)")
    if target == "j2g":
        return r"\(J_2^TgJ_2=" + (r"g\)" if positive else r"-g\)")
    if target == "j1square":
        return r"\(J_1^2=" + (r"I\)" if positive else r"-I\)")
    if target == "j2square":
        return r"\(J_2^2=" + (r"I\)" if positive else r"-I\)")
    raise ValueError(target)


def build_full_table() -> str:
    rows: list[str] = []
    with TABLE_PATH.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            commutation = (
                r"\([J_1,J_2]=0\)"
                if int(row["r"]) == 1
                else r"\(\{J_1,J_2\}=0\)"
            )
            status = row["status"]
            if status == "strict":
                result = "存在 strict contraction"
                result_class = "yes"
            elif status == "boundary_only_trace_obstruction":
                result = "只能在边界：contraction matrix 的 trace 被迫为零"
                result_class = "no"
            else:
                result = (
                    r"只能在边界：\(J_1^TAJ_1=\bar A\) "
                    "把半负定方向变成半正定方向"
                )
                result_class = "no"
            rows.append(
                "<tr>"
                f"<td>{'玻色' if row['statistics'] == 'boson' else '费米'}</td>"
                f"<td>{relation(row['s1'], 'j1g')}</td>"
                f"<td>{relation(row['q1'], 'j1square')}</td>"
                f"<td>{relation(row['s2'], 'j2g')}</td>"
                f"<td>{relation(row['q2'], 'j2square')}</td>"
                f"<td>{commutation}</td>"
                f"<td><code>{html.escape(row['metric'])}</code></td>"
                f'<td class="{result_class}">{result}</td>'
                f"<td><code>{html.escape(row['J1_word'])}</code>, "
                f"<code>{html.escape(row['J2_word'])}</code></td>"
                "</tr>"
            )
    if len(rows) != 64:
        raise RuntimeError(f"Expected 64 enumeration rows, found {len(rows)}")
    return "\n".join(rows)


def main() -> None:
    note_lines = NOTE_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    validate_coverage(note_lines)
    walkthrough = build_walkthrough(note_lines)
    table = build_full_table()
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    if template.count("{{NOTE_WALKTHROUGH}}") != 1:
        raise RuntimeError("Template must contain exactly one note walkthrough marker")
    if template.count("{{FULL_ENUMERATION_ROWS}}") != 1:
        raise RuntimeError("Template must contain exactly one enumeration marker")
    output = template.replace("{{NOTE_WALKTHROUGH}}", walkthrough)
    output = output.replace("{{FULL_ENUMERATION_ROWS}}", table)
    output = "\n".join(line.rstrip() for line in output.splitlines()) + "\n"
    OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(
        f"Wrote {OUTPUT_PATH.name}: {len(SEGMENTS)} note segments, "
        "continuous source coverage lines 22-1824, 64 enumeration rows."
    )


if __name__ == "__main__":
    main()
