sync:
	git commit -am "changes"
	git push origin master
	pipenv run python -m sync
