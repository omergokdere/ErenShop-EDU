/* ============================================================
   ErenShop Frontend - app.js
   Vanilla JavaScript ile API entegrasyonu.

   Öğrenilen konular:
   - fetch() API ile GET / POST / DELETE istekleri
   - async / await kullanımı
   - DOM manipülasyonu (innerHTML, addEventListener)
   - Modüler fonksiyon yapısı
   ============================================================ */

// ── AYARLAR ────────────────────────────────────────────────
const API_BASE = 'http://localhost:8000/api'; // Backend adresi

// ── DURUM (STATE) ───────────────────────────────────────────
let CUSTOMER_ID     = null; // Rastgele seçilen müşteri — init() içinde atanır
let allProducts     = [];   // Tüm ürünler (filtreleme için)
let currentCatId    = 0;    // Seçili kategori (0 = hepsi)
let cartItemCount   = 0;    // Rozet için

// ── DOM SEÇİCİLERİ ─────────────────────────────────────────
const productsGrid    = document.getElementById('productsGrid');
const categoriesBar   = document.getElementById('categoriesBar');
const cartBadge       = document.getElementById('cartBadge');
const cartSidebar     = document.getElementById('cartSidebar');
const overlay         = document.getElementById('overlay');
const cartItemsEl     = document.getElementById('cartItems');
const cartTotalEl     = document.getElementById('cartTotal');
const toast           = document.getElementById('toast');
const modalOverlay    = document.getElementById('modalOverlay');
const modalOrderNo    = document.getElementById('modalOrderNo');

// ── YARDIMCI: PARA BİRİMİ FORMATLAMA ──────────────────────
function formatMoney(amount) {
  return `₺${Number(amount).toFixed(2)}`;
}

// ── YARDIMCI: ÜRÜN EMOJİSİ ─────────────────────────────────
function getProductEmoji(name) {
  const n = name.toLowerCase();
  if (n.includes('laptop') || n.includes('bilgisayar')) return '💻';
  if (n.includes('telefon') || n.includes('iphone') || n.includes('samsung')) return '📱';
  if (n.includes('klavye')) return '⌨️';
  if (n.includes('mouse') || n.includes('fare')) return '🖱️';
  if (n.includes('monitor') || n.includes('ekran')) return '🖥️';
  if (n.includes('kulaklık') || n.includes('headset')) return '🎧';
  if (n.includes('kamera') || n.includes('webcam')) return '📷';
  if (n.includes('yazıcı') || n.includes('printer')) return '🖨️';
  if (n.includes('tablet') || n.includes('ipad')) return '📲';
  if (n.includes('kablo') || n.includes('adaptör')) return '🔌';
  return '📦';
}

// ── TOAST BİLDİRİM ──────────────────────────────────────────
let toastTimer;
function showToast(message, type = '') {
  clearTimeout(toastTimer);
  toast.textContent  = message;
  toast.className    = `toast show ${type}`;
  toastTimer = setTimeout(() => {
    toast.className = 'toast';
  }, 2800);
}

// ── SEPETİ AÇ / KAPAT ──────────────────────────────────────
function openCart() {
  cartSidebar.classList.add('open');
  overlay.classList.add('visible');
  loadCart(); // Açıldığında her zaman güncel veriyi çek
}

function closeCart() {
  cartSidebar.classList.remove('open');
  overlay.classList.remove('visible');
}

document.getElementById('cartToggleBtn').addEventListener('click', openCart);
document.getElementById('closeSidebarBtn').addEventListener('click', closeCart);
overlay.addEventListener('click', closeCart);

// ── KATEGORİLERİ YÜKLEYELİM ────────────────────────────────
async function loadCategories() {
  try {
    const res  = await fetch(`${API_BASE}/categories`);
    const json = await res.json();

    if (!json.success) return;

    json.data.forEach(cat => {
      const btn = document.createElement('button');
      btn.className    = 'cat-btn';
      btn.dataset.id   = cat.Id;
      btn.textContent  = cat.Name;
      btn.addEventListener('click', () => filterByCategory(cat.Id, btn));
      categoriesBar.appendChild(btn);
    });
  } catch {
    // Sunucu kapalıysa kategori barı sessizce boş kalır
  }
}

// ── KATEGORİYE GÖRE FİLTRELE ───────────────────────────────
function filterByCategory(catId, clickedBtn) {
  currentCatId = catId;

  // Aktif butonu güncelle
  document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
  clickedBtn.classList.add('active');

  // Arama kutusunu temizle
  document.getElementById('searchInput').value = '';

  renderProducts(catId === 0 ? allProducts : allProducts.filter(p => p.CategoryId === catId));
}

// ── ÜRÜN ARA ───────────────────────────────────────────────
document.getElementById('searchInput').addEventListener('input', async (e) => {
  const keyword = e.target.value.trim();

  if (!keyword) {
    renderProducts(currentCatId === 0 ? allProducts : allProducts.filter(p => p.CategoryId === currentCatId));
    return;
  }

  try {
    const res  = await fetch(`${API_BASE}/products/search?keyword=${encodeURIComponent(keyword)}`);
    const json = await res.json();
    if (json.success) renderProducts(json.data);
  } catch {
    showToast('Arama sırasında hata oluştu.', 'error');
  }
});

// ── TÜM ÜRÜNLERİ YÜKLEYELİM ───────────────────────────────
async function loadProducts() {
  // İskelet göster
  productsGrid.innerHTML = Array(8).fill('<div class="skeleton"></div>').join('');

  try {
    const res  = await fetch(`${API_BASE}/products`);
    const json = await res.json();

    if (!json.success) {
      productsGrid.innerHTML = '<p style="color:red">Ürünler yüklenemedi.</p>';
      return;
    }

    allProducts = json.data;
    renderProducts(allProducts);
  } catch {
    productsGrid.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;color:#888;padding:40px">
        <p style="font-size:2rem">⚠️</p>
        <p>Sunucuya bağlanılamadı.<br>API çalışıyor mu?</p>
      </div>`;
  }
}

// ── ÜRÜNLERİ RENDER ET ─────────────────────────────────────
function renderProducts(products) {
  if (!products.length) {
    productsGrid.innerHTML = '<p style="grid-column:1/-1;color:#888;padding:20px">Ürün bulunamadı.</p>';
    return;
  }

  productsGrid.innerHTML = products.map(p => {
    const outOfStock   = p.Stock === 0;
    const lowStock     = p.Stock > 0 && p.Stock <= 5;
    const stockLabel   = outOfStock ? '❌ Stok yok' : lowStock ? `⚠️ Son ${p.Stock} adet` : `✅ Stokta: ${p.Stock}`;
    const stockClass   = (outOfStock || lowStock) ? 'product-stock low' : 'product-stock';

    return `
      <div class="product-card">
        <div class="product-emoji">${getProductEmoji(p.Name)}</div>
        <div class="product-name">${p.Name}</div>
        <div class="product-price">${formatMoney(p.Price)}</div>
        <div class="${stockClass}">${stockLabel}</div>
        <button
          class="add-to-cart-btn"
          onclick="addToCart(${p.Id}, '${p.Name.replace(/'/g, "\\'")}')"
          ${outOfStock ? 'disabled' : ''}
        >
          ${outOfStock ? 'Stok Yok' : 'Sepete Ekle'}
        </button>
      </div>`;
  }).join('');
}

// ── SEPETE EKLE ─────────────────────────────────────────────
async function addToCart(productId, productName) {
  try {
    const res = await fetch(`${API_BASE}/cart/add`, {
      method : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body   : JSON.stringify({
        customerId: CUSTOMER_ID,
        productId : productId,
        quantity  : 1
      })
    });

    const json = await res.json();

    if (res.ok && json.success) {
      cartItemCount++;
      cartBadge.textContent = cartItemCount;
      showToast(`${productName} sepete eklendi!`, 'success');
    } else {
      const msg = json.detail?.message || json.message || 'Eklenemedi.';
      showToast(msg, 'error');
    }
  } catch {
    showToast('Sunucuya bağlanılamadı.', 'error');
  }
}

// ── SEPETİ YÜKLEYELİM ──────────────────────────────────────
async function loadCart() {
  cartItemsEl.innerHTML = '<p style="color:#aaa;text-align:center;margin-top:40px">Yükleniyor...</p>';

  try {
    const res  = await fetch(`${API_BASE}/cart/${CUSTOMER_ID}`);
    const json = await res.json();

    const items = json.data?.items ?? [];
    const total = json.data?.total ?? 0;

    // Rozet güncelle
    cartItemCount          = items.length;
    cartBadge.textContent  = cartItemCount;

    if (!items.length) {
      cartItemsEl.innerHTML = `
        <div class="cart-empty">
          <span class="cart-empty-icon">🛒</span>
          Sepetin boş.<br>Ürün eklemek için ürünlere göz at!
        </div>`;
      cartTotalEl.textContent = '₺0.00';
      document.getElementById('orderBtn').disabled = true;
      return;
    }

    document.getElementById('orderBtn').disabled = false;
    cartTotalEl.textContent = formatMoney(total);

    cartItemsEl.innerHTML = items.map(item => `
      <div class="cart-item" id="cartItem-${item.CartItemId}">
        <div class="cart-item-info">
          <div class="cart-item-name">${item.ProductName}</div>
          <div class="cart-item-detail">${item.Quantity} adet × ${formatMoney(item.UnitPrice)}</div>
        </div>
        <div class="cart-item-price">${formatMoney(item.Quantity * item.UnitPrice)}</div>
        <button class="remove-btn" onclick="removeFromCart(${item.CartItemId})" title="Kaldır">🗑</button>
      </div>`).join('');

  } catch {
    cartItemsEl.innerHTML = '<p style="color:red;text-align:center;margin-top:40px">Sepet yüklenemedi.</p>';
  }
}

// ── SEPETTEN KALDIR ─────────────────────────────────────────
async function removeFromCart(cartItemId) {
  try {
    const res = await fetch(`${API_BASE}/cart/items/${cartItemId}`, { method: 'DELETE' });

    if (res.ok) {
      document.getElementById(`cartItem-${cartItemId}`)?.remove();
      showToast('Ürün sepetten kaldırıldı.', '');
      loadCart(); // Toplamı yenile
    } else {
      showToast('Kaldırılamadı.', 'error');
    }
  } catch {
    showToast('Sunucuya bağlanılamadı.', 'error');
  }
}

// ── SİPARİŞ OLUŞTUR ────────────────────────────────────────
document.getElementById('orderBtn').addEventListener('click', async () => {
  const btn = document.getElementById('orderBtn');
  btn.disabled  = true;
  btn.textContent = 'İşleniyor...';

  try {
    const res = await fetch(`${API_BASE}/orders/create-from-cart`, {
      method : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body   : JSON.stringify({ customerId: CUSTOMER_ID })
    });

    const json = await res.json();

    if (res.ok && json.success) {
      closeCart();
      modalOrderNo.textContent = `Sipariş No: ${json.data?.OrderNumber ?? '—'}`;
      modalOverlay.classList.add('visible');

      // Ürün stoklarını yenile
      await loadProducts();
    } else {
      const msg = json.detail?.message || json.message || 'Sipariş oluşturulamadı.';
      showToast(msg, 'error');
    }
  } catch {
    showToast('Sunucuya bağlanılamadı.', 'error');
  } finally {
    btn.disabled    = false;
    btn.textContent = 'Siparişi Tamamla';
  }
});

// ── SİPARİŞ MODAL KAPAT ────────────────────────────────────
document.getElementById('modalCloseBtn').addEventListener('click', () => {
  modalOverlay.classList.remove('visible');
  cartItemCount         = 0;
  cartBadge.textContent = 0;
});

// ── "TÜMÜ" KATEGORİ BUTONU ─────────────────────────────────
document.querySelector('.cat-btn[data-id="0"]').addEventListener('click', function () {
  currentCatId = 0;
  document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
  this.classList.add('active');
  document.getElementById('searchInput').value = '';
  renderProducts(allProducts);
});

// ── RASTGELE MÜŞTERİ SEÇ ──────────────────────────────────
async function pickRandomCustomer() {
  try {
    const res  = await fetch(`${API_BASE}/customers`);
    const json = await res.json();
    if (!json.success || !json.data.length) return;

    const customers = json.data;
    const picked    = customers[Math.floor(Math.random() * customers.length)];
    CUSTOMER_ID     = picked.Id;

    const tag = document.getElementById('userTag');
    tag.textContent = `👤 ${picked.FirstName} ${picked.LastName}`;
    tag.title       = `Müşteri #${picked.Id} — ${picked.Email}`;
  } catch {
    // Hata olursa varsayılan 1 numaralı müşteriyi kullan
    CUSTOMER_ID = 1;
    document.getElementById('userTag').textContent = '👤 Eren Sarıteke';
  }
}

// ── SIDE NAV TOGGLE ────────────────────────────────────────
(function initSideNav() {
  const sideNav = document.getElementById('sideNav');
  const overlay = document.getElementById('sideNavOverlay');
  const openBtn = document.getElementById('menuToggle');
  const closeBtn = document.getElementById('menuClose');
  if (!sideNav || !overlay || !openBtn || !closeBtn) return;
  const open = () => { sideNav.classList.add('open'); overlay.classList.add('open'); };
  const close = () => { sideNav.classList.remove('open'); overlay.classList.remove('open'); };
  openBtn.addEventListener('click', open);
  closeBtn.addEventListener('click', close);
  overlay.addEventListener('click', close);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
})();

// ── UYGULAMA BAŞLANGICI ────────────────────────────────────
(async function init() {
  await pickRandomCustomer(); // Önce kullanıcıyı seç
  await loadCategories();
  await loadProducts();
})();
