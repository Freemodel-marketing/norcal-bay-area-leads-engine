🚀 Bay Area Real Estate Intelligence Engine
 - An automated data pipeline that extracts high-potential real estate leads from the San Francisco Bay Area, stores them in a cloud database, and visualizes them through a live web dashboard.

🛠️ System Architecture
-  The project follows a modern "Serverless" data stack:
-  Data Source: RentCast API (Filtering for properties with 30-90 days on market).
-  Automation: GitHub Actions (Scheduled Python runner).
-  Database: Supabase (PostgreSQL) for persistent cloud storage.
-  Frontend: Tailwind CSS + JavaScript hosted on Netlify.

📋 Features
-  Daily Automated Updates: Runs every day at 1:00 AM (Pacific Time) via GitHub Cron Jobs.
-  Intelligent Filtering: Targets "stale" listings (30+ days) to find motivated sellers.
-  Multi-City Support: Currently tracking San Mateo, Oakland, San Francisco, and San Jose.
-  Live Dashboard: Searchable web interface with CSV export functionality for CRM integration.

📈 Dashboard
-  The live dashboard is deployed at: https://automaticagentmarketingoutline.netlify.app/

📝 License
-  MIT License - Feel free to use and modify for your own real estate operations.
