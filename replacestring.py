import os
from os.path import join, getsize


def inplace_change(dir, filetype, old_string, new_string):

    for root, dirs, files in os.walk(dir):
        print root, "consumes",
        print sum(getsize(join(root, name)) for name in files),
        print "bytes in", len(files), "non-directory files"
        for filename in files:
            print filename
            if filename.endswith(filetype):
                print "## {} file has been found ##".format(filetype)
                with open(root + '/' + filename) as f:
                    newText = f.read().replace(old_string, new_string)

                with open(root + '/' + filename, "w") as f:
                    f.write(newText)


inplace_change(r"\\tm-fs01\edu\3DDA_18\sem04\rokoko\04_production\Assets\characters\civilianWoman\civilianWoman", ".ma", "fileInfo \"license\" \"student\";","fileInfo \"license\" \"education\";")
