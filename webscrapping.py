import requests
from bs4 import BeautifulSoup
import subprocess

with open("rs699.html", "r", encoding="utf-8") as f:
    text = f.read()
soup = BeautifulSoup(text, "html.parser")
# Accessing href in the main content of the HTML page
anchor_in_body_content = soup.find(id="user-list")

# Finding all the anchor tags
anchors = anchor_in_body_content.find_all("a")

# Looping over all the anchor tags to get the href attribute
for link in anchors:
    links = link.get("href")
    url = "https://opensnp.org" + links
    r = requests.get(url)
    content = r.content

    soup = BeautifulSoup(content, "html.parser")
    # Finding all the anchor tags
    download_anchors = soup.find_all("a", class_="btn btn-default")
    for download_link in download_anchors:
        links = download_link.get("href")
        data = "https://opensnp.org" + links
        print(data)
        response = requests.get(data, allow_redirects=True)
        file_name = data[data.find("data/") + len("data/") : data.rfind("?")]
        open(file_name, "wb").write(response.content)

        command = f"sed -i -n '/rsid\tchromosome\tposition/,$p' {file_name} && awk -i inplace 'BEGIN {{OFS=\"\t\"}} NR==1 {{print $1, \"allele\"}} NR>1 {{print $1, $4$5}}' {file_name} && sed -i 's/\t/,/g' {file_name}"

        subprocess.call(
            command,
            shell=True,
        )
# awk 'BEGIN {OFS="\t"} NR==1 {print $1, "allele"} NR>1 {print $1, $4$5}' 11452.ancestry.9790 > transposed_file.txt

# awk -F',' '{ for (i=1; i<=NF; i++) { a[i,NR] = $i } if (NF > maxNF) { maxNF = NF } } END { for (i=1; i<=maxNF; i++) { for (j=1; j<=NR; j++) { printf "%s%s", a[i,j], (j==NR ? "\n" : ",") } } }' 11452.ancestry.9790 > test.csv

# subprocess.call(
#     [
#         " sed -i -n '/rsid\tchromosome\tposition/,$p' "
#         + file_name
#         + ' | awk \'BEGIN {OFS="\t"} NR==1 {print $1, "allele"} NR>1 {print $1, $4$5}\'\ '
#         + " > "
#         + file_name
#         # + " && sed -i 's/\t/,/g' "
#         # + file_name
#     ],
#     shell=True,
# )
#
