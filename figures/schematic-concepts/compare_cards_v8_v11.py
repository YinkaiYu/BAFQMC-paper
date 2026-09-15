from pathlib import Path
import fitz
import subprocess
out=Path.cwd()/"pdf/schematic-concepts"
doc=fitz.open(); page=doc.new_page(width=560,height=610)
versions=[(8,"A  Independent colors / labels above",20,42),
          (9,"B  Independent colors / labels below",296,42),
          (10,"C  Local gray gradient / labels below",20,347),
          (11,"D  Full gradient + translucent cards",296,347)]
for v,label,x,y in versions:
 page.insert_text((x,y-13),label,fontsize=9.4,fontname="helv",color=(.16,.18,.21))
 src=fitz.open(out/f"C_refined_cards_v{v}.pdf")
 page.show_pdf_page(fitz.Rect(x,y,x+244,y+244),src,0)
 src.close()
path=out/"C_cards_comparison_v8-v11.pdf"
doc.save(path,garbage=4,deflate=True)
doc.close()
subprocess.run(["pdftoppm","-singlefile","-r","180","-png",str(path),str(path.with_suffix(""))],check=True)
print("Four-version comparison exported.")
