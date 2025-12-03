#!/usr/bin/env python3
"""
SNS投稿案を保存するスクリプト

使用方法:
    python save_posts.py

投稿案データをJSON形式で渡すか、対話的に入力してください。
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class SNSPostSaver:
    """SNS投稿案を保存するクラス"""

    def __init__(self, output_dir: str = "03_OUTPUT"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_filename(self, content_name: str = "投稿案") -> tuple[str, str]:
        """ファイル名を生成（YYYYMMDD形式）"""
        date_str = datetime.now().strftime("%Y%m%d")
        md_filename = f"{date_str}_{content_name}.md"
        tsv_filename = f"{date_str}_{content_name}.tsv"
        return md_filename, tsv_filename

    def save_markdown(self, posts: Dict[str, List[Dict]], filename: str):
        """MDファイルとして保存"""
        md_path = self.output_dir / filename

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# SNS投稿案\n\n")
            f.write(f"**生成日時:** {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n")

            # 𝕏用投稿案
            if "x_posts" in posts:
                f.write("## 𝕏（旧Twitter）用投稿案\n\n")
                for i, post in enumerate(posts["x_posts"], 1):
                    f.write(f"### 投稿案 {i}\n\n")
                    f.write(f"**投稿内容:**\n```\n{post['content']}\n```\n\n")
                    f.write(f"**文字数:** {post['char_count']}文字\n")
                    f.write(f"**バズの法則:** {post['buzz_rule']}\n")
                    f.write(f"**感情トリガー:** {post['emotion_trigger']}\n\n")
                    f.write("---\n\n")

            # Threads用投稿案
            if "threads_posts" in posts:
                f.write("## Threads用投稿案\n\n")
                for i, post in enumerate(posts["threads_posts"], 1):
                    f.write(f"### 投稿案 {i}\n\n")
                    f.write(f"**投稿内容:**\n```\n{post['content']}\n```\n\n")
                    f.write(f"**文字数:** {post['char_count']}文字\n")
                    f.write(f"**バズの法則:** {post['buzz_rule']}\n")
                    f.write(f"**感情トリガー:** {post['emotion_trigger']}\n\n")
                    f.write("---\n\n")

            # 風刺画プロンプト
            if "satire_images" in posts:
                f.write("## 風刺画プロンプト（Nano Banana Pro用）\n\n")
                for i, satire in enumerate(posts["satire_images"], 1):
                    f.write(f"### 風刺画 {i}\n\n")
                    f.write(f"**タイトル:** {satire['title']}\n\n")
                    f.write(f"**風刺画プロンプト:**\n```\n{satire['prompt']}\n```\n\n")
                    f.write(f"**構成説明:**\n{satire['composition']}\n\n")
                    f.write("---\n\n")

        print(f"✅ MDファイルを保存しました: {md_path}")
        return md_path

    def save_tsv(self, posts: Dict[str, List[Dict]], filename: str):
        """TSVファイルとして保存"""
        tsv_path = self.output_dir / filename

        with open(tsv_path, 'w', encoding='utf-8') as f:
            # ヘッダー
            f.write("No.\tPlatform\t投稿内容\t文字数\tバズの法則\t感情トリガー\n")

            # 𝕏用投稿案
            if "x_posts" in posts:
                for i, post in enumerate(posts["x_posts"], 1):
                    f.write(f"{i}\t𝕏\t{post['content']}\t{post['char_count']}\t")
                    f.write(f"{post['buzz_rule']}\t{post['emotion_trigger']}\n")

            # Threads用投稿案
            if "threads_posts" in posts:
                for i, post in enumerate(posts["threads_posts"], 1):
                    f.write(f"{i}\tThreads\t{post['content']}\t{post['char_count']}\t")
                    f.write(f"{post['buzz_rule']}\t{post['emotion_trigger']}\n")

            # 風刺画（タイトルのみ）
            if "satire_images" in posts:
                f.write("\n# 風刺画\n")
                f.write("No.\tType\tTitle\tPrompt (First 100 chars)\n")
                for i, satire in enumerate(posts["satire_images"], 1):
                    prompt_preview = satire['prompt'][:100] + "..." if len(satire['prompt']) > 100 else satire['prompt']
                    f.write(f"{i}\t風刺画\t{satire['title']}\t{prompt_preview}\n")

        print(f"✅ TSVファイルを保存しました: {tsv_path}")
        return tsv_path

    def save_posts(self, posts: Dict[str, List[Dict]], content_name: str = "投稿案"):
        """投稿案を保存（MD + TSV）"""
        md_filename, tsv_filename = self.generate_filename(content_name)

        md_path = self.save_markdown(posts, md_filename)
        tsv_path = self.save_tsv(posts, tsv_filename)

        return md_path, tsv_path


def create_sample_posts() -> Dict[str, List[Dict]]:
    """サンプルデータを生成（テスト用）"""
    return {
        "x_posts": [
            {
                "content": "これはサンプル投稿です。実際の投稿案に置き換えてください。",
                "char_count": 30,
                "buzz_rule": "稀有性",
                "emotion_trigger": "共感"
            }
        ],
        "threads_posts": [
            {
                "content": "これはThreads用のサンプル投稿です。𝕏より長めの文章でストーリー性を重視します。",
                "char_count": 45,
                "buzz_rule": "プロセスエコノミー",
                "emotion_trigger": "感動"
            }
        ],
        "satire_images": [
            {
                "title": "弊社のAI活用会議",
                "prompt": "Simple illustration of three office workers sitting at meeting table. Left: middle-aged manager with confused expression, labeled \"AI使ったことない\" in Japanese text bubble. Center: senior manager with stern face, labeled \"AI反対派\" in Japanese text bubble. Right: young employee with secretive smile, labeled \"こっそりAI使ってる\" in Japanese text bubble. Minimalist style, clean lines, soft colors, satirical tone, manga-inspired character design, white background.",
                "composition": "- 左: 部長（中年、困惑した表情）- ラベル「AI使ったことない」\n- 中央: 課長（厳しい顔）- ラベル「AI反対派」\n- 右: 新入社員（秘密の笑顔）- ラベル「こっそりAI使ってる」\n- 背景: 会議室、ミニマルスタイル\n- スタイル: 風刺画、シンプルな線画、マンガ風"
            }
        ]
    }


def main():
    """メイン処理"""
    saver = SNSPostSaver()

    print("=" * 60)
    print("SNS投稿案保存スクリプト")
    print("=" * 60)
    print()

    # 引数でJSONファイルが渡された場合
    if len(sys.argv) > 1:
        json_file = Path(sys.argv[1])
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                posts = json.load(f)
            content_name = json_file.stem
        else:
            print(f"❌ ファイルが見つかりません: {json_file}")
            return
    else:
        # サンプルデータを使用
        print("⚠️  引数が指定されていないため、サンプルデータを使用します。")
        print()
        posts = create_sample_posts()
        content_name = "サンプル投稿案"

    # 保存実行
    try:
        md_path, tsv_path = saver.save_posts(posts, content_name)
        print()
        print("=" * 60)
        print("✅ 保存が完了しました！")
        print("=" * 60)
        print(f"📄 MDファイル: {md_path}")
        print(f"📊 TSVファイル: {tsv_path}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
