# Already using commands from .py script, else use:
mkdir -p plots
mkdir -p doc
python3 plot_templates_no_qed.py
pdflatex main.tex