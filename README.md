# Bot Etimo Diamonds

Etimo Diamond V2 adalah game engine yang melibatkan bot dengan logic bot masing-masing dalam persaingan dengan bot dari pemain lainnya. Setiap bot yang dimiliki oleh pemain memiliki tujuan untuk mengumpulkan sebanyak mungkin diamond dalam permainan. Namun, proses pengumpulan diamond tidak akan mudah karena terdapat berbagai rintangan yang membuat permainan menjadi menarik dan kompleks. Untuk menjadi pemenang dalam pertandingan, setiap pemain harus mengimplementasikan strategi khusus pada bot-nya agar dapat mengatasi rintangan dan mengumpulkan diamond sebanyak mungkin. Dengan demikian, kreativitas dan kecerdasan dalam merancang strategi bot akan menjadi kunci untuk meraih kemenangan dalam Diamonds.

Pada project ini kami membuat Bot dengan menerapkan beberapa Algoritma Greedy diantaranya, yaitu 
1. Langkah bot ke diamond terdekat
2. Langkah bot ke diamond terdekat melalui teleport
3. Langkah bot ke base dengan kondisi terbaik
4. Langkah bot ke base melalui teleport

## Table of Contents

- [Requirements](#requirements)
- [Command](#command)
- [Author](#author)

## Requirements

- Node.js (https://nodejs.org/en) 
- Docker desktop (https://www.docker.com/products/docker-desktop/) 
- Yarn (npm install --global yarn)
- Python

## Command

To run the game engine, follow these steps:

1. Install Node.js from [here](https://nodejs.org/en).
2. Install Docker desktop from [here](https://www.docker.com/products/docker-desktop/).
3. Install Yarn globally by running `npm install --global yarn` in your terminal.
4. Install Python.
5. Download source code pada [here](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0)
6. Masuk ke root directory dari project: `cd tubes1-IF2110-game-engine-1.1.0`.
7. Install dependencies menggunakan Yarn: `yarn`.
8. Setup default environment variable dengan menjalankan script berikut: `./scripts/copy-env.bat`.
9. Setup local database (buka aplikasi docker desktop terlebih dahulu, lalu jalankan command berikut di terminal): `docker compose up -d database`.
10. Lalu jalankan script berikut. Untuk Windows: `./scripts/setup-db-prisma.bat`.
11. Build: `npm run build`.
12. Run: `npm run start`.

To run the bot, follow these steps:

1. Download source code pada [here](https://github.com/haziqam/tubes1-IF2211-bot-starter-pack/releases/tag/v1.0.1)
2. Masuk ke root directory dari project: `cd tubes1-IF2110-bot-starter-pack-1.0.1`.
3. Install dependencies menggunakan pip: `pip install -r requirements.txt`.
4. Run:`python main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo`.
5. Run bot bersamaan:`./run-bots.bat`.


## Author

- Farhan Raditya Adji (13522142)
- Rafif Rardhinto I. (13522159)
- M. Zaidan Sa'dun R. (13522146)


