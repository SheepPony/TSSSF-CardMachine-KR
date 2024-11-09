import os, glob
import os.path
import PIL_Helper
import argparse
from OS_Helper import Delete, CleanDirectory, BuildPage, BuildBack, AssertDirectory,RmRf,MkDirP
from sys import exit
import subprocess
import sys


print("Args:",sys.argv)
target_pons=[]
arg_consolidate = False
arg_full_filenames = False
for i in sys.argv[1:]:
    if i.startswith("-"):
        if i=="--consolidate":
            arg_consolidate=True
        elif i=="--full-filenames":
            arg_full_filenames=True
        else:
            print("What?",i)
            0/0
    else:
        print("Target PON:",i)
        target_pons.append(i)


if len(target_pons)<1:
    print("You must provide one or more .pon files as an argument!")
    sys.exit(1)


SCRATCH_DIR="scratch"
OUTPUT_DIR="output"

page_num=0
card_num=0
def generate_card_pack(ponpath):
    global page_num, card_num
    print("Generate:",ponpath)
    
    pon_name=os.path.split(ponpath)[1]
    CardFile = open(ponpath)
    card_set = os.path.splitext(os.path.split(ponpath)[1])[0].split("__")[0]

    # Read first line of file to determine module
    first_line = CardFile.readline()
    try:
        import_target="TSSSF_CardGen"#first_line.strip()
        print("Importing:",import_target)
        module = __import__(import_target)
    except ValueError:
        print("Failed to load module: " + str(ValueError))
        return
    module.CardSet = card_set
    

    # Create image directories
    if arg_consolidate:
        dirname="Combined"
    else:
        dirname=card_set
    
    bleed_path = os.path.join(OUTPUT_DIR, dirname+"_bleed-images")
    MkDirP(bleed_path)
    module.BleedsPath = bleed_path
    
    bleedback_path = os.path.join(OUTPUT_DIR, dirname+"_bleed-backs")
    MkDirP(bleedback_path)
    module.BleedBackPath = bleedback_path
    
    cropped_path = os.path.join(OUTPUT_DIR, dirname+"_cropped-images")
    MkDirP(cropped_path)
    module.CropPath = cropped_path
    
    vassal_path = os.path.join(OUTPUT_DIR, dirname+"_vassal-images")
    MkDirP(vassal_path)
    module.VassalPath = vassal_path
    
    module.FilenamesFull = arg_full_filenames
    

    # Load Card File and strip out comments
    cardlines = [line for line in CardFile if not line[0] in ('#', ';', '/')]
    CardFile.close()
    
    if not arg_consolidate:
        card_num=0
    # Make pages
    card_list = []
    back_list = []
    for line in cardlines:
        card_num+=1
        print(F"\r{pon_name:>32s} > #{card_num:03d}\r",end='',flush=True)
        card_list.append(module.BuildCard(line,card_num))
        back_list.append(module.BuildBack(line,card_num))
        # If the card_list is big enough to make a page
        # do that now, and set the card list to empty again
        if len(card_list) >= module.TOTAL_CARDS:
            page_num += 1
            #print("Building Page {}...".format(page_num))
            BuildPage(card_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, SCRATCH_DIR)
            BuildBack(back_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, SCRATCH_DIR)
            card_list = []
            back_list = []
    

    # If there are leftover cards, fill in the remaining
    # card slots with blanks and gen the last page
    if len(card_list) > 0:
        # Fill in the missing slots with blanks
        while len(card_list) < module.TOTAL_CARDS:
            card_list.append(module.BuildCard("BLANK"))
            back_list.append(module.BuildCard("BLANK"))
        BuildPage(card_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, SCRATCH_DIR)
        BuildBack(back_list, page_num, module.PAGE_WIDTH, module.PAGE_HEIGHT, SCRATCH_DIR)
    
def generate_pdf(name="preview"):
    imgfiles=os.listdir(SCRATCH_DIR)
    imgfiles.sort()
    fronts=[]
    backs=[]
    for imgfile in imgfiles:
        if imgfile.startswith("page_"):
            fronts.append(os.path.join(SCRATCH_DIR,imgfile))
        elif imgfile.startswith("backs_"):
            backs.append(os.path.join(SCRATCH_DIR,imgfile))
    print("\nCreating PDF...")
    subprocess.run(
        ["magick"]+fronts+[os.path.join(OUTPUT_DIR,name+"_front.pdf")],
        check=True)
    print("\nCreating PDF of backs...")
    subprocess.run(
        ["magick"]+backs+[os.path.join(OUTPUT_DIR,name+"_back.pdf")],
        check=True)
    
    print("\nCreating Combined PDF...")
    interleaved=[]
    for front in fronts:
        back= front.replace("page_","backs_")
        assert back in backs
        interleaved.append(front)
        interleaved.append(back)
    subprocess.run(
        ["magick"]+interleaved+[os.path.join(OUTPUT_DIR,name+"_interleave.pdf")],
        check=True)




# Setup
print("Clean&Setup directories...")
RmRf(OUTPUT_DIR)
RmRf(SCRATCH_DIR)
os.mkdir(OUTPUT_DIR)
os.mkdir(SCRATCH_DIR)

# Actual card generation
print("Start generation...")
for p in target_pons:
    generate_card_pack(p)
generate_pdf()

# Cleanup
print("Cleanup...")
RmRf(SCRATCH_DIR)

print("Done!")
