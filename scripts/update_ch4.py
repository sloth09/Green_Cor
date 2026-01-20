#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Ch4.docx: Discount Rate Formula (r = 0.07 → r = 0.0)
"""
import sys
sys.path.insert(0, r'C:\Users\user\.claude\plugins\marketplaces\anthropic-agent-skills\document-skills\docx')

from scripts.document import Document

doc = Document(r'C:\code\Green_Cor\unpacked_ch4', author="Claude", track_revisions=True, rsid="9A07CB47")

# Update discount rate in formula: r = 0.07 → r = 0.0
formula_node = doc["word/document.xml"].get_node(tag="w:r", contains="r = 0.07")
if formula_node:
    tags = formula_node.getElementsByTagName("w:rPr")
    rpr = tags[0].toxml() if tags else ""
    replacement = f'<w:del><w:r>{rpr}<w:delText>r = 0.07</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>r = 0.0</w:t></w:r></w:ins>'
    doc["word/document.xml"].replace_node(formula_node, replacement)
    print("[OK] Discount rate formula updated: r = 0.07 → r = 0.0")

# Skip alternative searches to avoid multiple matches

doc.save(validate=False)
print("[OK] Ch4.docx updated successfully")
print("[INFO] Changes saved with tracked changes enabled")
