import glob
import re
import os
from datetime import datetime
import pytz
from pp.models import Image, ImageFile, Book, Page, Line, Character

filenames = glob.glob("/vol/raw/*/*.tif") + glob.glob("/vol/raw/*/*.jpg")
for fn in filenames:
    print(fn)
    components = fn.split("/")
    frontname = components[3]
    backname = components[4]
    base_back = backname.split(".")[0]
    ext_back = backname.split(".")[1]
    newimage = Image.objects.get_or_create(basename=f"{frontname}/{base_back}")[0]
    newimagefiletry = ImageFile.objects.get_or_create(
        parent_image=newimage, filetype=ext_back, filepath=f"{frontname}/{backname}"
    )
    newimagefile = newimagefiletry[0]
    # If image has already been uploaded and source hasn't changed
    if newimagefile.date_uploaded <= datetime.fromtimestamp(
        os.path.getmtime(fn), tz=pytz.UTC
    ):
        print("already loaded, skipping")
        continue
    if ext_back == "jpg":
        newimage.web_file = newimagefile
        newimage.save()
    estc = re.search(r"^([a-z]+_[0-9]+_[0-9]+)", frontname).groups()[0]
    title = re.search(r"_([a-z]+[0-9]?)$", frontname).groups()[0]
    pagen = int(re.search(r"-([0-9]+)", backname).groups()[0])
    tryfol = re.search(r"page([1-2][rv])", backname)
    if tryfol is not None:
        pageside = tryfol.groups()[0]
        newpage = Page.objects.get_or_create(
            book=Book.objects.get_or_create(estc=estc, title=title)[0],
            sequence=pagen,
            side=pageside,
        )[0]
        print(f"Page {newpage}")
        tryline = re.search(r"line([0-9]+)", backname)
        if tryline is not None:
            linen = int(tryline.groups()[0])
            newline = Line.objects.get_or_create(sequence=linen, page=newpage)[0]
            newline.images.add(newimage)
        else:
            newpage.images.add(newimage)
    else:
        print("no side. skipping.")

