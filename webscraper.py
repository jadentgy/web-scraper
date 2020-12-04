from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

PATH = "D:\python web scrape\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# data to be extracted from site
data = ["Management Corporation Strata Title Plan Number", "Unique Entity Number (UEN)", "Management Name", "Street Address", "Telephone", "Management Telephone"]

for i in range(1, 4700):  # change range to specify what MCST number to crawl

    # "j" will be used to put into URL after going through zeropadding, which turns it into a string.
    j = i
    j = str(j).zfill(4)
    driver.get("https://opengovsg.com/strata-title/" + j)

    # check if we are in the right URL before extraction
    if driver.current_url != "https://opengovsg.com/strata-title/" + j:
        print("MCST number " + j + " does not exist. Moving on.")
        continue

    extracted_data = []

    # data extraction and saving data to extracted_data[]
    for m in data:
        try:
            extracted = driver.find_element_by_xpath("//td[contains(text(), '" + str(m) + "')]/following-sibling::td[1]").text
        except NoSuchElementException:
            extracted = "N.A."

        extracted_data.append(extracted)

    # saving data to a dataframe, which is then exported out
    df = pd.DataFrame({'MCST_no': extracted_data[0], "UEN": extracted_data[1],
        "Management Name": extracted_data[2],
        "Address": extracted_data[3],
        "Telephone": extracted_data[4],
        "Management Telephone": extracted_data[5]}, index=[0])

    df.to_csv(r'D:\python web scrape\test-invalid-url.csv', mode='a', index=False, header=False)

    i += 1

print("Last URL reached. Exiting...")
driver.quit()