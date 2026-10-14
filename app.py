
from flask import Flask, render_template_string, request
import joblib

app = Flask(__name__)

# Memuat model AI yang sudah dilatih
model = joblib.load("text_model.pkl")


HTML = r"""
<!DOCTYPE html>
<html lang="id" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#f7f9fc">
    <title>Detectra — Deteksi Pola Teks AI</title>

    <script>
        // Terapkan tema tersimpan sebelum halaman ditampilkan
        try {
            const savedTheme = localStorage.getItem("detectra-theme");
            if (savedTheme === "dark" || savedTheme === "light") {
                document.documentElement.dataset.theme = savedTheme;
            }
        } catch (error) {}
    </script>

    <style>
        :root {
            color-scheme: light;
            --bg: #f7f9fc;
            --surface: #ffffff;
            --surface-soft: #f0f5f7;
            --text: #172b35;
            --muted: #647681;
            --border: #e0e8ec;
            --primary: #0f766e;
            --primary-hover: #115e59;
            --primary-soft: #e0f2f1;
            --hero-glow: #e5f5f3;
            --shadow: 0 8px 30px rgba(20, 50, 60, 0.05);
        }
        
        .textarea-wrapper {
            position: relative;
        }

        .textarea-wrapper textarea {
            padding-bottom: 48px;
        }

        .clear-button {
            position: absolute;
            right: 12px;
            bottom: 12px;
            padding: 6px 10px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--surface);
            color: var(--muted);
            font-size: 12px;
            cursor: pointer;
            display: none;
        }

        .clear-button:hover {
            background: var(--surface-soft);
            color: var(--text);
        }

        .clear-button.visible {
            display: block;
        }

        html[data-theme="dark"] {
            color-scheme: dark;
            --bg: #111820;
            --surface: #1b2530;
            --surface-soft: #222f3b;
            --text: #edf4f6;
            --muted: #a4b4bd;
            --border: #34434f;
            --primary: #5eead4;
            --primary-hover: #99f6e4;
            --primary-soft: #203e3d;
            --hero-glow: #1b3033;
            --shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }

        * {
            box-sizing: border-box;
            scroll-behavior: smooth;
        }

        body {
            margin: 0;
            background: var(--bg);
            color: var(--text);
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.65;
            transition: background 0.2s, color 0.2s;
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        button, textarea {
            font: inherit;
        }

        button, a {
            -webkit-tap-highlight-color: transparent;
        }

        .container {
            width: min(1080px, calc(100% - 40px));
            margin: 0 auto;
        }

        .navbar {
            position: sticky;
            top: 0;
            z-index: 10;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
        }

        .nav-inner {
            min-height: 72px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 21px;
            font-weight: 800;
            letter-spacing: -0.7px;
        }

        .brand-icon {
            width: 38px;
            height: 38px;
            display: grid;
            place-items: center;
            border-radius: 11px;
            background: var(--primary);
            color: #ffffff;
            font-size: 21px;
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 26px;
            font-size: 14px;
            color: var(--muted);
        }

        .nav-links a:hover {
            color: var(--primary);
        }

        .theme-toggle {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 9px 13px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--surface);
            color: var(--text);
            cursor: pointer;
            white-space: nowrap;
        }

        .theme-toggle:hover {
            background: var(--surface-soft);
        }

        .hero {
            padding: 76px 0 68px;
            background:
                radial-gradient(ellipse at 85% 10%, var(--hero-glow), transparent 42%),
                var(--bg);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            align-items: center;
            gap: 56px;
        }

        .eyebrow {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 30px;
            background: var(--primary-soft);
            color: var(--primary);
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        h1, h2, h3, p {
            margin-top: 0;
        }

        h1 {
            margin: 20px 0 18px;
            font-size: clamp(36px, 5vw, 54px);
            line-height: 1.12;
            letter-spacing: -2px;
        }

        .hero p {
            max-width: 570px;
            color: var(--muted);
            font-size: 17px;
        }

        .button {
            display: inline-flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            padding: 12px 19px;
            border: 1px solid transparent;
            border-radius: 10px;
            background: var(--primary);
            color: #ffffff;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.15s, background 0.15s;
        }

        .button:hover {
            transform: translateY(-1px);
            background: var(--primary-hover);
        }

        html[data-theme="dark"] .button {
            color: #102522;
        }

        
        .button-outline {
    background: transparent;
    border-color: var(--border);
    color: var(--primary);
}

        .button-outline:hover {
            background: var(--primary);
            border-color: var(--primary);
            color: #ffffff;
        }

        html[data-theme="dark"] .button-outline:hover {
            color: #102522;
        }

        .hero-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 27px;
        }

        .hero-note {
            margin-top: 20px;
            color: var(--muted);
            font-size: 12px;
        }

        .hero-card {
            padding: 27px;
            border: 1px solid var(--border);
            border-radius: 20px;
            background: var(--surface);
            box-shadow: var(--shadow);
        }

        .preview-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            padding-bottom: 18px;
            border-bottom: 1px solid var(--border);
        }

        .preview-title {
            font-weight: 700;
        }

        .status {
            padding: 4px 9px;
            border-radius: 20px;
            background: var(--primary-soft);
            color: var(--primary);
            font-size: 11px;
            font-weight: 700;
        }

        .preview-document {
            margin: 24px 0;
            padding: 18px;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: var(--surface-soft);
        }

        .fake-line {
            height: 8px;
            margin: 11px 0;
            border-radius: 10px;
            background: var(--border);
        }

        .fake-line.short {
            width: 62%;
        }

        .preview-result {
            padding: 15px;
            border-radius: 12px;
            background: var(--primary-soft);
        }

        .preview-result small {
            color: var(--muted);
        }

        .preview-result strong {
            display: block;
            margin-top: 4px;
            color: var(--primary);
            font-size: 21px;
        }

        .section {
            padding: 76px 0;
            scroll-margin-top: 85px;
        }

        .section-alt {
            background: var(--surface-soft);
        }

        .section-heading {
            max-width: 650px;
            margin: 0 auto 36px;
            text-align: center;
        }

        .section-heading h2 {
            margin-bottom: 10px;
            font-size: clamp(27px, 4vw, 36px);
            letter-spacing: -1px;
        }

        .section-heading p {
            margin-bottom: 0;
            color: var(--muted);
        }

        .detector-card {
            max-width: 820px;
            margin: 0 auto;
            padding: 30px;
            border: 1px solid var(--border);
            border-radius: 18px;
            background: var(--surface);
            box-shadow: var(--shadow);
        }

        .field-label {
            display: block;
            margin-bottom: 9px;
            font-weight: 700;
        }

        textarea {
            display: block;
            width: 100%;
            min-height: 210px;
            resize: vertical;
            padding: 16px;
            border: 1px solid var(--border);
            border-radius: 12px;
            outline: none;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
        }

        textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-soft);
        }

        textarea::placeholder {
            color: var(--muted);
            opacity: 0.8;
        }

        .input-hint {
            margin: 10px 0 18px;
            color: var(--muted);
            font-size: 13px;
        }

        .submit-button {
            width: 100%;
        }

        .error-message {
            margin: 0 0 16px;
            padding: 12px 14px;
            border: 1px solid #e7a7a7;
            border-radius: 10px;
            background: #fff0f0;
            color: #922b2b;
        }

        .result-card {
            max-width: 820px;
            margin: 24px auto 0;
            padding: 26px;
            border: 1px solid var(--border);
            border-radius: 18px;
            background: var(--surface);
            box-shadow: var(--shadow);
        }

        .result-heading {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 14px;
            margin-bottom: 22px;
        }

        .result-heading h3 {
            margin-bottom: 5px;
        }

        .result-heading p {
            margin: 0;
            color: var(--muted);
            font-size: 13px;
        }

        .result-label {
            display: inline-block;
            margin-top: 10px;
            padding: 7px 12px;
            border-radius: 8px;
            background: var(--primary-soft);
            color: var(--primary);
            font-weight: 700;
        }

        .score-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .score-box {
            padding: 18px;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: var(--bg);
        }

        .score-top {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 12px;
            font-size: 14px;
        }

        .score-number {
            font-weight: 800;
            font-size: 19px;
        }

        .progress {
            height: 8px;
            overflow: hidden;
            border-radius: 10px;
            background: var(--border);
        }

        .progress-fill {
            height: 100%;
            border-radius: 10px;
            background: var(--primary);
        }

        .notice {
            margin: 20px 0 0;
            padding: 14px;
            border-radius: 10px;
            background: var(--surface-soft);
            color: var(--muted);
            font-size: 13px;
        }

        .steps {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .info-card {
            padding: 24px;
            border: 1px solid var(--border);
            border-radius: 15px;
            background: var(--surface);
        }

        .step-number {
            display: grid;
            width: 42px;
            height: 42px;
            place-items: center;
            margin-bottom: 17px;
            border-radius: 12px;
            background: var(--primary-soft);
            color: var(--primary);
            font-weight: 800;
        }

        .info-card h3 {
            margin-bottom: 9px;
            font-size: 18px;
        }

        .info-card p {
            margin-bottom: 0;
            color: var(--muted);
            font-size: 14px;
        }

        .about-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .about-card {
            padding: 26px;
            border: 1px solid var(--border);
            border-radius: 15px;
            background: var(--surface);
        }

        .about-card h3 {
            margin-bottom: 12px;
        }

        .about-card p,
        .about-card li {
            color: var(--muted);
            font-size: 14px;
        }

        .about-card ul {
            padding-left: 20px;
            margin-bottom: 0;
        }

        footer {
            padding: 27px 0;
            border-top: 1px solid var(--border);
            background: var(--surface);
            color: var(--muted);
            font-size: 13px;
        }

        .footer-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
        }

        @media (max-width: 760px) {
            .nav-inner {
                flex-wrap: wrap;
                padding: 13px 0;
                gap: 12px;
            }

            .nav-links {
                order: 3;
                width: 100%;
                justify-content: space-between;
                gap: 10px;
                font-size: 12px;
            }

            .theme-toggle {
                margin-left: auto;
                padding: 8px 10px;
                font-size: 12px;
            }

            .hero {
                padding: 48px 0;
            }

            .hero-grid {
                grid-template-columns: 1fr;
                gap: 30px;
            }

            .hero-card {
                max-width: 500px;
            }

            .section {
                padding: 55px 0;
            }

            .steps,
            .about-grid {
                grid-template-columns: 1fr;
            }

            .detector-card,
            .result-card {
                padding: 20px;
            }

            .footer-inner {
                flex-direction: column;
                align-items: flex-start;
            }
        }

        @media (max-width: 420px) {
            .container {
                width: min(100% - 28px, 1080px);
            }

            h1 {
                letter-spacing: -1px;
            }

            .score-grid {
                grid-template-columns: 1fr;
            }

            .result-heading {
                flex-direction: column;
            }

            .hero-actions .button {
                width: 100%;
            }
        }
    </style>
</head>

<body>
    <header class="navbar">
        <div class="container nav-inner">
            <a class="brand" href="#beranda" aria-label="Detectra - Beranda">
                <span class="brand-icon">D</span>
                <span>Detectra</span>
            </a>

            <nav class="nav-links" aria-label="Navigasi utama">
                <a href="#beranda">Beranda</a>
                <a href="#deteksi">Deteksi Teks</a>
                <a href="#cara-kerja">Cara Kerja</a>
                <a href="#tentang">Tentang</a>
            </nav>

            <button class="theme-toggle" id="themeToggle" type="button"
                    aria-label="Ganti tema">
                <span id="themeIcon">☾</span>
                <span id="themeLabel">Mode gelap</span>
            </button>
        </div>
    </header>

    <main>
        <section class="hero" id="beranda">
            <div class="container hero-grid">
                <div>
                    <span class="eyebrow">ALAT ANALISIS TEKS</span>
                    <h1>Kenali pola di balik sebuah teks.</h1>
                    <p>
                        Detectra membantu menganalisis apakah pola sebuah teks
                        lebih menyerupai tulisan manusia atau teks yang dibuat
                        oleh AI. Caranya sederhana: masukkan teks, lalu lihat
                        hasil analisisnya.
                    </p>

                    <div class="hero-actions">
                        <a class="button" href="#deteksi">Mulai Deteksi ↓</a>

                        <a class="button button-outline" href="#cara-kerja"
                        style="color: var(--primary);">
                            Pelajari Cara Kerja
                        </a>
                    </div>
                    
                    <div class="hero-note">
                        Prototipe akademik · Analisis teks Bahasa Indonesia
                    </div>
                </div>

                <div class="hero-card" aria-label="Ilustrasi proses analisis teks">
                    <div class="preview-top">
                        <span class="preview-title">Pratinjau Analisis</span>
                        <span class="status">Contoh</span>
                    </div>

                    <div class="preview-document">
                        <div class="fake-line"></div>
                        <div class="fake-line"></div>
                        <div class="fake-line short"></div>
                        <div class="fake-line"></div>
                        <div class="fake-line short"></div>
                    </div>

                    <div class="preview-result">
                        <small>Hasil akan ditampilkan setelah analisis</small>
                        <strong>Prediksi pola teks</strong>
                    </div>
                </div>
            </div>
        </section>

        <section class="section" id="deteksi">
            <div class="container">
                <div class="section-heading">
                    <h2>Coba deteksi teksmu</h2>
                    <p>
                        Tempelkan teks yang ingin diperiksa. Detectra akan
                        membandingkan pola teks tersebut dengan pola yang
                        dipelajari selama pelatihan.
                    </p>
                </div>

                <div class="detector-card">
                    <form method="POST" action="#hasil">
                        <label class="field-label" for="text">
                            Teks yang ingin dianalisis
                        </label>

                <div class="textarea-wrapper">
                    <textarea
                        id="text"
                        name="text"
                        placeholder="Tempelkan teks Bahasa Indonesia di sini..."
                        required>{{ text }}</textarea>

                    <button
                        type="button"
                        id="clearText"
                        class="clear-button"
                        aria-label="Hapus semua teks"
                        title="Hapus semua teks">
                        ✕ Clear
                    </button>
                </div>

                        <p class="input-hint">
                            Gunakan teks yang cukup panjang agar model memiliki
                            lebih banyak informasi untuk dianalisis.
                        </p>

                        {% if error %}
                            <div class="error-message" role="alert">
                                {{ error }}
                            </div>
                        {% endif %}

                        <button class="button submit-button" type="submit">
                            Analisis Teks
                        </button>
                    </form>
                </div>

                {% if result %}
                <div class="result-card" id="hasil">
                    <div class="result-heading">
                        <div>
                            <h3>Hasil Analisis</h3>
                            <p>Berikut adalah prediksi model untuk teks yang dimasukkan.</p>
                            <div class="result-label">{{ result }}</div>
                        </div>
                        <span class="status">Analisis selesai</span>
                    </div>

                    <div class="score-grid">
                        <div class="score-box">
                            <div class="score-top">
                                <span>Kecenderungan AI</span>
                                <span class="score-number">{{ ai_score }}%</span>
                            </div>
                            <div class="progress">
                                <div class="progress-fill"
                                     style="width: {{ ai_score }}%"></div>
                            </div>
                        </div>

                        <div class="score-box">
                            <div class="score-top">
                                <span>Kecenderungan manusia</span>
                                <span class="score-number">{{ human_score }}%</span>
                            </div>
                            <div class="progress">
                                <div class="progress-fill"
                                     style="width: {{ human_score }}%"></div>
                            </div>
                        </div>
                    </div>

                    <p class="notice">
                        <strong>Perlu diketahui:</strong> persentase ini adalah
                        keluaran model, bukan kepastian atau bukti siapa yang
                        menulis teks. Akurasi 96,65% diperoleh pada pengujian
                        dataset proyek dan belum menjamin kinerja pada semua
                        jenis teks di dunia nyata.
                    </p>
                </div>
                {% endif %}
            </div>
        </section>

        <section class="section section-alt" id="cara-kerja">
            <div class="container">
                <div class="section-heading">
                    <h2>Bagaimana Detectra bekerja?</h2>
                    <p>
                        Sistem menggunakan dua tahap utama untuk mempelajari
                        pola teks dan membuat prediksi.
                    </p>
                </div>

                <div class="steps">
                    <article class="info-card">
                        <div class="step-number">01</div>
                        <h3>Masukkan teks</h3>
                        <p>
                            Pengguna menempelkan teks ke kolom deteksi dan
                            menekan tombol Analisis Teks.
                        </p>
                    </article>

                    <article class="info-card">
                        <div class="step-number">02</div>
                        <h3>TF-IDF</h3>
                        <p>
                            TF-IDF mengubah kata dan kombinasi kata menjadi
                            angka agar pola teks dapat diproses oleh model.
                        </p>
                    </article>

                    <article class="info-card">
                        <div class="step-number">03</div>
                        <h3>Logistic Regression</h3>
                        <p>
                            Model mempelajari pola dari data pelatihan, lalu
                            menghasilkan prediksi kecenderungan AI atau manusia.
                        </p>
                    </article>
                </div>
            </div>
        </section>

        <section class="section" id="tentang">
            <div class="container">
                <div class="section-heading">
                    <h2>Tentang Detectra</h2>
                    <p>
                        Mengenal teknologi yang digunakan dan hal-hal yang
                        perlu dipahami ketika membaca hasil deteksi.
                    </p>
                </div>

                <div class="about-grid">
                    <article class="about-card">
                        <h3>Teknologi yang digunakan</h3>
                        <ul>
                            <li>Python dan Flask untuk aplikasi web.</li>
                            <li>TF-IDF untuk ekstraksi fitur teks.</li>
                            <li>Logistic Regression untuk klasifikasi.</li>
                            <li>Scikit-learn untuk pemrosesan dan pelatihan model.</li>
                        </ul>
                    </article>

                    <article class="about-card">
                        <h3>Evaluasi dan keterbatasan</h3>
                        <p>
                            Pada pengujian awal, model memperoleh akurasi
                            96,65% dari 448 sampel pengujian yang dipisahkan
                            dari dataset proyek.
                        </p>
                        <p>
                            Dataset ini menggunakan teks manusia dari Wikipedia
                            dan teks AI yang dihasilkan model Gemma. Perbedaan
                            sumber dan gaya penulisan dapat memengaruhi hasil.
                        </p>
                        <p>
                            Karena itu, angka pengujian tersebut bukan jaminan
                            akurasi pada teks lain. Hasil Detectra sebaiknya
                            digunakan sebagai indikasi awal, bukan sebagai
                            satu-satunya dasar untuk menilai penulis teks.
                        </p>
                    </article>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <div class="container footer-inner">
            <span><strong>Detectra</strong> — Prototipe deteksi pola teks AI</span>
            <span>Dibuat untuk proyek akademik Kecerdasan Buatan.</span>
        </div>
    </footer>

    <script>
        const themeToggle = document.getElementById("themeToggle");
        const themeIcon = document.getElementById("themeIcon");
        const themeLabel = document.getElementById("themeLabel");
        const root = document.documentElement;

        function updateThemeButton() {
            const isDark = root.dataset.theme === "dark";

            themeIcon.textContent = isDark ? "☀" : "☾";
            themeLabel.textContent = isDark ? "Mode terang" : "Mode gelap";
            themeToggle.setAttribute(
                "aria-label",
                isDark ? "Aktifkan mode terang" : "Aktifkan mode gelap"
            );
        }

        themeToggle.addEventListener("click", function () {
            const nextTheme =
                root.dataset.theme === "dark" ? "light" : "dark";

            root.dataset.theme = nextTheme;

            try {
                localStorage.setItem("detectra-theme", nextTheme);
            } catch (error) {
                // Tema tetap bisa diganti meskipun penyimpanan tidak tersedia.
            }

            updateThemeButton();
        });

        updateThemeButton();
        
        const textArea = document.getElementById("text");
        const clearButton = document.getElementById("clearText");

        function updateClearButton() {
            clearButton.classList.toggle(
                "visible",
                textArea.value.length > 0
            );
        }

        textArea.addEventListener("input", updateClearButton);

        
        
        clearButton.addEventListener("click", function () {
            // Hapus teks input
            textArea.value = "";

            // Hapus hasil analisis sebelumnya
            const resultSection = document.querySelector(".result-card");

            if (resultSection) {
                resultSection.remove();
            }

            // Hapus pesan error jika ada
            const errorMessage = document.querySelector(".error-message");

            if (errorMessage) {
                errorMessage.remove();
            }

            updateClearButton();
            textArea.focus();
        });

        // Tampilkan tombol jika teks masih terisi setelah analisis
        updateClearButton();

    </script>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    text = ""
    result = ""
    error = ""
    ai_score = 0
    human_score = 0

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if not text:
            error = "Masukkan teks terlebih dahulu sebelum melakukan analisis."
        else:
            try:
                # Mengambil probabilitas dari model
                probabilities = model.predict_proba([text])[0]
                scores = dict(zip(model.classes_, probabilities))

                ai_score = round(float(scores.get("ai", 0)) * 100, 2)
                human_score = round(float(scores.get("human", 0)) * 100, 2)

                # Menentukan kelas dengan skor tertinggi
                prediction = model.predict([text])[0]

                if prediction == "ai":
                    result = "Cenderung AI"
                else:
                    result = "Cenderung manusia"

            except Exception as e:
                app.logger.exception("Analisis teks gagal")
                error = (
                    "Analisis belum berhasil. Periksa model dan format "
                    "data yang digunakan, lalu coba kembali."
                )

    return render_template_string(
        HTML,
        text=text,
        result=result,
        error=error,
        ai_score=ai_score,
        human_score=human_score,
    )


if __name__ == "__main__":
    app.run(debug=True)
