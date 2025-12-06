# 🎨 ArtTrail - イラスト練習記録＆成長可視化プラットフォーム

![ArtTrail Demo Image](https://res.cloudinary.com/dq3xzarvh/image/upload/v1/media/posts/89b2a15ce2946f2b24b9274743f41c45_vnwsee)

ArtTrail（アートトレイル）は、イラスト練習の継続と成長を可視化することに特化したアプリケーションです。
「過去の自分の絵と比較したい」「日々の努力をヒートマップで実感したい」という課題を解決するために開発しました。

**🔗 デモURL (Live Demo):** [https://arttrail.onrender.com/accounts/login/](https://arttrail.onrender.com/accounts/login/)

> **⚠️ 注意:** 無料プランのRenderを使用しているため、スリープ状態からの起動に **30~60秒ほど** かかる場合があります。

---

## 🚀 開発背景 (Background)
最近お絵描きの練習を始めたのですが、過去の絵を確認したり、どのぐらいの頻度で絵を描いているのかを可視化できたら面白いと感じ、開発しました。
既存のSNSなどは他人に見せることが主目的であり、自らの技術向上をターゲットとした機能を有している点で差別化を図れていると思います。
そこで、**「練習の足跡(Trail)を残し、成長を実感できる場所」** をコンセプトに以下の機能を実装しました。

## ✨ 主な機能 (Key Features)

### 1. 📈 努力の可視化 (Contribution Heatmap)
* GitHubのContribution Graphのような**「カレンダー型ヒートマップ」**を実装。
* 日々の投稿数に応じてマスの色が変化し、継続的な練習のモチベーションを維持します。
* `datetime`と`calendar`ライブラリを使用し、月ごとの曜日ズレ（空白マス）も正確に計算しています。

### 2. ⚔️ Before / After 比較機能
* 任意の2枚の作品を選択し、比較する機能を搭載。
* 過去の作品と現在の作品を並べることで、技術の向上を一目で確認できます。
![ArtTrail Compare Demo](https://res.cloudinary.com/dq3xzarvh/image/upload/v1/media/posts/01f590582c34bd378dde056c4a8cfa21_blet44)

### 3. 🔐 権限管理とセキュリティ
* **ゲスト閲覧モード:** URL (`/?user=username`) を知っていれば、ログインなしでポートフォリオとして閲覧可能。
* **プライバシー保護:** 「模写（練習）」フラグが立った作品は、**本人以外には自動的に非表示**になるロジックを実装。
* **編集・削除権限:** `UserPassesTestMixin` を使用し、投稿者本人以外による操作をサーバーサイドで厳密にブロック。

### 4. 📱 マルチユーザー対応 & マイページ
* 誰でもアカウント作成・ログインが可能。
* ログイン中は「自分専用のダッシュボード」、ログアウト中は「ポートフォリオサイト」としてUIが動的に切り替わります。

---

## 🛠 使用技術 (Tech Stack)

### Backend
* **Python 3.11**
* **Django 5.0** (MVTアーキテクチャ)
* **PostgreSQL** (本番環境DB) / **SQLite** (開発環境DB)

### Frontend
* **HTML5 / CSS3** (Bootstrap 5)
* **JavaScript** (動的なUI制御)
* **Django Template Engine**

### Infrastructure / Tools
* **Render** (Webサーバーデプロイ)
* **Cloudinary** (画像ストレージ)
* **Whitenoise** (静的ファイル配信)
* **Git / GitHub**
* **Generative AI** (Copilot/Gemini) - 実装スピードの最大化に活用

---

## 💡 こだわりポイント (Engineering Highlights)

### 1. AIを活用した「爆速開発」
構想からデプロイまでを**約2日間**で完遂しました。
要件定義とDB設計は自身で行い、コーディングの実装には生成AIを活用することで開発工数を大幅に短縮しました。

### 2. スケーラビリティと運用への配慮
* **Cloudinary連携:** 本番環境（Render）のエフェメラルなファイルシステムに対応するため、画像ストレージを外部化（Cloudinary）。
* **ページネーション:** 作品数が増加しても動作が重くならないよう、`Paginator` を用いたページネーション機能を実装。

---

## 🔮 今後の展望 (Future Roadmap)
* **作品ごとのコメントや添削機能**
* **複数のタグ付け、タグ作成機能**
---

#　アップデート
*2025/12/7 詳細機能追加
