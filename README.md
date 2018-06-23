# valgrindsummerizer
Generated valgrind XML logs are separated based on interested category and remove likely duplicates 

Input

* Directory of available valgrind output logs in XMLformat (extension is .logs)
* vgsummerizer config file edited with interested kinds (or uninterested kinds)


Output

* XML outputs (that can be read by valkyrie) for each type of leak/ corruption without likely duplicates 

