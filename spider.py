import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import sys

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        return

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(2)

        container = driver.find_element(By.ID, "container")
        contents = container.find_element(By.ID, "contents")
        hiragana_divs = contents.find_elements(By.CLASS_NAME, "hiragana")

        if not hiragana_divs:
            print("No <div class='hiragana'> found inside the specified structure.")
        else:
            with open("lyrics.txt", "w", encoding="utf-8") as f:
                for div in hiragana_divs:
                    html = div.get_attribute("outerHTML")
                    soup = BeautifulSoup(html, "html.parser")

                    def extract_text(element):
                        result = ""
                        for child in element.children:
                            if child.name == "span" and "ruby" in child.get("class", []):
                                # Only write the text in <span class="rb">
                                rb = child.find("span", class_="rb")
                                if rb:
                                    result += rb.get_text()
                            elif hasattr(child, "children"):
                                result += extract_text(child)
                            elif child.string:
                                result += child.string
                        return result

                    text = extract_text(soup.div)
                    f.write(text.strip() + "\n")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

