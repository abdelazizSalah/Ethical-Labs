#!/usr/bin/env python3

# script to craft MD5 collisions of 2 PDFs via mutool and UniColl

# Abdelaziz Neamatallah getting code source from Ange Albertini 2018-2021

# uses mutool from https://mupdf.com/index.html

#importing libraries
import os # to deal with terminal 
import sys # to read and write files 
import hashlib # to evaluate the MD5 values

# Defining MUTOOL which will be used to merge, and create pdfs
MUTOOL = 'mutool'

def EnclosedString(document, begining, end):
    '''
    This fn is used to extract strings existing between two 
        points ( begining , end ) in certain document
    '''
    # look where is the index of the begining
    offset = document.find(begining) + len(begining)

    # return the defined part only
    return document[offset:document.find(end, offset)]

def getCount(document):
    '''
    This fn is used to extract the number of pages
    '''
    encString = EnclosedString(document, b'/Count', b'/') # the number of pages is encloused between them
    count = int(encString)
    return count

def procreate(listOfObjects):
  '''
  This fn takes a list from object IDs, and format them in the form of 0 R 
    which indicate refrencing.  

    This is how pdf is structured.
  '''   

  return b" 0 R ".join(listOfObjects) + b" 0 R"

def adjustPDF(contents): 
  '''
    This is the most important method which fix the xref part to not have any issues after modifing the pdf content.
    The xref part is the part which is responsibe for informing the pdf viewer where exactly each object is located, for example
    object 0 5, it says the offset of this object, so it can be located correctly.

    Algorithm: 
    1. extract the previous xref table
        startXREF = contents.find(b"\nxref\n0 ") + 1
        endXREF = contents.find(b" \n\n", startXREF) + 1
        origXref = contents[startXREF:endXREF]
    2. count number of objects
        objCount = int(origXref.splitlines()[1].split(b" ")[1])
        print("object count: %i" % objCount)
    3. generating new ref table
        xrefLines = [
        b"xref",
        b"0 %i" % objCount,
        # mutool declare its first xref like this
        b"0000000000 00001 f "
        ]
    4. loop and add the remaining objects.
        i = 1
        while i < objCount:
            # doesn't support comments at the end of object declarations
            off = contents.find(b"\n%i 0 obj\n" % i) + 1
            xrefLines.append(b"%010i 00000 n " % (off))
            i += 1

        xref = b"\n".join(xrefLines)
    5. make sure that the length was not changed to not affect the MD5 hash
    6. replace the old xref with the new xref
        contents = contents[:startXREF] + xref + contents[endXREF:]

        startStartXref = contents.find(b"\nstartxref\n", endXREF) + len(b"\nstartxref\n")
        endStartXref = contents.find(b"\n%%%%EOF", startStartXref)
        #   contents = contents[:startStartXref] + "%i" % startXREF + contents[endStartXref:]
        contents = contents[:startStartXref] + ("%i" % startXREF).encode() + contents[endStartXref:]'''
  # 1. extracting the previous xref table: 
  startXREF = contents.find(b'\nxref\n0 ') + 1
  endXREF = contents.find(b' \n\n', startXREF) + 1
  origXref = contents[startXREF:endXREF]

  # getting number of objects
  objCount = int(origXref.splitlines()[1].split(b' ')[1])
  print("object count: %i" % objCount)

  # generate new xref table
  xrefLines = [
      b"xref",
      b"0 %i" % objCount,
      # mutool declare its first xref like this
      b"0000000000 00001 f "
  ]

  # adding the new content with new offsets.
  i = 1
  while i < objCount:
      # doesn't support comments at the end of object declarations
      off = contents.find(b"\n%i 0 obj\n" % i) + 1
      xrefLines.append(b"%010i 00000 n " % (off))
      i += 1     
  

  ## the length of the newe crafted xref should be the same.
  xref = b"\n".join(xrefLines)

  # XREF length should be unchanged
  try:
      assert len(xref) == len(origXref)
  except AssertionError:
      print("<:", repr(origXref))
      print(">:", repr(xref))

  # now we change the xref table with the new crafted one
  contents = contents[:startXREF] + xref + contents[endXREF:]

  # now we need to locate the startXref and %%EOF

  '''
      at any pdf file there is something like this written :
      startxref -> we need to get the index of this
      123456
      %%EOF -> and the index of this


      this number 123456 says to the pdf reader go to this byte, and read the XREF table.
  '''
  startStartXref = contents.find(b"\nstartxref\n", endXREF) + len(b"\nstartxref\n")
  endStartXref = contents.find(b"\n%%%%EOF", startStartXref)
  contents = contents[:startStartXref] + ("%i" % startXREF).encode() + contents[endStartXref:]

  # everything is modified now, return the new pdf.
  return contents

# now lets exploit it and write our main logic:

# 1. read the arguments from the cmd, and make sure they are in the correct format
if len(sys.argv) == 1: # wrote the script name only with no arguments
    print("PDF MD5 collider")
    print("Wake up man!\nUsage: pdf.py <file1.pdf> <file2.pdf>")
    sys.exit()

# 2. read the given arguments (pdfs)
os.system(MUTOOL + ' merge -o first.pdf %s' % sys.argv[1]) # generate a new pdf called file1.pdf from the first argument, to have constant names
os.system(MUTOOL + ' merge -o second.pdf %s' % sys.argv[2])

# 3. add an empty page in the begining to make it easier to know the indicies ( you must create empty pdf and call it dummy.pdf)
'''
  Why we use the dummy file? 
  to make the first entry in the Kids just a dummy file, then to be easy to indicate the begining of the first
  page in the first file, and the first page in the second file.
'''
os.system(MUTOOL + ' merge -o merged.pdf dummy.pdf %s %s' % (sys.argv[1], sys.argv[2]))


# 4. open files in read as byte mode, and read thier content
with open("first.pdf", "rb") as f:
  d1 = f.read()
  print("Successfully read file 1")

with open("second.pdf", "rb") as f:
  d2 = f.read()
  print("Successfully read file 2")

with open("merged.pdf", "rb") as f:
  dm = f.read()
  print("Successfully read merged file")


# count pages of the first file
COUNT1 = getCount(d1)

# count pages of the second file
COUNT2 = getCount(d2)

print("COUNT1 is: ")
print(COUNT1)
print("COUNT2 IS ")
print(COUNT2)


# extracting the common kids -> all 24 pages objects.
kids = EnclosedString(dm, b"/Kids[", b"]")

# we skip the first dummy, and the last " 0 R" string
'''
    indexing explaination: 
        kids[:-4] we neglect the last 4 bytes which incldes 0 R and if there is any empty space to make the split correct
        then we split on 0 R, which will generate a list containing all kids (pages)
        then we need to skip the first page that is why we will start from 1 not 0 till the end [1:]
'''
pages = kids[:-4].split(b" 0 R ")[1:]

# 5. adding Kids in the correct format
KIDS1 = procreate(pages[:getCount(d1)]) # from 0 till the end of last page of the first pdf

KIDS2 = procreate(pages[getCount(d1):]) # from the page of the first pdf + 1 till the end

# now we have KIDS1 containing list of first pdf pages in correct pdf format, and same for pdf2. 

# 6. create a template for the header of pdf
'''
  we need to generate the prefix we need to add which in my case will be
  /ZizoHere /Zizo_was_Here using the ipc_pre
'''
template = b"""%%PDF-1.4

1 0 obj
<<
  /Type /Catalog

  %% for alignments (comments will be removed by merging or cleaning)
  /ZizoHere /Zizo_was_Here____ 
  /Pages 2 0 R
  %% to make sure we don't get rid of the other pages when garbage collecting
  /Fakes 3 0 R
  %% placeholder for UniColl collision blocks
  /0123456789ABCDEF0123456789ABCDEF012
  /0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0
>>
endobj

2 0 obj
<</Type/Pages/Count %(COUNT2)i/Kids[%(KIDS2)s]>>
endobj 

3 0 obj
<</Type/Pages/Count %(COUNT1)i/Kids[%(KIDS1)s]>>
endobj

%% overwritten - was a fake page to fool merging
4 0 obj
<< >>
endobj

"""

# 7. inserting the correct values in the template
contents = template.replace(b"%(COUNT1)i", str(COUNT1).encode())
contents = contents.replace(b"%(COUNT2)i", str(COUNT2).encode())
contents = contents.replace(b"%(KIDS1)s", KIDS1)
contents = contents.replace(b"%(KIDS2)s", KIDS2)

# 8. adjust parents for the first set of pages
# one to see the first pdf pages, and the other see the second
contents += dm[dm.find(b"5 0 obj"):].replace(b"/Parent 2 0 R", b"/Parent 3 0 R", COUNT1) 

# 9. adjust the pdf 
# not necessary (will be fixed by mutool anyway) but avoids warnings
contents = adjustPDF(contents)

# 10. writing new pdf as bytes 

with open("hacked.pdf", "wb") as f:
  f.write(contents)

# let's adjust offsets - -g to get rid of object 4 by garbage collecting
os.system(MUTOOL + ' clean -gggg hacked.pdf cleaned.pdf')

with open("cleaned.pdf", "rb") as f:
  cleaned = f.read()

# some mutool versions do different stuff :(
cleaned = cleaned.replace(
  b" 65536 f \n0000000016 00000 n \n",
  b" 65536 f \n0000000018 00000 n \n",
  1)

with open("pdf1.bin", "rb") as f:
  prefix1 = f.read()

with open("pdf2.bin", "rb") as f:
  prefix2 = f.read()

file1 = prefix1 + b"\n" + cleaned[192:]
file2 = prefix2 + b"\n" + cleaned[192:]

with open("ZizoAttackedFile1.pdf", "wb") as f:
  f.write(file1)

with open("ZizoAttackedFile2.pdf", "wb") as f:
  f.write(file2)

os.remove('first.pdf')
os.remove('second.pdf')
os.remove('merged.pdf')
os.remove('hacked.pdf')
os.remove('cleaned.pdf')

md5 = hashlib.md5(file1).hexdigest()

assert md5 == hashlib.md5(file2).hexdigest()

# to prove the files should be 100% valid
print()
os.system(MUTOOL + ' info -X ZizoAttackedFile1.pdf')
print()
print()
os.system(MUTOOL + ' info -X ZizoAttackedFile2.pdf')

print()
print("MD5: %s" % md5)
print("Success!")