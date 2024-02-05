import zipfile as z
import requests

# Get the latest version of BootStrap Icon file name and path.
response = requests.get("https://github.com/twbs/icons/releases/latest")
actual_version = response.url.split('/').pop()
dl_path = "https://github.com/twbs/icons/releases/download/" + actual_version + "/"
dl_name = "bootstrap-icons-" + actual_version[1:] + ".zip"
dl_full = dl_path + dl_name

# Download the file as "bsicons.zip"
dl_zfile = requests.get(dl_full, stream=True)
with open("bsicons.zip", 'wb') as f:
    f.write(dl_zfile.content)

zf = z.ZipFile("bsicons.zip")

# Choose the style
print('''What language are you using?
      1. American/English
      2. Nordic countries

      Choose a number and press enter.
''')
choice = int(input())
while choice not in range(1,3):
    print("Choose 1 or 2 and press enter") 
    choice = int(input())

# Create the new Json file with all the icons.
## American Style

## Nordic style
if choice == 1:
    newjson = "ClearCollect(\n\tcolBSIcons,\n"

    with zf as zipf:
        for file in zipf.namelist():
            if file.endswith(".svg"):
                filename = file[23:-4]
                newjson += '\t\t{IconName: "'+ filename + '",\n'
                filedata = zf.open(file).read().decode(encoding="UTF-8")
                filedata = filedata.replace('"',"'").replace("\n","\n\t\t\t")
                newjson += '\t\tIconData: "' + filedata + '\t"},\n'
    newjson = newjson[:-2]
    newjson += '\n")'

elif choice == 2:
    newjson = "ClearCollect(\n\tcolBSIcons;\n"

    with zf as zipf:
        for file in zipf.namelist():
            if file.endswith(".svg"):
                filename = file[23:-4]
                newjson += '\t\t{IconName: "'+ filename + '";\n'
                filedata = zf.open(file).read().decode(encoding="UTF-8")
                filedata = filedata.replace('"',"'").replace("\n","\n\t\t\t")
                newjson += '\t\tIconData: "' + filedata + '\t"};\n'
    newjson = newjson[:-2]
    newjson += '\n")'
else:
    print ("No input selected")


fp = open('BootstrapIcons.json', 'w')
fp.write(newjson)
fp.close()

# Congratulations
print(f'''
You have now the downloaded {actual_version} of Bootstrap Icons and it's saved in the BootstapIcons.json.\n
1. Open the file and copy the content to your power app in the OnStart field of the App.\n
2. Use the following code in the image content:
\t"data:image/svg+xml;utf8, " & EncodeUrl(
\tSubstitute(
\t\tLookUp(
\t\t\tcolBSIcons;
\t\t\tIconName = "<ICON NAME ex. grid-3x3-gap-fill>"
\t\t)
\t\t.IconData;
\t\t\t"currentColor";
\t\t\tPrimaryColorText
\t\t)
\t)
      ''')
