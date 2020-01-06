from pdf2image import convert_from_path, convert_from_bytes
import os
import sys
#fullpath = path + "/question_ccfc399b-4d4b-4011-9a57-376fe22c02c2.pdf"
#images = convert_from_path(fullpath)
#images[0].save('test.png', 'png')

if __name__ == "__main__":
    pathpdf = sys.argv[1]
    pathimage = sys.argv[2]

    print("INSIDE pdfconverter")
    print pathpdf
    print pathimage
    images = convert_from_path(pathpdf)
    images[0].save(pathimage,'png')