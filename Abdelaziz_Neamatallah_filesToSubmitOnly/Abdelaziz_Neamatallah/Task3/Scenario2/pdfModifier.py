def inject_collision(original_pdf, block_bin, output_pdf):
    with open(original_pdf, 'rb') as f:
        original = f.read()

    with open(block_bin, 'rb') as f:
        collision_block = f.read()[64:]  # skip prefix

    # Inject just before %EOF
    eof_marker = b'%%EOF'
    insert_point = original.rfind(eof_marker)

    if insert_point == -1:
        raise ValueError("%%EOF not found in PDF")

    new_pdf = (
        original[:insert_point] +
        b"\n% injected collision\n" +
        collision_block +
        b"\n" +
        original[insert_point:]
    )

    with open(output_pdf, 'wb') as f:
        f.write(new_pdf)

# Example usage:
inject_collision("file1.pdf", "msg1_64.bin", "result1.pdf")
inject_collision("file2.pdf", "msg1_64.bin", "result2.pdf")
