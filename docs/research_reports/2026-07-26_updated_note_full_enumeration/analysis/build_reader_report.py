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
        <p>原文说“玻色有 7 个 passed cases”，随后先列两类已有结构。
        第 1 类是由两个 anti-linear \(Z_2\) symmetries 组成的 time-reversal symmetry；
        第 2 类是 reflection positivity，并特别注明它不是 contraction semigroup。</p>
        """,
        r"""
        <p>这里的 anti-linear transformation 不是单独的 \(J\)，而是 \(J\mathcal K\)，
        其中 \(\mathcal K\) 做复共轭。若 \(J^2=-I\)，它具有 Kramers 型结构。
        reflection positivity 也不等于普通 reflection symmetry：除了反射变换，还要有
        跨反射面的正性条件。原文把这两类与后面的 contraction semigroup 并列，
        所以“7 个 passed”并不是“同一个半群判据产生 7 类”的意思。</p>
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
        Case 8 “mainly non-Hermitian”；Case 9 Failed；Case 10 Passed；
        Cases 11--16 全部 Failed。</p>
        """,
        r"""
        <p>这段的核心不等式应先写成标准 contraction form。因为此处
        \(J_2g\) 是 Hermitian，令 metric \(\eta=J_2g\)，则</p>
        <div class="scroll">\[
          \eta A+A^\dagger\eta\le0
          \quad\Longrightarrow\quad
          (e^A)^\dagger\eta e^A\le\eta .
        \]</div>
        <p>后一式由
        \(\frac{d}{dt}\bigl[e^{tA^\dagger}\eta e^{tA}\bigr]
        =e^{tA^\dagger}(\eta A+A^\dagger\eta)e^{tA}\le0\)
        对 \(t\in[0,1]\) 积分得到。这才是“contraction”的具体含义。
        本段的 Passed/Failed 是作者的手算标签；原文本身尚未为每一项写出
        strict interior、完整 Fock trace 和 square-root branch 的证明。</p>
        """,
    ),
    Segment(
        "boson-passed-list",
        "玻色作者版 passed-only 清单",
        118,
        144,
        r"""
        <p>“List passed ones only”译为“只列出通过的情形”。\(1''\) 是
        time-reversal symmetry；\(2''\) 是 reflection positivity，并保留
        “non-contraction semigroup”的说明；\(3''\) 与 \(4''\) 分别是
        “non-Hermitian case I/II”；\(5''\) 是 “Yinkai's case”；
        \(6''\) 是 “mainly non-Hermitian”；\(7''\) 是
        “also non-Hermitian”。它们分别对应前面的两类已有结构、
        Cases 5--8 与 Case 10。</p>
        """,
        r"""
        <p>这次重新编号很容易造成误读：\(1''\) 和 \(2''\) 不是前面 contraction
        inequality 的通过项；\(3''\)--\(7''\) 才来自该列表。
        此外，原文没有定义“non-hermitian case”究竟指 \(A\)、\(gA\)、哪一个 block，
        还是对应的 many-body Hamiltonian。因此读到这个标签时，应以紧邻的矩阵关系为准，
        不能把标签本身当作证明。</p>
        """,
    ),
    Segment(
        "fermion-list",
        r"费米候选条件与 Cases \(1'\)--\(10'\)",
        145,
        185,
        r"""
        <p>原文说已经检查了 8 类费米情形。\(1'\) 是两个 anti-linear \(Z_2\)
        symmetries，作者写“可能成立，但尚未证明”；\(2'\) 是玻色
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
        186,
        218,
        r"""
        <p>作者把费米候选重新编号为 \(1'''\)--\(8'''\)：
        \(1'''\) 保留“可能但未证明”的两个 anti-linear symmetries；
        \(2'''\) 是 Majorana reflection positivity；\(3'''\) 是
        time-reversal positivity；\(4'''\)--\(8'''\) 是原先标为 Passed
        的 \(5'\)--\(9'\)。随后作者提出 Comment：
        他怀疑玻色 \(4''\) 与 \(7''\) 之间的 commutator/anti-commutator 差别并不重要，
        并猜测同样的观察也适用于费米 \(2'''\) 与 \(6'''\)、
        \(3'''\) 与 \(7'''\)，以及 \(4'\) 与 \(8'''\)。</p>
        """,
        r"""
        <p>方括号 \([J_1,J_2]=0\) 表示对易，花括号
        \(\{J_1,J_2\}=0\) 表示反对易。Comment 选出的每一对，其他四条关系相同，
        只改变这一条，因此它正好提出一个可独立检验的问题：
        anti-linear condition \(J_1^TAJ_1=\bar A\) 作用到
        contraction inequality 后，究竟把同一个半负定方向保留下来，还是把它变成相反方向。
        这里先把问题按原文保留；答案应在完成后续计算并明确 contraction matrix 后再给出。</p>
        """,
    ),
    Segment(
        "boson-case7",
        "第二节开头与玻色 Case 7",
        219,
        228,
        r"""
        <p>第二节标题译为“新玻色情形的检验”。Case 7 取
        \(J_1^TgJ_1=g\)、\(J_1^2=I\)、
        \(J_2^TgJ_2=-g\)、\(J_2^2=I\)，并令 \(J_1,J_2\) 对易。
        作者先给出一个张量积实现，再指出可用更简单的 \(J_1=I_{2N}\)。
        最后一句说 metric 是 \(\eta=J_2g\)，并把 contraction 称为“physical”。</p>
        """,
        r"""
        <p>取 \(J_1=I_{2N}\) 后，\(J_1^TAJ_1=\bar A\) 直接要求 \(A=\bar A\)，
        即 \(A\) 为实矩阵。对 \(J_2=\sigma_x\otimes I_N\) 和玻色
        \(g=\begin{pmatrix}0&-I\\I&0\end{pmatrix}\)，</p>
        <div class="scroll">\[
          J_2g=\begin{pmatrix}I&0\\0&-I\end{pmatrix},
          \qquad (J_2g)^\dagger=J_2g,\qquad (J_2g)^2=I .
        \]</div>
        <p>因此它确实可以作为 indefinite metric。原文的 “physical” 没有给出定义；
        可核查的数学内容是 \((e^A)^\dagger(J_2g)e^A\le J_2g\)，
        不能把引号中的形容词当作额外结论。</p>
        """,
    ),
    Segment(
        "boson-case8-j1",
        r"玻色 Case 8：矩阵选择与 \(J_1^TAJ_1=\bar A\)",
        229,
        299,
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
        """,
        True,
    ),
    Segment(
        "boson-case8-j2",
        r"玻色 Case 8：\(J_2\) 分解、maximal subgroup 与 invariant cone",
        300,
        382,
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
        """,
        True,
    ),
    Segment(
        "boson-case3-j1",
        "玻色 Case 3：矩阵选择与第一条约束",
        383,
        444,
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
        """,
        True,
    ),
    Segment(
        "boson-case3-j2",
        "玻色 Case 3：subgroup、cone 与 “Not a contraction semigroup”",
        445,
        502,
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
        """,
        True,
    ),
    Segment(
        "boson-case4-j1",
        "玻色 Case 4：二维 block form",
        503,
        542,
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
        """,
        True,
    ),
    Segment(
        "boson-case4-j2",
        "玻色 Case 4：maximal subgroup、cone 与失败判断",
        543,
        571,
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
        572,
        636,
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
        637,
        684,
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
        "boson-case10-j1",
        "玻色 Case 10：第一条约束",
        685,
        745,
        r"""
        <p>Case 10 与 Case 9 相同地取 \(J_1^TgJ_1=-g\)，但令
        \(J_1^2=-I\)。作者选取一个与 \(J_2\) 对易的 realization，
        计算得到 \(B_{22}=\bar B_{11}\)、\(B_{21}=-\bar B_{12}\)，
        并给出 \(C,D\) 的相应关系。</p>
        """,
        r"""
        <p>这里的 \(B_{11}=\bar B_{22}\) 只把两个 diagonal blocks 配对，
        并不要求 \(B_{11}\) 本身 Hermitian；\(B_{12}=-\bar B_{21}\)
        也只是复共轭关系。原文显示的 \(A\) 完整记录了第一条约束，
        但还没有任何 eigenvalue inequality。</p>
        """,
        True,
    ),
    Segment(
        "boson-case10-j2",
        "玻色 Case 10：作者声称存在 contraction semigroup",
        746,
        799,
        r"""
        <p>原文先给出 maximal subgroup 的 block relations，再给出 convex cone
        的 relations 和相应 \(A\)，最后一句直接写
        “There's a contration semigroup.”，即“存在一个 contraction semigroup”
        （原文 <em>contration</em> 是拼写错误）。</p>
        """,
        r"""
        <p>这一段少了决定性的 matrix inequality。原文只证明
        \(J_2^TAJ_2=-\bar A\) 的线性解空间非空，却没有证明
        \(J_2gA+A^\dagger J_2g\le0\) 在该空间中有 strict solution。
        对本 Case 的关系直接施加 \(J_1^TAJ_1=\bar A\)，可得</p>
        <div class="scroll">\[
          J_1^T\overline{(J_2gA+A^\dagger J_2g)}J_1
          =-(J_2gA+A^\dagger J_2g).
        \]</div>
        <p>左边与原矩阵有相同的 eigenvalue signs；若右边多出负号，
        半负定和半正定必须同时成立。因此这里只允许等号边界，
        原文最后一句不能由前面的 block calculation 推出。</p>
        """,
        True,
    ),
    Segment(
        "boson-case11-j1",
        "玻色 Case 11：第一条约束",
        800,
        860,
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
        861,
        908,
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
        909,
        969,
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
        970,
        1017,
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
        1018,
        1032,
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
        1033,
        1051,
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
        1052,
        1078,
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
        1079,
        1111,
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
        1112,
        1178,
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
        1179,
        1188,
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
        1189,
        1239,
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
        r"费米 Case \(1'\)：第二个 anti-linear symmetry 与未完成证明",
        1240,
        1288,
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
        原文在这里明确承认证明未完成，因此 \(1'\) 应保持为 open candidate，
        而不是无符号定理。</p>
        """,
        True,
    ),
    Segment(
        "fermion-case5-j1",
        r"费米 Case \(5'\)：\(J_1\) 条件与原文矩阵笔误",
        1289,
        1312,
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
        1313,
        1368,
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
        1369,
        1412,
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
        1413,
        1486,
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
        1487,
        1546,
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
        1547,
        1607,
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
        1608,
        1667,
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
        1668,
        1741,
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
        1742,
        1751,
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
        1752,
        1804,
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
        1805,
        1864,
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
        1865,
        1936,
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
        1937,
        1939,
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
    if expected != 1940:
        raise RuntimeError(f"Note coverage ends at {expected - 1}, expected 1939")
    if len(note_lines) < 1939:
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
              <div class="translation">
                <div class="annotation-label">中文释义</div>
                {segment.translation}
              </div>
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
        "continuous source coverage lines 22-1939, 64 enumeration rows."
    )


if __name__ == "__main__":
    main()
