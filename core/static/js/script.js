document.addEventListener("DOMContentLoaded", function () {
// Variáveis globais para as instâncias dos gráficos
let salesValueChartInstance, dailySalesChartInstance, categoryChartInstance, brandChartInstance;

const themeToggleButton = document.getElementById('theme-toggle');
const themeIcon = themeToggleButton.querySelector('i');


// Lógica dos Gráficos do Dashboard
function initDashboardCharts() {
    if (document.getElementById('salesValueChart')) {
        // Destruir gráficos existentes antes de recriar
        if (salesValueChartInstance) salesValueChartInstance.destroy();
        if (dailySalesChartInstance) dailySalesChartInstance.destroy();
        if (categoryChartInstance) categoryChartInstance.destroy();
        if (brandChartInstance) brandChartInstance.destroy();

        const isLightTheme = document.body.classList.contains('light-mode');
        const textColor = isLightTheme ? '#212529' : '#e6edf3';
        const mutedColor = isLightTheme ? '#6c757d' : '#8b949e';
        const gridColor = isLightTheme ? '#dee2e6' : '#30363d';
        const primaryBgColor = isLightTheme ? '#ffffff' : '#161b22';

        function getLast7Days() {
            const dates = [];
            for (let i = 6; i >= 0; i--) {
                const d = new Date();
                d.setDate(d.getDate() - i);
                dates.push(`${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`);
            }
            return dates;
        }

        const chartLabels = getLast7Days();
        const chartOptions = {
            maintainAspectRatio: false, responsive: true,
            scales: {
                y: { beginAtZero: true, ticks: { color: mutedColor }, grid: { color: gridColor } },
                x: { ticks: { color: mutedColor }, grid: { display: false } }
            },
            plugins: { legend: { labels: { color: textColor } } }
        };

        const salesValueCtx = document.getElementById('salesValueChart').getContext('2d');
        salesValueChartInstance = new Chart(salesValueCtx, {
            type: 'line',
            data: { labels: chartLabels, datasets: [{ label: 'Valor em vendas', data: [1200, 1800, 1550, 2200, 2050, 2800, 3100], borderColor: '#58a6ff', backgroundColor: 'rgba(88, 166, 255, 0.1)', fill: true, tension: 0.4 }] },
            options: { ...chartOptions, plugins: { ...chartOptions.plugins, title: { display: true, text: 'Valor de Vendas (Últimos 7 dias)', color: textColor, font: { size: 16 } } } }
        });

        const dailySalesCtx = document.getElementById('dailySalesChart').getContext('2d');
        dailySalesChartInstance = new Chart(dailySalesCtx, {
            type: 'bar',
            data: { labels: chartLabels, datasets: [{ label: 'Quantidade de Vendas', data: [45, 62, 55, 78, 65, 88, 95], backgroundColor: 'rgba(248, 81, 73, 0.6)', borderColor: '#f85149', borderWidth: 1, borderRadius: 4 }] },
            options: { ...chartOptions, plugins: { ...chartOptions.plugins, title: { display: true, text: 'Quantidade de vendas diárias', color: textColor, font: { size: 16 } } } }
        });

        const doughnutChartOptions = {
            maintainAspectRatio: false, responsive: true,
            plugins: { legend: { position: 'top', labels: { color: textColor } }, title: { display: true, color: textColor, font: { size: 16 } } },
            cutout: '70%'
        };

        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        categoryChartInstance = new Chart(categoryCtx, {
            type: 'doughnut',
            data: { labels: ['Eletrônicos', 'Papelaria', 'Suprimentos', 'Outros'], datasets: [{ label: 'Produtos por Categoria', data: [300, 50, 100, 40], backgroundColor: ['#58a6ff', '#3fb950', '#d29922', '#f85149'], borderColor: primaryBgColor, borderWidth: 4 }] },
            options: { ...doughnutChartOptions, plugins: { ...doughnutChartOptions.plugins, title: { ...doughnutChartOptions.plugins.title, text: 'Produtos por Categoria' } } }
        });

        const brandCtx = document.getElementById('brandChart').getContext('2d');
        brandChartInstance = new Chart(brandCtx, {
            type: 'doughnut',
            data: { labels: ['Marca A', 'Logitech', 'Marca B', 'Razer'], datasets: [{ label: 'Produtos por Marca', data: [120, 250, 80, 150], backgroundColor: ['#58a6ff', '#f85149', '#3fb950', '#d29922'], borderColor: primaryBgColor, borderWidth: 4 }] },
            options: { ...doughnutChartOptions, plugins: { ...doughnutChartOptions.plugins, title: { ...doughnutChartOptions.plugins.title, text: 'Produtos por Marca' } } }
        });
    }
}

// Lógica do Seletor de Tema
function applyTheme(theme) {
    if (theme === 'light') {
        document.body.classList.add('light-mode');
        themeIcon.classList.remove('bi-moon-stars-fill');
        themeIcon.classList.add('bi-sun-fill');
    } else {
        document.body.classList.remove('light-mode');
        themeIcon.classList.remove('bi-sun-fill');
        themeIcon.classList.add('bi-moon-stars-fill');
    }
    // Recria os gráficos com as cores do novo tema
    initDashboardCharts();
}

themeToggleButton.addEventListener('click', (e) => {
    e.preventDefault();
    const currentTheme = document.body.classList.contains('light-mode') ? 'light' : 'dark';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
});

// Aplica o tema salvo ao carregar a página
const savedTheme = localStorage.getItem('theme') || 'dark';
applyTheme(savedTheme);
});