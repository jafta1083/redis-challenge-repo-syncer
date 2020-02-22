sync:
	-git commit -am "changes"
	git push origin master
	pipenv run python -m sync

sync_locally:
	LOCAL=true pipenv run python -m sync
