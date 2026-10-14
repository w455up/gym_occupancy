# 淡水運動中心健身房人數紀錄

每 30 分鐘由 GitHub Actions 抓一次 <https://wstssc.com.tw/> 首頁上的健身房（與游泳池）即時人數，存進 `data/occupancy.csv`，並用 GitHub Pages 顯示熱度圖，方便挑人少的時段去。

## 檔案

| 檔案 | 用途 |
|---|---|
| `scrape.py` | 抓網頁、解析人數、追加一行到 CSV（只用標準庫） |
| `.github/workflows/scrape.yml` | 每 30 分鐘執行 `scrape.py` 並 commit 資料 |
| `data/occupancy.csv` | 累積的資料 |
| `index.html` | 視覺化頁面：最新人數、各星期最空的 5 個時段、每週熱度圖、最近 7 天折線 |

## 設定步驟（約 3 分鐘）

1. 在 GitHub 建一個新的 **Public** repository（免費帳號要 public 才能用 Pages）。
2. 把這個資料夾所有檔案上傳（包含 `.github` 資料夾）。
3. **Settings → Actions → General → Workflow permissions** 選 **Read and write permissions**，存檔。
4. **Settings → Pages → Build and deployment**：Source 選 **Deploy from a branch**，Branch 選 `main` / `(root)`，存檔。
5. **Actions** 分頁 → 左邊「抓健身房人數」→ **Run workflow** 手動跑一次確認成功。

之後打開 `https://<你的帳號>.github.io/<repo 名稱>/` 就能看。

## 注意事項

- 只記錄營業時間 06:00–22:00（台北時間）。
- GitHub 的排程在尖峰時段可能延遲或偶爾漏跑，資料不會剛好每 30 分鐘一筆，但不影響平均。
- 若 Actions 出現「頁面上找不到健身房人數」，代表網站改版，需要調整 `scrape.py` 裡的正規表示式。
- 熱度圖大約累積 2～3 週後才會比較準。
