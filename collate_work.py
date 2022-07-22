import glob
import os
import shutil
import lxml.etree as ET
from acdh_collatex_utils.acdh_collatex_utils import CxCollate
from acdh_collatex_utils.post_process import (
    merge_tei_fragments,
    make_full_tei_doc,
    merge_html_fragments,
    define_readings,
    make_positive_app
)

from config import READING_WIT

XSLT_FILE = os.path.join(
    os.path.dirname(__file__),
    "fixtures",
    "make_tei.xslt"
)
XSL_DOC = ET.parse(XSLT_FILE)

to_collate_update = glob.glob(os.path.join("to_collate", "*.xml"))
for x in to_collate_update:
    with open(x, "r", encoding="utf8") as f:
        data = f.read()
    tei = ET.fromstring(data)
    transform = ET.XSLT(XSL_DOC)
    tei = transform(tei)
    os.makedirs("tmp_to_collate", exist_ok=True)
    new_save_path = os.path.join("tmp_to_collate", x.split('/')[-1])
    with open(new_save_path, "wb") as f:
        f.write(ET.tostring(tei, pretty_print=True, encoding="utf-8"))
    print(f" TEI updated ({new_save_path})")

input_glob = "./tmp_to_collate/*.xml"
output_dir = "./out/collated"
result_file = f'{output_dir}/collated.xml'
result_html = './index.html'

print("starting...")
out = CxCollate(
    glob_pattern=input_glob,
    glob_recursive=False,
    output_dir=output_dir,
    char_limit=False,
    chunk_size=7000,
).collate()

files = glob.glob(f"{output_dir}/*.tei")
print(len(files))
full_doc = merge_tei_fragments(files)
with open(result_file, 'w') as f:
    f.write(ET.tostring(full_doc, encoding='UTF-8').decode('utf-8'))
full_tei = make_full_tei_doc(result_file)
root = full_tei.tree
full_tei.tree_to_file(result_file)
positive_doc = make_positive_app(result_file)
positive_doc.tree_to_file(result_file)

crit_ap_with_rdgs = define_readings(result_file, READING_WIT)
with open(result_file, 'w') as f:
    f.write(
        ET.tostring(
            crit_ap_with_rdgs,
            encoding='UTF-8'
        ).decode('utf-8')
    )

files = glob.glob(f"{output_dir}/*.html")
full_doc = merge_html_fragments(files)
with open(result_html, 'w') as f:
    f.write(full_doc.prettify("utf-8").decode('utf-8'))

for x in glob.glob(f"{output_dir}/out__*"):
    print(f"removing {x}")
    os.remove(x)

shutil.rmtree("tmp_to_collate")
