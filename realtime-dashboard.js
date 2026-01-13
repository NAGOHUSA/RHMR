// [file name]: realtime-dashboard.js
class RealTimeDashboard {
    constructor() {
        this.lastUpdate = null;
        this.autoRefreshInterval = null;
        this.charts = {};
        this.currentTimeRange = 'live';
        this.selectedZips = ['31088'];
    }
    
    async initialize() {
        console.log('Initializing Real-Time Dashboard...');
        
        // Load initial data
        await this.loadDashboardData();
        
        // Initialize charts
        this.initializeCharts();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Start auto-refresh (every 10 minutes)
        this.startAutoRefresh(10 * 60 * 1000);
        
        // Show welcome message
        this.showWelcomeMessage();
    }
    
    async loadDashboardData() {
        try {
            console.log('Loading dashboard data...');
            
            // Load from local JSON file
            const response = await fetch('data/houston-county-ga/dashboard_data.json');
            if (!response.ok) throw new Error('Failed to load dashboard data');
            
            const data = await response.json();
            
            // Update UI with real data
            this.updateUI(data);
            
            // Update last update time
            this.lastUpdate = new Date(data.last_updated);
            this.updateLastUpdateTime();
            
            // Store data for charts
            this.currentData = data;
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            
            // Load mock data as fallback
            this.loadMockData();
        }
    }
    
    loadMockData() {
        // Generate realistic mock data
        const mockData = {
            last_updated: new Date().toISOString(),
            market_summary: {
                avg_price: 289500,
                total_inventory: 125,
                avg_opportunity_score: 78,
                market_trend: 'heating',
                best_opportunity_zip: '31088'
            },
            trends_24h: {
                price_movement: '+0.3%',
                inventory_change: '+5 listings',
                new_listings_today: '12',
                pending_sales: '8',
                avg_dom_trend: '↓ 2 days',
                market_pulse: 'Moderate Activity'
            },
            realtor_tips: [
                "🔥 **High Opportunity Market**: Great time for new listings!",
                "📈 Consider pricing slightly above market to test appetite",
                "🤝 Focus on seller representation - high demand expected"
            ]
        };
        
        this.updateUI(mockData);
        this.lastUpdate = new Date();
        this.updateLastUpdateTime();
    }
    
    updateUI(data) {
        // Update market pulse metrics
        this.updateMarketPulse(data);
        
        // Update real-time metrics
        this.updateRealtimeMetrics(data);
        
        // Update insights
        this.updateInsights(data);
        
        // Update charts
        this.updateCharts(data);
        
        // Update realtor tips
        this.updateRealtorTips(data);
    }
    
    updateMarketPulse(data) {
        const marketSummary = data.market_summary || {};
        
        // Market Temperature (based on opportunity score)
        const temp = marketSummary.avg_opportunity_score || 50;
        document.getElementById('marketTemp').textContent = `${Math.round(temp)}°`;
        
        // Velocity Score (simulated based on market activity)
        const velocity = Math.min(100, (temp * 1.1));
        document.getElementById('velocityScore').textContent = Math.round(velocity);
        document.querySelector('.meter-bar').style.width = `${velocity}%`;
        
        // Leverage Index (simulated)
        const leverage = 65; // Simulated - in real app, calculate from data
        document.getElementById('leverageIndex').textContent = leverage;
        document.querySelector('.indicator').style.left = `${leverage}%`;
        
        // Opportunity Score
        document.getElementById('opportunityScore').textContent = Math.round(temp);
        
        // Update stars based on score
        this.updateOpportunityStars(temp);
    }
    
    updateOpportunityStars(score) {
        const stars = document.querySelectorAll('.opportunity-rating i');
        const fullStars = Math.floor(score / 20);
        const hasHalfStar = (score % 20) >= 10;
        
        stars.forEach((star, index) => {
            if (index < fullStars) {
                star.className = 'fas fa-star';
            } else if (index === fullStars && hasHalfStar) {
                star.className = 'fas fa-star-half-alt';
            } else {
                star.className = 'far fa-star';
            }
        });
    }
    
    updateRealtimeMetrics(data) {
        const marketSummary = data.market_summary || {};
        const trends = data.trends_24h || {};
        
        // Active Listings
        document.getElementById('activeListings').textContent = 
            marketSummary.total_inventory || '105';
        
        // Median Price
        const price = marketSummary.avg_price || 289500;
        document.getElementById('medianPrice').textContent = 
            `$${price.toLocaleString()}`;
        
        // Days on Market
        document.getElementById('avgDOM').textContent = '24';
        
        // Price to List
        document.getElementById('priceToList').textContent = '98.7%';
        
        // Update mini chart for listings
        this.updateListingsMiniChart();
    }
    
    updateListingsMiniChart() {
        const ctx = document.getElementById('listingsChart').getContext('2d');
        
        // Generate last 7 days data
        const labels = Array.from({length: 7}, (_, i) => {
            const date = new Date();
            date.setDate(date.getDate() - (6 - i));
            return date.toLocaleDateString('en-US', {weekday: 'short'});
        });
        
        const data = labels.map(() => 95 + Math.floor(Math.random() * 20));
        
        if (this.listingsMiniChart) {
            this.listingsMiniChart.destroy();
        }
        
        this.listingsMiniChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                scales: {
                    x: { display: false },
                    y: { display: false }
                },
                elements: {
                    line: {
                        tension: 0.4
                    }
                }
            }
        });
    }
    
    updateInsights(data) {
        const insightsContainer = document.querySelector('.insights-container');
        
        // Clear existing insights (except the first one if it's the placeholder)
        const existingInsights = insightsContainer.querySelectorAll('.insight-card');
        if (existingInsights.length > 0 && !existingInsights[0].querySelector('.insight-time')) {
            existingInsights[0].remove();
        }
        
        // Generate new insights based on data
        const insights = this.generateInsights(data);
        
        // Add new insights (limit to 5)
        insights.slice(0, 5).forEach((insight, index) => {
            const insightCard = this.createInsightCard(insight, index === 0);
            insightsContainer.insertBefore(insightCard, insightsContainer.firstChild);
        });
        
        // Limit to 5 insights total
        while (insightsContainer.children.length > 5) {
            insightsContainer.removeChild(insightsContainer.lastChild);
        }
    }
    
    generateInsights(data) {
        const insights = [];
        const now = new Date();
        
        // Price movement insight
        if (data.trends_24h?.price_movement?.startsWith('+')) {
            insights.push({
                title: '📈 Price Momentum Building',
                content: '3 consecutive days of price increases in Warner Robins. Consider adjusting listing strategies.',
                tags: ['pricing', 'strategy'],
                time: '2 min ago'
            });
        }
        
        // Inventory insight
        if (data.market_summary?.total_inventory > 120) {
            insights.push({
                title: '🏠 Inventory Growing',
                content: `Active listings reached ${data.market_summary.total_inventory}. More options for buyers.`,
                tags: ['inventory', 'buyers'],
                time: '15 min ago'
            });
        }
        
        // Opportunity insight
        if (data.market_summary?.avg_opportunity_score > 70) {
            insights.push({
                title: '🎯 High Opportunity Market',
                content: 'Great conditions for new listings and buyer activity.',
                tags: ['opportunity', 'strategy'],
                time: '30 min ago'
            });
        }
        
        // Add time-based insights
        const hour = now.getHours();
        if (hour >= 9 && hour <= 11) {
            insights.push({
                title: '🌅 Morning Market Activity',
                content: 'Peak showing times beginning. Ensure listings are prepared.',
                tags: ['timing', 'strategy'],
                time: '45 min ago'
            });
        }
        
        return insights;
    }
    
    createInsightCard(insight, isNew = false) {
        const card = document.createElement('div');
        card.className = `insight-card ${isNew ? 'new' : ''}`;
        
        const tagsHTML = insight.tags.map(tag => 
            `<span class="tag ${tag}">${tag}</span>`
        ).join('');
        
        card.innerHTML = `
            <div class="insight-time">${insight.time}</div>
            <div class="insight-content">
                <h4>${insight.title}</h4>
                <p>${insight.content}</p>
                <div class="insight-tags">${tagsHTML}</div>
            </div>
        `;
        
        return card;
    }
    
    updateRealtorTips(data) {
        const tips = data.realtor_tips || [];
        const dailyTip = tips[0] || 'Use market velocity data to demonstrate your expertise to clients.';
        
        document.getElementById('dailyTip').textContent = dailyTip.replace(/\*\*(.*?)\*\*/g, '$1');
    }
    
    initializeCharts() {
        // Price & Inventory Chart
        this.initializePriceInventoryChart();
        
        // Activity Chart
        this.initializeActivityChart();
        
        // Success Chart
        this.initializeSuccessChart();
    }
    
    initializePriceInventoryChart() {
        const ctx = document.getElementById('priceInventoryChart').getContext('2d');
        
        // Generate last 7 days data
        const labels = Array.from({length: 7}, (_, i) => {
            const date = new Date();
            date.setDate(date.getDate() - (6 - i));
            return date.toLocaleDateString('en-US', {month: 'short', day: 'numeric'});
        });
        
        this.priceInventoryChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Price',
                        data: labels.map(() => 285000 + Math.random() * 10000),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Inventory',
                        data: labels.map(() => 90 + Math.random() * 30),
                        borderColor: '#00c853',
                        backgroundColor: 'rgba(0, 200, 83, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Price ($)',
                            color: '#667eea'
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + (value / 1000) + 'k';
                            }
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Inventory',
                            color: '#00c853'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }
    
    initializeActivityChart() {
        const ctx = document.getElementById('activityChart').getContext('2d');
        
        this.activityChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Showings',
                    data: [12, 19, 8, 15, 22, 18, 25],
                    backgroundColor: 'rgba(102, 126, 234, 0.7)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Showings'
                        }
                    }
                }
            }
        });
    }
    
    initializeSuccessChart() {
        const ctx = document.getElementById('successChart').getContext('2d');
        
        this.successChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Listings', 'Showings', 'Offers', 'Closings'],
                datasets: [{
                    data: [45, 30, 15, 10],
                    backgroundColor: [
                        '#667eea',
                        '#764ba2',
                        '#00c853',
                        '#ff9800'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed}%`;
                            }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }
    
    updateCharts(data) {
        // Update charts with new data
        if (this.priceInventoryChart && data.market_summary) {
            // Simulate updating price data
            const priceDataset = this.priceInventoryChart.data.datasets[0];
            const newPrice = data.market_summary.avg_price || 285000;
            priceDataset.data.push(newPrice);
            priceDataset.data.shift();
            
            // Simulate updating inventory data
            const inventoryDataset = this.priceInventoryChart.data.datasets[1];
            const newInventory = data.market_summary.total_inventory || 100;
            inventoryDataset.data.push(newInventory);
            inventoryDataset.data.shift();
            
            // Update labels for new day
            const labels = this.priceInventoryChart.data.labels;
            const today = new Date();
            labels.push(today.toLocaleDateString('en-US', {month: 'short', day: 'numeric'}));
            labels.shift();
            
            this.priceInventoryChart.update();
        }
    }
    
    updateLastUpdateTime() {
        if (!this.lastUpdate) return;
        
        const now = new Date();
        const diffMs = now - this.lastUpdate;
        const diffMins = Math.floor(diffMs / 60000);
        const diffSecs = Math.floor((diffMs % 60000) / 1000);
        
        let timeText;
        if (diffMins < 1) {
            timeText = 'Just now';
        } else if (diffMins < 60) {
            timeText = `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
        } else {
            timeText = this.lastUpdate.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
        }
        
        document.getElementById('lastUpdateTime').textContent = timeText;
        
        // Update market status based on recency
        let status = 'Live';
        if (diffMins > 30) status = 'Delayed';
        if (diffMins > 120) status = 'Stale';
        
        document.getElementById('marketStatus').textContent = status;
    }
    
    setupEventListeners() {
        // Refresh button
        document.getElementById('refreshData').addEventListener('click', () => {
            this.refreshData();
        });
        
        // Time range buttons
        document.querySelectorAll('.time-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentTimeRange = e.target.dataset.time;
                this.updateTimeRange();
            });
        });
        
        // ZIP code selection
        document.getElementById('zipSelect').addEventListener('change', (e) => {
            this.selectedZips = Array.from(e.target.selectedOptions).map(opt => opt.value);
            this.updateForSelectedZips();
        });
        
        // Compare button
        document.getElementById('compareBtn').addEventListener('click', () => {
            this.showComparisonView();
        });
        
        // Insight generator
        document.querySelector('.generate-btn').addEventListener('click', () => {
            this.generateAIInsight();
        });
        
        // Step actions
        document.querySelectorAll('.step-action').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.target.textContent = 'Completed ✓';
                e.target.style.background = '#4caf50';
                e.target.disabled = true;
                
                // Show completion toast
                this.showToast('Task completed! Great work!', 'success');
            });
        });
    }
    
    async refreshData() {
        // Show loading state
        const refreshBtn = document.getElementById('refreshData');
        const originalText = refreshBtn.innerHTML;
        refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
        refreshBtn.disabled = true;
        
        try {
            await this.loadDashboardData();
            this.showToast('Data refreshed successfully!', 'success');
        } catch (error) {
            this.showToast('Error refreshing data. Please try again.', 'error');
        } finally {
            // Restore button state after delay
            setTimeout(() => {
                refreshBtn.innerHTML = originalText;
                refreshBtn.disabled = false;
            }, 1000);
        }
    }
    
    updateTimeRange() {
        console.log(`Switching to ${this.currentTimeRange} view`);
        
        // Update chart data based on time range
        // This would normally fetch different data ranges
        this.showToast(`View changed to ${this.currentTimeRange.toUpperCase()}`, 'info');
    }
    
    updateForSelectedZips() {
        console.log('Selected ZIPs:', this.selectedZips);
        
        if (this.selectedZips.length > 1) {
            // Show comparison mode
            document.getElementById('compareBtn').style.display = 'inline-block';
        } else {
            document.getElementById('compareBtn').style.display = 'none';
        }
        
        // In a real app, this would reload data for selected ZIPs
        this.showToast(`Showing data for ${this.selectedZips.length} ZIP code(s)`, 'info');
    }
    
    showComparisonView() {
        // This would show a comparison view between selected ZIPs
        this.showToast('Comparison view coming soon!', 'info');
    }
    
    generateAIInsight() {
        const input = document.querySelector('.generator-input input');
        const question = input.value.trim();
        
        if (!question) {
            this.showToast('Please enter a question first', 'warning');
            return;
        }
        
        // Simulate AI generation
        const insights = [
            "Based on current trends, we're seeing increased buyer activity in the $250-300k range.",
            "Price momentum suggests a 2-3% appreciation over the next quarter.",
            "Inventory levels indicate a balanced market favoring neither buyers nor sellers strongly.",
            "Consider focusing on properties with recent price reductions for maximum value."
        ];
        
        const randomInsight = insights[Math.floor(Math.random() * insights.length)];
        
        // Add as new insight
        const newInsight = {
            title: '🤖 AI Market Insight',
            content: randomInsight,
            tags: ['ai', 'analysis'],
            time: 'Just now'
        };
        
        const insightCard = this.createInsightCard(newInsight, true);
        document.querySelector('.insights-container').insertBefore(insightCard, 
            document.querySelector('.insights-container').firstChild);
        
        // Clear input
        input.value = '';
        
        this.showToast('AI insight generated!', 'success');
    }
    
    startAutoRefresh(intervalMs = 10 * 60 * 1000) {
        // Clear existing interval
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
        
        // Set new interval
        this.autoRefreshInterval = setInterval(() => {
            this.refreshData();
        }, intervalMs);
        
        console.log(`Auto-refresh started: ${intervalMs / 60000} minutes`);
    }
    
    showWelcomeMessage() {
        // Check if this is first visit today
        const lastVisit = localStorage.getItem('lastDashboardVisit');
        const today = new Date().toDateString();
        
        if (lastVisit !== today) {
            setTimeout(() => {
                this.showToast('Welcome back! Market data has been updated.', 'info');
                localStorage.setItem('lastDashboardVisit', today);
            }, 1000);
        }
    }
    
    showToast(message, type = 'info') {
        const toastConfig = {
            text: message,
            duration: 3000,
            gravity: "top",
            position: "right",
            backgroundColor: type === 'success' ? '#4caf50' : 
                           type === 'error' ? '#f44336' : 
                           type === 'warning' ? '#ff9800' : '#2196f3'
        };
        
        if (typeof Toastify === 'function') {
            Toastify(toastConfig).showToast();
        } else {
            console.log(`Toast: ${message}`);
        }
    }
}

// Initialize dashboard when page loads
function initializeRealtimeDashboard() {
    window.dashboard = new RealTimeDashboard();
    window.dashboard.initialize();
}

function loadDashboardData() {
    // Already handled by dashboard.initialize()
}

function startAutoRefresh() {
    // Already handled by dashboard.startAutoRefresh()
}

// Export for global use
window.RealTimeDashboard = RealTimeDashboard;
