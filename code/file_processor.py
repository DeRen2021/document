import os
import json
from datetime import datetime
import magic
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()



class FileProcessor:
    def __init__(self, folder_path="../file"):
        self.folder_path = folder_path
        self.github_raw_base_url = os.getenv('GITHUB_RAW_BASE_URL', 'https://github.com/DeRen2021/document')

    def get_file_info(self, file_path):
        """获取文件信息"""
        stats = os.stat(file_path)
        mime = magic.Magic(mime=True)
        relative_path = os.path.relpath(file_path, start=os.getcwd())
        
        return {
            "name": os.path.basename(file_path),
            "size": stats.st_size,
            "last_modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
            "type": mime.from_file(file_path),
            "url": f"{self.github_raw_base_url}/{relative_path}",
            "path": relative_path
        }

    def process_folder(self):
        """处理文件夹中的所有文件"""
        result = []
        
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):
                file_info = self.get_file_info(file_path)
                result.append(file_info)
        print(result)
        return result

    def save_json(self, data, output_file="file_info.json"):
        """保存处理结果为JSON文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    processor = FileProcessor()
    results = processor.process_folder()
    processor.save_json(results)
    print(f"处理完成，共处理了 {len(results)} 个文件")

if __name__ == "__main__":
    main() 