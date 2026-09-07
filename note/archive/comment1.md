我看完了你上传的 `main.pdf`。这篇手稿的核心结果是足够像 Letter 的：**把 bosonic sign problem 的判据从“局域 hopping 是否 frustrated”改写为“HS 解耦后的一体传播子是否有 RP/TRS 对称性”**。现在的问题不是结果不够，而是正文把“如何证明”写成了主线，导致“为什么重要、物理图像是什么、它打开了什么新区域”被数学细节淹没。PRL 正文核心部分通常约四个期刊页；APS 也明确提醒 Supplemental Material 不能只是用来规避长度限制，正文必须本身有说服力。([APS Journals][1])

下面这份方案可以直接当作 revision checklist。

---

## 1. 总体重构目标：从“推导型论文”改成“判据型 Letter”

你现在正文其实已经把故事写出来了：AFQMC 中 sign 的来源不是局域矩阵元，而是 HS 后一体传播子的整体代数结构；因此 frustrated bosonic models 只要满足 RP/TRS，就能进入 sign-free BAFQMC 的新区域。你在 Introduction 里已经说到 frustrated models 可在 RP/TRS 下 sign-free，并用 Fig. 1 表示“upper-left quadrant”是本文打开的新区域。 

建议把全文主线压缩成一句话：

> **Geometric frustration is not a no-go theorem for bosonic QMC; it is a limitation of local-weight representations. In auxiliary-field language, the sign is controlled by symmetries of one-body propagators, and RP/TRS gives sign-free frustrated bosonic simulations.**

正文所有内容都要服务于这句话。推导、分支选择、cone 的闭合性、Kramers 证明、semigroup 解释、local update ratio，都应该退到 Supplemental Material；正文只保留读者判断“结果是什么、为什么可信、能算什么模型”的最小公式链条。

---

## 2. 建议的新正文结构与篇幅分配

建议保留 section 标题，但去掉大多数 subsection；PRL 风格可以用短 section 加粗段首标签。

| 新结构                                              |      目标篇幅 | 作用                                                             |
| ------------------------------------------------ | --------: | -------------------------------------------------------------- |
| Abstract                                         |        极短 | 只说 gap、method、two criteria、frustrated benchmark                |
| I. Introduction                                  | 0.7–0.9 页 | 建立“world-line/SSE frustration vs AFQMC symmetry”的物理故事          |
| II. Bosonic AFQMC weights                        | 0.6–0.8 页 | 先粒子数守恒，再 paired；只给 weight 和 Green function                     |
| III. Symmetry criteria for nonnegative weights   | 0.9–1.1 页 | 先 TRS/number-conserving，再 RP/paired；只给 theorem statement 和物理解释 |
| IV. Frustrated Bose-Hubbard models and benchmark | 0.8–1.0 页 | 给模型、说明为什么 WL/SSE frustrated 但 BAFQMC sign-free、解释 Fig. 2       |
| V. Concluding remarks                            | 0.3–0.5 页 | 合并 Discussion/Summary：意义、pole limitation、projector outlook     |

两张图最多。Fig. 1 很适合讲“新 territory”，但应缩小到 single-column cartoon；Fig. 2 是结果图，应保留。若版面紧张，可以把 Fig. 1 压成 Fig. 2 的 inset，或者把 Fig. 1 移到 SM，在 Introduction 用一句话描述。

---

## 3. Abstract：重写成“PRL 摘要”，不要列技术清单

当前摘要列了 Gaussian trace formula、Green function、local-update ratios、paired formulation、pole structure、benchmarks 等很多内容，读起来像长文摘要。PRL 摘要应突出一个中心发现：**bosonic AFQMC 的 sign-free 判据**。

建议英文草稿：

> Auxiliary-field quantum Monte Carlo is controlled by symmetries of one-body propagators, but a sign-free bosonic framework has been lacking. We formulate finite-temperature bosonic AFQMC and prove nonnegative weights from Kramers time-reversal symmetry in the number-conserving sector and from reflection positivity, including paired fields. This makes frustrated two-flavor Bose-Hubbard models sign-free in auxiliary-field language. Triangular-cluster benchmarks agree with exact diagonalization and reveal the pole-limited regime.

如果 Fig. 2 目前只展示了粒子数守恒 benchmark，就不要在摘要里写 “for both number-conserving and paired formulations, where BAFQMC agrees with exact diagonalization”。当前正文也显示 paired benchmark 还没有写完，而 Fig. 2 caption 只对应 number-conserving benchmark。 建议二选一：要么补 paired benchmark 到 SM 或主图，要么把摘要和 Introduction 里的 paired benchmark claim 改成“paired sign-free model class”。

---

## 4. Introduction：保留故事，压缩背景

Introduction 现在最强的部分是：先说 bosonic/spin QMC 的传统 sign-free 边界来自 world-line/SSE 的局域权重，再说 AFQMC 先 trace out quantum operators，sign 由全局一体传播子的对称性控制。这个故事应该保留。

建议改成四段：

第一段：**传统图像。**
“在 world-line/SSE 中，frustration 通常导致负局域权重；因此 frustrated bosons 被认为难以 sign-free 模拟。”

第二段：**转折。**
“AFQMC 不 sample 局域路径，而是 sample HS field 后的全局 Gaussian trace。Fermionic AFQMC 已经说明 sign 由一体传播子的 symmetry 控制。”

第三段：**gap。**
“Bosonic analog missing，因为 bosonic Gaussian trace 有 pole、paired terms 有 metaplectic branch，需要新的 positivity criteria。”

第四段：**本文结果。**
用三句话说：

1. 建立 finite-temperature BAFQMC weight formulas。
2. 证明两条 nonnegative-weight routes：TRS for number-conserving, RP for paired/general Gaussian slices。
3. 给 frustrated triangular two-flavor Bose-Hubbard benchmark，说明它位于 Fig. 1 的新区域。

需要删掉或压缩的内容：一般 QMC 的定义、“polynomial in system size”的泛泛介绍、过长的 sign problem 背景。PRL 读者知道这些；你的新意是“frustration is representation-dependent”。

---

## 5. Section II：从头重写，不要逐行压缩

现在 Section II 从 Nambu spinor、symplectic Lie algebra、block form、HS、trace formula、Green function、local update、stabilization一路展开，公式非常密。正文甚至给出了 full Nambu generator、symplectic condition、normal-ordering scalar shift 等细节。 这些都适合 SM，不适合 Letter 主文。

新的 Section II 应按你说的顺序反过来：**先粒子数守恒，再粒子数不守恒/paired**。

### II 的正文保留公式建议

**Number-conserving BAFQMC.—**
先给最简单、最容易被理论物理读者接受的版本：

[
Z=\int D\phi, P_{\rm aux}(\phi), W(\phi),
\qquad
W(\phi)=\mathrm{Tr}\prod_{\ell=1}^{L_\tau} e^{\hat h_\ell(\phi_\ell)} .
]

若每个 slice 保守粒子数，

[
\hat h_\ell=\hat{\boldsymbol a}^\dagger B_\ell(\phi_\ell)\hat{\boldsymbol a}+\xi_\ell ,
\qquad
\mathcal B(\phi)=e^{B_1}e^{B_2}\cdots e^{B_{L_\tau}},
]

则

[
W_N(\phi)=
e^{\sum_\ell \xi_\ell}\det[I-\mathcal B(\phi)]^{-1}.
]

这一条是 Section II 的第一核心公式。你现在正文中 Eq. (21) 已经有它，并且也说这是 time-reversal-symmetry criterion 的自然起点。 建议把它提前，作为读者进入文章的第一扇门。

再给一个 observable 公式即可：

[
\langle \hat a_i^\dagger \hat a_j\rangle_\phi
=============================================

[\mathcal B(I-\mathcal B)^{-1}]_{ji}.
]

不要在正文保留完整 block Green function 解释、Wick theorem 展开、local update ratio；这些移入 SM。你现在 Eq. (22)–(31) 的 Green function、Metropolis ratio、stabilization 说明都属于 implementation detail。

**Paired / non-number-conserving BAFQMC.—**
然后说：允许 anomalous terms 时，粒子数不守恒，需要 Nambu space。只保留：

[
\hat\chi=(\hat{\boldsymbol a},\hat{\boldsymbol a}^\dagger)^T,\qquad
\hat\chi,\hat U(\phi)=\hat U(\phi),M(\phi)\hat\chi,
]

[
W_P(\phi)=
e^{\sum_\ell \xi_\ell}
\det[I-M(\phi)]^{-1/2},
\qquad
G(\phi)=[I-M(\phi)]^{-1}\Omega .
]

你现在 Eq. (18) 和 Eq. (23) 已经是这个内容。 正文只需一句话解释：square root 不是 principal branch，而是从稳定可收敛区域连续延拓得到的 metaplectic branch；详细推导和 branch choice 放 SM。你的 SM 已经有 branch choice 的解释。

### II 中应该移到 SM 的内容

* 当前 Eq. (1)–(7) 的完整 symplectic Lie algebra 表述；
* HS transformation 的连续/离散 contour 细节，只在主文保留一句；
* Eq. (15)–(17) 的 BCH 推导；
* Eq. (22)–(31) 的 Green-function block、local update ratio、low-rank update；
* stabilization 讨论。

一个可执行原则：**正文 II 不超过 6 个 displayed equations**。超过这个数，读者会再次进入“数学附录模式”。

---

## 6. Section III：把“证明”改成“两个物理判据”

当前 Section III 的开头其实很适合保留：它明确说 BAFQMC sign 不由局域矩阵元控制，而由 HS 后 Gaussian propagators 的代数结构控制；并指出 RP naturally allows pairing，TRS gives determinant criterion in the number-conserving case。 但后面 cone 定义、闭合性、trace 非负证明、Trotter product、semigroup 解释过长，应移入 SM。

新的 Section III 也要按顺序反过来：**先粒子数守恒 TRS，再 paired/RP**。

### III.A Number-conserving TRS criterion

主文只写 theorem statement 和物理解释：

[
\Theta=UK,\qquad \Theta^2=-1,
]

若每个 number-conserving slice 满足

[
\Theta B_\ell \Theta^{-1}=B_\ell
\quad
\text{or equivalently}\quad
U^\dagger B_\ell^* U=B_\ell ,
]

则

[
W_N(\phi)=e^{\sum_\ell \xi_\ell}\det[I-\mathcal B(\phi)]^{-1}\ge 0 .
]

物理解释一句话就够：

> Kramers TRS pairs complex eigenvalues of (\mathcal B); real eigenvalues have even multiplicity, so every potentially negative factor in (\det(I-\mathcal B)) appears twice.

你当前正文已经有这个证明的长版本：非实本征值成共轭对，实本征值由于 (\Theta^2=-1) 具有偶重数，因此 determinant 非负。 主文保留这句话，完整 generalized-eigenspace proof 放 SM。

特别建议你检查当前 Eq. (51)/(60) 的复共轭记号。由 Eq. (57) 可见 (b) 与 (c) 两个 flavor 的 HS 势应为 complex-conjugate partners；因此 two-flavor block form 更自然写成类似

[
B_\ell=
\begin{pmatrix}
D_\ell & F_\ell\
-F_\ell^* & D_\ell^*
\end{pmatrix},
]

而不是两个完全相同的 (D_\ell) block。当前 PDF/OCR 中 Eq. (60) 看起来像 (\mathrm{diag}(D_\ell,D_\ell))，这会让读者困惑。请在 LaTeX 源文件里确认 bar/star 是否丢失。

### III.B Reflection positivity criterion

RP 的正文不要从 axiomatic QFT 历史讲起。现在 RP 历史引用占了不少空间。 改成一句：

> The second mechanism is reflection positivity, which turns the bosonic trace into a sum of reflected norm squares.

然后给 operator-level sufficient condition：

[
\hat h_\ell
===========

\hat q_\ell+\theta(\hat q_\ell)
+\sum_{\mu\nu}K_{\mu\nu}^{(\ell)}
\hat X_{\mu,\ell}\theta(\hat X_{\nu,\ell})
+\xi_\ell ,
\qquad
K^{(\ell)}\succeq0,\ \xi_\ell\in\mathbb R .
]

结论：

[
e^{\hat h_\ell}\in e^{\xi_\ell}\mathcal K_\theta,
\qquad
W(\phi)=\mathrm{Tr}\prod_\ell e^{\hat h_\ell}\ge0 .
]

再给 Gaussian specialization：

[
\hat h_\ell=
\hat\chi^T
\begin{pmatrix}
D_\ell & F_\ell\
F_\ell^T & \bar D_\ell
\end{pmatrix}
\hat\chi+\xi_\ell,
\qquad
F_\ell=F_\ell^\dagger\succeq0 .
]

你现在正文已经给了这个 Gaussian RP test，并指出它允许 frustrated lattice，因为 frustrated hopping 可以藏在 (D) 中，而正性只要求 reflected coupling (F\succeq0)。 这正是主文最该强调的物理图像。

### III 中应该移到 SM 的内容

* (K_\theta) cone 的完整定义、加法/乘法闭合证明；
* (\mathrm{Tr},R\theta(R)=|\mathrm{Tr}R|^2) 的证明；
* Lie-Trotter product proof；
* semigroup formulation；
* regularized RP proof；
* Kramers generalized eigenspace proof。

主文只保留两个“盒装判据”：TRS determinant criterion 和 RP cone criterion。它们是你的核心结果，不能移走；证明可以移走。

---

## 7. Section IV：补成真正的“应用结果”部分

现在 Section IV 已经有模型类：two-flavor bosonic lattice model，(H_K)、(H_U)，并指出当 (B) 含 frustrated hopping 时，该模型处于 local-weight methods 困难但 BAFQMC 可处理的区域。 这部分方向对，但写法仍偏证明，需要改成“一个显式例子 + 一个数值检验”。

### IV.A 模型段落

保留最小 Hamiltonian：

[
\hat H_K=
\hat{\boldsymbol b}^\dagger T\hat{\boldsymbol b}
+
\hat{\boldsymbol c}^\dagger T^*\hat{\boldsymbol c}
-\mu\sum_i(\hat n_{bi}+\hat n_{ci}),
]

[
\hat H_U=
U_1\sum_i(\hat n_{bi}+\hat n_{ci})^2
+
U_2\sum_i(\hat n_{bi}-\hat n_{ci})^2 ,
\qquad U_1\le0,\ U_2\ge0 .
]

建议把 hopping matrix 从 (B) 改名为 (T) 或 (K)。现在正文里 (B) 同时表示 hopping matrix 和 single-particle propagator product，很容易混淆。Letter 中符号必须省脑力。

然后用两句话解释 HS 后为什么 sign-free：

> The (U_1) channel generates identical real scalar potentials for the two flavors, while the (U_2) channel generates opposite imaginary potentials. Thus the two flavors see complex-conjugate one-body Hamiltonians and form a Kramers pair. The same decoupled slices can also be written as (q+\theta(q)), giving the RP interpretation.

你现在正文已经写了 Eq. (57) 后的这两条证明，但它太长。 主文只保留这两句话，HS 公式放 SM。

### IV.B Frustrated triangular benchmark

当前 Fig. 2 caption 说明你已经比较了 2×3 triangular cluster 上 BAFQMC/BPQMC 与 ED 的 density 和 kinetic energy：panels (a,b) 扫 (\beta,U_2)，固定 (\mu=-2.5,U_1=0)；panels (c,d) 扫 (\beta,U_1)，固定 (\mu=-5,U_2=1)。 正文应补一个紧凑段落：

> Figure 2 benchmarks the number-conserving algorithm on a (2\times3) triangular cluster, where exact diagonalization is available. We choose positive nearest-neighbor hopping (t>0), which is frustrated in a world-line/SSE representation on the nonbipartite triangular lattice, but remains sign-free here because the two HS-decoupled flavors are related by Kramers TRS and RP. Across the tested (U_2), (U_1), and (\beta) ranges, BAFQMC reproduces ED results for both the density and kinetic energy within statistical errors. This confirms that the determinant weight and symmetry criteria produce an exact, sign-problem-free sampling of a frustrated bosonic model.

这里要避免过度解释曲线，只要说 agreement。PRL 读者需要看到“它真的能算一个 frustrated case”。

### Fig. 2 必改项

1. Caption 里 “BPQMC” 很可能应改为 “BAFQMC”。
2. Caption 加上 (t=1)、(\Delta\tau)、boundary condition、MC sweeps/statistical error、ED occupation cutoff 或 Hilbert-space truncation。Boson ED 若没有 cutoff 说明，referee 一定会问。
3. 图中 panel label 和 legend 太小的话要重画；PRL 双栏压缩后可读性很重要。
4. 如果主文仍声称 paired formulation benchmark，也必须加 paired data。否则把相关 claim 改成 “paired model class is sign-free by RP”，paired numerical benchmark 放到后续工作或 SM。

### Paired model 段落

当前 paired benchmark 部分写了 onsite anomalous term，并说它贡献正的 inter-half block (F\succeq0)，所以 slice remains reflection-positive。 这很好，但不要叫 benchmark，除非有图。建议写成：

> The RP criterion also immediately covers non-number-conserving extensions. Adding (-\Delta_p\sum_i(\hat b_i\hat c_i+\hat b_i^\dagger\hat c_i^\dagger)) turns on a positive reflected pairing block (F\propto \Delta_p I), so the BAFQMC weight remains nonnegative. This illustrates why RP is more general than the number-conserving TRS determinant criterion.

这段 5–6 行即可。

---

## 8. Section V：把 Discussion 和 Summary 合并成 Concluding remarks

当前 Discussion 写得很重要，但太长：它详细讨论 pole、nonphysical configurations、低温/强相互作用时权重接近 pole、paired case 稳定性、projector QMC outlook。 这些内容需要压成三段，细节进 SM。现在 Section VI 是空的，应删除。

建议新 Section V 结构：

第一段：**意义。**
“本文建立 bosonic AFQMC 的 sign-free symmetry framework；frustrated 不再等价于 sign problem；Fig. 1 upper-left quadrant 是新 computable territory。”

第二段：**限制。**
“Sign-free does not mean numerically effortless。Bosonic determinant has poles (\det(I-\mathcal B)=0)，所以 finite-temperature algorithm 最适合 dilute/moderate density、moderate temperature、weak-to-intermediate interactions。Regularized interpretation and pole diagnostics are in SM。”

第三段：**展望。**
“Projector BAFQMC 是自然下一步，可能绕开 finite-temperature pole structure，并将方法推向低温/强耦合 frustrated bosons。”

不要在主文中展开“nonphysical configurations may suggest negative occupation numbers”这种细节；这容易让非专家读者怀疑算法物理性。主文可以说 “regularized auxiliary-field configurations near pole surfaces require care”，然后把详细解释放 SM。

---

## 9. Supplemental Material 的重组方案

你的 SM 已经包含 algebra、trace formula、Green function/update ratio、regularization、semigroup RP、TRS proof。 现在要把正文移出的内容系统放进去，并补 benchmark details。

建议 SM 目录改成：

1. **Bosonic Gaussian algebra and trace formulas**

   * symplectic Lie algebra
   * normal ordering scalar (\xi)
   * number-conserving coherent-state derivation
   * paired/metaplectic branch derivation

2. **Green functions, observables, and update ratios**

   * equal-time Green function
   * local update determinant ratio
   * stabilization notes

3. **Proof of reflection positivity**

   * reflection cone
   * trace positivity
   * Gaussian RP test
   * semigroup/regularized RP

4. **Proof of the Kramers TRS criterion**

   * generalized eigenspace proof
   * determinant nonnegativity

5. **Regularized bosonic weights and pole structure**

   * Gaussian cutoff
   * physical vs auxiliary-field configurations
   * practical diagnostics

6. **Model and benchmark details**

   * HS decoupling for (U_1,U_2)
   * triangular lattice geometry
   * ED cutoff
   * MC parameters
   * additional scans
   * paired data, if available

这样 SM 不是“正文删下来的碎片”，而是一个可审阅的技术支撑文件。

---

## 10. 公式取舍清单

建议正文最多保留这些公式：

1. (Z=\int D\phi,P_{\rm aux}W), (W=\mathrm{Tr},\hat U_\phi)
2. number-conserving slice 和 (\mathcal B_\phi)
3. (W_N=e^{\sum\xi}/\det(I-\mathcal B))
4. number-conserving Green function
5. paired (W_P=e^{\sum\xi}\det(I-M)^{-1/2})
6. paired (G=(I-M)^{-1}\Omega)
7. TRS condition (\Theta^2=-1), (\Theta B_\ell\Theta^{-1}=B_\ell)
8. RP sufficient condition (q+\theta(q)+XK\theta(X)), (K\succeq0)
9. Gaussian RP block (F\succeq0)
10. frustrated two-flavor Bose-Hubbard Hamiltonian
11. paired extension Hamiltonian, if retained

其它都进 SM。特别是当前 Eq. (26)–(31) 的 local update ratio 不应在 PRL 主文出现；它对实现重要，但不是 Letter 的核心 physics result。

---

## 11. 语言风格的具体改法

现在很多句子是“mathematical proof mode”。建议改成“claim + physical image + formula”的顺序。

例如，当前写法偏向：

> We define a cone (K_\theta). It is closed under addition and multiplication. Therefore ...

Letter 写法应变成：

> Reflection positivity makes each Gaussian slice a reflected square. Since left and right bosonic algebras commute, products of such slices remain reflected squares, and their traces are nonnegative.

然后再给一行公式。

TRS 部分同理。不要先讲 generalized eigenspace；先讲：

> The two boson flavors form a Kramers pair. A negative determinant factor can only appear twice.

然后给 determinant 公式或一句 proof sketch。

---

## 12. 一些必须检查的技术/排版一致性问题

1. **BAFQMC vs BPQMC**：Fig. 2 caption 目前写 “BPQMC”，全文应统一。
2. **(B) 的重名问题**：(B) 同时用作 hopping matrix 和 single-particle propagator product，建议改 hopping 为 (T)，propagator product 为 (\mathcal B)。
3. **TRS block 复共轭**：检查 Eq. (51)、Eq. (60) 是否丢了 bar/star。由 Eq. (57) 看，两个 flavor 应看到 conjugate potentials。
4. **paired benchmark claim**：没有 paired data 就不要在摘要和 Introduction 声称 benchmark 包含 paired formulation。
5. **Fig. 2 benchmark 信息**：补 MC 参数和 ED cutoff。
6. **Section VI**：删除空的 Summary and Outlook；保留 Acknowledgments。
7. **正文引用 SM 的方式**：不要每个公式都说“shown in SM”；只在段末说 “Derivations and update formulas are given in SM”。
8. **不要过度强调局限**：pole structure 必须诚实讲，但不要让 Conclusion 变成 warning section。主线仍应是“new exact-simulation territory”。

---

## 13. 推荐的实际修改顺序

第一步，不要在原文上逐句改。新建一个 PRL skeleton，只把必须公式复制过去。

第二步，先写新版 Abstract 和 Introduction。把“geometric frustration is not a no-go theorem in auxiliary-field language”作为唯一中心句。

第三步，重写 Section II，先 number-conserving determinant，再 paired metaplectic determinant。写完后检查：一个非专门做 symplectic algebra 的 condensed matter theorist 是否能在 5 分钟内读懂。

第四步，重写 Section III，只保留两个 theorem boxes：TRS 和 RP。每个 theorem 后加一句物理图像。

第五步，补 Section IV benchmark 段落，修 Fig. 2 caption。把 paired 部分写成 sign-free extension，而不是未完成 benchmark。

第六步，把 Discussion 压缩成 Concluding remarks 三段，其余 pole 细节移入 SM。

第七步，最后再清理 SM。SM 的目标不是越长越好，而是让 referee 在质疑某一步时能快速找到证明。

---

## 14. 最终正文应给读者留下的印象

读完主文后，理论物理读者应该只记住三件事：

1. **BAFQMC 的 bosonic weight 是 (\det(I-\mathcal B)^{-1}) 或 paired 情形的 (\det(I-M)^{-1/2})，所以 sign/pole structure 与 fermions 不同。**
2. **只要 HS 后的一体传播子满足 Kramers TRS 或 RP，权重非负；frustration 可以存在于一体 hopping 中，不再自动导致 sign problem。**
3. **一个 triangular-lattice two-flavor Bose-Hubbard benchmark 已经验证了这个框架。**

这三点比完整证明更适合 PRL 正文。证明必须存在，但应该在 SM 中支撑主文，而不是替代主文的故事。

[1]: https://journals.aps.org/prl/authors?utm_source=chatgpt.com "Physical Review Letters - Information for Authors - APS Journals"
