(TeX-add-style-hook
 "releve"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "a4paper" "10pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "margin=0.5in")))
   (TeX-run-style-hooks
    "latex2e"
    "[[[bodyText]]]"
    "article"
    "art10"
    "geometry"
    "graphicx"
    "verbatim"
    "kpfonts"
    "setspace"
    "tabularx"
    "colortbl"
    "xcolor")
   (LaTeX-add-array-newcolumntypes
    "Y"
    "s"
    "b")
   (LaTeX-add-xcolor-definecolors
    "darkgrey"))
 :latex)

