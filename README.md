# collate-me
Repo to collate XML/TEI Documents


## how it works

* add XML/TEI files into `to_collate` 
* set the `@xml:id` of your "Leitmanifestation" in `config.py`
* go to https://github.com/freud-digital/collate-me/actions/workflows/download_work.yml and click **Run workflow**

After the collation the result is
* checked into the repo
  * the HTML collation table is called `./index.html`
  * the XML/TEI collation can be found under `.out/collated/collated.xml`
* and served vit GitHub-Pages
  * HTML: https://freud-digital.github.io/collate-me/
  * XML/TEI: https://freud-digital.github.io/collate-me/out/collated/collated.xml