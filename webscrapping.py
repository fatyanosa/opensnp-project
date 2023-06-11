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

        subprocess.call(
            [" sed -i -n '/rsid\tchromosome\tposition/,$p' " + file_name],
            shell=True,
        )

        subprocess.call(
            [" sed -i 's/\t/,/g' " + file_name],
            shell=True,
        )
