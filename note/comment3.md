我看完了你上传的 `main.tex`、`SM.tex` 和两张图。核心判断是：**现在的手稿不是“内容不够”，而是正文承担了太多证明、算法手册和数学附录的功能；PRL版本应该把正文改成一个清晰的物理故事：辅助场表示改变了玻色符号问题的判据，RP/TRS 使权重非负，从而打开 frustrated bosons 的新可计算区域。**

PRL 的正文目标应压到约 3750 words/4 pages 量级，摘要还要控制在 PRL 的短摘要要求内；APS 对 Supplemental Material 的定位也不是“正文装不下的全部东西”，而是“对部分读者有用但不影响理解主结果”的材料。因此正文必须自洽、可读，SM 负责证明和实现细节。APS style guide 也明确说短文不一定需要多层标题，这支持你去掉 subsection，只保留 section 层级。([APS Journals][1]) 你提到的几篇 sign-problem-free QMC Letter 也基本是这个模式：正文提出一个 guiding principle / sufficient condition / physical consequence，技术证明放在 SM；例如 PRL 115, 250601 的摘要就是“guiding principle”，PRL 116, 250601 强调“两条充分条件”，PRL 117, 267002 的 arXiv 记录还明确写过 accepted PRL 版本“moved part of the paper into the Supplemental Material”。([arXiv][2])

## 一、最终正文应讲的“一个故事”

建议把整篇正文压成下面这条主线：

**传统世界线/SSE 的玻色 QMC 符号问题由局域跃迁矩阵元控制，所以几何阻挫通常导致负权重；而在 AFQMC 中，玻色算符被先解析迹掉，Monte Carlo 采样的是辅助场背景下的全局 Gaussian trace。于是符号问题不再由局域 hopping sign 决定，而由每个辅助场构型的单粒子传播矩阵是否具有 RP/TRS 结构决定。由此，某些 frustrated bosonic models 也可以 sign-problem-free。**

正文所有内容都围绕这个故事服务。凡是不能直接帮助读者理解这条线的推导、引理、闭包证明、branch choice、regularization、update ratio、stabilization，都移到 SM。

## 二、建议的新正文结构和篇幅预算

建议正文保留 5 个 section，不要 subsection：

| Section | 建议标题                                        | 目标功能                                                      | 目标篇幅          |
| ------- | ------------------------------------------- | --------------------------------------------------------- | ------------- |
| I       | Introduction                                | 提出问题、物理直觉、本文结果                                            | 650–800 words |
| II      | Bosonic Auxiliary-Field Quantum Monte Carlo | 只给采样权重公式；先 number conserving，再 paired                     | 500–650 words |
| III     | Symmetry Conditions for Nonnegative Weights | 只给 TRS/RP 判据和物理解释                                         | 700–850 words |
| IV      | Frustrated Two-Flavor Bose-Hubbard Model    | 写清模型、为什么 frustrated、为什么 BAFQMC sign-free、Fig. 2 benchmark | 650–800 words |
| V       | Concluding Remarks                          | 合并 Discussion + Summary，讲意义、局限、展望                         | 450–600 words |

现在正文大约 5300 words，display equations 约 67 个；PRL 版本建议压到 **正文 3000–3300 words + 图注 300–450 words + 12–16 个 displayed equations**。Section II 和 III 是压缩重点：现在这两节加起来约 2100 words、52 个 displayed equations；PRL 版本应压到约 1300–1500 words、8–10 个核心公式。

## 三、摘要：必须重写成“结果型摘要”

现在摘要像方法论文摘要：列了 Gaussian trace、Green function、update ratio、pole structure、benchmark 等很多点。PRL 摘要应该只回答三件事：**问题是什么，发现了什么，为什么重要。**

可以直接改成类似下面这个版本，长度约 579 characters，符合短摘要风格：

> Auxiliary-field QMC is usually associated with fermions, while frustrated bosons are regarded as sign-problematic in world-line formulations. We formulate finite-temperature bosonic AFQMC and show that its weights are nonnegative when the Hubbard-Stratonovich propagators obey either Kramers time-reversal symmetry or reflection positivity. The criteria apply to frustrated two-flavor Bose-Hubbard models on the triangular lattice, where benchmark calculations agree with exact diagonalization. The formulation exposes a sign-free bosonic regime inaccessible to local-weight QMC.

注意两点：第一，不要在摘要里说 “derive Green’s function and local-update ratios”，这些是技术支撑，不是 Letter 卖点。第二，除非你补上 paired benchmark 图或数据，否则摘要里不要写 “benchmarks ... for both number-conserving and paired formulations”；可以改成 “including paired formulations” 或只说 number-conserving benchmark。

## 四、Introduction 的改法

当前 Introduction 有一个优点：物理动机是对的；但写得像综述，铺垫太长。建议改成 5–6 段，每段只完成一个任务。

第一段：直接提出玻色 sign problem 的传统直觉。不要从 QMC 的基本定义讲起。可以这样开头：

> For bosons and spins, sign-problem-free QMC is usually associated with a basis in which all local off-diagonal weights are nonnegative. This intuition is powerful, but it also ties the sign problem to world-line or SSE representations. On frustrated lattices, such a local basis often does not exist.

第二段：转折到 AFQMC。核心句应是：

> AFQMC asks a different question: after the interacting problem is decoupled by Hubbard-Stratonovich fields, the quantum degrees of freedom are traced out exactly, and the sign is determined by a global Gaussian trace.

第三段：借用 fermionic AFQMC 的类比，但不要变成文献综述。只说：fermionic case 说明 symmetry of one-body propagators can protect positivity；本文把这个思想推进到 bosons。这里引用你合作者的几篇 Letter。

第四段：指出 bosonic case 的新难点：不是 determinant，而是 inverse determinant / square-root determinant；有 poles；paired case 有 metaplectic branch。这一段只讲物理障碍，不展开证明。

第五段：本文结果。建议用三句话，而不是现在的 “three layers” 长段：

1. formulate finite-temperature BAFQMC;
2. prove two positivity mechanisms: Kramers TRS for number-conserving propagators and RP for general Gaussian propagators including pairing;
3. demonstrate frustrated two-flavor Bose-Hubbard models on triangular lattice.

第六段：解释 Fig. 1。Fig. 1 是有用的，但 caption 和正文都应更直接：**BAFQMC 的 sign-free 区域不是 SSE/WLQMC 区域的子集，而是沿 RP/TRS 方向扩展，尤其包括 frustrated + RP/TRS 的象限。**

删掉当前 Introduction 最后一段 “The rest of the paper...” 这种常规导读。PRL 里可以省。

## 五、Section II：重写成“权重公式节”，不要做推导节

新 Section II 的标题建议：

```latex
\section{Bosonic Auxiliary-Field Quantum Monte Carlo}
```

这一节必须先讲粒子数守恒，再讲粒子数不守恒。建议正文只保留下面 4 组公式。

第一，给出 HS 后的采样形式：

```latex
Z=\int {\cal D}\phi\, P_{\rm aux}(\phi) W(\phi),\qquad
W(\phi)=\mathrm{Tr}\prod_{\ell=1}^{L_\tau} e^{\hat h_\ell(\phi_\ell)} .
```

这就是把 interacting bosons 变成 auxiliary-field ensemble 的入口。不要在正文展开 generic HS contour、continuous/discrete HS、normal-ordering scalar shift 等细节；放 SM。

第二，number-conserving slice：

```latex
\hat h_\ell=\hat{\mathbf a}^\dagger B_\ell(\phi_\ell)\hat{\mathbf a}
+\xi_\ell(\phi_\ell),\qquad
{\cal B}(\phi)=e^{B_1}e^{B_2}\cdots e^{B_{L_\tau}} .
```

第三，number-conserving bosonic trace formula：

```latex
W_{\rm nc}(\phi)
=\exp\!\left(\sum_\ell \xi_\ell\right)
\det\!\left[I-{\cal B}(\phi)\right]^{-1}.
```

这条公式是正文最重要的公式之一。要马上解释物理含义：fermions give (\det(I+{\cal B}))，bosons give the inverse of (I-{\cal B})，因此 bosonic AFQMC 的困难是 poles 而不是 zeros。

第四，再给 paired/general Gaussian extension：

```latex
\hat\chi=(\hat{\mathbf a},\hat{\mathbf a}^\dagger)^T,\qquad
\hat h_\ell=-\frac12 \hat\chi^T\Omega A_\ell \hat\chi+\xi_\ell,
\qquad
{\cal M}=e^{A_1}\cdots e^{A_{L_\tau}},
```

```latex
W_{\rm p}(\phi)
=\exp\!\left(\sum_\ell \xi_\ell\right)
\det\!\left[I-{\cal M}(\phi)\right]^{-1/2}.
```

这之后只保留一句：

> Equal-time correlators follow from (G_\chi=(I-{\cal M})^{-1}\Omega), and all update ratios, branch choices, and stabilization details are given in the Supplemental Material.

当前 Section II 中以下内容应全部移到 SM：

* (\Omega A+A^T\Omega=0) 的完整 Lie algebra 讨论；
* (A) 的 block form 和 (\Delta,\Delta') 的一般形式；
* ([\hat h,\hat\chi]=-A\hat\chi) 的推导；
* coherent-state trace derivation；
* metaplectic branch 的详细解释；
* Green function blocks；
* local-update ratio；
* QR/SVD/symplectic stabilization；
* “scalar (\xi) absorbs normal-ordering constant” 的详细说明。

正文只需要告诉读者：**BAFQMC 采样权重是什么，它为什么不同于 fermionic AFQMC，它的 sign/pole 问题在哪里。**

## 六、Section III：先 TRS，后 RP；只给判据，不给证明

新 Section III 标题：

```latex
\section{Symmetry Conditions for Nonnegative Weights}
```

因为你要先讲粒子数守恒，所以这一节第一部分应是 number-conserving Kramers TRS。不要用 subsection，但可以用段首短语 “First, ...” 和 “Second, ...”。

### 1. Number-conserving TRS 判据

正文保留：

```latex
\Theta=UK,\qquad UU^*=-I,
```

```latex
U^\dagger \overline{B_\ell}U=B_\ell,\qquad \xi_\ell\in\mathbb R .
```

然后给出核心 determinant 解释：

```latex
\det(I-{\cal B})
=
\prod_{\lambda\notin\mathbb R}|1-\lambda|^2
\prod_{r\in\mathbb R}(1-r)^{m_r}\ge 0,
```

并用两三句话解释：nonreal eigenvalues form conjugate pairs；real eigenvalues have even algebraic multiplicity by Kramers degeneracy；therefore determinant is nonnegative and (W_{\rm nc}\ge0) whenever finite。

这就是 PRL 正文需要的全部证明。当前关于 generalized eigenspace、(\Theta v) 线性无关、even multiplicity 的详细证明移到 SM。

建议保留 two-flavor block form，因为它直接服务后面的模型：

```latex
\hat h_\ell=
(\hat{\mathbf b}^\dagger,\hat{\mathbf c}^\dagger)
\begin{pmatrix}
D_\ell & F_\ell\\
-\overline{F_\ell} & \overline{D_\ell}
\end{pmatrix}
\binom{\hat{\mathbf b}}{\hat{\mathbf c}}
+\xi_\ell .
```

但不要展开 (D_\ell,F_\ell) 任意复矩阵的所有数学讨论。正文只说：this form is natural for two-flavor bosons; frustration can be hidden in (D_\ell), while the second flavor is its Kramers partner。

### 2. RP 判据

RP 是 paired/general Gaussian 的关键，但现在正文写得太数学。PRL 正文建议只保留 operator-level sufficient condition：

```latex
\theta(i)=-i,\qquad
\theta(\hat b_i)=\hat c_i,
```

```latex
\hat h_\ell=
\hat q_\ell+\theta(\hat q_\ell)
+\sum_{\mu\nu}K_{\mu\nu}\hat X_{\mu\ell}\theta(\hat X_{\nu\ell})
+\xi_\ell,\qquad
K\succeq0,\quad \xi_\ell\in\mathbb R .
```

然后写物理解释：

> Each factor is a reflected square. Products of reflected squares remain in the reflection-positive cone, and the trace of such an operator is a norm square. Therefore (W(\phi)\ge0).

这句话比当前一整页证明更适合 PRL。cone 的定义、closure proof、Lie-Trotter、semigroup regularization 全部放 SM。Gaussian matrix block form (F\succeq0) 可以留一句，不必给完整矩阵：

> For Gaussian slices this condition reduces to a positive semidefinite reflected coupling block; in particular, it naturally allows anomalous (bc+b^\dagger c^\dagger) terms.

### 3. Section III 末尾必须回到物理图像

Section III 的结尾建议写成：

> The important point is that neither criterion refers to the sign of a local hopping matrix element. Positivity is imposed after HS decoupling, at the level of the one-body imaginary-time propagator. This is why a geometrically frustrated hopping problem can be sign-free in BAFQMC.

这句话是整篇的物理核心，必须清楚。

## 七、Section IV：补完整个 benchmark 故事

新 Section IV 标题建议：

```latex
\section{Frustrated Two-Flavor Bose-Hubbard Model}
```

不要再分 “Sign-problem-free models” 和 “Benchmark results”。这节要一口气讲完：模型、sign-free 原因、数值验证。

### 1. 模型公式应合并并加上 chemical potential

当前模型正文和 Fig. 2 caption 里出现了 (\mu=-2.5)、(\mu=-5)，但模型 Hamiltonian 里没有 (\mu)。这会让读者困惑。建议正文主模型写成：

```latex
\begin{aligned}
\hat H_{\triangle}
=&\, t\sum_{\langle ij\rangle}
(\hat b_i^\dagger\hat b_j+\hat c_i^\dagger\hat c_j+\mathrm{H.c.})
-\mu\sum_i \hat n_{i,+}  \\
&+U_1\sum_i \hat n_{i,+}^2
+U_2\sum_i \hat n_{i,-}^2 ,
\end{aligned}
```

with

```latex
\hat n_{i,\pm}=\hat b_i^\dagger\hat b_i\pm \hat c_i^\dagger\hat c_i,
\qquad U_1\le0,\quad U_2\ge0 .
```

然后解释：(t>0) on triangular lattice is frustrated for local-weight QMC because the hopping sign cannot be removed around every triangular loop. 但 HS 后，(n_+) 用 real field，(n_-) 用 imaginary field，(b) 和 (c) sectors 成为 complex conjugate partners，所以满足 TRS/RP。

不要在正文写两条 HS 积分公式；放 SM。正文只需一句：

> The (U_1) and (U_2) channels are decoupled by real and imaginary onsite fields, respectively, so that the (c)-sector one-body matrix is the complex conjugate of the (b)-sector matrix for every configuration.

这比两条 HS 公式更清楚。

### 2. paired model 的位置要谨慎

当前正文写了 paired benchmark：

```latex
\hat H_{\mathrm{pair}}^{\triangle}
= \hat H_K^\triangle+\hat H_U
-\Delta_p\sum_i(\hat b_i\hat c_i+\hat b_i^\dagger\hat c_i^\dagger).
```

但你说 Fig. 2 现在只有粒子数守恒 benchmark。那正文不要声称已经 benchmark 了 paired formulation，除非你加 paired 数据。建议处理方式二选一：

**方案 A：没有 paired 数据时。** 在 Section III 讲 RP 可处理 pairing，Section IV 只 benchmark number-conserving model。paired Hamiltonian 可以在 Section III 末尾或 SM 作为 “a sign-free paired extension” 提一下，不放进 benchmark 叙事。

**方案 B：准备补 paired 数据。** 把 Fig. 2 改成两行：上排 number-conserving benchmark，下排 paired benchmark；否则摘要和正文都不要写 “both number-conserving and paired benchmarks”。

目前最稳妥的是方案 A。

### 3. Fig. 2 正文必须写出来

Section IV 应加入一段类似下面的文字：

> Figure 2 benchmarks the number-conserving formulation on a (2\times3) triangular cluster against exact diagonalization. We compare the density (n=N_s^{-1}\sum_i\langle n_{i,+}\rangle) and kinetic energy (E_{\rm kin}) over two parameter cuts: varying (U_2) at (U_1=0,\mu=-2.5), and varying (U_1) at (U_2=1,\mu=-5). The BAFQMC data agree with ED within statistical errors over the entire range shown, confirming both the bosonic trace formula and the nonnegative-weight construction.

这里要强调：**图不是为了展示新相图，而是 proof of principle：frustrated lattice + nonnegative BAFQMC + correct observables。**

### 4. Fig. 2 本身需要修改

当前 Fig. 2 信息是有的，但视觉上不够 PRL：

* caption 里的 “BPQMC” 应改成 “BAFQMC”；
* legends 太大、重复太多，建议只保留一个总 legend：lines = ED, open symbols = BAFQMC；颜色表示 (U_1) 或 (U_2)；
* panel c/d 里 “(U_1=-0)” 很奇怪，改成 (U_1=0)；
* (E_{\mathrm{kinetic}}) 改成 (E_{\rm kin})；
* caption 应写清楚 (2\times3) triangular cluster、(t)、(\mu)、(U_1/U_2) cuts；
* Trotter step、sweeps、stabilization、ED boson cutoff、error estimation 放 SM，不要塞进 caption。

Fig. 1 也建议简化：去掉阴影和过多装饰；加明确坐标轴，例如 horizontal axis: “local-weight sign-free / frustrated”，vertical axis: “RP/TRS absent / present”。PRL 图最好少字、少渐变、强信息。

## 八、Section V：合并 Discussion 和 Summary，改成 Concluding Remarks

删除当前空的 Summary and Outlook，把 Discussion 压缩并重写为：

```latex
\section{Concluding Remarks}
```

建议三段。

第一段：总结核心成果。

> We have shown that the bosonic sign problem in AFQMC is governed by symmetries of the HS-decoupled Gaussian propagators rather than by local hopping signs. Kramers TRS protects number-conserving weights, while RP extends the construction to paired propagators.

第二段：讲物理意义。

> This establishes a sign-free route to frustrated bosonic models that are not naturally accessible to world-line or SSE formulations. The triangular two-flavor benchmark is the minimal demonstration.

第三段：讲限制和展望，但不要太长。

> The finite-temperature bosonic weight has poles, so sign-free does not mean numerically effortless. The present formulation is most stable in dilute/moderate-density regimes; developing projector BAFQMC and better pole-regularized sampling is an important next step.

当前 Discussion 中关于 infinite variance、zeros vs poles、nonphysical configurations、density cap 的内容太细。建议保留 “poles are the practical limitation” 这个物理信息；详细讨论放 SM 或 future methods paper。

## 九、具体“保留/移走”清单

### 正文必须保留的公式

1. (Z=\int{\cal D}\phi,P_{\rm aux}W)
2. number-conserving (\hat h_\ell=\hat a^\dagger B_\ell\hat a+\xi_\ell)
3. ({\cal B}=\prod_\ell e^{B_\ell})
4. (W_{\rm nc}=e^{\sum\xi}\det(I-{\cal B})^{-1})
5. paired/Nambu (\hat h_\ell=-\frac12\chi^T\Omega A_\ell\chi+\xi_\ell)
6. (W_{\rm p}=e^{\sum\xi}\det(I-{\cal M})^{-1/2})
7. TRS condition (U^\dagger\bar B_\ell U=B_\ell), (UU^*=-I)
8. determinant positivity factorization
9. RP reflected-square condition
10. triangular-lattice two-flavor Hamiltonian
11. optional paired extension Hamiltonian, only if不声称 benchmark
12. density/kinetic energy definition，必要时只放一条

### 移到 SM 的内容

* bosonic quadratic algebra；
* trace formula derivations；
* branch/metaplectic details；
* cutoff regularization；
* Green function derivation；
* update ratio；
* stabilization；
* RP cone proof；
* semigroup viewpoint；
* Kramers degeneracy proof；
* HS decoupling formulas；
* numerical implementation details for Fig. 2。

SM 现在已有大部分数学内容，但缺一个关键部分：**Numerical details for Fig. 2**。建议新增 SM section，列出 (\Delta\tau)、thermalization sweeps、measurement sweeps、binning/error bars、ED occupation cutoff、chemical potential、boundary condition、stabilization interval、pole/cutoff处理方式。PRL referee 很可能会问这些。

## 十、语言和排版上的具体修正

题目建议改成：

```latex
Sign-Problem-Free Bosonic Auxiliary-Field Quantum Monte Carlo
```

“Auxiliary-Field” 加连字符，更像固定形容词。

正文统一用：

```latex
\dagger
```

不要用 `\hat a^+`。现在 `a^+` 数学上能懂，但物理读者更习惯 (a^\dagger)。

删掉 main 里的 theorem/lemma/proposition 环境。Letter 正文不要出现 theorem 风格；SM 可以保留。

正文里不要说 “as shown in Sec. ... of the SM” 太多次。建议集中一句：

> Derivations of the trace formulas, Green functions, update ratios, and regularized treatment of poles are given in the Supplemental Material.

每个公式后都引用 SM 会打断节奏。

`references.bib` 需要补齐你提到的四篇 Letter/Rapid 参考文献。当前 bib 里有 PRL 116, 250601，但我没有看到 PRB 91, 241117(R)、PRL 115, 250601、PRL 117, 267002 的完整条目；而现有 `wei2015prb` 实际是 PRB 92, 161105，不是你说的 PRB 91, 241117(R)。这个要修正。

最后，正式投稿时不要把 `SM.tex` 直接 `\input{SM.tex}` 到主文末尾作为同一个 PDF 的一部分；可以本地联调时这样做，但提交版应准备独立的 manuscript 和 Supplemental Material 文件。

## 十一、推荐的实际执行顺序

第一步，复制一个 `main_prl.tex`，不要在原稿上直接改。先把所有 `\subsection` 删除，按五个 section 建空架子。

第二步，把当前 Section II 和 III 整段剪到 SM 中对应位置，只从中复制回正文的核心公式。先不润色语言，先完成“搬家”。

第三步，按“number-conserving first, paired second”重写 Section II。完成后检查：这一节不应超过 6 个 displayed equations。

第四步，按“TRS first, RP second”重写 Section III。完成后检查：这一节不应出现 proof-like phrases such as “Indeed,” “To show this,” “Using ... one finds ...” 太多；这些都应在 SM。

第五步，补写 Section IV。先写 number-conserving triangular model和 Fig. 2 文字，不要急着写 paired benchmark。若没有 paired 数据，删掉摘要和正文中 “both formulations benchmarked” 的说法。

第六步，重画/简化 Fig. 2 legend，改 caption；Fig. 1 去装饰化。

第七步，重写 Introduction 和 Concluding Remarks。注意 Introduction 最后一段不要列目录，而是把物理意义说完。

第八步，最后写摘要。摘要一定最后写，因为它应只反映最终正文的主线。

第九步，用 `texcount` 检查正文长度；目标是正文加图注不超过 3500–3700 words，display equations 不超过 16 个。

按照这个方案改完后，文章的定位会从“一个完整数学推导的长方法稿”变成“一个 Letter：提出玻色 AFQMC 的 sign-free symmetry principle，并用 frustrated triangular bosons 做 proof of principle”。这正是你想对标的几篇 sign-problem-free QMC Letter 的写法。

[1]: https://journals.aps.org/authors/length-guide?utm_source=chatgpt.com "Length Limits and Guidelines for Physical Review Article Types"
[2]: https://arxiv.org/abs/1506.05349 "[1506.05349] Split orthogonal group: A guiding principle for sign-problem-free fermionic simulations"
