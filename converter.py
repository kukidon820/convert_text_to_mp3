import aspose.words as aw


def convert_to_pdf(file:str):
    doc = aw.Document(file)
    doc.save(f'{file}.pdf')
    return f'{file}.pdf'

