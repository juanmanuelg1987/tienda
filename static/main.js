// main.js - Interactividad avanzada catálogo y menú

document.addEventListener('DOMContentLoaded', function() {
    // Menú hamburguesa para móvil (si se agrega en el futuro)
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.navbar-links');
    if (burger && nav) {
        burger.addEventListener('click', function() {
            nav.classList.toggle('active');
        });
    }

    // --- Wishlist/Favoritos ---
    function getWishlist() {
        return JSON.parse(localStorage.getItem('wishlist') || '[]');
    }
    function setWishlist(list) {
        localStorage.setItem('wishlist', JSON.stringify(list));
    }
    function toggleWishlist(id) {
        let list = getWishlist();
        if (list.includes(id)) {
            list = list.filter(x => x !== id);
        } else {
            list.push(id);
        }
        setWishlist(list);
        renderWishlist();
    }
    function renderWishlist() {
        const list = getWishlist();
        document.querySelectorAll('.wishlist-btn').forEach(btn => {
            const pid = btn.getAttribute('data-product-id');
            if (list.includes(pid)) {
                btn.classList.add('text-danger');
                btn.classList.remove('text-secondary');
                btn.querySelector('i').classList.replace('bi-heart', 'bi-heart-fill');
            } else {
                btn.classList.remove('text-danger');
                btn.classList.add('text-secondary');
                btn.querySelector('i').classList.replace('bi-heart-fill', 'bi-heart');
            }
        });
    }
    document.body.addEventListener('click', function(e) {
        if (e.target.closest('.wishlist-btn')) {
            const btn = e.target.closest('.wishlist-btn');
            const pid = btn.getAttribute('data-product-id');
            toggleWishlist(pid);
            e.preventDefault();
        }
    });
    renderWishlist();

    // --- Filtros avanzados y paginación ---
    const productsContainer = document.getElementById('catalogoProductos');
    if (productsContainer) {
        let allCards = Array.from(productsContainer.children);
        const filtro = document.getElementById('categoryFilter');
        const buscador = document.getElementById('searchInput');
        // Filtros avanzados (precio, oferta, stock)
        let minPrice = 0, maxPrice = 999999;
        let onlyOffers = false, onlyStock = false, onlyFavs = false;
        // Crear controles visuales
        const filtrosDiv = document.createElement('div');
        filtrosDiv.className = 'row mb-3 g-2 align-items-center';
        filtrosDiv.innerHTML = `
          <div class="col-12 col-md-3">
            <label class="form-label mb-1">Precio mínimo</label>
            <input type="number" min="0" id="minPrice" class="form-control" placeholder="$0">
          </div>
          <div class="col-12 col-md-3">
            <label class="form-label mb-1">Precio máximo</label>
            <input type="number" min="0" id="maxPrice" class="form-control" placeholder="$99999">
          </div>
          <div class="col-6 col-md-2">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" id="onlyOffers">
              <label class="form-check-label" for="onlyOffers">Solo ofertas</label>
            </div>
          </div>
          <div class="col-6 col-md-2">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" id="onlyStock">
              <label class="form-check-label" for="onlyStock">Solo disponibles</label>
            </div>
          </div>
          <div class="col-12 col-md-2">
            <button id="showFavs" class="btn btn-outline-danger w-100"><i class="bi bi-heart-fill"></i> Favoritos</button>
          </div>
        `;
        productsContainer.parentNode.insertBefore(filtrosDiv, productsContainer);
        // Listeners filtros
        filtrosDiv.querySelector('#minPrice').addEventListener('input', e => { minPrice = Number(e.target.value)||0; filtrarPaginar(); });
        filtrosDiv.querySelector('#maxPrice').addEventListener('input', e => { maxPrice = Number(e.target.value)||999999; filtrarPaginar(); });
        filtrosDiv.querySelector('#onlyOffers').addEventListener('change', e => { onlyOffers = e.target.checked; filtrarPaginar(); });
        filtrosDiv.querySelector('#onlyStock').addEventListener('change', e => { onlyStock = e.target.checked; filtrarPaginar(); });
        filtrosDiv.querySelector('#showFavs').addEventListener('click', e => { onlyFavs = !onlyFavs; e.target.classList.toggle('btn-danger', onlyFavs); filtrarPaginar(); });
        // --- Paginación visual ---
        let currentPage = 1;
        const perPage = 6;
        const pagDiv = document.createElement('nav');
        pagDiv.className = 'd-flex justify-content-center mt-3';
        productsContainer.parentNode.appendChild(pagDiv);
        function filtrarPaginar() {
            let list = allCards.filter(card => {
                const cat = filtro.value;
                const q = buscador.value.toLowerCase();
                const cardCat = card.getAttribute('data-category');
                const cardName = card.getAttribute('data-name');
                const price = parseFloat(card.querySelector('.badge.bg-warning')?.textContent.replace(/[^\d.]/g, '')) || 0;
                const offer = card.querySelector('.badge.bg-danger');
                const stock = Number(card.querySelector('.list-group-item strong + strong')?.textContent || card.querySelector('.card-body .badge.bg-warning')?.textContent || 0);
                const pid = card.querySelector('.wishlist-btn')?.getAttribute('data-product-id') || '';
                const favs = getWishlist();
                let ok = true;
                if ((cat !== 'all' && cardCat !== cat) || !cardName.includes(q)) ok = false;
                if (price < minPrice || price > maxPrice) ok = false;
                if (onlyOffers && !offer) ok = false;
                if (onlyStock && stock <= 0) ok = false;
                if (onlyFavs && !favs.includes(pid)) ok = false;
                return ok;
            });
            // Paginación
            const totalPages = Math.ceil(list.length / perPage) || 1;
            if (currentPage > totalPages) currentPage = totalPages;
            list.forEach((card, i) => {
                card.style.display = (i >= (currentPage-1)*perPage && i < currentPage*perPage) ? '' : 'none';
            });
            // Render paginación
            let pagHTML = '<ul class="pagination">';
            for (let i = 1; i <= totalPages; i++) {
                pagHTML += `<li class="page-item${i===currentPage?' active':''}"><a class="page-link" href="#">${i}</a></li>`;
            }
            pagHTML += '</ul>';
            pagDiv.innerHTML = pagHTML;
            pagDiv.querySelectorAll('.page-link').forEach((a, idx) => {
                a.addEventListener('click', e => { e.preventDefault(); currentPage = idx+1; filtrarPaginar(); });
            });
        }
        filtro.addEventListener('change', filtrarPaginar);
        buscador.addEventListener('input', filtrarPaginar);
        filtrarPaginar();
    }

    // --- Carrito AJAX visual (simulado) ---
    document.querySelectorAll('.add-to-cart-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (btn.getAttribute('href') === '#') {
                e.preventDefault();
                var toast = new bootstrap.Toast(document.getElementById('cartToast'));
                toast.show();
                // Actualiza contador en navbar (simulado)
                let badge = document.getElementById('cart-count-badge');
                if (badge) {
                    let n = parseInt(badge.textContent)||0;
                    badge.textContent = n+1;
                }
            }
        });
    });
});
