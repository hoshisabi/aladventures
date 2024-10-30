let adventures = [];
let filteredAdventures = [];
let currentPage = 1;
const itemsPerPage = 50;

let filters = {
    campaign: '',
    tier: '',
    hours: ''
};

// Fetch and load the JSON data
fetch('/_data/all_adventures.json')
    .then(response => response.json())
    .then(data => {
        adventures = data;
        applyFilters();
        setupEventListeners();
    });

function setupEventListeners() {
    // Add event listeners for filters
    ['campaign', 'tier', 'hours'].forEach(filter => {
        document.getElementById(filter).addEventListener('change', (e) => {
            filters[filter] = e.target.value;
            currentPage = 1; // Reset to first page when filtering
            applyFilters();
        });
    });

    // Add pagination event listeners
    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            displayResults();
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        if (currentPage < getTotalPages()) {
            currentPage++;
            displayResults();
        }
    });
}

function applyFilters() {
    filteredAdventures = adventures.filter(adventure => {
        // Handle campaign filter for both array and single value cases
        const campaignMatch = !filters.campaign || (
            Array.isArray(adventure.campaign)
                ? adventure.campaign.includes(filters.campaign)
                : adventure.campaign === filters.campaign
        );

        return campaignMatch &&
            (!filters.tier || adventure.tiers === parseInt(filters.tier)) &&
            (!filters.hours || adventure.hours === parseInt(filters.hours));
    });

    displayResults();
}

function getTotalPages() {
    return Math.ceil(filteredAdventures.length / itemsPerPage);
}

function displayResults() {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, filteredAdventures.length);
    const currentPageData = filteredAdventures.slice(startIndex, endIndex);

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    currentPageData.forEach(adventure => {
        const card = document.createElement('div');
        card.className = 'border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow';

        // Handle campaign display for both array and single value cases
        const campaignDisplay = Array.isArray(adventure.campaign)
            ? adventure.campaign.join(', ')
            : adventure.campaign;

        card.innerHTML = `
            <h2 class="text-xl font-semibold mb-2">${adventure.title}</h2>
            <p class="text-gray-600 mb-2">Code: ${adventure.code}</p>
            <p class="text-gray-600 mb-2">Campaign: ${campaignDisplay}</p>
            <p class="text-gray-600 mb-2">Authors: ${adventure.authors.join(', ')}</p>
            <p class="text-gray-600 mb-2">Hours: ${adventure.hours}</p>
            ${adventure.tiers ? `<p class="text-gray-600 mb-2">Tier: ${adventure.tiers}</p>` : ''}
            <a href="${adventure.url}" target="_blank" class="text-blue-600 hover:text-blue-800">View on DMs Guild</a>
        `;
        resultsDiv.appendChild(card);
    });

    // Update pagination UI
    const totalPages = getTotalPages();
    document.getElementById('current-page').textContent = currentPage;
    document.getElementById('total-pages').textContent = totalPages;
    document.getElementById('prev-page').disabled = currentPage === 1;
    document.getElementById('next-page').disabled = currentPage === totalPages;

    // Update results info
    document.getElementById('showing-start').textContent = startIndex + 1;
    document.getElementById('showing-end').textContent = endIndex;
    document.getElementById('total-results').textContent = filteredAdventures.length;

    // Scroll to top of results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}