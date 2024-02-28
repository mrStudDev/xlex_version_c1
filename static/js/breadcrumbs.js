document.addEventListener("DOMContentLoaded", function () {
    const breadcrumbElement = document.getElementById('breadcrumbs');
    const path = window.location.pathname.split('/').filter(Boolean);
    const nonClickableSegments = [
        'caso',
        'disciplina',
        'ramo-direito',
        'tags',
        'post',
        'categorias',
        'principios-single',
        'banca',
        'universal',
        'advanced-results',
        'sumula-search',
        'searchs',
        'sumula',
        'juris-single',
        'article-single',
        'categorias-social',
        'esfera',
        'categories',
        'modelo-single',
        'sumula-singular',
        'ramo-direito-doc',
        'tipo-doc',
        'tags-docs',
        'delete-modelo',
        'blog-post',
        'tags-blog-social',
        'principio-single',
        'principio-ramos',

    ]; // Lista de segmentos não clicáveis

    let breadcrumbHTML = '<li class="breadcrumb-item"><a href="/">Home</a></li>';
    let breadcrumbPath = '';

    path.forEach((segment, index) => {
        breadcrumbPath += '/' + segment;
        if (index < path.length - 1 && !nonClickableSegments.includes(segment)) {
            // Segmentos intermediários que não estão na lista nonClickableSegments
            breadcrumbHTML += `<li class="breadcrumb-item"><a href="${breadcrumbPath}">${segment}</a></li>`;
        } else {
            // Último segmento ou segmentos na lista nonClickableSegments
            breadcrumbHTML += `<li class="breadcrumb-item active" aria-current="page">${segment}</li>`;
        }
    });

    breadcrumbElement.innerHTML = breadcrumbHTML;
});