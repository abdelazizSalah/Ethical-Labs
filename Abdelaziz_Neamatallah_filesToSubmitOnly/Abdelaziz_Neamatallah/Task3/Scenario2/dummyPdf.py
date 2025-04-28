def wrap_as_pdf(input_bin, output_pdf):
    with open(input_bin, "rb") as f:
        content = f.read()
    
    # Append minimal valid PDF footer
    pdf = content + b"""
endobj
xref
0 1
0000000000 65535 f 
trailer
<< /Root 1 0 R >>
startxref
%d
%%%%EOF
""" % len(content)

    with open(output_pdf, "wb") as f:
        f.write(pdf)

wrap_as_pdf("file1.bin", "collision1.pdf")
wrap_as_pdf("file2.bin", "collision2.pdf")
