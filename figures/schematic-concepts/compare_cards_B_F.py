from pathlib import Path
import fitz
import subprocess
out=Path(__file__).resolve().parents[2]/"pdf/schematic-concepts"
variants=[("C_refined_cards_B_aligned","B  Flat colors",20),
          ("C_refined_cards_v13_mint_raised_type","F  Gradient colors",296)]
doc=fitz.open(); page=doc.new_page(width=560,height=304)
reference=None
for name,label,x in variants:
 src=fitz.open(out/(name+".pdf"))
 spans=[s for b in src[0].get_text("dict")["blocks"] if "lines" in b for l in b["lines"] for s in l["spans"]]
 layout={s["text"]:tuple(round(n,3) for n in s["bbox"]) for s in spans}
 if reference is None: reference=layout
 else: assert layout==reference,"Label layout differs between B and F"
 page.insert_text((x,29),label,fontsize=10,fontname="helv",color=(.16,.18,.21))
 page.show_pdf_page(fitz.Rect(x,42,x+244,286),src,0)
 src.close()
path=out/"C_cards_comparison_B_F.pdf"
doc.save(path,garbage=4,deflate=True); doc.close()
subprocess.run(["pdftoppm","-singlefile","-r","180","-png",str(path),str(path.with_suffix(""))],check=True)
print("B/F comparison exported; all label bounding boxes match.")
