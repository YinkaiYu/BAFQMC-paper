$out_dir = '.build';
$aux_dir = '.build';

$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error %O %S';

$success_cmd = 'cp %D %R.pdf';
