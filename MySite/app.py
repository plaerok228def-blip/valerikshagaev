import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Валера | 3D NEON PROTOCOL</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Share+Tech+Mono&display=swap');

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        html { scroll-behavior: smooth; }

        body {
            font-family: 'Oswald', sans-serif;
            background-color: #020005;
            color: #fff;
            line-height: 1.6;
            overflow-x: hidden;
            perspective: 1000px;
            cursor: crosshair; 
        }

        #ocean-canvas {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: -1; filter: blur(80px); opacity: 0.6; pointer-events: none;
        }

        nav {
            background: rgba(3, 0, 5, 0.4); border-bottom: 1px solid rgba(157, 0, 255, 0.2);
            padding: 20px 0; position: fixed; width: 100%; top: 0; z-index: 100; backdrop-filter: blur(20px);
        }

        .nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: center; gap: 40px; }

        nav a {
            color: #a899b3; text-decoration: none; font-family: 'Share Tech Mono', monospace;
            font-size: 16px; text-transform: uppercase; letter-spacing: 2px;
            transition: all 0.3s ease; position: relative;
        }

        nav a:hover { color: #fff; text-shadow: 0 0 15px #9d00ff; }
        
        .ticker-wrap {
            width: 100%; overflow: hidden; background-color: #9d00ff; color: #000;
            padding: 10px 0; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;
            border-bottom: 2px solid #fff; box-shadow: 0 0 30px rgba(157, 0, 255, 0.8);
            margin-top: 65px; position: relative; z-index: 10;
        }
        .ticker {
            display: inline-block; white-space: nowrap; animation: ticker 20s linear infinite;
            font-family: 'Share Tech Mono', monospace; font-size: 14px;
        }
        @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-50%, 0, 0); } }

        section {
            min-height: 100vh; padding: 120px 20px; display: flex; flex-direction: column;
            justify-content: center; align-items: center; position: relative;
        }

        .container { max-width: 1200px; width: 100%; position: relative; z-index: 2; }

        .section-title {
            font-size: 50px; margin-bottom: 50px; text-transform: uppercase;
            border-bottom: 2px solid #9d00ff; padding-bottom: 15px; display: inline-block;
            text-shadow: 0 0 20px rgba(157, 0, 255, 0.5); animation: neon-pulse 2s infinite alternate;
        }

        @keyframes neon-pulse {
            0% { text-shadow: 0 0 10px rgba(157, 0, 255, 0.3); }
            100% { text-shadow: 0 0 30px rgba(157, 0, 255, 0.8), 0 0 10px #fff; }
        }

        .reveal { opacity: 0; transform: translateY(50px); transition: all 1s cubic-bezier(0.2, 0.8, 0.2, 1); }
        .reveal.active { opacity: 1; transform: translateY(0); }

        .hero-title { font-size: 120px; line-height: 0.9; text-shadow: 0 0 30px #9d00ff, 5px 5px 0px #2a004a; margin-bottom: 20px; text-align: center;}
        .hero-sub { font-family: 'Share Tech Mono', monospace; color: #d48aff; font-size: 20px; letter-spacing: 5px; margin-bottom: 20px; text-align: center;}
        .hero-text { font-family: 'Share Tech Mono'; color: #ccc; max-width: 700px; margin: 0 auto; font-size: 20px; text-align: center;}

        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
        
        .glass-card {
            background: rgba(10, 0, 20, 0.6); 
            border: 1px solid rgba(157, 0, 255, 0.3); 
            padding: 40px; border-radius: 15px;
            backdrop-filter: blur(15px); 
            box-shadow: 0 15px 35px rgba(0,0,0,0.6);
            transition: transform 0.1s ease, box-shadow 0.3s ease, border-color 0.3s ease;
            transform-style: preserve-3d;
            position: relative;
            will-change: transform;
        }

        .glass-card:hover {
            box-shadow: 0 0 50px rgba(157, 0, 255, 0.5), inset 0 0 20px rgba(157, 0, 255, 0.2);
            border-color: #d48aff;
        }

        .card-content { transform: translateZ(30px); }

        .glass-card h3 { 
            color: #d48aff; font-size: 28px; margin-bottom: 20px; font-family: 'Share Tech Mono', monospace;
            transition: text-shadow 0.3s; 
        }
        
        .glass-card:hover h3 { text-shadow: 0 0 15px #9d00ff; }

        .glass-card p { 
            font-family: 'Share Tech Mono', monospace; color: #a899b3; font-size: 16px;
        }

        .stats-grid {
            display: grid; grid-template-columns: repeat(3, 1fr);
            background: rgba(10, 0, 20, 0.7); border: 1px solid #9d00ff;
            padding: 40px; text-align: center; gap: 20px; border-radius: 15px;
            box-shadow: 0 0 40px rgba(157, 0, 255, 0.15); backdrop-filter: blur(10px);
        }
        .stat-item h2 { font-size: 70px; text-shadow: 0 0 25px #9d00ff; font-family: 'Share Tech Mono', monospace;}
        .stat-item p { color: #d48aff; font-family: 'Share Tech Mono', monospace; text-transform: uppercase; letter-spacing: 2px;}

        .barcode-visual {
            width: 100%; height: 120px; margin: 30px 0;
            background: repeating-linear-gradient(90deg, #fff 0, #fff 2px, #000 2px, #000 6px, #fff 6px, #fff 10px, #000 10px, #000 12px, #fff 12px, #fff 16px, #000 16px, #000 20px, #fff 20px, #fff 22px);
            border: 10px solid #000; box-shadow: 0 0 40px rgba(157, 0, 255, 0.5);
        }

        .photo-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .photo-card { background: rgba(8, 0, 15, 0.7); border: 1px solid #2a004a; padding: 10px; border-radius: 10px; transition: all 0.3s; backdrop-filter: blur(5px);}
        .photo-card:hover { border-color: #9d00ff; box-shadow: 0 0 30px rgba(157, 0, 255, 0.4); transform: scale(1.05);}
        .photo-img { width: 100%; height: 250px; object-fit: cover; display: block; filter: grayscale(70%); transition: filter 0.3s;}
        .photo-card:hover .photo-img { filter: grayscale(0%); }
        .photo-caption { text-align: center; padding: 15px; color: #d48aff; font-family: 'Share Tech Mono', monospace; text-transform: uppercase;}

        footer {
            text-align: center; padding: 40px; border-top: 1px solid rgba(157, 0, 255, 0.2);
            font-family: 'Share Tech Mono', monospace; color: #888; background: #020005; position: relative; z-index: 10;
        }

        @media (max-width: 768px) {
            .hero-title { font-size: 60px; }
            .stats-grid { grid-template-columns: 1fr; }
            .nav-container { gap: 15px; }
            nav a { font-size: 12px; }
            .glass-card { transform: none !important; }
        }
    </style>
</head>
<body>

    <canvas id="ocean-canvas"></canvas>

    <nav>
        <div class="nav-container">
            <a href="#home">Главная</a>
            <a href="#dossier">Досье</a>
            <a href="#optics">Оптика</a>
            <a href="#archive">Архив</a>
            <a href="#contact">Связь</a>
        </div>
    </nav>

    <div class="ticker-wrap">
        <div class="ticker">
            СИСТЕМА АКТИВИРОВАНА // НЕОНОВЫЙ ПРОТОКОЛ // ВАЛЕРА ШАГАЕВСКИЙ // 13 МИНУТ ДО СИНГУЛЯРНОСТИ // СНАЙПЕРЫ ОБНАРУЖЕНЫ // &nbsp;&nbsp;&nbsp; СИСТЕМА АКТИВИРОВАНА // НЕОНОВЫЙ ПРОТОКОЛ // ВАЛЕРА ШАГАЕВСКИЙ // 13 МИНУТ ДО СИНГУЛЯРНОСТИ // СНАЙПЕРЫ ОБНАРУЖЕНЫ //
        </div>
    </div>

    <section id="home">
        <div class="container reveal">
            <div class="hero-sub">[ LOCAL_LEGEND: OVERRIDE_ACTIVE ]</div>
            <h1 class="hero-title">Валера<br>Шагаевский</h1>
            <p class="hero-text">
                Тот, кто не поддается законам физики. Его тренировка — это 13 минут чистого хаоса. Снайперы пытаются поймать его в прицел уже 15 лет, но видят лишь неоновый след.
            </p>
        </div>
    </section>

    <section id="dossier">
        <div class="container">
            <h1 class="section-title reveal">// Досье</h1>
            <div class="stats-grid reveal" style="margin-bottom: 50px;">
                <div class="stat-item">
                    <h2>13</h2>
                    <p>Минут до выхода</p>
                </div>
                <div class="stat-item">
                    <h2>15</h2>
                    <p>Лет вне матрицы</p>
                </div>
                <div class="stat-item">
                    <h2>0</h2>
                    <p>Попаданий</p>
                </div>
            </div>
            <div class="grid">
                <div class="glass-card reveal card-tilt">
                    <div class="card-content">
                        <h3>Протокол «13 минут»</h3>
                        <p>Это не просто время тренировки. Это строго закодированный алгоритм. За 13 минут Валера успевает войти в зал, синхронизироваться с нейросетью тренажеров, понять, что сегодня день отдыха, и покинуть объект до того, как система безопасности успеет заблокировать двери.</p>
                    </div>
                </div>
                <div class="glass-card reveal card-tilt">
                    <div class="card-content">
                        <h3>Фантомный режим</h3>
                        <p>Вот уже 15 лет лучшие стрелки планеты пытаются вычислить его траекторию. Они используют тепловизоры, спутники и дроны. Но Валера движется по законам квантовой физики — он одновременно везде и нигде.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="optics">
        <div class="container reveal" style="text-align: center;">
            <h1 class="section-title">// Оптический камуфляж</h1>
            <div class="glass-card card-tilt" style="max-width: 800px; margin: 0 auto;">
                <div class="card-content">
                    <p style="margin-bottom: 20px;">Его коронная стрижка — это не просто стиль, а оптический камуфляж. Рисунок на его голове сбивает системы наведения.</p>
                    <div class="barcode-visual"></div>
                    <p style="color: #fff; letter-spacing: 5px; font-size: 24px; text-shadow: 0 0 10px #9d00ff;">ШТРИХ-КОД АКТИВЕН</p>
                    <p style="margin-top: 20px;">Снайперы видят не человека, а лишь набор белых и черных полос, что дает Валере преимущество в несколько миллисекунд для ухода в неон.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="archive">
        <div class="container">
            <h1 class="section-title reveal">// Фотоархив</h1>
            <div class="photo-grid">
                <!-- ВАЖНО: Фото должны лежать в папке static с именами 1.jpg, 2.jpg и т.д. -->
                <div class="photo-card reveal">
                    <img src="/static/1.jpg" alt="Фото 1" class="photo-img">
                    <div class="photo-caption">Кадр 1: Выход в неон</div>
                </div>
                <div class="photo-card reveal">
                    <img src="/static/2.jpg" alt="Фото 2" class="photo-img">
                    <div class="photo-caption">Кадр 2: Уклонение от пули</div>
                </div>
                <div class="photo-card reveal">
                    <img src="/static/3.jpg" alt="Фото 3" class="photo-img">
                    <div class="photo-caption">Кадр 3: Синхронизация</div>
                </div>
                <div class="photo-card reveal">
                    <img src="/static/4.jpg" alt="Фото 4" class="photo-img">
                    <div class="photo-caption">Кадр 4: Стрижка в профиль</div>
                </div>
                <div class="photo-card reveal">
                    <img src="/static/5.jpg" alt="Фото 5" class="photo-img">
                    <div class="photo-caption">Кадр 5: Снайпер промахнулся</div>
                </div>
                <div class="photo-card reveal">
                    <img src="/static/6.jpg" alt="Фото 6" class="photo-img">
                    <div class="photo-caption">Кадр 6: Уход в закат</div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact">
        <div class="container reveal" style="text-align: center;">
            <h1 class="section-title">// Связь</h1>
            <div class="glass-card card-tilt" style="max-width: 800px; margin: 0 auto;">
                <div class="card-content">
                    <p>Прямая линия с Валерой закрыта по соображениям безопасности. Любая попытка отследить его сигнал будет заблокирована оптическим камуфляжем.</p>
                    <p>Если вам жизненно необходимо передать информацию, оставьте её в анонимном терминале. Но помните: даже здесь за вами могут наблюдать.</p>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <p>[ WARNING: THIS IS A JOKE / ШУТОЧНЫЙ ФОРМАТ ]</p>
        <p>2026 // 3D NEON PROTOCOL</p>
    </footer>

    <script>
        const tiltCards = document.querySelectorAll('.card-tilt');
        tiltCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = ((y - centerY) / centerY) * -10; 
                const rotateY = ((x - centerX) / centerX) * 10;  
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
            });
        });

        document.addEventListener("DOMContentLoaded", function() {
            const reveals = document.querySelectorAll('.reveal');
            const revealOnScroll = () => {
                const windowHeight = window.innerHeight;
                const elementVisible = 100;
                reveals.forEach((reveal) => {
                    const elementTop = reveal.getBoundingClientRect().top;
                    if (elementTop < windowHeight - elementVisible) {
                        reveal.classList.add('active');
                    }
                });
            };
            window.addEventListener('scroll', revealOnScroll);
            revealOnScroll();
        });

        const canvas = document.getElementById('ocean-canvas');
        const ctx = canvas.getContext('2d');
        
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        const colors = [
            'rgba(157, 0, 255, 0.5)',
            'rgba(0, 150, 255, 0.4)',
            'rgba(255, 0, 150, 0.4)',
            'rgba(100, 0, 200, 0.5)'
        ];

        let blobs = [];
        function initBlobs() {
            blobs = [];
            for(let i = 0; i < 8; i++) {
                blobs.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    radius: Math.random() * 300 + 200,
                    vx: (Math.random() - 0.5) * 0.4,
                    vy: (Math.random() - 0.5) * 0.4,
                    color: colors[Math.floor(Math.random() * colors.length)]
                });
            }
        }
        initBlobs();

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            initBlobs();
        });

        function animateOcean() {
            ctx.clearRect(0, 0, width, height);
            blobs.forEach(blob => {
                blob.x += blob.vx;
                blob.y += blob.vy;
                if (blob.x < -blob.radius) blob.x = width + blob.radius;
                if (blob.x > width + blob.radius) blob.x = -blob.radius;
                if (blob.y < -blob.radius) blob.y = height + blob.radius;
                if (blob.y > height + blob.radius) blob.y = -blob.radius;
                let gradient = ctx.createRadialGradient(blob.x, blob.y, 0, blob.x, blob.y, blob.radius);
                gradient.addColorStop(0, blob.color);
                gradient.addColorStop(1, 'transparent');
                ctx.beginPath();
                ctx.fillStyle = gradient;
                ctx.arc(blob.x, blob.y, blob.radius, 0, Math.PI * 2);
                ctx.fill();
            });
            requestAnimationFrame(animateOcean);
        }
        animateOcean();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)