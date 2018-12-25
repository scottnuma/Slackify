import re

def get_id(text):
    return re.findall(r"(?:http|https):\/\/(?:open\.spotify\.com\/track\/(\w+))?", text)


if __name__ == "__main__":
    test_urls = [
        "https://open.spotify.com/track/1aPSpiKWnzzkU49dXtrA3Q?si=xrCDkj5KTaq7SgrEawI2mg",
        "https://open.spotify.com/track/1aPSpiKWnzzkU49dXtrA3Q",
        "some text https://open.spotify.com/track/1aPSpiKWnzzkU49dXtrA3Q?si=xrCDkj5KTaq7SgrEawI2mg other text",
        "some text https://open.spotify.com/track/1aPSpiKWnzzkU49dXtrA3Q?si=xrCDkj5KTaq7SgrEawI2mg.",
        "some text https://open.spotify.com/track/1aPSpiKWnzzkU49dXtrA3Q other text",
        "some text",
        "some text https://open.spotify.com/track/1aPSpiKWnzzkU49dXtrA3Q.some text https://open.spotify.com/track/1aPSpiKWnzzkU49dXtrA3Q."
    ]

    print("starting test")
    for test_url in test_urls:
        print()
        print(test_url)
        result = get_id(test_url)
        print(result)