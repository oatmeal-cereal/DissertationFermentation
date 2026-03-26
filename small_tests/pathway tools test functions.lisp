(loop for x in (get-class-all-instances '|Enzymatic-Reactions|)
    do (loop for item in (get-slot-values x 'alternative-substrates)
	    when (fequal 'GLUCOSE (first item))
        collect (get-slot-value x 'enzyme)) )

(get-class-all-instances '|Enzymatic-Reactions|)

(loop for x in (get-class-all-instances '|Enzymatic-Reactions|)
    when (pathway-allows-enzrxn :enzrxn 'x :single-species '"Saccharomyes cerevisiae")
    collect x
)

(pathway-allows-enzrxn )

;;; get enzymatic reactions from compound (?)

(reactions-of-compound '|GLUCOSE| :enzymatic? t)
(reactions-of-compound '|CPD0-2040| :enzymatic? t)

(loop for x in (reactions-of-compound '|CPD0-2040| :enzymatic? t)
    collect (get-name-string x :strip-html? t))

(loop for x in (get-class-all-instances '|Enzymatic-Reactions|)
    append (loop for y in (pathways-of-enzrxn 'x) collect y ) )

(loop for x in (pathways-of-enzrxn 'ENZRXN0-8627) collect x)

(loop for x in (all-substrates)
    when (fequal 'pyruvate (get-name-string 'x)) collect x)

(loop for x in (all-substrates)
    when (fequal 'PHENYLETHANOLAMINE (get-name-string x)) collect x)

(loop for x in (all-substrates)
    when (fequal 'phenylethanolamine (get-slot-value x 'names)) collect x)

(get-name-string '|ENZRXN0-8627| :strip-html? t :include-species-strain-name? t)
(get-name-string '|RXN-982| :strip-html? t :include-species-strain-name? t)

;;; write file

(with-open-file (str "../filename.txt" 
                    :direction :output
                    :if-exists :supersede
                    :if-does-not-exist :create)
    (format str (concatenate 'string "my" "." "text")))

(loop for x in (all-substrates)

    with-open-file (str "../compound_mapping.txt" :direction :output :if-does-not-exist :create)
    (format str (concatenate 'string x "~" (get-name-string x))))