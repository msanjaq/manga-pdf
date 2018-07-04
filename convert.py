import img2pdf

files = [ "{}.png".format(i) for i in range(1,3735)]

pdf_bytes = img2pdf.convert(files)

file = open("Hero.pdf", "wb")
file.write(pdf_bytes)
