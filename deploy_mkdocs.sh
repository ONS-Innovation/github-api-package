mkdocs build
mv ./site ../site
git checkout gh-pages
rm -rf ./*
mv ../site/ ./
mv ./site/* ./
git add .
git commit -m "MkDocs Rebuild: $(date)"
git push