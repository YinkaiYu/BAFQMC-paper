# 含配对 Gaussian 权重的解析延拓反例

这份说明独立于本轮正文与补充材料的结构修改。按照本轮作者决定，文章暂时保留既定的 TRS/RP 论断，反例及其对适用范围的影响留待下一轮处理。下面区分已经直接核实的结论与尚待研究的问题。

**已确认的核心问题：从收敛算符迹得到的配对 Gaussian 权重，解析延拓后可以有限且为负，即使切片同时满足目前写下的 Majorana TRS 和 RP 代数条件。** 因而“只要远离行列式极点就保证正性”不能直接由收敛域中的证明推出。这不是数值误差，也不能通过随意选取正平方根消除。

## 1. 一个两模、单切片的例子

取两个普通玻色模，令

$$
\hat h=-x(\hat n_b+\hat n_c+1)
       +\kappa(\hat b^+\hat c^++\hat b\hat c),
\qquad x,\kappa>0.
$$

这里的参数已经包含时间步长，均为无量纲数。一个切片已经足以检验正性定理，无需引入相互作用、格子或 Monte Carlo 采样。常数项取为 −x，使整个算符恰好是中心化的二次型，没有遗漏的 normal-ordering 标量。

沿用文章的记号，

$$
\hat\chi=(\hat b,\hat c,\hat b^+,\hat c^+)^{\mathsf T},
\qquad
\Omega=\begin{pmatrix}0&I_2\\-I_2&0\end{pmatrix},
\qquad
C=\begin{pmatrix}0&I_2\\I_2&0\end{pmatrix},
$$

$$
\hat h=-\frac12\hat\chi^{\mathsf T}\Omega A\hat\chi,
\qquad
A=\begin{pmatrix}
       -xI_2&\kappa\sigma_x\\
       -\kappa\sigma_x&xI_2
   \end{pmatrix},
\qquad \xi=0.
$$

直接相乘可得

$$
A^{\mathsf T}\Omega+\Omega A=0,
\qquad A^2=(x^2-\kappa^2)I_4.
$$

## 2. 它确实满足目前的 TRS 和 RP 条件

在文章的反线性算符映射约定下，取

$$
\Theta_+=U_+\mathcal K,\qquad
\Theta_-=U_-\mathcal K,\qquad
U_+=I_4,\qquad
U_-=\begin{pmatrix}-\sigma_y&0\\0&\sigma_y\end{pmatrix}.
$$

两个矩阵都满足

$$
U_a^{\mathsf T}\Omega U_a=\Omega,\qquad
C\overline U_aC=U_a,\qquad
\overline A U_a=U_aA.
$$

前三个等式分别检验 canonical commutators、Hermitian conjugation 和切片不变性；它们对所有实 x、κ 都成立。此外，

$$
\overline U_+U_+=I_4,\qquad
\overline U_-U_-=-I_4,\qquad
\overline U_-U_+=-\overline U_+U_-.
$$

因此这确实是一个满足两两反对易条件的 {+,−} 集合，不是遗漏了“物理 TRS”条件的形式矩阵例子。

RP 条件也可以在算符层面直接读出。令 θ 把 b 反线性地映射为 c，并取

$$
\hat q=-x(\hat n_b+\tfrac12).
$$

则

$$
\hat h=\hat q+\theta(\hat q)
 +\kappa\hat b\,\theta(\hat b)
 +\kappa\hat b^+\,\theta(\hat b^+).
$$

两个反射耦合的系数均为正。在正文的对称分块写法中，这对应于 F=(κ/2)I₂；因混合块在二次型中出现两次，不能误写为 κI₂。由此可见，这个例子同时涉及配对 TRS 和 RP 的延拓主张。

## 3. 先在收敛区准确计算算符迹

设 x>κ，并记

$$
\omega=\sqrt{x^2-\kappa^2}>0.
$$

先作普通模变换

$$
\hat d_\pm=\frac{\hat b\pm\hat c}{\sqrt2}.
$$

两个模完全分离：

$$
\hat h=\hat h_++\hat h_-,
\qquad
\hat h_\pm=-x(\hat d_\pm^+\hat d_\pm+\tfrac12)
 \pm\frac{\kappa}{2}(\hat d_\pm^{+2}+\hat d_\pm^2).
$$

选择实 r 满足 tanh(2r)=κ/x，再作 canonical Bogoliubov 变换

$$
\hat d_\pm=\cosh r\,\hat\beta_\pm
                  \pm\sinh r\,\hat\beta_\pm^+.
$$

代入后，配对项消失，得到

$$
\hat h_\pm=-\omega(\hat\beta_\pm^+\hat\beta_\pm+\tfrac12).
$$

因此普通 Fock-space 迹绝对收敛：

$$
W_\pm=\sum_{n=0}^{\infty}e^{-\omega(n+1/2)}
     =\frac1{2\sinh(\omega/2)},
$$

$$
\boxed{
W_{\rm bare}=\operatorname{Tr}e^{\hat h}
=\frac1{4\sinh^2(\omega/2)}>0.
}
$$

这个表达式包含了全部零点因子，不存在通过补一个 normal-ordering 常数改变符号的余地。

## 4. 同一个函数延拓后变为负数

现在考虑 0<x<κ，令

$$
\nu=\sqrt{\kappa^2-x^2}>0.
$$

将上述已由算符迹确定的函数解析延拓，即 ω=iν，得到

$$
\boxed{
W_{\rm cont}
=-\frac1{4\sin^2(\nu/2)}<0,
\qquad \nu\notin2\pi\mathbb Z.
}
$$

这个结果处处远离所排除的行列式极点。它也不是仅凭“迹的平方为正”推测出的符号，而是从明确的收敛迹表达式直接延拓所得。

更清楚地看，令 z=x²−κ²。函数 1/[4sinh²(√z/2)] 对 √z 的符号不敏感，是 z 的单值亚纯函数。绕开 z=0 的极点不能把两模权重从负值改成正值。

Nambu 行列式恰好显示了信息缺口：

$$
\det(I_4-e^A)=16\sinh^4(\omega/2).
$$

在稳定区，由算符迹选定的平方根为 4sinh²(ω/2)。延拓到 ω=iν 时，它变为 −4sin²(ν/2)。若此时改用正实平方根 +4sin²(ν/2)，得到的是另一个规定的权重，不再是刚才那个收敛迹的解析延拓。

这里没有收敛算符迹为负的矛盾。κ>x 时，h 沿一个玻色 quadrature 方向无上界，e^h 不再是 trace-class 算符，普通迹不收敛。问题恰恰在于把收敛域内的正性推广到了“延拓值有限”的更大范围。

## 5. Majorana 模平方证明具体在哪里失效

为直接对应第 2 节给出的对称性，两个 Majorana 扇区应取为

$$
\hat f_\pm=\frac{\hat b\pm i\hat c}{\sqrt2}.
$$

它们与第 3 节用于计算迹的普通解耦模 d₊、d₋ 不同。对于 P=Θ₊Θ₋，f₊、f₋ 的本征值分别为 −1、+1，而 Θ₊ 交换二者。算符在这两扇区中分解为

$$
\hat h_\pm^{(P)}
=-x(\hat f_\pm^+\hat f_\pm+\tfrac12)
 \pm\frac{i\kappa}{2}(\hat f_\pm^{+2}-\hat f_\pm^2).
$$

两扇区彼此共轭，各自的稳定模频率仍为 ω，所以每个扇区的迹仍是 1/[2sinh(ω/2)]。

在收敛区，两扇区的迹既相等又为实数，可以写成

$$
W=W_+W_-=W_+\overline{W_+}.
$$

沿相同解析延拓到 ω=iν 后，

$$
W_+=W_-=\frac1{2i\sin(\nu/2)}.
$$

它们成为相同的纯虚数。因此 W₊W₋ 为负，而 W₊ 的模平方为正。这两个结果已经是不同的函数。

反幺正变换会同时共轭复参数和延拓路径。收敛域内的共轭关系不能在任意延拓路径的终点自动保留。若强制把另一个扇区定义为共轭路径上的结果，就需要重新说明这种规定如何对应原始统计权重；不能一面宣称沿既定路径解析延拓，一面在终点重新改成模平方。

对应到当前 SM，需下一轮重新审查的是从共轭扇区到 Eq. (S158)，即源码标号 eq:trs_majorana_modulus_square，以及后续模行列式公式的全局延伸。算符分解本身和收敛域内的迹因式分解并未被这个例子推翻。

## 6. 当前非保护类别的反例也暴露出内部冲突

当前 SM 中用于说明“单个负平方 TRS 不足”的纯配对例子为

$$
A=-s(i\tau_y)\otimes I_2,
\qquad
W=-\frac1{4\sin^2(s/2)},
\qquad s\in\mathbb R\setminus2\pi\mathbb Z.
$$

这里 τ 作用于 Nambu 指标，σ 作用于两种 flavor。这个例子实际上还具有

$$
U_1=I_2\otimes\sigma_x,\qquad
U_2=I_2\otimes\sigma_z,\qquad
U_3=I_2\otimes(i\sigma_y).
$$

三个相应的反幺正映射保持 canonical 和 Hermitian-conjugation 条件、保持 A，且两两反对易，平方依次为 +、+、−。所以它同时属于 {+,+,−}，也包含 Majorana {+,−} 子集。

这意味着，当前用于排除单个负平方类别的例子，与同一延拓规定下“Majorana 类受保护”和“三个以上对称性全部受保护”的表格结论发生直接冲突。下一轮不能只在表格脚注加一句“远离极点”解决，也需要重新检查非保护类别的证据是否位于最终选定的权重定义域中。

本轮没有完成 {−,−} 与 {+,+,+} 在整个延拓域内的独立证明审计，不能据此给出一张修正后的完整周期表。

## 7. 已确认的边界与下一轮要解决的问题

这个反例没有推翻粒子数守恒时的单 Kramers 判据。那里的权重是无平方根歧义的逆行列式，复共轭本征值成对，实本征值的代数重数为偶数，行列式正性证明不依赖上述配对扇区延拓。

它也没有证明文章的既有 benchmark 数据有误。稳定二次热因子与 unitary HS 因子的有限乘积处于可直接研究算符迹的范围；已有数值数据与广义延拓定理是不同层次的证据。当前需处理的是定理所覆盖的全部配置及其权重定义，不能仅凭 benchmark 一致性代替全局证明。

下一轮需要明确选择并证明以下对象之一：

1. 收敛的原始 Gaussian 算符迹，并在这个域内重新完成所有保护类和非保护类的分类。
2. 一个明确的正规化权重，说明它如何由原始模型得到、分支如何固定、TRS/RP 是否保护该定义；若采用模平方规定，还需验证它没有改变所求配分函数和更新比。

本说明不预先替作者选择下一轮路线。

## 8. 可复核的矩阵与有限截断检查

同目录的 [verify.py](verify.py) 只检验上述反例，不生成或增加论文 benchmark。通过仓库的 WSL 入口运行：

    .\scripts\run-in-wsl.ps1 'python3 docs/research_reports/2026-09-10_trs_branch_issue/verify.py'

每个模保留 d 个 Fock 态，将 h 压缩到 d² 维空间后计算有限矩阵指数的迹，结果如下。

| x | κ | 解析表达式 | d=6 | d=10 | d=14 |
| --- | --- | --- | --- | --- | --- |
| 1.2 | 0.4 | 0.7029907517 | 0.6990060654 | 0.7029167283 | 0.7029894555 |
| 0.2 | 0.6 | −3.2096837895 | 54.16175908 | 758.6856414 | 11770.71162 |

稳定例子的截断迹趋向准确的收敛迹。第二行的有限矩阵迹始终为正并迅速增长，与负的延拓值显然不同。这里的截断数值用于直观核验；普通迹不收敛的结论来自前面的谱与 quadrature 分析，不依赖仅有三个截断点的外推。
