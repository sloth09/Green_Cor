#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Ch1_2.docx: Version (2.3→2.4) and Discount Rate (7%→0%)
"""
import sys
sys.path.insert(0, r'C:\Users\user\.claude\plugins\marketplaces\anthropic-agent-skills\document-skills\docx')

from scripts.document import Document

doc = Document(r'C:\code\Green_Cor\unpacked_ch1_2', author="Claude", track_revisions=True, rsid="15CF3B06")

# Update 1: Version 2.3 → 2.4
version_node = doc["word/document.xml"].get_node(tag="w:r", contains="버전 2.3")
if version_node:
    tags = version_node.getElementsByTagName("w:rPr")
    rpr = tags[0].toxml() if tags else ""
    # Only replace "2.3" part, keep "버전 " unchanged
    replacement = f'<w:r w:rsidR="15CF3B06">{rpr}<w:t xml:space="preserve">&#48260;&#51204; </w:t></w:r><w:del><w:r>{rpr}<w:delText>2.3</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>2.4</w:t></w:r></w:ins>'
    doc["word/document.xml"].replace_node(version_node, replacement)
    print("[OK] Version updated: 2.3 → 2.4")

# Update 2: Discount rate 7% → 0% (No Discounting)
discount_node = doc["word/document.xml"].get_node(tag="w:r", contains="할인율 7%")
if discount_node:
    tags = discount_node.getElementsByTagName("w:rPr")
    rpr = tags[0].toxml() if tags else ""
    # Get the original text element
    text_nodes = discount_node.getElementsByTagName("w:t")
    if text_nodes:
        # Replace "할인율 7%를 적용한" → "할인율 0% (No Discounting)를 적용한"
        # Only mark the change: "7%" → "0% (No Discounting)"
        replacement = f'<w:del><w:r>{rpr}<w:delText>&#54624;&#51064;&#50984; 7%&#47484; &#51201;&#50857;&#54620;</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>&#54624;&#51064;&#50984; 0% (No Discounting)&#47484; &#51201;&#50857;&#54620;</w:t></w:r></w:ins>'
        doc["word/document.xml"].replace_node(discount_node, replacement)
        print("[OK] Discount rate updated: 7% → 0% (No Discounting)")

doc.save(validate=False)  # Skip validation due to settings.xml schema issue
print("[OK] Ch1_2.docx updated successfully")
print("[INFO] Changes saved with tracked changes enabled")
