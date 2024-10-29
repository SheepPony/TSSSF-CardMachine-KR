# TSSSF-CardMachine (KR)
Modified by SheepPony  
Originally by Horrible People Productions  
version: OH GOD EVERYTHING IS STILL TERRIBLE

## What is this?
This is a fork of `Card Machine` by `Horrible People Games`, extensively modified to be able to handle Korean text. You can use this to generate the Korean translated versions of Core and Extra Credit decks.

## Installing
This code was created and used under Linux. I have not tested on Windows or Mac, but in theory this code should be fairly cross-platform.

Please note that some required files are under a submodule. Please use the command below to clone this repo, or else the submodules may not get pulled.  
`git clone --recurse-submodules https://github.com/SheepPony/TSSSF-CardMachine-KR.git`

This code depends on the `pillow` Python package.  
`ImageMagick` is required for PDF generation.


## Running
You must first generate the translated `.pon` file by running `python3 translator.py` under the `CardDefinitions/` directory.

After doing so, run the actual card generation by executing:  
`python3 GameGen.py CardDefinitions/Core_1.1.5__KR.pon CardDefinitions/Extra_Credit_1.0.1__KR.pon`

The card images and PDFs will be generated under `output/`.

## Differences from upstream
- This code can only generate TSSSF; support for BaBOC, Dominion, etc has been removed.
- Directory hierarchy was shifted around to my liking.
- Can generate PDFs of multiple card packs at once.
- Tried to un-spaghettify the code in general.

## Additional Explanation
For explanation of the translation script, or the fonts, 
please refer to the README files of the `CardDefinitions` and `Resources` submodules.

