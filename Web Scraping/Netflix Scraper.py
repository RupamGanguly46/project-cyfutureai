# import os
# from playwright.sync_api import sync_playwright

# # Folder to store articles
# os.makedirs(r"C:\Users\HP\Desktop\Customer Care Cyfuture\Web Scraping\articles", exist_ok=True)

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=True)
#     page = browser.new_page()
#     page.goto("https://help.netflix.com/en", timeout=60000)
#     page.wait_for_timeout(2000)

#     article_index = 1

#     categories = page.locator("div.category.category-card")
#     cat_count = categories.count()

#     for i in range(cat_count):
#         cat = categories.nth(i)
#         category_name = cat.locator("strong.category-name").inner_text()
#         print(f"\n📁 Category: {category_name}")

#         summaries = cat.locator("summary.subcategory-header")
#         sub_count = summaries.count()

#         for j in range(sub_count):
#             summary = summaries.nth(j)
#             sub_name = summary.locator("strong.subcategory-name").inner_text()
#             print(f"🔽 Expanding subcategory: {sub_name}")
#             summary.click()
#             page.wait_for_timeout(500)

#             articles = summary.locator("xpath=following-sibling::ul[contains(@class, 'articles-list')]//a[contains(@class, 'article-link')]")
#             link_count = articles.count()

#             for k in range(link_count):
#                 articles = summary.locator("xpath=following-sibling::ul[contains(@class, 'articles-list')]//a[contains(@class, 'article-link')]")
#                 link = articles.nth(k)

#                 try:
#                     link.wait_for(state="attached", timeout=5000)
#                     href = link.get_attribute("href")
#                     if not href:
#                         continue

#                     full_url = f"https://help.netflix.com{href}"
#                     print(f"[{article_index}] Visiting: {full_url}")

#                     page.goto(full_url)
#                     page.wait_for_timeout(1500)

#                     # ✅ Expand all input[checkbox] inside left-pane
#                     checkboxes = page.locator("div.left-pane input[type='checkbox']")
#                     for n in range(checkboxes.count()):
#                         try:
#                             checkboxes.nth(n).check()
#                         except:
#                             pass  # Ignore if already checked or non-interactive

#                     # ✅ Extract all visible text inside left-pane
#                     left_text = page.locator("div.left-pane").inner_text()

#                     # ✅ Clean up redundant newlines
#                     cleaned = '\n'.join([line.strip() for line in left_text.splitlines() if line.strip()])

#                     # ✅ Save to file
#                     with open(f"articles/article_{article_index}.txt", "w", encoding="utf-8") as f:
#                         f.write(cleaned)

#                     article_index += 1

#                     # Return to homepage and reopen the structure
#                     page.goto("https://help.netflix.com/en")
#                     page.wait_for_timeout(1500)

#                     categories = page.locator("div.category.category-card")
#                     cat = categories.nth(i)
#                     summaries = cat.locator("summary.subcategory-header")
#                     summary = summaries.nth(j)
#                     summary.click()
#                     page.wait_for_timeout(500)

#                 except Exception as e:
#                     print(f"⚠️ Error: {e}")

#     browser.close()

# print("\n✅ All articles saved successfully.")

# import os
# from playwright.sync_api import sync_playwright
# from markdownify import markdownify as md  # <-- added for markdown support

# # Folder to store articles
# output_dir = r"C:\Users\HP\Desktop\Customer Care Cyfuture\Web Scraping\articles"
# os.makedirs(output_dir, exist_ok=True)

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=True)
#     page = browser.new_page()
#     page.goto("https://help.netflix.com/en", timeout=60000)
#     page.wait_for_timeout(2000)

#     article_index = 1
#     categories = page.locator("div.category.category-card")
#     cat_count = categories.count()

#     for i in range(cat_count):
#         cat = categories.nth(i)
#         category_name = cat.locator("strong.category-name").inner_text()
#         print(f"\n📁 Category: {category_name}")

#         summaries = cat.locator("summary.subcategory-header")
#         sub_count = summaries.count()

#         for j in range(sub_count):
#             summary = summaries.nth(j)
#             sub_name = summary.locator("strong.subcategory-name").inner_text()
#             print(f"🔽 Expanding subcategory: {sub_name}")
#             summary.click()
#             page.wait_for_timeout(500)

#             articles = summary.locator(
#                 "xpath=following-sibling::ul[contains(@class, 'articles-list')]//a[contains(@class, 'article-link')]"
#             )
#             link_count = articles.count()

#             for k in range(link_count):
#                 articles = summary.locator(
#                     "xpath=following-sibling::ul[contains(@class, 'articles-list')]//a[contains(@class, 'article-link')]"
#                 )
#                 link = articles.nth(k)

#                 try:
#                     link.wait_for(state="attached", timeout=5000)
#                     href = link.get_attribute("href")
#                     if not href:
#                         continue

#                     full_url = f"https://help.netflix.com{href}"
#                     print(f"[{article_index}] Visiting: {full_url}")
#                     page.goto(full_url)
#                     page.wait_for_timeout(1500)

#                     # ✅ Expand all collapsible checkboxes inside left-pane
#                     checkboxes = page.locator("div.left-pane input[type='checkbox']")
#                     for n in range(checkboxes.count()):
#                         try:
#                             checkboxes.nth(n).check()
#                         except:
#                             pass

#                     # ✅ Get raw HTML from the left-pane
#                     left_html = page.locator("div.left-pane").inner_html()

#                     # ✅ Convert to markdown
#                     markdown = md(left_html, heading_style="ATX")  # ATX = # for headings

#                     # ✅ Save to file
#                     filepath = os.path.join(output_dir, f"article_{article_index}.md")
#                     with open(filepath, "w", encoding="utf-8") as f:
#                         f.write(markdown)

#                     article_index += 1

#                     # Return to homepage and reopen the structure
#                     page.goto("https://help.netflix.com/en")
#                     page.wait_for_timeout(1500)

#                     categories = page.locator("div.category.category-card")
#                     cat = categories.nth(i)
#                     summaries = cat.locator("summary.subcategory-header")
#                     summary = summaries.nth(j)
#                     summary.click()
#                     page.wait_for_timeout(500)

#                 except Exception as e:
#                     print(f"⚠️ Error: {e}")

#     browser.close()

# print("\n✅ All articles saved successfully as Markdown.")


# import os
# import re
# from playwright.sync_api import sync_playwright
# from markdownify import markdownify as md

# # Output folder
# output_dir = r"C:\Users\HP\Desktop\Customer Care Cyfuture\knowledge_base\articles"
# os.makedirs(output_dir, exist_ok=True)

# EXCLUDE_PATTERNS = [
#     r"(?i)Was this article helpful\?", 
#     r"(?i)Yes\s*No", 
#     r"(?i)Contact us.*?yourself",
#     r"!\[.*?\]\(.*?\)",  # markdown images like ![](url)
#     r"<img[^>]+>",        # raw <img> tags if any
# ]

# def clean_text(html):
#     markdown = md(html, heading_style="ATX")
    
#     for pattern in EXCLUDE_PATTERNS:
#         markdown = re.sub(pattern, '', markdown, flags=re.DOTALL).strip()
    
#     # Remove multiple blank lines
#     markdown = re.sub(r'\n{2,}', '\n\n', markdown)

#     return markdown

# from bs4 import BeautifulSoup
# from markdownify import markdownify as md
# import re

# def clean_text(html):
#     soup = BeautifulSoup(html, "lxml")

#     # ✅ Remove related articles module
#     related = soup.find("div", class_="related-articles-module")
#     if related:
#         related.decompose()

#     # ✅ Remove feedback section (helpful, contact us)
#     footer_texts = [
#         "Was this article helpful?",
#         "Yes",
#         "No",
#         "Contact us if you have a different issue",
#         "can’t fix it yourself",
#     ]
#     for tag in soup.find_all(text=True):
#         if any(ft.lower() in tag.lower() for ft in footer_texts):
#             tag.extract()

#     # ✅ Remove any <img> tags
#     for img in soup.find_all("img"):
#         img.decompose()

#     # ✅ Convert to Markdown
#     markdown = md(str(soup), heading_style="ATX")

#     # ✅ Strip excessive newlines
#     markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()

#     return markdown



# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=True)
#     page = browser.new_page()
#     page.goto("https://help.netflix.com/en", timeout=60000)
#     page.wait_for_timeout(2000)

#     article_index = 1

#     categories = page.locator("div.category.category-card")
#     for i in range(categories.count()):
#         cat = categories.nth(i)
#         category_name = cat.locator("strong.category-name").inner_text()

#         summaries = cat.locator("summary.subcategory-header")
#         for j in range(summaries.count()):
#             summary = summaries.nth(j)
#             sub_name = summary.locator("strong.subcategory-name").inner_text()
#             summary.click()
#             page.wait_for_timeout(500)

#             articles = summary.locator("xpath=following-sibling::ul[contains(@class, 'articles-list')]//a[contains(@class, 'article-link')]")
#             for k in range(articles.count()):
#                 articles = summary.locator("xpath=following-sibling::ul[contains(@class, 'articles-list')]//a[contains(@class, 'article-link')]")
#                 link = articles.nth(k)

#                 try:
#                     link.wait_for(state="attached", timeout=5000)
#                     href = link.get_attribute("href")
#                     if not href:
#                         continue

#                     full_url = f"https://help.netflix.com{href}"
#                     print(f"[{article_index}] Visiting: {full_url}")

#                     page.goto(full_url)
#                     page.wait_for_timeout(1500)

#                     # Expand all hidden sections in left-pane
#                     checkboxes = page.locator("div.left-pane input[type='checkbox']")
#                     for m in range(checkboxes.count()):
#                         try:
#                             checkboxes.nth(m).check()
#                         except:
#                             pass

#                     # Get the HTML of just the article content
#                     left_html = page.locator("div.left-pane").inner_html()

#                     # Clean and convert to markdown
#                     content = clean_text(left_html)

#                     # Save
#                     file_path = os.path.join(output_dir, f"article_{article_index}.md")
#                     with open(file_path, "w", encoding="utf-8") as f:
#                         f.write(content)

#                     article_index += 1

#                     # Go back and re-expand the nav
#                     page.goto("https://help.netflix.com/en")
#                     page.wait_for_timeout(1500)

#                     categories = page.locator("div.category.category-card")
#                     cat = categories.nth(i)
#                     summaries = cat.locator("summary.subcategory-header")
#                     summary = summaries.nth(j)
#                     summary.click()
#                     page.wait_for_timeout(500)

#                 except Exception as e:
#                     print(f"⚠️ Error: {e}")

#     browser.close()

# print("\n✅ All articles saved in Markdown format without footer junk.")

import os
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
from markdownify import markdownify as md

ARTICLES_DIR = Path(r"C:\Users\HP\Desktop\Customer Care Cyfuture\knowledge_base\articles")
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

def clean_text(html: str, title: str) -> str:
    print(f"[DEBUG] Cleaning HTML of length: {len(html)}")
    soup = BeautifulSoup(html, "lxml")

    # Remove unwanted sections
    for selector in [
        ".related-articles-module",
        "#was-this-article-helpful",
        "footer",
        "img",
    ]:
        for tag in soup.select(selector):
            print(f"[DEBUG] Removing tag by selector: {selector}")
            tag.decompose()

    # Carefully remove footer texts
    footer_texts = [
        "Was this article helpful?", "Yes", "No",
        "Contact us if you have a different issue", "can’t fix it yourself"
    ]
    for tag in soup.find_all(string=True):
        if any(ft.lower() in tag.lower() for ft in footer_texts):
            print(f"[DEBUG] Removing matched text: {tag.strip()}")
            tag.extract()

    # Since this is already inside the left-pane, convert whole soup
    markdown_body = md(str(soup), heading_style="ATX")
    markdown_body = re.sub(r"\n{3,}", "\n\n", markdown_body).strip()

    full_markdown = f"# {title.strip()}\n\n{markdown_body}"
    print(f"[DEBUG] Final markdown length: {len(full_markdown)}")
    return full_markdown


def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://help.netflix.com/en", timeout=60000)
    page.wait_for_timeout(2000)

    article_index = 1
    categories = page.locator("div.category.category-card")
    cat_count = categories.count()

    print(f"[DEBUG] Found {cat_count} categories.")

    for i in range(cat_count):
        try:
            cat = categories.nth(i)
            cat_name = cat.locator("strong.category-name").inner_text()
            print(f"\n[DEBUG] Category {i+1}/{cat_count}: {cat_name}")

            summaries = cat.locator("summary.subcategory-header")
            sub_count = summaries.count()

            for j in range(sub_count):
                try:
                    summary = summaries.nth(j)
                    sub_name = summary.locator("strong.subcategory-name").inner_text()
                    print(f"  [DEBUG] Subcategory {j+1}/{sub_count}: {sub_name}")
                    summary.click()
                    page.wait_for_timeout(1000)

                    articles = summary.locator("xpath=following-sibling::ul[contains(@class, 'articles-list')]//a[contains(@class, 'article-link')]")
                    art_count = articles.count()

                    for k in range(art_count):
                        try:
                            link = articles.nth(k)
                            article_title = link.inner_text()
                            article_href = link.get_attribute("href")

                            if not article_href:
                                continue

                            full_url = f"https://help.netflix.com{article_href}"
                            print(f"    [DEBUG] Visiting article {k+1}/{art_count}: {article_title} ({article_href})")
                            page.goto(full_url, timeout=30000)
                            page.wait_for_timeout(1500)

                            try:
                                title_elem = page.locator("h1.kb-title")
                                actual_title = title_elem.inner_text()
                            except:
                                actual_title = article_title

                            left_pane = page.locator("div.left-pane")
                            if left_pane.count() == 0:
                                print(f"[WARNING] Empty left-pane: {full_url}")
                                continue

                            html = left_pane.inner_html()
                            print(f"[DEBUG] left-pane HTML length: {len(html)}")
                            print(f"[DEBUG] left-pane sample: {html[:200]}")


                            markdown = clean_text(html, actual_title)

                            filename = ARTICLES_DIR / f"{article_index:04d}_{sanitize_filename(cat_name)}_{sanitize_filename(sub_name)}_{sanitize_filename(actual_title)}.md"
                            with open(filename, "w", encoding="utf-8") as f:
                                f.write(markdown)

                            print(f"      ✅ Saved: {filename.name}")
                            article_index += 1

                            page.goto("https://help.netflix.com/en", timeout=60000)
                            page.wait_for_timeout(1500)
                            categories = page.locator("div.category.category-card")
                            cat = categories.nth(i)
                            summaries = cat.locator("summary.subcategory-header")
                            summary = summaries.nth(j)
                            summary.click()
                            page.wait_for_timeout(500)

                        except Exception as e:
                            print(f"      [ERROR] Article loop error: {e}")
                            continue
                except Exception as e:
                    print(f"    [ERROR] Subcategory loop error: {e}")
                    continue
        except Exception as e:
            print(f"[ERROR] Category loop error: {e}")
            continue

    browser.close()
    print("\n✅ Scraping complete.")
