import PyPDF2
import base64


def reverse_caesar_cipher(text, shift):
    """Mengembalikan teks berdasarkan pergeseran tertentu (Caesar cipher)."""
    result = []
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            new_char = chr(start + (ord(char) - start - shift + 26) % 26)
            result.append(new_char)
        else:
            result.append(char)
    return ''.join(result)


def decode_metadata_base64(metadata):
    """Dekode metadata dari Base64 dan Caesar cipher."""
    decoded_metadata = {}
    for key, value in metadata.items():
        base64_decoded = base64.b64decode(value).decode()
        original_text = reverse_caesar_cipher(base64_decoded, 4)
        decoded_metadata[key] = original_text
    return decoded_metadata


def create_pdf_without_hidden_logo(input_pdf, output_pdf):
    """Membuat PDF tanpa halaman dengan logo yang disembunyikan dan halaman kosong di akhir."""
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        # Tambahkan semua halaman kecuali yang pertama dan terakhir
        for page in pdf_reader.pages[1:-1]:
            pdf_writer.add_page(page)

        # Tulis ke file output
        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)

    # Dapatkan metadata dan dekode
    decoded_metadata = decode_metadata_base64(pdf_reader.metadata)

    print("Metadata terdekode:", decoded_metadata)


input_pdf = 'output_with_hidden_logo_and_metadata.pdf'
output_pdf = 'output_without_hidden_logo.pdf'

create_pdf_without_hidden_logo(input_pdf, output_pdf)
