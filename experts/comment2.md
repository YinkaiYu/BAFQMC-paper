你的手稿现在已经有一个很好的 Letter 核心：**BAFQMC 把玻色体系的 sign-free 条件从“局域矩阵元是否受挫”转移到“HS 后一体传播子的全局对称性”上，因此可以进入 frustrated-but-RP/TRS 的新区域**。这个故事在引言和 Fig. 1 里已经出现了，但后面的正文又转回了“证明型论文”的写法：Section II 和 III 把代数、trace formula、Green’s function、update ratio、RP cone、Kramers 证明等都铺在正文里，导致主线被技术细节淹没。PRL 正文核心部分通常要压到约四个期刊页，且 PRL 摘要要求非常短；APS 风格指南也明确说 Supplemental Material 应放“有用但不是理解主结果所必需”的材料，短文章甚至不一定需要复杂层级标题。([APS Journals][1]) ([Cloudinary][2])

下面给你一套可以直接照着执行的重构方案。

## 1. 先确定新的“物理故事线”

整篇正文只讲一个故事：

**世界线/SSE 中，玻色 hopping 的几何受挫通常意味着 sign problem；但在 AFQMC 中，玻色自由度被 trace 掉，权重变成一体传播子的 determinant 或 metaplectic determinant。因此 sign problem 不再由局域 hopping 符号决定，而由 HS 后的一体传播子是否有 Kramers TRS 或 reflection positivity 决定。由此，frustrated bosonic models 可以 sign-problem-free 地模拟。**

这就是正文中每一节都要服务的主线。当前手稿已经在摘要、引言和 Fig. 1 中表达了“frustrated + RP/TRS 是新 computable territory”的思想；引言还把结果分成 formal formula、sign-free mechanisms、triangular-lattice benchmarks 三层。这个三层结构是对的，但在正文中需要改成物理叙事，而不是证明叙事。

建议新的正文结构如下：

```latex
\section{Introduction}
\section{Bosonic AFQMC Formulation}
\section{Symmetry Criteria for Nonnegative Weights}
\section{Frustrated Bose-Hubbard Examples and Benchmarks}
\section{Concluding Remarks}
```

不要再设 `A.`, `B.`, `C.` subsection。每一节内部用自然段推进。Supplemental Material 可以保留 subsection，因为那里承担证明和实现细节。

## 2. 摘要和引言先做“压缩重写”

当前摘要信息量太多，像完整论文摘要，不像 PRL abstract。PRL 摘要 ≤600 characters；APS 风格指南还要求摘要自洽、单段、无 displayed equations、无编号引用。([Cloudinary][2])

你可以把摘要压成类似下面这一版：

> We formulate a sign-problem-free auxiliary-field quantum Monte Carlo method for interacting bosons. After Hubbard-Stratonovich decoupling, the bosonic weight is controlled by the symmetry of the resulting one-body propagators rather than by local hopping signs. We show that Kramers time-reversal symmetry and reflection positivity guarantee nonnegative weights, including paired formulations. This opens exact simulations of frustrated bosonic models, as demonstrated for two-flavor Bose-Hubbard models on the triangular lattice.

这版的重点是：**方法—机制—新 territory—benchmark**。不要在摘要里写 trace formula、Green’s function、local update ratio、pole structure 的全套清单；pole structure 可以最后一句略提，或者只放 concluding remarks。

引言建议压成四段：

第一段：QMC sign problem 是瓶颈；对玻色/自旋体系，world-line/SSE 的直觉是 hopping frustration 造成 sign problem。

第二段：AFQMC 是另一种表示。把玻色算符 trace 掉后，权重由一体传播子决定；费米 AFQMC 的经验说明 sign-free 条件常由 symmetry 而非 local signs 控制。现在玻色体系缺少系统框架。

第三段：本文结果。用一句话列出核心：BAFQMC finite-temperature formulation；number-conserving Kramers TRS criterion；reflection positivity criterion including pairing；frustrated triangular-lattice benchmarks。

第四段：Fig. 1。把 Fig. 1 作为“conceptual map”，强调 upper-left quadrant。当前 Fig. 1 的思想非常适合作为 PRL 图：它把“BAFQMC 的新区域”可视化了。正文中不需要长 roadmap，只需一句 “The technical derivations are given in the Supplemental Material.”

## 3. Section II：只保留 BAFQMC 的核心公式，且先 number-conserving

你当前 Section II 从 Nambu spinor、symplectic algebra、quadratic generator、HS、trace formula、Green’s function、update ratio、stabilization 一路写下来，公式密度过高。正文中真正必须留下的是：**AFQMC 后权重是什么，以及这个权重为什么能用于讨论 sign problem**。

新的 Section II 建议叫：

```latex
\section{Bosonic AFQMC Formulation}
```

段落顺序如下。

第一段：从 HS 后的 configuration ensemble 开始，不要从 symplectic Lie algebra 开始。

保留：

[
Z=\int \mathcal D\phi, P_{\rm aux}(\phi) W(\phi),\qquad
W(\phi)= {\rm Tr},\hat U(\phi).
]

然后一句话解释：对每个 auxiliary-field configuration，(\hat U(\phi)) 是 imaginary time 中一系列 bosonic Gaussian propagators 的乘积。

第二段：**先讲 number-conserving case**。这是你希望调整的主要顺序，也更符合物理读者直觉。

保留：

[
\hat U(\phi)=\prod_{\ell=1}^{L} \exp!\left(\hat{\boldsymbol a}^\dagger B_\ell(\phi)\hat{\boldsymbol a}+\xi_\ell\right),
\qquad
B(\phi)=e^{B_1}e^{B_2}\cdots e^{B_L}.
]

[
W(\phi)=\exp!\left(\sum_\ell \xi_\ell\right)\det[ I-B(\phi)]^{-1}.
]

这一式是 Section II 的主角。你现在 Eq. (21) 已经是这个形式，并且它是后面 TRS criterion 的自然起点。

接着保留一个观测量公式：

[
\langle a_i a_j^\dagger\rangle_\phi=[I-B(\phi)]^{-1}*{ij},\qquad
\langle a_j^\dagger a_i\rangle*\phi=[B(I-B)^{-1}]_{ij}.
]

这一式足够告诉读者：不仅权重能算，observables 也能算。当前正文 Eq. (23)–(25) 的详细 Nambu Green’s function 可以简化到这一步。

第三段：再讲 paired/general case。这里只需引入 Nambu 记号和最终公式，不要推导。

[
\hat\chi=(\hat{\boldsymbol a},\hat{\boldsymbol a}^\dagger)^T,\qquad
M(\phi)=e^{A_1}e^{A_2}\cdots e^{A_L},
]

[
W(\phi)=\exp!\left(\sum_\ell \xi_\ell\right)\det[I-M(\phi)]^{-1/2}.
]

补一句：“The square root is taken on the metaplectic branch fixed by continuity from a convergent region.” 你现在对 branch choice 和 pole 的解释很长，正文留这一句即可；细节已经适合放进 SM。

第四段：一句话指向 SM。

> The derivations of the Gaussian trace formulas, the Nambu Green’s function, local-update ratios, and stabilization issues are given in the Supplemental Material.

这一节应该控制在 **0.7–0.9 PRL 页**，最多 5 个 displayed equations。

明确移动到 SM 的内容：

| 当前正文内容                                                               | 处理                                                      |
| -------------------------------------------------------------------- | ------------------------------------------------------- |
| Eq. (1)–(7) Nambu spinor、symplectic form、general quadratic generator | 移到 SM “Bosonic Gaussian algebra”                        |
| Eq. (10)–(11) Trotter-HS 的一般推导                                       | 正文只保留一句；具体 HS 公式放 examples 或 SM                         |
| Eq. (15)–(17) BCH/linear action proof                                | 移到 SM                                                   |
| Eq. (22)–(25) full Nambu Green’s function                            | 正文保留最简单 number-conserving correlator；full formula 移到 SM |
| Eq. (27)–(31) Metropolis ratio/local update                          | 全部移到 SM                                                 |
| stabilization paragraph                                              | 移到 SM 或最后一句简述                                           |

## 4. Section III：先 TRS，再 RP；每个 criterion 只留“公式 + 物理图像”

新的 Section III 建议叫：

```latex
\section{Symmetry Criteria for Nonnegative Weights}
```

这节的开头不要从 RP 历史讲起。当前 Section III 先讲 RP，又花很多篇幅定义 (K_\theta)、证明闭合性和 trace positivity；这些是数学证明，不适合 PRL 正文。你应该先讲 number-conserving TRS，因为它最贴近上一节的 determinant 公式，也符合你想把粒子数守恒放前面的要求。

### 4.1 先写 number-conserving TRS criterion

正文保留：

[
\Theta=UK,\qquad \Theta^2=-1,
]

以及 slice-level 条件。这里我强烈建议你在重写前检查 Eq. (46) 的复共轭记号。对 antiunitary symmetry，通常应是类似

[
U^\dagger B_\ell^* U=B_\ell
]

或等价写法，而不是单纯 (U^\dagger B_\ell U=B_\ell)。当前手稿中 Eq. (46) 显示为 (U^\dagger B_\ell U=B_\ell)，但后文又用 antiunitary Kramers 配对来推出复共轭本征值成对；这在逻辑上很容易被审稿人抓住。

物理解释只写两三句：

> The antiunitary symmetry pairs every nonreal eigenvalue of (B) with its complex conjugate. Real eigenvalues are Kramers degenerate because (\Theta^2=-1). Hence every potentially negative factor (1-r) occurs an even number of times, and the determinant cannot change sign.

保留 determinant positivity 公式：

[
\det(I-B)=\prod_{\lambda\notin\mathbb R}|1-\lambda|^2
\prod_{r\in\mathbb R}(1-r)^{m_r}\ge 0,
\qquad m_r\ {\rm even}.
]

当前正文已经有这个公式，适合留下；详细 Kramers 证明移到 SM。

### 4.2 再写 RP criterion，作为 paired/non-number-conserving 的更强机制

RP 的正文写法应从物理图像开始：

> Reflection positivity pairs two commuting bosonic algebras, here conveniently represented by two flavors (b) and (c). A reflected square has a nonnegative trace, and products of such slices remain in the positive cone. Therefore the full BAFQMC weight is nonnegative.

保留一个 operator criterion：

[
\hat h_\ell=\hat q_\ell+\theta(\hat q_\ell)
+\sum_{\mu\nu}K_{\mu\nu}\hat X_\mu\theta(\hat X_\nu)+\xi_\ell,
\qquad K\succeq 0,\quad \xi_\ell\in\mathbb R .
]

再保留 Gaussian paired 的实用判据：

[
\hat h_\ell=\hat\chi^T
\begin{pmatrix}
D_\ell & F_\ell\
F_\ell^T & \bar D_\ell
\end{pmatrix}
\hat\chi+\xi_\ell,\qquad F_\ell=F_\ell^\dagger\succeq0 .
]

这是当前 Eq. (42) 的精华，很适合正文。

然后一段话点出关键：

> TRS is the simplest route for number-conserving decouplings; RP is more flexible and naturally accommodates anomalous pairing terms. Both conditions are imposed after HS decoupling, so they are insensitive to whether the original hopping pattern is frustrated in a world-line basis.

这节也控制在 **0.8–1.0 PRL 页**。

明确移动到 SM 的内容：

| 当前正文内容                                       | 处理                    |
| -------------------------------------------- | --------------------- |
| RP 历史综述                                      | 引言或正文中最多一句；其余删        |
| (K_\theta) cone 定义、闭合性证明、trace factorization | 移到 SM                 |
| Lie-Trotter product proof                    | 移到 SM                 |
| semigroup 解释                                 | 移到 SM，正文不出现           |
| Kramers 证明的 generalized eigenspace 细节        | 移到 SM                 |
| 关于 pole regularization 的长说明                  | Section V 简短提及，详细放 SM |

## 5. Section IV：把例子写成“最小工作模型 + Fig. 2 证明它真的能跑”

新的 Section IV 建议叫：

```latex
\section{Frustrated Bose-Hubbard Examples and Benchmarks}
```

这一节要完成三件事：给模型、说明为什么 sign-free、展示 Fig. 2 benchmark。不要再分 “Sign-problem-free models” 和 “Benchmark results”。

### 5.1 模型只保留一个主例子

保留两 flavor 模型：

[
\hat H_K=\hat{\boldsymbol b}^\dagger B\hat{\boldsymbol b}
+\hat{\boldsymbol c}^\dagger B\hat{\boldsymbol c},
]

[
\hat H_U=U_1\sum_i(\hat n_{bi}+\hat n_{ci})^2
+U_2\sum_i(\hat n_{bi}-\hat n_{ci})^2,
\qquad U_1\le0,\quad U_2\ge0.
]

但这里有第二个需要认真检查的地方：如果你要声称 (B) 可以含有 nontrivial Peierls phases，那么在 TRS/RP 结构中 (c) flavor 的 hopping 很可能应当是 (B^*) 或 (\theta(B))，而不是同一个 (B)。当前 Eq. (52) 写两个 flavor 都是 (B)，这对 Fig. 2 的 real triangular hopping 没问题，但对“nontrivial Peierls phases”的广义表述可能不成立。建议二选一：

第一种，保守写法：正文只说 (B) 可以是 triangular-lattice real frustrated hopping，不再说 nontrivial Peierls phases。

第二种，广义写法：把 kinetic term 改成 (b^\dagger B b+c^\dagger B^*c)，并同步修改后续 TRS/RP 表述。

### 5.2 HS decoupling 不要逐式展开

当前 Eq. (55)–(57) 的 HS decoupling 细节太多。正文可以只给 decoupled slice 的结构，或者甚至只说：

> The (U_1) channel is decoupled with a real field coupled symmetrically to the two flavors, while the (U_2) channel is decoupled with an imaginary field coupled with opposite signs. Each time slice then has the reflected form (\hat h_\ell=\hat q_\ell+\theta(\hat q_\ell)) and, equivalently, satisfies the Kramers TRS condition.

如果要保留一式，就保留当前 Eq. (57)；Eq. (55)–(56) 放 SM。当前正文已经说明 Eq. (57) 可写成 (q_\ell+\theta(q_\ell))，也可满足 TRS，因此这个模型同时被 RP 和 TRS 保护。

### 5.3 Fig. 2 必须在正文中讲清楚

你现在 Fig. 2 已经放了 number-conserving benchmark，但正文还没写完，并且 caption 中有 “BPQMC” 的 typo，应改成 “BAFQMC”。

建议正文直接写这一段：

> We benchmark the number-conserving formulation on a (2\times3) triangular cluster with positive nearest-neighbor hopping (t>0), a frustrated sign choice for world-line/SSE simulations. Figure 2 compares BAFQMC with exact diagonalization for the density and kinetic energy. Panels (a,b) vary (\beta) and (U_2) at fixed (U_1=0) and (\mu=-2.5), while panels (c,d) vary (\beta) and (U_1) at fixed (U_2=1) and (\mu=-5). The BAFQMC results agree with ED within statistical errors over the plotted parameter range, validating both the Gaussian weight formula and the symmetry protection of the frustrated simulation.

这段一定要出现在 Fig. 2 前后。否则 Fig. 2 只是“图在那里”，没有服务正文故事。

Caption 建议改成：

> **FIG. 2. Benchmark of sign-free BAFQMC against exact diagonalization for the two-flavor frustrated Bose-Hubbard model on a (2\times3) triangular cluster.** (a,b) Density and kinetic energy versus inverse temperature (\beta) for several (U_2), with (U_1=0) and (\mu=-2.5). (c,d) The same observables for several (U_1), with (U_2=1) and (\mu=-5). Error bars are smaller than the symbol size where not visible.

### 5.4 paired benchmark 的取舍

当前摘要说你有 number-conserving and paired formulations 的 benchmarks，但正文里只看到 Fig. 2 的 number-conserving benchmark；paired part 只是写了 Eq. (64) 的 anomalous term 和 (F=\Delta\tau\Delta_p I/2\succeq0)，后面还留着 “To be finished......”。

这里必须做一个明确取舍：

若 paired data 已经有，建议加一个很小的 Fig. 3，最多两 panel：例如 density / kinetic energy / pair correlator 与 ED 对比，展示 (\Delta_p>0) 时 BAFQMC 仍然 sign-free。正文只需一段。

若 paired data 还没有准备好，就不要在摘要中写 “benchmarks ... for both number-conserving and paired formulations”。可以改成 “We further present a paired sign-free formulation and benchmark the number-conserving case...” 或把 paired numerical data 放 SM。

PRL 正文中不能留下 “To be finished”。这是非常显眼的 unfinished signal。

## 6. Section V：把 Discussion 和 Summary 合并为 “Concluding Remarks”

当前 Discussion 有价值，但写得太长，且 Section VI 是空的。你应该把 Section V 和 VI 合并为：

```latex
\section{Concluding Remarks}
```

建议三段式。

第一段：总结核心成果，不重复公式。

> We have developed a finite-temperature BAFQMC framework in which sign freedom is protected by the symmetry of HS-decoupled one-body propagators. The resulting criteria—Kramers TRS for number-conserving decouplings and RP for more general paired decouplings—show that geometric frustration is not a fundamental obstruction in auxiliary-field language.

第二段：简短讲 pole limitation。当前 Discussion 中关于 bosonic poles、nonphysical configurations、dilute regime、paired case stability的内容很重要，但正文应浓缩。当前手稿写到 number-conserving BAFQMC 在低密度、moderately high temperatures、weak-to-intermediate interactions 更适合；paired case 避免了 number-conserving case 边界处 near-divergent weights，但 density 有上限。这些结论可以保留，但不要展开成四五段。

可写成：

> The price is that bosonic determinants have poles rather than zeros. The finite-temperature algorithm is therefore most stable in dilute or moderately filled regimes and at not-too-low temperatures. Paired RP formulations avoid the sharp pole at the boundary of the physical sector but introduce their own density limitations.

第三段：outlook。

> A natural next step is a projector BAFQMC formulation, which may reduce the finite-temperature pole difficulty and extend the method toward lower temperatures and stronger interactions. The symmetry criteria established here also provide a guide for constructing new frustrated bosonic and spin models accessible to unbiased simulation.

然后删掉空的 Section VI。

## 7. Supplemental Material 重新承担“证明论文”的角色

你的 SM 现在其实已经包含大量应当承接正文删减内容的材料：bosonic quadratic algebra、Gaussian trace formula、Green’s function、update ratio、regularized weight、regularized RP、TRS proof。

建议把 SM 目录调整成和正文对应的顺序：

```latex
I. Bosonic Gaussian algebra and trace formulas
   A. Number-conserving trace formula
   B. Paired trace formula and metaplectic branch

II. Green’s functions, observables, and local updates
   A. Equal-time Green’s function
   B. Fast-update ratio
   C. Stabilization

III. Proof of the time-reversal-symmetry criterion

IV. Reflection positivity for bosonic Gaussian operators
   A. Positive cone and trace positivity
   B. Gaussian slice criterion
   C. Regularized / semigroup formulation

V. Pole structure and regularized weights

VI. Additional numerical details and benchmarks
```

注意正文顺序是 number-conserving first，所以 SM 中也最好先给 number-conserving trace formula，再给 paired formula。这样读者从正文跳到 SM 时不会被顺序打断。

## 8. 需要立即执行的删改清单

把正文中的公式数量压到大约 14–18 个。建议保留：

1. (Z=\int D\phi P_{\rm aux}W)
2. number-conserving (\hat U) and (B)
3. number-conserving (W=\det(I-B)^{-1})
4. number-conserving Green’s function
5. paired (M)
6. paired (W=\det(I-M)^{-1/2})
7. TRS criterion
8. determinant positivity
9. RP operator criterion
10. RP Gaussian block criterion
11. example (H_K)
12. example (H_U)
13. triangular (H_K^\triangle)
14. paired (H_{\rm pair}^\triangle), only if paired formulation remains in main text

正文中删除或移走：

* 所有 BCH 推导；
* (K_\theta) cone 的完整证明；
* Lie-Trotter 证明；
* local update ratio；
* stabilization 细节；
* semigroup 细节；
* long discussion of infinite-variance analogy；
* “The rest of the paper...” 这种长 roadmap；
* 所有 subsection 标题；
* “To be finished......”。

## 9. 最后做一次 correctness/style 检查

在重写之前，建议你专门检查三处数学一致性，因为它们不是单纯风格问题：

第一，TRS 条件 Eq. (46) 是否缺少 complex conjugation。antiunitary symmetry 的矩阵条件应当显式包含 (K) 的作用，否则后面的 complex-conjugate eigenvalue pairing 逻辑不完整。

第二，Eq. (60) 的 block structure。由 Eq. (57) 看，(c) flavor 的 onsite field 是 (b) flavor 的复共轭；若 (B) real，则应类似 ({\rm diag}(D_\ell,\bar D_\ell))，而不是 ({\rm diag}(D_\ell,D_\ell))。当前文本显示为 ({\rm diag}(D_\ell,D_\ell))，需要核对。

第三，若保留 “nontrivial Peierls phases”，two-flavor kinetic term 可能需要 (B) 与 (B^*) 成对，而不是两个 flavor 同取 (B)。若不想展开这点，正文就只讲 Fig. 2 使用的 real triangular hopping。

## 10. 建议的实际工作顺序

第一天先不改句子，只改结构：删掉 subsection，按五个 section 重排，把 Section II/III 中要进 SM 的段落剪出去。第二天重写 Section II 和 III，只留下上述核心公式。第三天补 Section IV 的 Fig. 2 正文和 caption，同时决定 paired benchmark 是否进正文。第四天压缩 Introduction、Abstract 和 Concluding Remarks。最后统一检查符号、TRS 复共轭、BAFQMC/BPQMC typo、公式编号、SM 引用。

最重要的取舍原则是：**正文只回答“为什么这是一个新的 sign-free 机制、它的最小公式是什么、它在哪个 frustrated model 上真的工作”；凡是回答“这个公式如何严格推导、branch 如何定义、update ratio 如何得到、regularization 如何证明”的内容，都放进 Supplemental Material。**

[1]: https://journals.aps.org/prl/authors?utm_source=chatgpt.com "Physical Review Letters - Information for Authors - APS Journals"
[2]: https://res.cloudinary.com/apsphysics/image/upload/v1715884920/aps-journals-style-guide_tnoyln.pdf "APS Journals Style Guide Authors120924.docx"
