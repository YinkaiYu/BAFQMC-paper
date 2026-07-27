"""Expanded reader-first explanations that replace compressed legacy sections."""

from __future__ import annotations


FERMION_FRAMEWORK_EXPLANATION = r"""
<h4>先回答：物理传播中究竟是 \(e^A\) 还是 \(e^{gA}\)</h4>
<p>
note 已经固定
\[
  \hat h=\frac12\chi^TgA\chi,\qquad
  g=\begin{pmatrix}0&I\\I&0\end{pmatrix},\qquad
  gA+A^Tg=0 .
\]
这里 \(\{\chi_i,\chi_j\}=g_{ij}\)。不要先凭矩阵外观猜测传播元；
直接计算 \(\hat h\) 对 Nambu 算符的对易子。利用
\[
  [\chi_i\chi_j,\chi_k]
  =\chi_i\{\chi_j,\chi_k\}
   -\{\chi_i,\chi_k\}\chi_j
  =\chi_i g_{jk}-g_{ik}\chi_j ,
\]
再使用 \((gA)^T=-gA\)，得到
</p>
<div class="scroll">\[
  [\hat h,\chi_k]=-\sum_j A_{kj}\chi_j,\qquad
  [\hat h,\chi]=-A\chi .
\]</div>
<p>
因此 Baker--Campbell--Hausdorff 展开逐阶给出
</p>
<div class="scroll">\[
  e^{\hat h}\chi e^{-\hat h}
  =\chi+[\hat h,\chi]
  +\frac1{2!}[\hat h,[\hat h,\chi]]+\cdots
  =e^{-A}\chi .
\]</div>
<p>
结论没有歧义：在 note 当前的 Nambu convention 中，
<strong>单粒子传播由 \(A\) 生成</strong>，Fock trace 中出现
\(e^{A_1}\cdots e^{A_k}\)。矩阵 \(gA\) 的作用是给
\(\chi_i\chi_j\) 提供反对称系数；它不是单粒子传播元。
</p>

<h4>换成 Majorana basis 也不会把传播元变成 \(gA\)</h4>
<p>
对每个 complex fermion，把 annihilation/creation operators
换成两个 normalized Majorana combinations。矩阵写法为
</p>
<div class="scroll">\[
  \gamma=U\chi,\qquad
  U=\frac1{\sqrt2}
  \begin{pmatrix}I&I\\-iI&iI\end{pmatrix},
  \qquad UgU^T=I,\qquad U^\dagger U=I .
\]</div>
<p>
把 \(\chi=U^\dagger\gamma\) 代回二次算符，并使用
\(U^{-T}g=U\)，得到
</p>
<div class="scroll">\[
  \hat h
  =\frac12\gamma^T(UAU^\dagger)\gamma,\qquad
  e^{UAU^\dagger}=Ue^AU^\dagger .
\]</div>
<p>
所以 Majorana generator 是 \(UAU^\dagger\)，它与 \(A\)
由相似变换相连，具有相同 eigenvalues，也给出同一个 determinant。
正确换基需要把 \(A\)、两个 anti-linear transformations 和
contraction metric 一起变换。单独写 \(gA\) 不是换基，因为
一般不存在 \(gA=SAS^{-1}\)。
</p>

<h4>note 第一节的费米不等式实际控制了错误的矩阵指数</h4>
<p>
Cases \(3'\)--\(10'\) 都规定
\(J_2^2=-I\)、\(J_2^TgJ_2=-g\)。由实正交性可逐步推出
</p>
<div class="scroll">\[
  J_2^T=-J_2,\qquad gJ_2=-J_2g .
\]</div>
<p>
note 写下
</p>
<div class="scroll">\[
  iJ_2gA-iA^\dagger J_2g\le0 .
\]</div>
<p>
为看清它是什么，不必给 \(gA\) 另起名字。直接利用
\((gA)^\dagger=A^\dagger g\) 与 \(gJ_2=-J_2g\)，可改写为
</p>
<div class="scroll">\[
  iJ_2(gA)+(gA)^\dagger(iJ_2)\le0 .
\]</div>
<p>
因为 \(iJ_2\) 是 Hermitian involution，这确实是一个标准
contraction inequality；但它控制的是 \(e^{t(gA)}\)，不是 trace
公式中的 \(e^{tA}\)。这不是“还少一句 basis transport”便能自动补好的
小缺口，而是 note 当前两条核心公式使用了不同传播矩阵。若不修改定义，
或不重新做完整换基，这个 inequality 不能用于证明所写 fermionic
AFQMC weight 非负。
</p>

<div class="warning">
  <strong>一个 \(2\times2\) 精确检验立即暴露问题。</strong>
  取
  \[
    g=\sigma_x,\qquad J_1=\sigma_x,\qquad
    J_2=i\sigma_y,\qquad A=iy\sigma_z .
  \]
  它满足 Case \(3'\) 的五条关系、\((gA)^T=-gA\)、
  \(J_1^TAJ_1=\bar A\)，而且 note 的不等式严格成立：
  \[
    iJ_2gA-iA^\dagger J_2g=-2yI<0\qquad(y>0).
  \]
  但是物理二次算符为
  \[
    \hat h=iy\left(c^+c-\frac12\right),
  \]
  所以
  \[
    \Tr e^{\hat h}
    =e^{-iy/2}+e^{iy/2}
    =2\cos\frac y2 .
  \]
  它在 \(y=\pi\) 取零，在 \(y=2\pi\) 取 \(-2\)。
  因此“\(e^{gA}\) 严格收缩”没有阻止
  \(\det(I+e^A)^{1/2}\) 过零并变负。
</div>

<h4>若坚持使用 note 顶部的 \(e^A\)，正确的收缩条件是什么</h4>
<p>
同一组 \(J_2\) 关系使
\[
  \eta=J_2g
\]
成为 Hermitian involution：
</p>
<div class="scroll">\[
  (J_2g)^\dagger=J_2g,\qquad (J_2g)^2=I .
\]</div>
<p>
因而直接作用于物理传播 \(e^A\) 的标准条件是
</p>
<div class="scroll">\[
  J_2gA+A^\dagger J_2g\le0 .
\]</div>
<p>
这与 note 写的式子相比，不仅少了 \(i\)，第二项的符号也不同。
对它求导才得到
</p>
<div class="scroll">\[
  \frac{d}{dt}
  \left[e^{tA^\dagger}(J_2g)e^{tA}\right]
  =
  e^{tA^\dagger}
  \left(A^\dagger J_2g+J_2gA\right)e^{tA}\le0 ,
\]</div>
<p>
从而
\[
  (e^{tA})^\dagger(J_2g)e^{tA}\le J_2g .
\]
若 \(M_1,M_2\) 都满足这个有限变换不等式，则
</p>
<div class="scroll">\[
  \begin{aligned}
  &(M_1M_2)^\dagger(J_2g)(M_1M_2)-J_2g\\
  &=M_2^\dagger
    [M_1^\dagger(J_2g)M_1-J_2g]M_2\\
  &\quad+[M_2^\dagger(J_2g)M_2-J_2g]\le0 .
  \end{aligned}
\]</div>
<p>
这才是与 note 的 determinant formula 对齐的 contraction semigroup：
每个时间片控制 \(e^{A_\ell}\)，相乘后控制
\(e^{A_1}\cdots e^{A_k}\)。
</p>

<h4>对应的 maximal subgroup 与 invariant cone 也必须分解 \(A\)</h4>
<p>
仍写 \(\eta=J_2g\)。对一个满足费米二次型条件与
\(J_1^TAJ_1=\bar A\) 的 \(A\)，分成
</p>
<div class="scroll">\[
  \begin{aligned}
  A_{\rm subgroup}
  &=\frac12(A-\eta A^\dagger\eta),\\
  A_{\rm cone}
  &=\frac12(A+\eta A^\dagger\eta).
  \end{aligned}
\]</div>
<p>
第一项满足
\[
  \eta A_{\rm subgroup}
  +A_{\rm subgroup}^\dagger\eta=0,
\]
因而 \(e^{A_{\rm subgroup}}\) 保持 \(\eta\)，属于 maximal subgroup。
第二项满足
\[
  \eta A_{\rm cone}=A_{\rm cone}^\dagger\eta .
\]
只有再要求 \(\eta A_{\rm cone}\le0\)，它才是 contraction cone
的方向。由费米条件 \(A^\dagger=-g\bar A g\) 可进一步验证
</p>
<div class="scroll">\[
  \begin{array}{c|c}
  J_2^TAJ_2=\bar A
  &A\ \text{属于 maximal-subgroup 线性空间}\\[2pt]
  J_2^TAJ_2=-\bar A
  &A\ \text{属于 cone 的线性空间}
  \end{array}
\]</div>
<p>
所以后文逐例解 \(J_2^TAJ_2=\pm\bar A\) 这一步本身可以保留；
真正需要改的是最后施加半负定性的 matrix。
</p>

<h4>这项修正怎样改变 Cases \(1'\)--\(10'\) 的读取</h4>
<div class="scroll">
<table>
  <thead><tr>
    <th>case</th><th>按 \(e^A\) 检查的结果</th><th>应怎样理解</th>
  </tr></thead>
  <tbody>
    <tr><td>\(1'\)</td><td>maximal-subgroup 边界</td>
    <td>交换 \(J_1,J_2\) 的名字后，确实是 \(9'\) 的双 symmetry
    特例；第三节对两个 \(J\) 都取正号是相容的。</td></tr>
    <tr><td>\(3',4'\)</td><td>只有等号边界，没有 strict interior</td>
    <td>Majorana reflection positivity 与 time-reversal positivity
    是已知定理，但 note 的 real Nambu matrices 不是把这些定理完整换基后的条件。</td></tr>
    <tr><td>\(5',6',7',8'\)</td><td>存在 strict interior</td>
    <td>这些是直接控制 \(e^A\) 的四个候选类。Case \(5'\)
    末尾的 \(J_2gA\le0\) 方向正确；Cases \(6'\)--\(8'\)
    末尾多写的 \(i\) 应去掉。</td></tr>
    <tr><td>\(9',10'\)</td><td>只有等号边界</td>
    <td>\(J_1\) 把候选半负定方向翻成半正定方向，故不能存在
    nonzero strict cone。第一节把 \(9'\) 标为 Passed
    是沿用了错误的 \(e^{gA}\) 判据。</td></tr>
  </tbody>
</table>
</div>

<h4>\(1'\)：为什么 “just a special case of semigroup Case \(9'\)”</h4>
<p>
Case \(1'\) 有两个 anti-linear transformations。第一个
\(J_1\mathcal K\) 满足 \(J_1^2=-I\)，第二个
\(J_2\mathcal K\) 满足 \(J_2^2=+I\)；二者都翻转 \(g\)，并且对易。
Case \(9'\) 的五条离散关系正好把这两个 \(J\) 的角色交换：
semigroup 中负责第一条实性条件的 \(J_1\) 平方为 \(+I\)，
负责 contraction metric 的 \(J_2\) 平方为 \(-I\)。
</p>
<p>
Case \(9'\) 的正确 \(e^A\)-contraction metric 是
\(\eta=J_2g\)；等号边界为
</p>
<div class="scroll">\[
  J_2gA+A^\dagger J_2g=0
  \quad\Longleftrightarrow\quad
  J_2^TAJ_2=\bar A .
\]</div>
<p>
所以交换 Case \(1'\) 的两个 \(J\) 后，Case \(1'\) 手算中
\[
  J_1^TAJ_1=\bar A,\qquad J_2^TAJ_2=\bar A
\]
正好表示：一个 \(J\) 保证 weight real，另一个 \(J\) 把
propagation 限制在 maximal subgroup。原报告此前说这里必须
“一正一负”是由错误地分解 \(gA\) 得出的，现已纠正。
</p>
<p>
还要注意，\(9'\) 在正确判据下并没有 strict cone；因此
“special case”只能解释双 symmetry 边界，不能替 \(9'\)
增加一个新的无符号 interior。
</p>

<h4>\(2'\)：为什么说费米对应物 “exists but not useful”</h4>
<p>
这一句本身没有给 \(J_1,J_2\)、没有给 \(A\) 的 block form，
也没有给 positivity inequality，所以不能从 note 原文唯一恢复一个
可穷举的 Case。能够确定的是，作者指向 bosonic operator
reflection positivity 的 fermionic analogue。
</p>
<p>
对玻色算符，跨 reflection plane 的项可写成
\[
  \sum_\alpha \lambda_\alpha
  \hat X_\alpha\theta(\hat X_\alpha),\qquad \lambda_\alpha\ge0 .
\]
费米算符也可构造 reflected products，但当 \(\hat X_\alpha\)
含奇数个 fermion operators 时，交换左右两侧的算符次序会产生负号。
因此必须把 fermion parity、固定 phase 与 ordering convention
一起写入 reflection map，不能逐字复制玻色公式。
</p>
<p>
note 没有解释 “not useful”。结合紧接着的 \(3'\)，较可信的历史解释是：
graded fermionic reflection positivity 已经能够改写成 Majorana
reflection positivity，所以它没有提供一个额外的 AFQMC 分类入口。
这是根据上下文作出的解释，不是 note 已完成的证明。若要把 \(2'\)
写进文章，仍需作者明确给出 reflection map、ordering phase 与
“没有用”究竟是指不独立、难以 HS 实现，还是不能扩大模型集合。
</p>

<h4>\(3'\)：Majorana reflection positivity 原本在说什么</h4>
<p>
在原始 Majorana theorem 中，可选
\[
  J_1=\sigma_x\otimes I,\qquad
  J_2=i\sigma_y\otimes I .
\]
\(J_1\mathcal K\) 交换两组 Majorana operators，
\(iJ_2\) 选择跨 reflection plane coupling 的正方向。把 Majorana
operators 分成 \(\gamma^{(1)},\gamma^{(2)}\)，允许的 quadratic form
具有
</p>
<div class="scroll">\[
  \begin{aligned}
  \gamma^T A_{\rm M}\gamma
  ={}&\gamma^{(1)T}B\gamma^{(1)}
  +\gamma^{(2)T}\bar B\gamma^{(2)}\\
  &+2i\,\gamma^{(1)T}C\gamma^{(2)},
  \qquad C=C^\dagger,\quad C\ \text{半正定}.
  \end{aligned}
\]</div>
<p>
前两项互为 reflection partners。把 \(C\) diagonalize 后，最后一项
成为带非负系数的 reflected Majorana pairs 之和。这个 operator cone
对 multiplication 封闭，其 trace 非负；当 \(C=0\) 时，weight
退化为左右两侧互为复共轭所得的 \(|W|^2\)。
这就是 Majorana reflection positivity 的物理与代数内容。参见
<a href="https://arxiv.org/abs/1601.01994">Wei et al.,
Majorana Positivity and the Fermion Sign Problem</a>，以及
<a href="https://arxiv.org/html/1712.09412v3#S5">
semigroup formulation 的 Majorana-RP block form</a>。
</p>
<p>
然而，note 当前的 \(A\) 是 Nambu propagation generator；原始
Majorana theorem 中的 generator 应当是 \(UAU^\dagger\)，不是
\(gA\)。前面的 \(2\times2\) 反例正说明 literal Case \(3'\)
conditions 没有重现这个定理。标签指出了作者的动机，不能代替换基。
</p>

<h4>\(4'\)：time-reversal positivity 比 TR invariance 多了什么</h4>
<p>
Case \(4'\) 想把 \(J_1^2\) 改成 \(-I\)，对应 Kramers time reversal。
对两种 fermion flavors，可写
</p>
<div class="scroll">\[
  T(c_i)=d_i,\qquad T(d_i)=-c_i,\qquad T(i)=-i .
\]</div>
<p>
\(T^2=-1\) 作用在 odd-fermion sector；对 quadratic Hamiltonian
这样的 even operator，两个负号相乘，\(T^2=+1\)。普通
time-reversal invariance 只要求 \(T(\hat h_0)=\hat h_0\)。
time-reversal positivity 还从这些 even operators 中选择一个有方向的
positive cone：annihilation/creation combinations 必须与 Kramers
partner 成对，creation pairs 的相对负号由 fermion ordering 固定。
这个 cone 与 TR-invariant maximal subgroup 相乘后仍封闭，并具有
非负 trace。参见
<a href="https://arxiv.org/html/2510.06226#S2">Wei,
Time-reversal positivity, Sec. II</a>。
</p>
<p>
与 \(3'\) 相同，已知 theorem 使用正确的 Majorana/time-reversal
generator。note 的 Nambu 条件却控制 \(e^{gA}\)，所以 literal
Case \(4'\) 也没有得到该 theorem。其名称说明研究目标，不是证明。
</p>

<h4>\(5'\)--\(10'\) 接下来究竟要检查什么</h4>
<p>
从这一点开始，每个 case 都应按同一顺序读取：
</p>
<ol>
  <li>用 \(gA+A^Tg=0\) 保证它确实表示 fermion quadratic operator；</li>
  <li>用 \(J_1^TAJ_1=\bar A\) 限制 weight 的 complex-conjugation structure；</li>
  <li>用 \(J_2^TAJ_2=+\bar A\) 找 maximal-subgroup 线性空间，
  用负号找 cone 的线性空间；</li>
  <li>最后统一检查
  \(J_2gA+A^\dagger J_2g\le0\)，因为只有它控制 trace 公式中的 \(e^A\)。</li>
</ol>
<p>
按这套一致标准，Cases \(5'\)--\(8'\) 有 strict cone，
Cases \(9',10'\) 只能在 maximal-subgroup boundary。后面逐段讲解会把
note 每一例实际写出的 matrix 与这套正确判据逐项对照，不再用
“possibly has positivity”代替缺失的推导。
</p>
"""


FERMION_PASSED_COMMENT_EXPLANATION = r"""
<p>
方括号 \([J_1,J_2]=0\) 表示对易，花括号
\(\{J_1,J_2\}=0\) 表示反对易。作者的 Comment 是在问：其他四条
\(J,g\) 关系相同时，只改变这一条，strict cone 是否仍然存在。
这个问题必须先指定被收缩的传播矩阵。note 没有保持这一点一致，
所以它的 passed-only 清单需要重审。
</p>
<p>
以 note 顶部实际出现的 \(e^A\) 为准，metric 是
\(\eta=J_2g\)，生成元条件是
\[
  \eta A+A^\dagger\eta\le0 .
\]
完整穷举与解析计算给出：
</p>
<div class="scroll">
<table>
  <thead><tr><th>原 case</th><th>对易关系</th><th>直接 \(e^A\) 结果</th></tr></thead>
  <tbody>
    <tr><td>\(3'\)</td><td>反对易</td><td>只有等号边界</td></tr>
    <tr><td>\(4'\)</td><td>反对易</td><td>只有等号边界</td></tr>
    <tr><td>\(5'\)</td><td>反对易</td><td>存在 strict interior</td></tr>
    <tr><td>\(6'\)</td><td>反对易</td><td>存在 strict interior</td></tr>
    <tr><td>\(7'\)</td><td>对易</td><td>存在 strict interior</td></tr>
    <tr><td>\(8'\)</td><td>对易</td><td>存在 strict interior</td></tr>
    <tr><td>\(9'\)</td><td>对易</td><td>只有等号边界</td></tr>
    <tr><td>\(10'\)</td><td>对易</td><td>只有等号边界</td></tr>
  </tbody>
</table>
</div>
<p>
为什么会这样，可以看 contraction matrix
\[
  H(A)=J_2gA+A^\dagger J_2g .
\]
第一条 anti-linear constraint 会把 \(H(A)\) 变成自己或自己的相反数。
变成自己时可以存在全部本征值为负的 \(H(A)\)；变成相反数时，
\(H(A)\) 的谱必须关于零对称。若又要求 \(H(A)\le0\)，唯一可能就是
\(H(A)=0\)。对易/反对易并非装饰，它与
\(J_1^TgJ_1=\pm g\) 的符号共同决定这两种结果。
</p>
<p>
若改去研究 note 第一节那个控制 \(e^{gA}\) 的式子，反对易的
Majorana classes 会重新出现；但那不是当前 Nambu trace formula
中的传播。两张 passed 清单不能合并。报告后文所称“完整穷举”
统一采用物理传播 \(e^A\)，并把 note 原来的 \(e^{gA}\) 结果单独列为
公式诊断，而不再把它称作 fermionic AFQMC 无符号结论。
</p>
"""


EXPLANATION_OVERRIDES = {
    "fermion-list": FERMION_FRAMEWORK_EXPLANATION,
    "fermion-passed-comment": FERMION_PASSED_COMMENT_EXPLANATION,
}
