"""
- 04/08/2024
- Basic WebScraping Programme & CSV Export 
- Using Class: To use instances of this & its attributes/methods
"""
# 1: Import modules
import requests
import csv
from bs4 import BeautifulSoup # Will refer to this as B.S

# 2: Set up Class with Methods to call (functions)
    # 1 to parser HTML page
    # 2 to export to CSV
# 2A: Parser class
class Parser:
    def __init__(self, url): # Obj initializer
        self.url = url
        self.response = requests.get(self.url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, "html.parser")
        #return self.soup

    def html_page(self):
        if self.response.status_code == 200:
            print(f"Got Webpage! {self.response.status_code}")
            return self.soup
        else:
            raise Exception(f"Failed to get web page! Due to {self.response.status_code}!")
                # "raise Except" for error handling/debugging

    def target_content(self, a_tag, a_attribute=None, a_target_attribute=None):
        # Dynamic input for finding content -- more generic code 
        contents = self.soup.find_all(a_tag, attrs=a_attribute)
        result_list = [] # New empty list to hold extracted HTML results

        """Two indepent "if" statement (mutually exclusive) to check HTML results."""
        # 1st "if" to extract user specified attributes from HTML
        # 2nd "if" checks if extracted value is non-empty/valid to then append to list
            # You would still want the results of extract even if not the specified attributes (i.e. HTML content)
        for content in contents:
            if a_target_attribute is not None: # Checks "thruthy" values
               result = content.get(a_target_attribute)
            else:
               result = content.text.strip() # Remove whitespaces
            
            if result is not None: # Checks "thruthy" values
               result_list.append(result)
        return result_list 
       
    # Converting the result list into seperate chunks
    def chunk_list(self, user_input_list, chunk_size):
        chunks = [] # New empty list to hold new chunks of zise
        
        # Iterate to chunks specified size by User
        i = 0 
        while i < len(user_input_list):
            chunk = user_input_list[i:i + chunk_size] # sclice current index (i) to chunk size
            chunks.append(chunk) # Append result to chunks empty list
            i += chunk_size
            #print(i)
        return chunks

# 2B: CSV export class
class CSVExporter:
    def __init__(self, file_name):
        self.file_name = file_name
    
    """Indepent "if" & "for" operations."""
    def csv_export(self, datas, headers=None):
        with open(self.file_name, "w", newline="") as my_file:
            file_writer = csv.writer(my_file)
                # Writes TOP Headers of CSV
            if headers is not None: 
                file_writer.writerow(headers) # Ref: html_search_1
                # Writes the subsequents rows for each results 
            for data in datas:
                file_writer.writerow(data) # Ref: html_search_2

# 3: Create Instance of the Parser & CSV class 
    # main() used to call methods & attributes from class Parser/CSV
def main():
    url = "https://uk.finance.yahoo.com/world-indices/" # Target URL
    
    web_scrape = Parser(url=url)
    web_scrape.html_page()

    """Configurable list: Users to define values to search in HTML."""
    # Searching "Titles" -- 2nd & 3rd arguments can be empty (i.e "")
    html_search_1 = web_scrape.target_content(
        a_tag="a", 
        a_attribute={"data-test": "quoteLink"}, 
        a_target_attribute="title"
        )
        
    # Searching "Prices" -- 2nd & 3rd arguments can be empty (i.e "")
    html_search_2 = web_scrape.target_content(
        a_tag="fin-streamer",
        a_attribute={"data-test": "colorChange"},
        a_target_attribute="value"
        )
        
    # Chunk the 2nd html list in groups of 4
    price_chunks = web_scrape.chunk_list(user_input_list=html_search_2, chunk_size=4)

    # Prep data searched for CSV export
    user_data = []
    
    for i in range(len(html_search_1)):
        data = [html_search_1[i]] # Start with html_page_1
        #print(i, data) -- check index iteration works
        if i < len(price_chunks):
            for price in price_chunks[i]:
                data.append(price)
                #print(i, data) -- check index iteration works
        user_data.append(data)

    # Setup CSV file with requierd headers
    headers_list = ["Indices Name", "Latest Price", "BP Change", "Percentage Change", "Volume"]
    export_to_csv = CSVExporter(file_name="Yahoo_World_Indices.csv")
    export_to_csv.csv_export(datas=user_data, headers=headers_list)

# Main Runner
if __name__ == "__main__":
    main()


