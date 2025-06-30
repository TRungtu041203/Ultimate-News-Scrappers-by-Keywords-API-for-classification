import openai
import csv
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
# client = OpenAI()

# Set your OpenAI API key (or use an environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

def categorize_article(article_text):
    """
    Use OpenAI's GPT (ChatCompletion) API to categorize an article.
    The prompt instructs the model to assign one or more of the following categories:
    
      1. Tổng quan ngành video games tại Việt Nam
      2. Việc phát triển games tại Việt Nam, green gaming, và bảo vệ môi trường
      3. Việc phát triển games và sử dụng công cụ AIs
      4. Esports in Vietnam
      
    If none apply, the model should answer "None".
    """
    prompt = (
        "You are an expert Vietnamese game related news categorizer. Your task is to read the article text below and assign one or more categories "
        "from the list below, based solely on the content and context of the article. Please output only a comma-separated "
        "list of the exact category names (without any additional commentary). If the article does not clearly fit any of the "
        "categories, output 'None'.\n\n"
        "The categories are defined as follows:\n"
        "1. 'Tổng quan ngành video games tại Việt Nam': Articles that provide a general overview or background of the video game industry in Vietnam.\n"
        "2. 'Việc phát triển games tại Việt Nam, green gaming, và bảo vệ môi trường': Articles discussing the development of games in Vietnam with an emphasis on environmental sustainability, including topics like green gaming or environmental protection initiatives.\n"
        "3. 'Việc phát triển games và sử dụng công cụ AIs': Articles related to the development of video games and/or the use of artificial intelligence tools in game creation or gameplay.\n"
        "4. 'Esports in Vietnam': Articles focused on competitive gaming, esports events, or the esports industry within Vietnam.\n\n"
        "Based on the article text provided, please choose the applicable category or categories (if multiple, separate them with commas).\n\n"
        "Article Text:\n" + article_text + "\n\nCategories:"
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use gpt-4 if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant that categorizes news articles."},
                {"role": "user", "content": prompt}         
            ],   
                temperature=0.0  # Lower temperature for more deterministic output
        )
        print("Raw API response:", response)  # Debugging line to see the raw response
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print("Error during categorization:", e)
        return "None"

def main(input_csv, output_csv):
    articles = []
    # Read the input CSV file (assumes UTF-8 BOM for Excel compatibility)
    with open(input_csv, newline='', encoding='utf-8-sig') as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            articles.append(row)
    
    # Open the output CSV file and prepare to write results.
    # We add a "Categories" column to the existing columns.
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as fout:
        fieldnames = list(articles[0].keys()) + ["Categories"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        
        for idx, article in enumerate(articles, start=1):
            # Combine available text for categorization.
            # Adjust the following if your CSV uses different column names.
            text_parts = []
            if "Title" in article:
                text_parts.append(article["Title"])
            if "Summary" in article:
                text_parts.append(article["Summary"])
            if "Content" in article:
                text_parts.append(article["Content"])
            combined_text = "\n".join(text_parts)
            
            print(f"Categorizing article {idx}...")
            print (f"Combined text first: {combined_text[:100]}...")  # Print first 100 chars for debugging
            print (f"Combined text last: {combined_text[-100:]}...")  # Print last 100 chars for debugging
            categories = categorize_article(combined_text)
            article["Categories"] = categories
            
            writer.writerow(article)
            # Pause to help avoid rate limits; adjust the delay as needed.
            time.sleep(1)
    
    print(f"Categorization completed. Results saved to {output_csv}")

if __name__ == "__main__":
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # output_csv_file = f"categorized_articles_{timestamp}.csv"
    # input_csv_file = r"D:\Data\vietnews\output\motgame_20250404_174106 - Copy.csv"  # Change to your input file path
    # output_csv_file = os.path.join(r"D:\Data\vietnews\output", output_csv_file)  # Change to your desired output path
    # # Ensure the output directory exists
    # main(input_csv_file, output_csv_file)
    test_text = (
        "Ngành Game Việt Nam: Tiềm năng tỷ đô nhưng thách thức không nhỏ\n" 
        "Ngành công nghiệp game tại Việt Nam đang trên đà phát triển mạnh mẽ, với gần 60 triệu người chơi và doanh thu đạt 507 triệu USD trong năm 2023. Trong đó, riêng ngành công nghiệp game di động tại Việt Nam đang phát triển với tốc độ chóng mặt, dẫn đầu xu hướng tăng trưởng toàn cầu. Các nghiên cứu thị trường cho thấy, Việt Nam cùng với các nước Đông Nam Á đang là khu vực có tốc độ tăng trưởng game di động cao nhất thế giới, đạt mức 7,4% mỗi năm từ 2022 đến 2025. Nhận thấy tiềm năng to lớn này, Bộ Thông tin và Truyền thông (Bộ TT&TT) đã đặt ra mục tiêu đầy tham vọng: đưa doanh thu ngành game Việt Nam cán mốc 1 tỷ USD trong vòng 5 năm tới, đến năm 2030."
        "Cơ hội to lớn và những thách thức của ngành Game tại Việt Nam\n"
        "Ngành game toàn cầu đang trên đà tăng trưởng mạnh mẽ, với doanh thu dự kiến đạt 212,4 tỷ USD vào năm 2026, trong đó game di động chiếm tỷ trọng đáng kể (42%). Trung Quốc, Mỹ và Nhật Bản tiếp tục khẳng định vị thế là những thị trường game lớn nhất thế giới."
        "Việt Nam cũng không nằm ngoài xu hướng này. Năm 2023, doanh thu game nội địa đạt hơn 507 triệu USD, cộng thêm 200 triệu USD từ game xuất khẩu. Xét về quy mô thị trường, Việt Nam hiện đứng thứ 5 Đông Nam Á về doanh thu game di động và thứ 3 về số lượng người chơi, với hơn 54,6 triệu game thủ trong năm 2023. Đặc biệt, Google dự báo con số này sẽ còn tăng trưởng ấn tượng, đưa tổng doanh thu từ game và ứng dụng tại Việt Nam lên 2,7 tỷ USD vào năm 2026."
    )
    print("Predicted Categories:", categorize_article(test_text))
