.PHONY: requirements
requirements:
	poetry export --without-hashes > requirements.txt
	git add requirements.txt
	git commit -m "Update requirements.txt"
	git push