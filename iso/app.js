/* Комната памяти: параллакс, свет, предметы с историями. */

const scene = document.getElementById('scene');
const modal = document.getElementById('modal');
const modalBody = document.getElementById('modal-body');
const hint = document.getElementById('hint');
const intro = document.getElementById('intro');
const cap = document.querySelector('.cap');

/* на телефоне показываем комнату целиком, на десктопе — во весь экран */
const room = document.getElementById('room');
function fitMode() {
  const mobile = window.innerWidth <= 640;
  room.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  room.setAttribute('viewBox', mobile ? '150 30 1070 910' : '80 10 1160 900');
}
fitMode();
window.addEventListener('resize', fitMode);

const layers = [
  { el: document.getElementById('layer-back'), x: 6, y: 4 },
  { el: document.getElementById('layer-window'), x: 14, y: 9 },
  { el: document.getElementById('layer-wall'), x: 20, y: 13 },
  { el: document.getElementById('layer-shelf'), x: 26, y: 17 },
  { el: document.getElementById('layer-sideboard'), x: 34, y: 22 },
  { el: document.getElementById('layer-chair'), x: 44, y: 28 },
  { el: document.getElementById('layer-table'), x: 50, y: 32 },
  { el: document.getElementById('layer-plant'), x: 58, y: 36 },
  { el: document.getElementById('layer-dust'), x: 70, y: 44 },
];

let lightOn = false;

/* ---------------------------------------------------------------- вход --- */
document.getElementById('enter').addEventListener('click', () => {
  intro.classList.add('hidden');
  cap.classList.add('show');
  hint.classList.add('show');
  setTimeout(() => hint.classList.remove('show'), 7000);
});

/* ----------------------------------------------------------- параллакс --- */
function parallax(nx, ny) {
  layers.forEach((layer) => {
    if (!layer.el) return;
    const tx = -nx * layer.x;
    const ty = -ny * layer.y;
    layer.el.style.transform = `translate3d(${tx.toFixed(2)}px, ${ty.toFixed(2)}px, 0)`;
  });
}

window.addEventListener('mousemove', (event) => {
  const nx = event.clientX / window.innerWidth - 0.5;
  const ny = event.clientY / window.innerHeight - 0.5;
  parallax(nx, ny);
});

window.addEventListener('deviceorientation', (event) => {
  if (event.gamma === null) return;
  const nx = Math.max(-1, Math.min(1, event.gamma / 45));
  const ny = Math.max(-1, Math.min(1, (event.beta - 45) / 45));
  parallax(nx * 0.9, ny * 0.9);
}, true);

/* --------------------------------------------------------------- тосты --- */
function toast(text) {
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = text;
  document.body.append(el);
  requestAnimationFrame(() => el.classList.add('show'));
  setTimeout(() => {
    el.classList.remove('show');
    setTimeout(() => el.remove(), 450);
  }, 2200);
}

/* ---------------------------------------------------------------- свет --- */
function toggleLamp() {
  lightOn = !lightOn;
  const glow = document.getElementById('lampGlow');
  const core = document.getElementById('lampCore');
  glow.style.transition = 'opacity .9s ease';
  core.style.transition = 'opacity .9s ease';
  glow.style.opacity = lightOn ? '0.95' : '0';
  core.style.opacity = lightOn ? '0.8' : '0';
  scene.classList.toggle('night', !lightOn);
  toast(lightOn ? 'Свет включён' : 'Свет выключен');
}

/* ------------------------------------------------------------ контент --- */
const CONTENT = {
  lamp: null,

  letters: () => `
    <p class="eyebrow">Шкатулка · письма</p>
    <div class="letter">
      <p>Здравствуй, дорогая моя.</p>
      <p>Пишу тебе из дома, окно открыто, яблони уже отцвели. Крыша держится, я подлатал угол
      у крыльца. Не сердись, что редко пишу: почта идёт долго, а я всё откладываю.</p>
      <p>Внук приезжал в июне, помог с забором, наловил нам рыбы. Смеялся, что я всё ещё
      храню катушки, а я говорю: это чтобы голос остался.</p>
      <p class="sign">Твой Иван</p>
    </div>
    <p class="m-text" style="margin-top:18px">Август 1974 года. Письмо хранилось в шкатулке
    вместе с фотографиями и ключом от дома.</p>
  `,

  voice: () => `
    <p class="eyebrow">Патефон · запись голоса</p>
    <h2 class="m-title">«Чтобы голос остался»</h2>
    <div class="player">
      <button class="play" id="play" aria-label="Слушать запись">▶</button>
      <div class="wave" id="wave"></div>
    </div>
    <audio id="audio" src="../assets/voice/1974.mp3" preload="metadata"></audio>
    <div class="transcript">
      <time>Катушечная запись · осень 1974</time>
      Внук, это я. Записываю на катушечник, чтобы голос остался. Дом у реки стоит, крыша цела,
      яблони цветут. Приезжай, когда сможешь. И бабушку не забывай.
    </div>
  `,

  photos: () => `
    <p class="eyebrow">Фотографии</p>
    <h2 class="m-title">Лето в доме у реки</h2>
    <div class="gallery">
      <figure class="shot"><img src="../assets/photos/river.svg" alt="Дом у реки">
        <figcaption>Июнь 1968 · снято на «Смену»</figcaption></figure>
      <figure class="shot"><img src="../assets/photos/window.svg" alt="Окно с геранью">
        <figcaption>То же окно, герань каждого лета</figcaption></figure>
    </div>
  `,

  video: () => `
    <p class="eyebrow">Видео · 8 мм</p>
    <h2 class="m-title">Двор, записанный на плёнку</h2>
    <video class="video" src="../assets/video/archive.mp4" controls playsinline preload="metadata"></video>
    <p class="m-text" style="margin-top:14px">Фрагмент из домашнего архива. Звука нет — плёнка
    была без звука, поэтому здесь только изображение.</p>
  `,

  'letter-chair': () => `
    <p class="eyebrow">Кресло · история</p>
    <h2 class="m-title">Плед</h2>
    <p class="m-text">Зимой он всегда сидел здесь и читал вслух. Плед связала бабушка,
    локти истёрлись до лысины. Когда становится тихо, кажется, что кресло ещё держит его спину.</p>
    <p class="m-text">Такой предмет не догадается открыть сам: у него нет подсветки и подписи.
    Именно поэтому он и держит воспоминание сильнее, чем явная кнопка.</p>
  `,
};

function buildWave() {
  const wave = document.getElementById('wave');
  wave.innerHTML = '';
  for (let i = 0; i < 42; i++) {
    const bar = document.createElement('i');
    bar.style.animationDelay = `${(i * 0.03).toFixed(2)}s`;
    wave.append(bar);
  }
}

function openModal(key) {
  const render = CONTENT[key];
  if (!render) return;
  modalBody.innerHTML = render();
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');

  if (key === 'voice') {
    buildWave();
    const audio = document.getElementById('audio');
    const button = document.getElementById('play');
    const wave = document.getElementById('wave');
    button.addEventListener('click', () => {
      if (audio.paused) {
        audio.play();
        button.textContent = '❚❚';
        wave.classList.add('playing');
      } else {
        audio.pause();
        button.textContent = '▶';
        wave.classList.remove('playing');
      }
    });
    audio.addEventListener('ended', () => {
      button.textContent = '▶';
      wave.classList.remove('playing');
    });
  }
}

function closeModal() {
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
  const audio = document.getElementById('audio');
  const video = modalBody.querySelector('video');
  if (audio) audio.pause();
  if (video) video.pause();
  setTimeout(() => { modalBody.innerHTML = ''; }, 300);
}

document.querySelectorAll('.hot').forEach((hot) => {
  hot.addEventListener('click', () => {
    const key = hot.dataset.open;
    if (key === 'lamp') return toggleLamp();
    openModal(key);
  });
  hot.addEventListener('keydown', (event) => {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    event.preventDefault();
    hot.click();
  });
});

document.getElementById('close').addEventListener('click', closeModal);
modal.addEventListener('click', (event) => {
  if (event.target === modal) closeModal();
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeModal();
});
