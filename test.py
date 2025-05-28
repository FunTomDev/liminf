import morfeusz2

first_name = "Jasiek"

morf = morfeusz2.Morfeusz()

if not first_name:
    print('')
analyses = morf.generate(first_name)
for form, base, tags, _, _ in analyses:
    if ':voc:' in tags:
        print(form)
        break
# fallback if no vocative form found
print(first_name)