import os
from mutagen.id3 import ID3, TIT2, TPE1, TALB
from mutagen.mp3 import MP3

def process_mp3_files(folder_path):
    # 固定的标签信息
    NEW_ARTIST = "Louis George Alexander"
    NEW_ALBUM = "NCE_book4-fluency-in-english"

    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误：文件夹 {folder_path} 不存在")
        return

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)

            try:
                print(f"正在处理: {filename}")

                # --- 步骤 1: 删除所有已有 Tag ---
                # ID3().delete(file_path) 会尝试删除 ID3v1 和 ID3v2 标签
                try:
                    basic_id3 = ID3(file_path)
                    basic_id3.delete()
                    print("  [OK] 已删除旧标签")
                except Exception:
                    # 如果文件本身没有标签，会进入这里，继续执行即可
                    print("  [Info] 文件原本无标签")

                # --- 步骤 2: 设置新的 Tag ---
                # 获取不带后缀的文件名作为 Title
                new_title = os.path.splitext(filename)[0]

                # 初始化新的标签对象
                audio = MP3(file_path)
                # 如果删除后没有标签字典，则新建一个
                if audio.tags is None:
                    audio.add_tags()

                # 添加新的标签帧
                # encoding=3 表示使用 UTF-8 编码，防止在不同播放器上出现乱码
                audio.tags.add(TIT2(encoding=3, text=new_title))    # 标题 (Title)
                audio.tags.add(TPE1(encoding=3, text=NEW_ARTIST)) # 艺术家 (Artist)
                audio.tags.add(TALB(encoding=3, text=NEW_ALBUM))  # 专辑 (Album)

                # 保存修改 (v2_version=3 强制保存为兼容性最好的 ID3v2.3)
                audio.save(v2_version=3)
                print(f"  [OK] 已更新标签: Title='{new_title}', Artist='{NEW_ARTIST}'")

            except Exception as e:
                print(f"  [Error] 处理文件 {filename} 时出错: {e}")

if __name__ == "__main__":
    # 在这里输入你的 MP3 文件所在的文件夹路径
    # 如果就在当前目录下，可以使用 "."
    target_folder = "./mp3_book4-fluency-in-english"
    process_mp3_files(target_folder)
    print("\n所有操作已完成！")
