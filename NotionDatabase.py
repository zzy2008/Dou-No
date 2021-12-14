import requests
import json
import time


class NotionDatabase:
    def __init__(self, token):
        self.database_url = "https://api.notion.com/v1/databases"
        self.page_url = "https://api.notion.com/v1/pages"
        self.headers = {'Authorization': f'Bearer {token}',
                        'Notion-Version': '2021-08-16',
                        "Content-Type": "application/json"}

    def create_a_database(self, page_id):
        create_database_data = {
            "parent": {"type": "page_id", "page_id": page_id},
            "title": [{"type": "text", "text": {"content": "Media List"}}],
            "icon": {"type": "emoji", "emoji": "🎬"},
            "properties": {
                "Title": {"title": {}},
                "Score": {"select": {"options": [
                    {"name": "⭐️", "color": "gray"},
                    {"name": "⭐️⭐️", "color": "gray"},
                    {"name": "⭐️⭐️⭐️", "color": "gray"},
                    {"name": "⭐️⭐️⭐️⭐️", "color": "gray"},
                    {"name": "⭐️⭐️⭐️⭐️⭐️", "color": "gray"},
                ]}},
                "Short Comments": {"rich_text": {}},
                "Date": {"date": {}},
                "Douban": {"url": {}},
                "Director": {"multi_select": {}},
                "Genres": {"multi_select": {}},
                "Countries of origin": {"multi_select": {}},
                "IMDb": {"url": {}},
                "Poster": {"files": {}},
                "Year": {"select": {}},
                "Status": {"select": {}}
            }
        }

        data = json.dumps(create_database_data)

        r = requests.request("POST", url=self.database_url,
                             headers=self.headers, data=data)
        if r.status_code == 200:
            database_id = eval(r.text.replace(
                ":null", ":'null'").replace(":false", ":'false'"))["id"]
            return database_id
        else:
            print("创建数据库失败，请检查是否页面有授权给集成使用，再重新使用本程序~")
            input("请按Enter回车键退出。")
            exit()

    def create_a_page(self,
                      database_id,
                      movie_title,
                      movie_rate,
                      movie_comment,
                      movie_date,
                      movie_link,
                      imdb_link,
                      poster_l_url,
                      movie_director,
                      movie_country,
                      movie_genre,
                      movie_year,
                      movie_status):
        create_page_data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Title": {"title": [{"text": {"content": movie_title}}]},
                "Score": {"select": {"name": movie_rate}},
                "Short Comments": {"rich_text": [{"text": {"content": movie_comment}}]},
                "Date": {"date": {"start": movie_date}},
                "Douban": {"url": movie_link},
                "IMDb": {"url": imdb_link},
                "Poster": {"files": [{"name": poster_l_url, "external": {"url": poster_l_url}}]},
                "Director": {"multi_select": movie_director},
                "Countries of origin": {"multi_select": movie_country},
                "Genres": {"multi_select": movie_genre},
                "Year": {"select": movie_year},
                "Status": {"select": movie_status}
            }
        }

        data = json.dumps(create_page_data)
        r = requests.request("POST", url=self.page_url,
                             headers=self.headers, data=data)
        if r.status_code == 200:
            print(f"《{movie_title}》详情上传至Notion成功。")
            failure = ""
            return failure
        else:
            print(f"《{movie_title}》详情上传至Notion失败。")
            failure = f"《{movie_title}》"
            return failure
