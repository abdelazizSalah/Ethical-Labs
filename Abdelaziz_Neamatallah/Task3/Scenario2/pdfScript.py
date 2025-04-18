def inject_collision(pdf_in, bin_in, pdf_out):
    with open(pdf_in, 'rb') as fpdf, open(bin_in, 'rb') as fbin:
        pdf_data = fpdf.read()
        collision_block = fbin.read()[64:]  # Skip prefix

    # Inject collision block as a comment at the end
    injected = pdf_data + b"\n% Collision block start\n" + collision_block + b"\n% Collision block end\n"

    with open(pdf_out, 'wb') as fout:
        fout.write(injected)

# Apply to both versions
inject_collision("file1.pdf", "file1.bin", "clean_version.pdf")
inject_collision("file2.pdf", "file2.bin", "malicious_version.pdf")
print('done')
