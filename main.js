gsap.registerPlugin(ScrollTrigger);

// ═══ Loading Screen ═══
const loader = document.getElementById('loader');
const loaderProgress = document.getElementById('loader-progress');
const loaderText = document.getElementById('loader-text');

// ═══ Hero Canvas Scroll Animation ═══
const canvas = document.getElementById("hero-lightpass");
const context = canvas.getContext("2d");

const frameCount = 240;
const currentFrame = index => (
  `assets/frames/frame_${(index + 1).toString().padStart(4, '0')}.jpg`
);

const images = [];
const airpods = {
  frame: 0
};

let loadedCount = 0;

for (let i = 0; i < frameCount; i++) {
  const img = new Image();
  img.onload = () => {
    loadedCount++;
    const pct = Math.round((loadedCount / frameCount) * 100);
    if (loaderProgress) loaderProgress.style.width = pct + '%';
    if (loaderText) loaderText.textContent = pct + '%';

    // First frame loaded — draw it immediately
    if (loadedCount === 1) render();

    // All frames loaded — hide loader
    if (loadedCount === frameCount) {
      setTimeout(() => {
        loader.classList.add('hidden');
        // Refresh ScrollTrigger after loader is gone
        ScrollTrigger.refresh();
      }, 300);
    }
  };
  img.src = currentFrame(i);
  images.push(img);
}

gsap.to(airpods, {
  frame: frameCount - 1,
  snap: "frame",
  ease: "none",
  scrollTrigger: {
    trigger: ".content",
    start: "top top",
    end: "bottom bottom",
    scrub: 1
  },
  onUpdate: render
});

function render() {
  if(!images[airpods.frame]) return;
  
  const img = images[airpods.frame];
  
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
  const hRatio = canvas.width / img.width;
  const vRatio = canvas.height / img.height;
  const ratio = Math.min(hRatio, vRatio);
  const centerShift_x = (canvas.width - img.width * ratio) / 2;
  const centerShift_y = (canvas.height - img.height * ratio) / 2;  
  
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.drawImage(img, 0, 0, img.width, img.height,
                      centerShift_x, centerShift_y, img.width * ratio, img.height * ratio); 
}

// ═══ GSAP: Fade in hero text boxes ═══
const textBoxes = document.querySelectorAll(".text-box");
textBoxes.forEach((box) => {
    gsap.to(box, {
        opacity: 1,
        y: 0,
        duration: 1,
        scrollTrigger: {
            trigger: box,
            start: "top 70%",
            end: "bottom 30%",
            toggleActions: "play reverse play reverse"
        }
    });
});

// ═══ GSAP: Animate product cards on scroll ═══
const productCards = document.querySelectorAll(".product-card");
productCards.forEach((card, i) => {
    gsap.to(card, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        delay: i * 0.15,
        ease: "power3.out",
        scrollTrigger: {
            trigger: card,
            start: "top 85%",
            toggleActions: "play none none none"
        }
    });
});

// ═══ GSAP: Animate contact cards ═══
const contactCards = document.querySelectorAll(".contact-card");
contactCards.forEach((card, i) => {
    gsap.fromTo(card, 
        { opacity: 0, y: 30 },
        {
            opacity: 1,
            y: 0,
            duration: 0.7,
            delay: i * 0.12,
            ease: "power2.out",
            scrollTrigger: {
                trigger: ".contact-links",
                start: "top 85%",
                toggleActions: "play none none none"
            }
        }
    );
});

// Update canvas on resize
window.addEventListener("resize", () => {
    render();
});

// ═══ WhatsApp Order Integration ═══
const WHATSAPP_NUMBER = '212611227356';

document.querySelectorAll('.btn-order').forEach(btn => {
    btn.addEventListener('click', function () {
        const productName = this.dataset.product || 'Lunaris Product';
        const productPrice = this.dataset.price || '';

        const now = new Date();
        const orderTime = now.toLocaleString('en-GB', {
            dateStyle: 'full',
            timeStyle: 'short'
        });

        const message =
            `Hello, I would like to order this product:\n` +
            `Product: ${productName}\n` +
            `Price: ${productPrice}\n` +
            `Time of order: ${orderTime}`;

        const waURL = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
        window.open(waURL, '_blank');
    });
});
