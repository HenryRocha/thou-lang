default: gen_ll compile run

debug: gen_ll_debug compile run

gen_ll:
	pipenv run python3 ./main.py $(IN)

gen_ll_debug:
	pipenv run python3 ./main.py -d -vvvv $(IN) 2>&1 > ./out/thoulog.log

compile:
	llc -filetype=obj ./out/output.ll -o ./out/program.o
	gcc -no-pie ./out/program.o -o ./out/program

run:
	sh -c "./out/program"

clean:
	rm ./out/*.ll ./out/*.o ./out/*.log ./out/program
