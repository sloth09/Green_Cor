#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert DOCX and PPTX files to PDF using COM automation."""

import os
import sys
import comtypes.client

def convert_docx_to_pdf(docx_path, pdf_path):
    """Convert a DOCX file to PDF using Word COM."""
    docx_path = os.path.abspath(docx_path)
    pdf_path = os.path.abspath(pdf_path)

    word = comtypes.client.CreateObject("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False

    try:
        doc = word.Documents.Open(docx_path, ReadOnly=True)
        doc.SaveAs(pdf_path, FileFormat=17)  # 17 = wdFormatPDF
        doc.Close(False)
        print(f"[OK] {os.path.basename(pdf_path)} saved")
    except Exception as e:
        print(f"[ERROR] DOCX conversion failed: {e}")
        sys.exit(1)
    finally:
        word.Quit()


def convert_pptx_to_pdf(pptx_path, pdf_path):
    """Convert a PPTX file to PDF using PowerPoint COM."""
    pptx_path = os.path.abspath(pptx_path)
    pdf_path = os.path.abspath(pdf_path)

    ppt = comtypes.client.CreateObject("PowerPoint.Application")
    ppt.Visible = True  # PowerPoint requires Visible=True

    try:
        deck = ppt.Presentations.Open(pptx_path, ReadOnly=True)
        deck.SaveAs(pdf_path, 32)  # 32 = ppSaveAsPDF
        deck.Close()
        print(f"[OK] {os.path.basename(pdf_path)} saved")
    except Exception as e:
        print(f"[ERROR] PPTX conversion failed: {e}")
        sys.exit(1)
    finally:
        ppt.Quit()


if __name__ == "__main__":
    base = r"D:\code\Green_Cor\docs\paper"

    docx_file = os.path.join(base, "paper.docx")
    pptx_file = os.path.join(base, "presentation.pptx")

    if os.path.exists(docx_file):
        convert_docx_to_pdf(docx_file, os.path.join(base, "paper.pdf"))
    else:
        print(f"[WARN] {docx_file} not found")

    if os.path.exists(pptx_file):
        convert_pptx_to_pdf(pptx_file, os.path.join(base, "presentation.pdf"))
    else:
        print(f"[WARN] {pptx_file} not found")
