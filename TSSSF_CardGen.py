import os, glob, shutil, traceback, random
import PIL_Helper
import os.path
import config

LANGMODE="KR"
IS_TRANSLATION= True #False
ARTIST = "Pixel Prism" #"SheepPony"
COPYRIGHT_TEXT_OVERRIDE=None#"Character by TastiMelon. TSSSF by Horrible People Games. Art by SheepPony."

assert LANGMODE in ("EN","KR")

TYPE, PICTURE, SYMBOLS, TITLE, KEYWORDS, BODY, FLAVOR, EXPANSION, CLIENT = range(9)
DIRECTORY = "TSSSF"
#ARTIST = "Pixel Prism"

if LANGMODE=="KR" and IS_TRANSLATION:
    VERSION_ADDITIONAL='사이버 멸종위기종 보호센터 번역팀 / 트씁v0.9'
else:
    VERSION_ADDITIONAL=''
    
def text_preprocess(s):
    s=s.replace("…","...") # Replace Ellipsis unicode (U+2026) with three periods.
    return s

LegacySymbolMode = False
PAGE_WIDTH = 3
PAGE_HEIGHT = 3
TOTAL_CARDS = PAGE_WIDTH*PAGE_HEIGHT


workspace_path = os.path.dirname("workspace")
card_set = os.path.dirname("deck.cards")
CardSet = os.path.dirname("deck.cards") # will be set by GameGen.py
CardPath = DIRECTORY+"/Card-Art/"
ResourcePath = DIRECTORY+"/resources/"
FontsPath = DIRECTORY+"/fonts/"
BleedsPath = DIRECTORY+"/bleed-images/" # will be set by GameGen.py
BleedBackPath = DIRECTORY+"/bleed-backs/" # will be set by GameGen.py
CropPath = DIRECTORY+"/cropped-images/" # will be set by GameGen.py
VassalPath = DIRECTORY+"/vassal-images/" # will be set by GameGen.py


import collections
FontParams=collections.namedtuple(
    "FontParams",[
        "fTitle","fTitleSmall",
        "fBody","fBodySmall","fBodySmaller",
        "fBar","fBarSmall",
        "fFlavor",
        "fCopyright",
        "fCopyrightTop",
        "offsetBarY",
        "offsetTitleTwolineY",
        "offsetTitleSmallY",
        "offsetBodyLeading",
        "offsetFlavorLeading",
        "titleWidthThresh",
        "offsetTitleLeading"])

# ORIGINAL
fpOriginal=FontParams(
    fTitle=       (FontsPath+"TSSSFBartholomew-Bold.otf", 55),
    fTitleSmall=  (FontsPath+"TSSSFBartholomew-Bold.otf", 45),
    fBody=        (FontsPath+"TSSSFCabin-Medium.ttf",     35),
    fBodySmall=   (FontsPath+"TSSSFCabin-Medium.ttf",     35),
    fBodySmaller= (FontsPath+"TSSSFCabin-Medium.ttf",     31),
    fBar=         (FontsPath+"TSSSFCabin-Medium.ttf",     38),
    fBarSmall=    (FontsPath+"TSSSFCabin-Medium.ttf",     35),
    fFlavor=      (FontsPath+"KlinicSlabBookIt.otf",      28),
    fCopyright=   (FontsPath+"TSSSFCabin-Medium.ttf",     18),
    fCopyrightTop=   (FontsPath+"TSSSFCabin-Medium.ttf", 18),
    offsetBarY=           0,
    offsetTitleTwolineY=  0,
    offsetTitleSmallY=    0,
    offsetBodyLeading=    0,
    offsetFlavorLeading=  0,
    titleWidthThresh=     50,
    offsetTitleLeading=   0)

# JEJU
fpJeju=FontParams(
    fTitle=       (FontsPath+"CookieRun Bold.ttf", 48),
    fTitleSmall=  (FontsPath+"CookieRun Bold.ttf", 38),
    fBody=        (FontsPath+"JejuGothicTSSSF.ttf",        32),
    fBodySmall=   (FontsPath+"JejuGothicTSSSF.ttf",        32),
    fBodySmaller= (FontsPath+"JejuGothicTSSSF.ttf",        28),
    fBar=         (FontsPath+"JejuGothicTSSSF.ttf",        35),
    fBarSmall=    (FontsPath+"JejuGothicTSSSF.ttf",        32),
    fFlavor=      (FontsPath+"JejuMyeongjo.ttf",      24),
    fCopyright=   (FontsPath+"TSSSFCabin-Medium.ttf", 18),
    fCopyrightTop=   (FontsPath+"JejuGothicTSSSF.ttf", 18),
    offsetBarY=          +8,
    offsetTitleTwolineY=  0,
    offsetTitleSmallY=   +5,
    offsetBodyLeading=   +5,
    offsetFlavorLeading=  0,
    titleWidthThresh=     14,
    offsetTitleLeading=  +8)

# JEJU-Noto
font_index=1
fpJeNo=FontParams(
    fTitle=       (FontsPath+"CookieRun Bold.ttf", 48),
    fTitleSmall=  (FontsPath+"CookieRun Bold.ttf", 38),
    fBody=        (FontsPath+"JejuGothicTSSSF.ttf",        32),
    fBodySmall=   (FontsPath+"JejuGothicTSSSF.ttf",        32),
    fBodySmaller= (FontsPath+"JejuGothicTSSSF.ttf",        28),
    fBar=         (FontsPath+"JejuGothicTSSSF.ttf",        35),
    fBarSmall=    (FontsPath+"JejuGothicTSSSF.ttf",        32),
    fFlavor=      (FontsPath+"NotoSerifCJK-SemiBold.ttc",  22,font_index),
    fCopyright=   (FontsPath+"TSSSFCabin-Medium.ttf", 18),
    #fCopyrightTop=   (FontsPath+"NotoSansCJK-Medium.ttc", 18,font_index),
    fCopyrightTop=   (FontsPath+"JejuGothicTSSSF.ttf", 18),
    offsetBarY=          +8,
    offsetTitleTwolineY=  0,
    offsetTitleSmallY=   +5,
    offsetBodyLeading=   +5,
    offsetFlavorLeading=  -2,
    titleWidthThresh=     14,
    offsetTitleLeading=  +8)

# NOTO
font_index=1
fpNoto=FontParams(
    fTitle=       (FontsPath+"CookieRun Regular.ttf", 55),
    fTitleSmall=  (FontsPath+"CookieRun Regular.ttf", 45),
    fBody=        (FontsPath+"NotoSansCJK-Medium.ttc", 30,font_index),
    fBodySmall=   (FontsPath+"NotoSansCJK-Medium.ttc", 30,font_index),
    fBodySmaller= (FontsPath+"NotoSansCJK-Medium.ttc", 27,font_index),
    fBar=         (FontsPath+"NotoSansCJK-Regular.ttc", 35,font_index),
    fBarSmall=    (FontsPath+"NotoSansCJK-Regular.ttc", 32,font_index),
    fFlavor=      (FontsPath+"NotoSansCJK-Light.ttc", 24,font_index),
    fCopyright=   (FontsPath+"TSSSFCabin-Medium.ttf", 18),
    fCopyrightTop=   (FontsPath+"TSSSFCabin-Medium.ttf", 18),
    offsetBarY=          -4,
    offsetTitleTwolineY=  0,
    offsetTitleSmallY=    0,
    offsetBodyLeading=   -4,
    offsetFlavorLeading= -2,
    titleWidthThresh=     16,
    offsetTitleLeading=   0)

if LANGMODE=="EN":
    fontparam=fpOriginal#fpJeju
elif LANGMODE=="KR":
    fontparam=fpJeNo
else:
    0/0


VassalTemplatesPath = DIRECTORY+"/vassal templates/"
VassalWorkspacePath = DIRECTORY+"/vassal workspace/"
VassalImagesPath = os.path.join(VassalWorkspacePath, "images")
VASSAL_SCALE=(260,359)

VassalCard = [0]
ART_WIDTH = 601
ART_HEIGHT = 444
base_w = 889
base_h = 1215
base_w_center = base_w/2
base_h_center = base_h/2
w_marg = 31
h_marg = 36
baserect=[(w_marg,h_marg),(base_w-w_marg,base_h-h_marg)]
textmaxwidth = 689

croprect=(50,63,788+50,1088+63)

TextHeightThresholds = [363, 378, 600]
TitleWidthThresholds = [fontparam.titleWidthThresh] #This is in #characters, fix later plox
BarTextThreshold = [500] #pixels



fonts = {
    "Title":PIL_Helper.BuildFont(*fontparam.fTitle),
    "TitleSmall":PIL_Helper.BuildFont(*fontparam.fTitleSmall),
    "Body":PIL_Helper.BuildFont(*fontparam.fBody),
    "BodySmall":PIL_Helper.BuildFont(*fontparam.fBodySmall),
    "BodyChangeling":PIL_Helper.BuildFont(*fontparam.fBodySmaller),
    "Bar":PIL_Helper.BuildFont(*fontparam.fBar),
    "BarSmall":PIL_Helper.BuildFont(*fontparam.fBarSmall),
    "Flavortext":PIL_Helper.BuildFont(*fontparam.fFlavor),
    "Copyright":PIL_Helper.BuildFont(*fontparam.fCopyright),
    "CopyrightTop":PIL_Helper.BuildFont(*fontparam.fCopyrightTop)
}





Anchors = {
    "Blank": (base_w_center, 300),
    "PonyArt": (172, 224),
    "ShipArt": (172, 224),#(173, 226),
    "GoalArt": (172, 224),#(174, 224),
    "Symbol1": (58+50,56+63),
    "Symbol2": (58+50,160+63),
    "LoneSymbol": (108,153),
    "TimelineSymbol": (58+50,535+63),
    "GoalSymbol2": (108,613),
    "Title": (-65-50, 160),
    "TitleTwoLine": (-65-50, 159+fontparam.offsetTitleTwolineY),
    "TitleSmall": (-65-50, 157+fontparam.offsetTitleSmallY),
    "Bar": (-68-50, 598+67+fontparam.offsetBarY),
    "Body": (base_w_center, 735),
    "BodyShiftedUp": (base_w_center, 730),
    "Flavor": (base_w_center, -110),
    "Expansion": (640+50, 525+63),
    "Copyright": (-38-50, -13-61),
    "CopyrightTop": (-38-50, 92)
}

ArtMissing = [
    PIL_Helper.LoadImage(CardPath+"/artmissing01.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing02.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing03.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing04.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing05.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing06.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing07.png"),
    ]


if LANGMODE=="KR":
    def trykor(fp):
        fn,ex=os.path.splitext(fp)
        kfp=fn+"-kor"+ex
        #print("Finding:",kfp)
        if os.path.exists(kfp):
            #print("  Found")
            return kfp
        else:
            #print("  404!")
            return fp
else:
    trykor=lambda fp:fp
    
Frames = {
    "START": PIL_Helper.LoadImage(trykor(ResourcePath+"/BLEED-Blank-Start-bleed.png")),
    "Warning": PIL_Helper.LoadImage(CardPath+"/Warning_.png"),
    "Pony": PIL_Helper.LoadImage(trykor(ResourcePath+"/BLEED-Blank-Pony-bleed.png")),
    "Ship": PIL_Helper.LoadImage(trykor(ResourcePath+"/BLEED-Blank-Ship-bleed.png")),
    "Rules1": PIL_Helper.LoadImage(CardPath+"/BLEED_Rules1.png"),
    "Rules3": PIL_Helper.LoadImage(CardPath+"/BLEED_Rules3.png"),
    "Rules5": PIL_Helper.LoadImage(CardPath+"/BLEED_Rules5.png"),
    "Goal": PIL_Helper.LoadImage(trykor(ResourcePath+"/BLEED-Blank-Goal-bleed.png")),
    "Derpy": PIL_Helper.LoadImage(trykor(CardPath+"/BLEED_Card - Derpy Hooves.png")),
    "TestSubject": PIL_Helper.LoadImage(CardPath+"/BLEED_Card - OverlayTest Subject Cheerilee.png")
    }



Symbols = {
    "male": PIL_Helper.LoadImage(ResourcePath+"/Symbol-male.png"),
    "female": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Female.png"),
    "malefemale": PIL_Helper.LoadImage(ResourcePath+"/Symbol-MaleFemale.png"),
    "earth pony": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Earth-Pony.png"),
    "unicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Unicorn.png"),
    "uniearth": PIL_Helper.LoadImage(ResourcePath+"/symbol-uniearth.png"),
    "pegasus": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Pegasus.png"),
    "alicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Alicorn.png"),
    "changelingearthpony": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingEarthPony.png"),
    "changelingunicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingUnicorn.png"),
    "changelingpegasus": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingPegasus.png"),
    "changelingalicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingAlicorn.png"),
    "dystopian": PIL_Helper.LoadImage(ResourcePath+"/symbol-dystopian-future.png"),
    "ship": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Ship.png"),
    "goal": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Goal.png"),
    "0": PIL_Helper.LoadImage(ResourcePath+"/symbol-0.png"),
    "1": PIL_Helper.LoadImage(ResourcePath+"/symbol-1.png"),
    "2": PIL_Helper.LoadImage(ResourcePath+"/symbol-2.png"),
    "3": PIL_Helper.LoadImage(ResourcePath+"/symbol-3.png"),
    "4": PIL_Helper.LoadImage(ResourcePath+"/symbol-4.png"),
    "3-4": PIL_Helper.LoadImage(ResourcePath+"/symbol-34.png"),
    "2-3": PIL_Helper.LoadImage(ResourcePath+"/symbol-23.png")
    }
TIMELINE_SYMBOL_LIST = ["Dystopian"]

Expansions = {
#    "Everfree14": PIL_Helper.LoadImage(ResourcePath+"/symbol-Everfree14.png"),
    "Indiegogo": PIL_Helper.LoadImage(ResourcePath+"/symbol-Indiegogo.png"),
#    "Birthday": PIL_Helper.LoadImage(ResourcePath+"/symbol-birthday.png"),
#    "Bronycon": PIL_Helper.LoadImage(ResourcePath+"/symbol-Bronycon14.png"),
#    "Summer": PIL_Helper.LoadImage(ResourcePath+"/symbol-summer-lovin.png"),
#    "Apricity": PIL_Helper.LoadImage(ResourcePath+"/symbol-apricity.png"),
#    "BronyCAN": PIL_Helper.LoadImage(ResourcePath+"/symbol-Bronycan14.png"),
    "Xtra": PIL_Helper.LoadImage(ResourcePath+"/symbol-extracredit.png"),
#    "Xtra-dark": PIL_Helper.LoadImage(ResourcePath+"/symbol-extracredit-black.png"),
#    "NMND": PIL_Helper.LoadImage(ResourcePath+"/symbol-nightmarenights.png"),
#    "Ciderfest": PIL_Helper.LoadImage(ResourcePath+"/symbol-ponyvilleciderfest.png"),
#    "Adventure": PIL_Helper.LoadImage(ResourcePath+"/symbol-adventure.png"),
#    "Custom": PIL_Helper.LoadImage(ResourcePath+"/symbol-custom.png"),
#    "Power": PIL_Helper.LoadImage(ResourcePath+"/symbol-power.png"),
#    "Multiplicity": PIL_Helper.LoadImage(ResourcePath+"/symbol-multiplicity.png"),
#    "Canon": PIL_Helper.LoadImage(ResourcePath+"/symbol-canon.png"),
#    "Dungeon": PIL_Helper.LoadImage(ResourcePath+"/symbol-dungeon.png"),
#    "50": PIL_Helper.LoadImage(ResourcePath+"/symbol-50.png"),
#    "2014": PIL_Helper.LoadImage(ResourcePath+"/symbol-2014.png"),
#    "Hearthswarming": PIL_Helper.LoadImage(ResourcePath+"/symbol-hearthswarming.png"),
#    "Ponycon 2015": PIL_Helper.LoadImage(ResourcePath+"/symbol-ponynyc.png"),
#    "Patreon": PIL_Helper.LoadImage(ResourcePath+"/symbol-Patreon.png"),
#    "Gameshow": PIL_Helper.LoadImage(ResourcePath+"/symbol-gameshow.png"),
#    "BABScon": PIL_Helper.LoadImage(ResourcePath+"/symbol-BABScon.png")
    "Korean": PIL_Helper.LoadImage(ResourcePath+"/symbol-korean.png"),
    "SP1off": PIL_Helper.LoadImage(ResourcePath+"/symbol-sp.png"),
    }

ColorDict={
    "START": (58, 50, 53),
    "START bar text": (237, 239, 239),
    "START flavor": (28, 20, 23),
    "Pony": (70, 44, 137),
    "Pony bar text": (234, 220, 236),
    "Pony flavor": (25, 2, 51),
    "Goal": (18, 57, 98),
    "Goal flavor": (7, 34, 62),
    "Shipwrecker": (8, 57, 98),
    "Shipwrecker flavor": (0, 34, 62),
    "Ship": (206, 27, 105),
    "Ship bar text": (234, 220, 236),
    "Ship flavor": (137, 22, 47),
    "Copyright": (255, 255, 255),
    "Copyright-Special": (30, 30, 30),
    "Blankfill": (200,200,200)
    }

RulesDict={
    "{replace}": "While in your hand, you may discard a Pony card from the grid and play this card in its place. This power cannot be copied.",
    "{swap}": "You may swap 2 Pony cards on the shipping grid.",
    "{3swap}": "You may swap up to 3 Pony cards on the grid.",
    "{draw}": "You may draw a card from the Ship or Pony deck.",
    "{goal}": "You may discard a Goal and draw a new one to replace it.",
    "{search}": "You may search the Ship or Pony discard pile for a card of your choice and play it.",
    "{copy}": "You may copy the power of any Pony card currently on the shipping grid, except for Changelings.",
    "{hermaphrodite}": "May count as either {male} or {female} for all Goals, Ships, and powers.",
    "{double pony}": "This card counts as 2 Ponies.",
    "{love poison}": "Instead of playing this ship with a Pony card from your hand, or connecting two ponies already on the grid, take a Pony card from the shipping grid and reattach it elsewhere with this Ship. That card's power activates.",
    "{keyword change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card counts as having any one keyword of your choice, except pony names.",
    "{gender change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card becomes the opposite gender.",
    "{race change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card becomes a race of your choice. This cannot affect Changelings.",
    "{timeline change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card counts as {postapocalypse}.",
    "{play from discard}": "You may choose to play the top card on the Pony discard pile with this Ship, rather than use a Pony card from your hand.",
    }


if config.page_bleed:
    backs = {
        "START": PIL_Helper.LoadImage(ResourcePath + "BLEED-Start-Back.png"),
        "Pony": PIL_Helper.LoadImage(ResourcePath + "BLEED-Pony-Back.png"),
        "Goal": PIL_Helper.LoadImage(ResourcePath + "BLEED-Goal-Back.png"),
        "Ship": PIL_Helper.LoadImage(ResourcePath + "BLEED-Ship-Back.png"),
        "Card": PIL_Helper.LoadImage(ResourcePath + "BLEED-Pony-Back.png"),
        "Shipwrecker": PIL_Helper.LoadImage(ResourcePath + "BLEED-Pony-Back.png"),
        "BLANK": PIL_Helper.LoadImage(ResourcePath + "Blank - Intentionally Left Blank.png"),
        "Rules1": PIL_Helper.LoadImage(CardPath + "Rules2.png"),
        "Rules3": PIL_Helper.LoadImage(CardPath + "Rules4.png"),
        "Rules5": PIL_Helper.LoadImage(CardPath + "Rules6.png"),
        "TestSubject": PIL_Helper.LoadImage(ResourcePath + "BLEED-Pony-Back.png"),
        "Warning": PIL_Helper.LoadImage(CardPath + "Card - Contact.png")
        }
else:
    backs = {
        "START": PIL_Helper.LoadImage(ResourcePath + "Back-Start.png"),
        "Pony": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
        "Goal": PIL_Helper.LoadImage(ResourcePath + "Back-Goals.png"),
        "Ship": PIL_Helper.LoadImage(ResourcePath + "Back-Ships.png"),
        "Card": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
        "Shipwrecker": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
        "BLANK": PIL_Helper.LoadImage(ResourcePath + "Blank - Intentionally Left Blank.png"),
        "Rules1": PIL_Helper.LoadImage(CardPath + "Rules2.png"),
        "Rules3": PIL_Helper.LoadImage(CardPath + "Rules4.png"),
        "Rules5": PIL_Helper.LoadImage(CardPath + "Rules6.png"),
        "TestSubject": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
        "Warning": PIL_Helper.LoadImage(CardPath + "Card - Contact.png")
        }


# Sanity check - all cards should have the same dimensions
if config.enforce_card_dimensions:
    for k in Frames:
        v=Frames[k]
        wdiff=abs(v.width - config.card_px_width)
        hdiff=abs(v.height - config.card_px_height)
        if max(wdiff,hdiff)>config.card_dimension_mismatch_leeway:
            print("Card dimension mismatch for Frame",k)
            print(F"{v.width}x{v.height} != {config.card_px_width}x{config.card_px_height}")
            0/0
    if config.enforce_front_back_dimension_match:
        for k in backs:
            v=backs[k]
            if abs(v.height-config.card_px_height) > config.card_dimension_mismatch_leeway:
                if config.resize_back_to_match_front:
                    print("Resizing back frame",k)
                    print(F"{v.width}x{v.height} --> {config.card_px_width}x{config.card_px_height}")
                    backs[k]=PIL_Helper.ResizeImage(v,(config.card_px_width,config.card_px_height))
                else:
                    print("Back dimension mismatch for Frame",k)
                    print(F"{v.width}x{v.height} != {config.card_px_width}x{config.card_px_height}")
                    0/0
        

def FixFileName(tagin):
    FileName = tagin.replace("\n", "")
    invalid_chars = [",", "?", '"', ":"]
    for c in invalid_chars:
        FileName = FileName.replace(c,"")
    FileName = u"{0}.png".format(FileName)
    #print FileName
    return FileName

def FixUnicode(text):
    text=text.replace(r'\n','\n')
    if LegacySymbolMode:
        text=text.replace(';', u"\u2642")
        text=text.replace('*', u"\u2640")
        text=text.replace('>', u"\u26A4")
        #text=text.replace('#', u"\u2714")
        text=text.replace('<', u"\u2764")
        text=text.replace('%', u"\uE000")
        text=text.replace('8', u"\uE001")
        text=text.replace('9', u"\uE002")
        text=text.replace('@', u"\uE003")
        text=text.replace('$', u"\uE004")
    else:
        text=text.replace('{male}', u"\u2642")
        text=text.replace('{female}', u"\u2640")
        text=text.replace('{malefemale}', u"\u26A4")
        #text=text.replace('{goal}', u"\u2714")
        text=text.replace('{ship}', u"\u2764")
        text=text.replace('{earthpony}', u"\uE000")
        text=text.replace('{unicorn}', u"\uE001")
        text=text.replace('{pegasus}', u"\uE002")
        text=text.replace('{alicorn}', u"\uE003")
        text=text.replace('{postapocalypse}', u"\uE004")
    return text

def SaveCard(filepath, image_to_save):
    '''
    If the filepath already exists, insert _001 just before the
    extension. If that exists, increment the number until we get to
    a filepath that doesn't exist yet.
    '''
    if os.path.exists(filepath):
        basepath, extension = os.path.splitext(filepath)
        i = 0
        while os.path.exists(filepath):
            i += 1
            filepath = "{}_{:>03}{}".format(basepath, i, extension)
    image_to_save.save(filepath, dpi=(300, 300))

def BuildCard(linein,cardno=0):
    tags = linein.strip('\n').strip('\r').replace(r'\n', '\n').split('`')
    tags=[text_preprocess(i) for i in tags]
    try:
        im = PickCardFunc(tags[TYPE], tags)
        if len(tags) >= 2:
            if len(tags) == 2:
                filename = FixFileName(tags[0]+"_"+tags[1])
            else:
                filename = FixFileName(tags[0]+"_"+tags[3])
            filename=F"{cardno:03d}_"+filename
            SaveCard(os.path.join(BleedsPath, filename), im)
            im_crop=im.crop(croprect)
            SaveCard(os.path.join(CropPath, filename), im_crop)
            im_vassal=PIL_Helper.ResizeImage(im_crop, VASSAL_SCALE)
            SaveCard(os.path.join(VassalPath, filename), im_vassal)
        else:
            im_crop=im.crop(croprect)
        #MakeVassalCard(im_cropped)
    except Exception as e:
        print("Warning, Bad Card: {0}".format(tags))
        traceback.print_exc()
        im=MakeBlankCard()
        im_crop = im.crop(croprect)
    
    if config.page_bleed:
        cutline_color=(255,60,60)
        if tags[TYPE]=="START":
            cutline_color=(255,60,60)
        elif tags[TYPE]=="Ship":
            cutline_color=(0,0,0)
        im=PIL_Helper.AddCutLine(im,line_color=cutline_color)
        
        return im
    else:
        return im_crop

def BuildBack(linein,cardno=0):
    tags = linein.strip('\n').strip('\r').replace(r'\n', '\n').split('`')
    tags=[text_preprocess(i) for i in tags]
    try:
        if tags[TYPE] == "Credits":
            im=MakeCreditsCard(False)
        else:
            im=backs[tags[TYPE]]
        if len(tags) >= 2:
            if len(tags) == 2:
                filename = FixFileName(tags[0]+"_"+tags[1])
            else:
                filename = FixFileName(tags[0]+"_"+tags[3])
            filename=F"{cardno:03d}_"+filename
            SaveCard(os.path.join(BleedBackPath, filename), im)
        else:
            im_crop=im.crop(croprect)
        #MakeVassalCard(im_cropped)
    except Exception as e:
        print("Warning, Bad Card: {0}".format(tags))
        traceback.print_exc()
        im=MakeBlankCard()
        im_crop = im.crop(croprect)
    
    if config.page_bleed:
        cutline_color=(255,60,60)
        if tags[TYPE]=="START":
            cutline_color=(255,60,60)
        elif tags[TYPE]=="Ship":
            cutline_color=(0,0,0)
        im=PIL_Helper.AddCutLine(im,line_color=cutline_color)
    
    return im
  
def PickCardFunc(card_type, tags):
    if tags[TYPE] == "START":
        return MakeStartCard(tags)
    elif tags[TYPE] == "Pony":
        return MakePonyCard(tags)
    elif tags[TYPE] == "Ship":
        return MakeShipCard(tags)
    elif tags[TYPE] == "Goal":
        return MakeGoalCard(tags)
    elif tags[TYPE] == "BLANK":
        return MakeBlankCard()
    elif tags[TYPE] == "Credits":
        return MakeCreditsCard(True)
    elif tags[TYPE] == "Rules1":
        return MakeSpecialCard("Rules1")
    elif tags[TYPE] == "Rules3":
        return MakeSpecialCard("Rules3")
    elif tags[TYPE] == "Rules5":
        return MakeSpecialCard("Rules5")
    elif tags[TYPE] == "TestSubject":
        return MakePonyCard(tags)
    elif tags[TYPE] == "Card":
        return MakeSpecialCard(tags[PICTURE])
    else:
        raise Exception("No card of type {0}".format(tags[TYPE]))

def GetFrame(card_type):
    return Frames[card_type].copy()

def AddCardArt(image, filename, anchor):
    
    if filename == "NOART":
        return
    
    filepath=os.path.join(CardPath, filename)
    filepath=trykor(filepath)
    if os.path.exists(filepath):
        art = PIL_Helper.LoadImage(filepath)
    else:
        art = random.choice(ArtMissing)
    # Find desired height of image based on width of 600 px
    w, h = art.size
    #h = int((float(ART_WIDTH)/w)*h)
    art_aspect=w/h
    card_aspect=ART_WIDTH/ART_HEIGHT
    if abs(art_aspect-card_aspect)>0.01:
        print("Art aspect ratio is off by more than 1%!")
        print("Art:",w,h,art_aspect)
        print("Card:",ART_WIDTH,ART_HEIGHT,card_aspect)
        0/0
    # Resize image to fit in frame
    art = PIL_Helper.ResizeImage(art, (ART_WIDTH,ART_HEIGHT))
    image.paste(art, anchor)

def AddSymbols(image, symbols, card_type=""):
    # Remove any timeline symbols from the symbols list
    pruned_symbols = set(symbols)-set(TIMELINE_SYMBOL_LIST)
    if card_type == "Goal":
        positions = [Anchors["LoneSymbol"], Anchors["GoalSymbol2"]]
    else:
        # If there's only one non-timeline symbol in the list,
        # Set it right on the corner of the picture.
        # Otherwise, adjust so the symbols share the space
        if len(pruned_symbols) == 1:
            positions = [Anchors["LoneSymbol"]]
        else:
            positions = [Anchors["Symbol1"], Anchors["Symbol2"]]

    for index,s in enumerate(symbols):
        sym = Symbols.get(s.lower(), None)
        if sym:
            if s in TIMELINE_SYMBOL_LIST:
                image.paste(sym, Anchors["TimelineSymbol"], sym)
            else:
                image.paste(sym, positions[index], sym)

def TitleText(image, text, color):
    font = fonts["Title"]
    anchor = Anchors["Title"]
    leading = -9
    if text.count('\n') > 0:
        anchor = Anchors["TitleTwoLine"]
        font = fonts["TitleSmall"]
        leading = -15
    elif len(text)>TitleWidthThresholds[0]:
        anchor = Anchors["TitleSmall"]
        font = fonts["TitleSmall"]
    #print(repr(text))
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = anchor,
        valign = "center",
        halign = "right",
        leading_offset = leading+fontparam.offsetTitleLeading
        )

def BarText(image, text, color):
    bar_text_size = PIL_Helper.GetTextBlockSize(text,fonts["Bar"],textmaxwidth)
    if bar_text_size[0] > BarTextThreshold[0]:
        font = fonts["BarSmall"]
    else:
        font = fonts["Bar"]
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = Anchors["Bar"],
        halign = "right"
        )

def BodyText(image, text, color, flavor_text_size=0, font=None):
    # Replacement of keywords with symbols
    for keyword in RulesDict:
        if keyword in text:
            text = text.replace(keyword, RulesDict[keyword])
    text = FixUnicode(text)
    if font is None:
        font = fonts["Body"]
    anchor = Anchors["Body"]
    leading = -1+fontparam.offsetBodyLeading
    # Get the size of the body text as (w,h)
    body_text_size = PIL_Helper.GetTextBlockSize(
        text, fonts["Body"], textmaxwidth
        )
    # If the height of the body text plus the height of the flavor text
    # doesn't fit in on the card in the normal position, move the body text up
    if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[0]:
        anchor = Anchors["BodyShiftedUp"]
    # If they still don't fit, makes the body text smaller
    if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[1]:
        font = fonts["BodySmall"]
        body_text_size = PIL_Helper.GetTextBlockSize(
            text, font, textmaxwidth
            )
        # If they still don't fit, make it smaller again. They're probably
        # the changeling cards
        if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[1]:
            font = fonts["BodyChangeling"]
            leading = -3+fontparam.offsetBodyLeading
    Anchors["BodyShiftedUp"]
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = anchor,
        halign = "center",
        max_width = textmaxwidth,
        leading_offset=leading
        )

def FlavorText(image, text, color):
    return PIL_Helper.AddText(
        image = image,
        text = text,
        font = fonts["Flavortext"],
        fill = color,
        anchor = Anchors["Flavor"],
        valign = "bottom",
        halign = "center",
        leading_offset=+1+fontparam.offsetFlavorLeading,
        max_width = textmaxwidth,
        )

def AddExpansion(image, expansion):
    #print "Expansion: {}".format(expansion)
    expansion_symbol = Expansions.get(expansion, None)
    if expansion_symbol:
        image.paste(expansion_symbol, Anchors["Expansion"], expansion_symbol)

def CopyrightText(tags, image, color, do_bottom=True, do_top=True):
    card_set = CardSet.replace('_',' ')
    #print tags[CLIENT], repr(tags)
    if len(tags)-1 >= CLIENT:
        card_set += " " + str(tags[CLIENT])
    
    
    text = "{}; TSSSF by Horrible People Games. Art by {}.".format(
        card_set,
        ARTIST
        )
    
    if COPYRIGHT_TEXT_OVERRIDE:
        text=COPYRIGHT_TEXT_OVERRIDE
        
    if do_bottom:
        PIL_Helper.AddText(
            image = image,
            text = text,
            font = fonts["Copyright"],
            fill = color,
            anchor = Anchors["Copyright"],
            valign = "bottom",
            halign = "right",
            )
    
    if do_top and VERSION_ADDITIONAL:
        #print("Add text",repr(VERSION_ADDITIONAL))
        PIL_Helper.AddText(
            image = image,
            text = VERSION_ADDITIONAL,
            font = fonts["CopyrightTop"],
            fill = color,
            anchor = Anchors["CopyrightTop"],
            valign = "bottom",
            halign = "right",
            )

def MakeBlankCard():
    image = PIL_Helper.BlankImage(base_w, base_h)
    
    PIL_Helper.AddText(
        image = image,
        text = "This Card Intentionally Left Blank",
        font = fonts["Title"],
        fill = ColorDict["Blankfill"],
        anchor = Anchors["Blank"],
        max_width = textmaxwidth
        )    
    return image

def MakeStartCard(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["PonyArt"])
    TitleText(image, tags[TITLE], ColorDict["START"])
    AddSymbols(image, tags[SYMBOLS].split('!'))
    BarText(image, tags[KEYWORDS], ColorDict["START bar text"])
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["START flavor"])
    BodyText(image, tags[BODY], ColorDict["START"], text_size)
    CopyrightText(tags, image, ColorDict["Copyright"])
    if len(tags) > EXPANSION:
        AddExpansion(image, tags[EXPANSION])
    return image

def MakePonyCard(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["PonyArt"])
    TitleText(image, tags[TITLE], ColorDict["Pony"])
    AddSymbols(image, tags[SYMBOLS].split('!'))
    BarText(image, tags[KEYWORDS], ColorDict["Pony bar text"])
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["Pony flavor"])
    BodyText(image, tags[BODY], ColorDict["Pony"], text_size)
    CopyrightText(tags, image, ColorDict["Copyright"])
    if len(tags) > EXPANSION:
        AddExpansion(image, tags[EXPANSION])
    return image

def MakeShipCard(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["ShipArt"])
    TitleText(image, tags[TITLE], ColorDict["Ship"])
    AddSymbols(image, tags[SYMBOLS].split('!'), "Ship")
    #AddSymbols(image, "Ship")
    BarText(image, tags[KEYWORDS], ColorDict["Ship bar text"])
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["Ship flavor"])
    BodyText(image, tags[BODY], ColorDict["Ship"], text_size)
    CopyrightText(tags, image, ColorDict["Copyright"])
    if len(tags) > EXPANSION:
        AddExpansion(image, tags[EXPANSION])
    return image

def MakeGoalCard(tags):
    image = GetFrame(tags[TYPE])
    AddCardArt(image, tags[PICTURE], Anchors["GoalArt"])
    TitleText(image, tags[TITLE], ColorDict["Goal"])
    AddSymbols(image, tags[SYMBOLS].split('!'), card_type="Goal")
    text_size = FlavorText(image, tags[FLAVOR], ColorDict["Goal flavor"])
    BodyText(image, tags[BODY], ColorDict["Goal"], text_size)
    CopyrightText(tags, image, ColorDict["Copyright"])
    if len(tags) > EXPANSION:
        AddExpansion(image, tags[EXPANSION])
    return image

def MakeSpecialCard(picture):
    print(repr(picture))
    image= GetFrame(picture)
    CopyrightText([], image, ColorDict["Copyright"])
    return image

def MakeCreditsCard(front):
    if front:
        image=PIL_Helper.LoadImage(ResourcePath + "CC-f.png")
    else:
        image=PIL_Helper.LoadImage(ResourcePath + "CC-b.png")
    #image= GetFrame(picture)
    CopyrightText([], image, ColorDict["Copyright-Special"],do_bottom=False)
    return image
    
def InitVassalModule():
    pass

def MakeVassalCard(im):
    VassalCard[0]+=1
    #BuildCard(line).save(VassalImagesPath + "/" + str(VassalCard) + ".png")
    im.save(VassalImagesPath + "/" + str(VassalCard[0]) + ".png")
    
def CompileVassalModule():
    pass

if __name__ == "__main__":
    print("Not a main module. Run GameGen.py")
else:
    print("TSSSF Module imported!")
