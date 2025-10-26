from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import csv
import time
import re

def setup_driver():
    """Set up Selenium Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_total_pages(soup):
    """Extract total number of pages from pagination"""
    pagination = soup.find('div', class_='paginate')
    if pagination:
        # Try to find the last page number (usually the >> or » link)
        pages = pagination.find_all('a', class_='j-filter-pagination')
        if pages:
            # Get the highest page number
            max_page = 1
            for page in pages:
                page_num = page.get('data-ci-pagination-page')
                if page_num and page_num.isdigit():
                    max_page = max(max_page, int(page_num))
            
            # Also check the text content for page numbers
            page_links = pagination.find_all('a')
            for link in page_links:
                text = link.get_text(strip=True)
                if text.isdigit():
                    max_page = max(max_page, int(text))
            
            print(f"  Detected {max_page} total pages")
            return max_page
    return 1

def scrape_continent(continent_url):
    """Scrape all schools from a continent page (with pagination)"""
    driver = setup_driver()
    all_schools = []
    
    try:
        print(f"\nLoading: {continent_url}")
        driver.get(continent_url)
        time.sleep(3)
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Get total pages
        total_pages = get_total_pages(soup)
        print(f"Found {total_pages} pages to scrape")
        
        # Scrape each page
        for page_num in range(1, total_pages + 1):
            if page_num > 1:
                page_url = f"{continent_url}/page/{page_num}"
                print(f"\nLoading page {page_num}/{total_pages}: {page_url}")
                driver.get(page_url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
            else:
                print(f"\nScraping page {page_num}/{total_pages}")
            
            # Find all school list items
            school_list = soup.find('ul', class_='listSchools')
            if not school_list:
                print("  ⚠ No school list found")
                continue
            
            schools_on_page = 0
            
            for li in school_list.find_all('li'):
                try:
                    # Find school name
                    school_name_tag = li.find('p', class_='font-bold')
                    if not school_name_tag:
                        # Try alternative selector for featured schools
                        school_name_tag = li.find('p', class_='feature-headline')
                    
                    if not school_name_tag:
                        continue
                    
                    school_name = school_name_tag.get_text(strip=True)
                    
                    # Find country and city
                    meta_tag = li.find('p', class_='meta')
                    country = ""
                    city = ""
                    
                    if meta_tag:
                        # Country is in the img alt attribute
                        country_img = meta_tag.find('img', class_='icon', src=re.compile(r'flags'))
                        if country_img:
                            country = country_img.get('alt', '')
                        
                        # City is in the second img alt attribute (marker icon)
                        city_img = meta_tag.find('img', class_='icon--following')
                        if city_img:
                            city = city_img.get('alt', '')
                    
                    # Find school URL
                    school_url = ""
                    link = li.find('a', href=re.compile(r'/school/'))
                    if link:
                        school_url = "https://inteachers.net" + link.get('href', '')
                    
                    # Skip United States schools
                    if school_name and country and country != "United States":
                        all_schools.append({
                            'school_name': school_name,
                            'city': city,
                            'country': country,
                            'url': school_url
                        })
                        schools_on_page += 1
                
                except Exception as e:
                    continue
            
            print(f"  ✓ Found {schools_on_page} schools on page {page_num}")
        
        return all_schools
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []
    
    finally:
        driver.quit()

def load_existing_data():
    """Load existing data from JSON file if it exists"""
    try:
        with open('international_schools_full.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_results(all_schools):
    """Save all school data"""
    if not all_schools:
        print("\n⚠ No data to save")
        return
    
    # Remove duplicates
    unique_schools = []
    seen = set()
    
    for school in all_schools:
        key = (school['school_name'], school['country'])
        if key not in seen:
            seen.add(key)
            unique_schools.append(school)
    
    # Save to JSON
    with open('international_schools_full.json', 'w', encoding='utf-8') as f:
        json.dump(unique_schools, f, indent=2, ensure_ascii=False)
    
    # Save to CSV
    with open('international_schools_full.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['School Name', 'City', 'Country', 'URL'])
        for school in sorted(unique_schools, key=lambda x: (x['country'], x['school_name'])):
            writer.writerow([
                school['school_name'],
                school['city'],
                school['country'],
                school['url']
            ])
    
    # Print summary by country
    print("\n" + "="*70)
    print("SCHOOLS BY COUNTRY")
    print("="*70)
    
    country_counts = {}
    for school in unique_schools:
        country = school['country']
        country_counts[country] = country_counts.get(country, 0) + 1
    
    for country in sorted(country_counts.keys()):
        print(f"{country}: {country_counts[country]} schools")
    
    print("\n" + "="*70)
    print(f"TOTAL SCHOOLS: {len(unique_schools)}")
    print("="*70)
    
    print("\n✓ Data saved to:")
    print("  - international_schools_full.json")
    print("  - international_schools_full.csv")

if __name__ == "__main__":
    print("="*70)
    print("INTERNATIONAL SCHOOLS SCRAPER")
    print("="*70)
    
    # Load existing data
    all_schools = load_existing_data()
    if all_schools:
        print(f"\n✓ Loaded {len(all_schools)} schools from previous session")
    
    # ====== PASTE YOUR CONTINENT URLS HERE ======
    continent_urls = [
        "https://inteachers.net/international-schools/in/asia",
        "https://inteachers.net/international-schools/in/europe",
        "https://inteachers.net/international-schools/in/africa",
        "https://inteachers.net/international-schools/in/north-america",
        "https://inteachers.net/international-schools/in/south-america",
        "https://inteachers.net/international-schools/in/central-america",
        "https://inteachers.net/international-schools/in/middle-east",
        "https://inteachers.net/international-schools/in/australasia",
    ]
    # ==========================================
    
    for url in continent_urls:
        if url.strip() and url.startswith('http'):
            print(f"\n{'='*70}")
            print(f"PROCESSING: {url.split('/')[-1].upper()}")
            print('='*70)
            
            continent_schools = scrape_continent(url.strip())
            
            if continent_schools:
                print(f"\n✓ Scraped {len(continent_schools)} schools from this continent")
                all_schools.extend(continent_schools)
                save_results(all_schools)
            else:
                print("⚠ No schools found")
    
    if all_schools:
        print("\n" + "="*70)
        print("✓ SCRAPING COMPLETE!")
        print("="*70)
        save_results(all_schools)
    else:
        print("\n⚠ No schools collected")