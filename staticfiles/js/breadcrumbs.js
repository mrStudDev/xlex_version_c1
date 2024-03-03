document.addEventListener("DOMContentLoaded", function () {
    const breadcrumbElement = document.getElementById('breadcrumbs');
    const path = window.location.pathname.split('/').filter(Boolean);
    const nonClickableSegments = [


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