.PHONY: requirements
requirements:
	poetry export --without-hashes -f requirements.txt --output requirements.txt
	git add requirements.txt
	git commit -m "Update requirements.txt"
	git push