# TRS 定理、periodic table 与 odd-parity pairing 整合

本轮以修改前的 1b207e7 为 diff 基线，以 66c6cd4 的导师修订稿为行文参照，将 note/TimeReversalSymmetriesQMC.tex 的结论整合进正文和补充材料。

正文的 Theorem 1 现在覆盖含配对的二次传播，给出三个基本无符号类别：Majorana {+,-}、Kramers {-,-} 和玻色子特有的 {+,+,+}。Table I 对照玻色和费米分类，并直接显示新增的 {+,+,+} 类。原有粒子数守恒分块式、最简 benchmark Hamiltonian 和两组数值结果均保留。摘要及结论各补充了与新结果直接相关的说明。

odd-parity 配对的排除结论明确限定于每个格点采用同一矩阵作用于 annihilation doublet 的内部时间反演。正文指出其在三个基本 TRS 类别中只能由 {+,+,+} 保护。补充材料完整推导 det U=1、负平方变换的唯一性、其与所有允许变换对易的性质，以及三个正平方变换的构造。

补充材料保留并展开三类 positivity 机制、算符迹分支、排除类别的反例、高阶对称性集合、费米 Nambu/Majorana 对应、共轭配对模型、三角格子 odd-parity 模型及 HS 分解。相变与凝聚讨论保持为可研究的物理问题；两谷 condensate locking 的结论保留其试探态范围。一般 Nambu 迹公式统一为带 (-1)^N 的形式，并补齐准粒子占据展开中的零点因子。

## 验证

- 进行了独立物理审读和首次读者／PRL 行文审读，修正了矩阵列向量与算符变换约定，以及 reduced commutator 与逆合同变换的区别。
- WSL 中完成 2484 项代数与数值断言，覆盖非对易 Kramers 传播、split-orthogonal 行列式与 Cayley 恒等式、完整 Nambu HS 对称性、负权重反例、odd-pair 排除代数及两谷能量系数。
- 两个非对易 paired slices 的有限 Fock-space 迹趋于含正确分支符号的约化公式。单模截断维数为 6、10、14 时，相对误差分别为 6.99e-5、5.65e-8、4.19e-11。这些是公式核验，没有增加文章的 benchmark。
- 通过仓库 WSL 入口编译并检查 PDF 页面。正文在第 5 页结束，含参考文献和补充材料的完整稿为 38 页。
- 正式稿没有未定义引用、重复标签或 overfull 警告。保留的提示均已存在于基线：REVTeX 默认字号、nameref 的 label 重定义、BibTeX 的 jnrlst 设置、内部 SM 占位条目的空年份，以及原参考文献段落的轻微 underfull（badness 1337）。diff 的下划线／删除线会另产生轻微 underfull 排版提示。

## 引用核对

下列 15 个键此前已存在于 references.bib，本轮首次用于 main.tex／SM.tex。作者、标题、期刊、卷页、年份和 DOI 已与出版社／Crossref 核对，适用的 arXiv 编号也核对了对应记录。Klich 条目直接以 arXiv 的期刊与 DOI 记录交叉核验；Yu 等的条目保持 arXiv 形式。

| BibTeX 键 | 文中的作用 | 权威记录 |
| --- | --- | --- |
| radzihovskyChoi2009pwave | 共振 Bose 气体的有限动量超流 | [PRL 103, 095302](https://doi.org/10.1103/PhysRevLett.103.095302) |
| papenbrockReimannKavoulakis2012pwave | 旋转双组分玻色气体的精确 p-wave paired states | [PRL 108, 075304](https://doi.org/10.1103/PhysRevLett.108.075304) |
| readSachdev1991frustrated | 受挫磁体中的 Schwinger-boson singlet bonds | [PRL 66, 1773](https://doi.org/10.1103/PhysRevLett.66.1773) |
| sachdev1992kagome | Kagome／三角反铁磁体的 bosonic spinons 与配对构造 | [PRB 45, 12377](https://doi.org/10.1103/PhysRevB.45.12377) |
| klich2014jstat | Paired fermion Gaussian trace 与平方根符号 | [arXiv:1403.7824](https://arxiv.org/abs/1403.7824) |
| choiRadzihovsky2011finite | p-wave 原子—分子耦合及相变背景 | [PRA 84, 043612](https://doi.org/10.1103/PhysRevA.84.043612) |
| dongCuiShen2016pwave | Rb 混合气体的宽 p-wave Feshbach 共振 | [PRA 94, 062702](https://doi.org/10.1103/PhysRevA.94.062702) |
| jiaGuoHuangWang2026pwave | NaRb 异核 p-wave 分子的实验实现 | [PRL 137, 093001](https://doi.org/10.1103/smgh-m2yq) |
| liPanLiu2019droplets | p-wave 玻色气体的量子涨落与液滴 | [PRA 100, 053620](https://doi.org/10.1103/PhysRevA.100.053620) |
| lermaHernandezDukelsky2019pwave | 双组分 p-wave 配对可积模型 | [PRR 1, 032021](https://doi.org/10.1103/PhysRevResearch.1.032021) |
| liNatuParamekanti2014chiral | 双谷玻色子的 counterflow 与 flavor order | [Nature Communications 5, 5174](https://doi.org/10.1038/ncomms6174) |
| liParamekantiHemmerich2014chiral | 电流序与单玻色凝聚的分离 | [Nature Communications 5, 3205](https://doi.org/10.1038/ncomms4205) |
| yuWuZhang2025vestigial | 双谷实验中的两步热熔化 | [arXiv:2507.07494](https://arxiv.org/abs/2507.07494) |
| zhangYinWang2013pair | 三角格子的 pair hopping 与 pair supersolid | [PRB 88, 174515](https://doi.org/10.1103/PhysRevB.88.174515) |
| pelissettoVicari2002critical | 条件性的 O(4) Wilson–Fisher 相变讨论 | [Physics Reports 368, 549–727](https://doi.org/10.1016/S0370-1573(02)00219-3) |

上述新增引文均有核对过身份的 exact-key PDF，保存在本地 local_reference_pdfs/manuscript/。Zhang–Yin–Wang 条目使用出版社的 7 页期刊版，替换了作者列表不同的旧候选 arXiv 缓存。缓存清单也补齐了原先已引用的 Han–Wan–Yao 论文。

没有新增 BibTeX 条目或修改参考文献事实字段。唯一的 BibTeX 源码变动是 pelissettoVicari2002critical 标题内的 discretionary hyphens，用于消除新增引文的 underfull 排版提示；显示标题和文献信息均保持原样。
