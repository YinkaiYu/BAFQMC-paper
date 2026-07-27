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

<h4>先区分 Wei 论文的 Majorana 公式与 note 的 Nambu 公式</h4>
<p>
Wei 的 semigroup 论文从 real Majorana basis 出发，写成
\[
  \hat h=\frac14\gamma^T A_{\rm M}\gamma,\qquad
  A_{\rm M}^T=-A_{\rm M},\qquad
  W=\det\!\left(I+\prod_\ell e^{A_{{\rm M},\ell}}\right)^{1/2}.
\]
论文中的 \(J_2^{\rm M}\) 是 real skew-symmetric orthogonal matrix，
所以
\[
  \eta_{\rm M}=iJ_2^{\rm M}
\]
是 Hermitian involution。利用
\(A_{\rm M}^\dagger=-\bar A_{\rm M}\)，论文的 Eq. (3)
</p>
<div class="scroll">\[
  i\left(J_2^{\rm M}A_{\rm M}
  -\bar A_{\rm M}J_2^{\rm M}\right)\le0
\]</div>
<p>
恰好就是
\[
  \eta_{\rm M}A_{\rm M}
  +A_{\rm M}^\dagger\eta_{\rm M}\le0 .
\]
它直接控制 determinant 中的 \(e^{A_{\rm M}}\)，所以
<strong>arXiv:1712.09412 的这一步没有这里所担心的传播元错位</strong>。
参见
<a href="https://arxiv.org/html/1712.09412v3#S4">
该论文的 Eqs. (2)--(3) 及其前面的定义</a>。
</p>
<p>
note 改用
\[
  \hat h=\frac12\chi^TgA\chi,\qquad
  g=\begin{pmatrix}0&I\\I&0\end{pmatrix},
\]
以后，Majorana generator 与 Nambu generator 的关系不是
\(A_{\rm M}=gA\)，而是前面推导的
\[
  A_{\rm M}=UAU^\dagger .
\]
因此 metric 也必须随这个相似变换一起拉回：
</p>
<div class="scroll">\[
  \eta_{\rm N}
  =U^\dagger\eta_{\rm M}U .
\]</div>
<p>
在最简单的 canonical block 中，
\[
  g=\sigma_x,\qquad
  J_2^{\rm M}=i\sigma_y,\qquad
  U=\frac1{\sqrt2}
  \begin{pmatrix}1&1\\-i&i\end{pmatrix}.
\]
直接相乘得到
\[
  \eta_{\rm N}
  =U^\dagger(iJ_2^{\rm M})U
  =\sigma_z .
\]
若沿用 note 的 real matrix \(J_2=i\sigma_y\)，同一个 matrix 又可写成
\[
  \eta_{\rm N}=J_2g=(i\sigma_y)\sigma_x=\sigma_z .
\]
这说明 Wei 论文的 \(iJ_2^{\rm M}\) 在 note 这组 Nambu
记号中变成了 \(J_2g\)，不能只把原来的 \(i\) 留在 \(J_2\) 前面、
再额外插入一个 \(g\)。
</p>

<h4>为什么本组 fermion cases 不能取 \(\eta=iJ_2g\)</h4>
<p>
Cases \(3'\)--\(10'\) 都规定
\(J_2^2=-I\)、\(J_2^TgJ_2=-g\)。由实正交性可逐步推出
</p>
<div class="scroll">\[
  J_2^T=-J_2,\qquad gJ_2=-J_2g,\qquad
  (J_2g)^\dagger=J_2g,\qquad (J_2g)^2=I .
\]</div>
<p>
所以 \(J_2g\) 本身已经是 Hermitian involution；反而
\[
  (iJ_2g)^\dagger=-iJ_2g
\]
是 anti-Hermitian matrix，不能充当 contraction semigroup 所要求的
Hermitian metric。只有在另一支
\(J_2^TgJ_2=g,\ J_2^2=-I\) 中，\(J_2g\) 才是
anti-Hermitian，此时 \(\eta=iJ_2g\) 才正确。note 的
Cases \(3'\)--\(10'\) 全部不在那一支。
</p>

<h4>第一节显示的不等式与顶部的 Nambu trace formula 没有对齐</h4>
<p>
note 第一节写下
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
contraction inequality；但它把 \(gA\) 当作 generator，控制的是
\(e^{t(gA)}\)，不是 note 顶部 trace 公式中的 \(e^{tA}\)。
它保留了 Wei Majorana 公式的 \(iJ_2\)，同时又把 Nambu quadratic
coefficient \(gA\) 直接放进指数；这不是上一段所示的完整
\(A_{\rm M}=UAU^\dagger\) basis transport。因此，更准确的说法不是
“Wei 论文用了错误的矩阵指数”，而是：
<strong>note 第一节把两套 convention 拼在了一起，所得不等式不能直接证明
它自己写下的 Nambu AFQMC weight 非负。</strong>
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
  因此即使 note 的原不等式对 \(gA\) 给出负定矩阵，它仍没有阻止
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
真正需要逐例复核的是最后施加半负定性时，左侧标签与右侧实际乘法
是否一致。
</p>

<h4>具体 cases 的左侧标签与右侧矩阵并不一致</h4>
<p>
后文常用
\[
  J_2=-i\sigma_y\otimes R,\qquad
  g=\sigma_x\otimes I .
\]
按标准 Pauli multiplication，
</p>
<div class="scroll">\[
  J_2g=-\sigma_z\otimes R,\qquad
  iJ_2g=-i\sigma_z\otimes R .
\]</div>
<p>
note 的右侧显示矩阵都是第一种，即 \(J_2g\)，不是第二种
\(iJ_2g\)。逐项对照如下：
</p>
<div class="scroll">
<table>
  <thead><tr>
    <th>case</th><th>左侧原标签</th><th>右侧实际算出的 prefactor</th>
    <th>应怎样读取</th>
  </tr></thead>
  <tbody>
    <tr><td>\(5'\)</td><td>\(J_2gA\)</td>
    <td>\(-\sigma_z\otimes I\)</td>
    <td>左右一致，正是 \(\eta A\)；这里最清楚地写对了 metric。</td></tr>
    <tr><td>\(9'\)</td><td>\(iJ_2gA\)</td>
    <td>\(-\sigma_z\otimes\sigma_x\)</td>
    <td>右侧是 \(J_2gA\)，左侧多了 \(i\)。</td></tr>
    <tr><td>\(10'\)</td><td>\(iJ_2gA\)</td>
    <td>\(-\sigma_z\otimes\sigma_z\)</td>
    <td>右侧是 \(J_2gA\)，左侧多了 \(i\)。</td></tr>
    <tr><td>\(6'\)</td><td>\(iJ_2gA\)</td>
    <td>\(-\sigma_z\otimes\sigma_x\)</td>
    <td>右侧是 \(J_2gA\)，左侧多了 \(i\)。</td></tr>
    <tr><td>\(7'\)</td><td>\(iJ_2gA\)</td>
    <td>\(-\sigma_z\otimes I\)</td>
    <td>右侧是 \(J_2gA\)，左侧多了 \(i\)。</td></tr>
    <tr><td>\(8'\)</td><td>\(iJ_2gA\)</td>
    <td>\(-\sigma_z\otimes\sigma_x\)</td>
    <td>右侧是 \(J_2gA\)，左侧多了 \(i\)。</td></tr>
  </tbody>
</table>
</div>
<p>
因此，后面的手算并没有一致地执行第一节那条
\(iJ_2gA-iA^\dagger J_2g\le0\)。Case \(5'\) 明确使用正确的
Nambu metric；其余五例虽然左侧多写了 \(i\)，右侧 block multiplication
也仍是在算正确的 \(J_2gA\)。这意味着这些 case 的
\(J_2^TAJ_2=\pm\bar A\) 线性分解和右侧 semidefinite test
不应整体作废，只需按 \(\eta=J_2g\) 重新检查允许的生成元中是否存在
\(\eta A+A^\dagger\eta<0\) 的解。
</p>

<h4>这项修正怎样改变 Cases \(1'\)--\(10'\) 的读取</h4>
<div class="scroll">
<table>
  <thead><tr>
    <th>case</th><th>按 \(e^A\) 检查的结果</th><th>应怎样理解</th>
  </tr></thead>
  <tbody>
    <tr><td>\(1'\)</td><td>\(J_2gA+A^\dagger J_2g=0\)</td>
    <td>交换 \(J_1,J_2\) 的名字后，确实是 \(9'\) 的双 symmetry
    特例；第三节对两个 \(J\) 都取正号是相容的。</td></tr>
    <tr><td>\(3',4'\)</td><td>半负定条件只能取等号，不存在负定生成元</td>
    <td>Majorana reflection positivity 与 time-reversal positivity
    是已知定理，但 note 的这两组 real Nambu signs
    不是把这些定理完整换基后的条件。</td></tr>
    <tr><td>\(5',6',7',8'\)</td><td>存在使收缩矩阵负定的生成元</td>
    <td>这些是直接控制 \(e^A\) 的四类。Case \(5'\)
    的标签和计算都正确；Cases \(6'\)--\(8'\) 的左侧标签应去掉
    \(i\)，其右侧实际计算已经是 \(J_2gA\)。
    Wei 的 canonical metric 完整拉回后也使用 \(\eta=J_2g\)，
    并允许收缩矩阵负定；一个 physical model 还可能同时满足其中多个
    \(J_1\) labels。与已知 positivity classes 的具体对应关系取决于
    完整的 basis transformation。</td></tr>
    <tr><td>\(9',10'\)</td><td>任何满足半负定条件的生成元都被迫满足等号</td>
    <td>两例都满足
    \(J_1^T\overline{(J_2gA+A^\dagger J_2g)}J_1
    =-(J_2gA+A^\dagger J_2g)\)。若括号内的矩阵半负定，
    左边也半负定，于是括号内的矩阵同时半正定，只能为零。
    Case \(9'\) 另有负权重反例，所以原 Passed 标签不能保留。</td></tr>
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
还要注意，\(9'\) 在正确判据下并没有满足
\(\eta A+A^\dagger\eta<0\) 的生成元；因此 “special case”
只能解释两条反线性对称性同时成立的等号部分，不能由此增加一组
已经证明权重非负的传播矩阵。
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
\(gA\)。前面的 \(2\times2\) 反例正说明：第一节那条以
\(gA\) 为 generator 的不等式没有重现这个定理。标签指出了作者的
动机，不能代替把 generator、metric 和两个 \(J\) 一起换基。
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
按这套一致标准，Cases \(5'\)--\(8'\) 有负定生成元，
Cases \(9',10'\) 中凡满足半负定条件的生成元都只能满足
\(J_2gA+A^\dagger J_2g=0\)。后面逐段讲解会把
note 每一例实际写出的 matrix 与这套正确判据逐项对照，不再用
“possibly has positivity”代替缺失的推导。
</p>
"""


FERMION_PASSED_COMMENT_EXPLANATION = r"""
<p>
方括号 \([J_1,J_2]=0\) 表示对易，花括号
\(\{J_1,J_2\}=0\) 表示反对易。作者的 Comment 是在问：其他四条
\(J,g\) 关系相同时，只改变这一条，负定生成元是否仍然存在。
下面以 note 开头 trace 公式中实际出现的传播矩阵 \(e^A\) 为准。
本组 Cases \(3'\)--\(10'\) 都有
\[
  J_2^TgJ_2=-g,\qquad J_2^2=-I,
\]
所以正确的 Hermitian metric 是
\[
  \eta=J_2g,\qquad \eta^\dagger=\eta,\qquad \eta^2=I,
\]
而生成元必须满足
\[
  \eta A+A^\dagger\eta\le0.
\]
</p>

<h4>先把 \(J_1\) 对收缩不等式的作用完整算出来</h4>
<p>
每个候选生成元还满足
\[
  J_1^TAJ_1=\bar A .
\]
对此式分别取复共轭和转置，得到后面会用到的两条式子：
</p>
<div class="scroll">\[
  J_1^T\bar A J_1=A,\qquad
  J_1^TA^TJ_1=A^\dagger .
\]</div>
<p>
因为本组的 \(\eta=J_2g\) 是实矩阵，先计算
\(J_1^T\bar\eta J_1=J_1^TJ_2gJ_1\)。四种正负号可以逐项写成
</p>
<div class="scroll">\[
\begin{array}{c|c|c}
J_1^TgJ_1 & J_1J_2\text{ 的关系}
&J_1^T\bar\eta J_1\\ \hline
g &[J_1,J_2]=0
&J_1^TJ_2gJ_1=J_2(J_1^TgJ_1)=+\eta\\
g &\{J_1,J_2\}=0
&J_1^TJ_2gJ_1=-J_2(J_1^TgJ_1)=-\eta\\
-g &[J_1,J_2]=0
&J_1^TJ_2gJ_1=J_2(J_1^TgJ_1)=-\eta\\
-g &\{J_1,J_2\}=0
&J_1^TJ_2gJ_1=-J_2(J_1^TgJ_1)=+\eta .
\end{array}
\]</div>
<p>
现在把这张表代回完整的收缩矩阵，而不是用一句话略过：
</p>
<div class="scroll">\[
\begin{aligned}
J_1^T\overline{\left(\eta A+A^\dagger\eta\right)}J_1
={}&(J_1^T\bar\eta J_1)(J_1^T\bar A J_1)\\
&+(J_1^TA^TJ_1)(J_1^T\bar\eta J_1)\\
={}&
\begin{cases}
\eta A+A^\dagger\eta,
&J_1^T\bar\eta J_1=+\eta,\\
-(\eta A+A^\dagger\eta),
&J_1^T\bar\eta J_1=-\eta.
\end{cases}
\end{aligned}
\]</div>
<p>
第一种结果与半负定条件相容，但它本身还不证明负定解存在；
Octave 会另行解 \(gA+A^Tg=0\) 和 \(J_1^TAJ_1=\bar A\)，并检验
\(\eta A+A^\dagger\eta<0\)。
</p>
<p>
第二种结果为什么迫使等号，可以直接用矩阵不等式证明。若
\[
  \eta A+A^\dagger\eta\le0,
\]
那么复共轭再作正交基变换仍保持半负定，因此
\[
  J_1^T\overline{\left(\eta A+A^\dagger\eta\right)}J_1\le0.
\]
但第二种结果又说左边等于
\(-(\eta A+A^\dagger\eta)\)，所以
\[
  -(\eta A+A^\dagger\eta)\le0
  \quad\Longleftrightarrow\quad
  \eta A+A^\dagger\eta\ge0.
\]
同一个 Hermitian matrix 同时满足 \(\le0\) 和 \(\ge0\)，只能有
\[
  \boxed{\eta A+A^\dagger\eta=0}.
\]
满足这个等式的生成元指数化以后有
\[
  (e^A)^\dagger\eta e^A=\eta,
\]
所以它们属于保持 \(\eta\) 的 maximal subgroup。这里直接使用矩阵
不等式即可，不需要借助“谱关于零对称”这句较难核对的描述。
</p>

<h4>把四种结果逐项代入 Cases \(3'\)--\(10'\)</h4>
<div class="scroll">
<table>
  <thead><tr><th>原 case</th><th>\(J_1^TgJ_1\)</th><th>对易关系</th>
  <th>\(J_1^T\bar\eta J_1\)</th><th>直接 \(e^A\) 结果</th></tr></thead>
  <tbody>
    <tr><td>\(3',4'\)</td><td>\(+g\)</td><td>反对易</td>
    <td>\(-\eta\)</td><td>由上面的两组不等式推出只能取等号</td></tr>
    <tr><td>\(5',6'\)</td><td>\(-g\)</td><td>反对易</td>
    <td>\(+\eta\)</td><td>不等式相容；Octave 找到负定生成元</td></tr>
    <tr><td>\(7',8'\)</td><td>\(+g\)</td><td>对易</td>
    <td>\(+\eta\)</td><td>不等式相容；Octave 找到负定生成元</td></tr>
    <tr><td>\(9',10'\)</td><td>\(-g\)</td><td>对易</td>
    <td>\(-\eta\)</td><td>由上面的两组不等式推出只能取等号</td></tr>
  </tbody>
</table>
</div>
<p>
这里也能直接回答 Comment 的三组比较。\(1'''\) 与 \(5'''\)
分别对应 \(3'\) 与 \(7'\)：前者是“保持 \(g\)+反对易”，只能取等号；
后者是“保持 \(g\)+对易”，允许负定生成元。\(2'''\) 与
\(6'''\) 同理，分别对应 \(4'\) 与 \(8'\)。
</p>
<p>
原文第三组逐字写成 \(3'\) 与 \(7'''\)。这两项不仅改变对易关系，
还把 \(J_1^TgJ_1=g\) 改成 \(-g\)，所以不能只检验
commutator/anti-commutator。若作者本意是
\(3'''\) 与 \(7'''\)，它们分别对应 \(5'\) 与 \(9'\)：
“翻转 \(g\)+反对易”给 \(+\eta\)，而“翻转 \(g\)+对易”给
\(-\eta\)，正好构成受控比较。\(J_1^2=\pm I\) 没有进入上述推导，
所以 \(3',4'\)、\(5',6'\)、\(7',8'\)、\(9',10'\) 各自成对。
</p>
<p>
Wei 论文的 Majorana classes 控制的是
\(e^{A_{\rm M}}\)，其中 \(A_{\rm M}=UAU^\dagger\)，不是
\(e^{gA}\)。完成 metric 与 anti-linear operations 的同一换基后，
canonical Majorana-RP 与 Kramers semigroups 落入上表的
\(J_2g\) 中允许负定生成元的分支；具体是 \(5'\)--\(8'\)
中哪一个或哪几个
labels 取决于 complex-fermion basis 和模型是否具有额外 symmetries。
note 第一节那个单独控制 \(e^{gA}\) 的式子只能作为
检查 note 的 Majorana 与 Nambu 两套 convention 是否一致的式子，
不能与任何一张物理无符号类别清单合并。报告后文所称“完整穷举”
统一采用物理传播 \(e^A\)。
</p>
"""


EXPLANATION_OVERRIDES = {
    "fermion-list": FERMION_FRAMEWORK_EXPLANATION,
    "fermion-passed-comment": FERMION_PASSED_COMMENT_EXPLANATION,
}
