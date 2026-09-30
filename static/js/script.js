// Add basic interactive functionality if needed
document.addEventListener('DOMContentLoaded', () => {
    console.log("SalaryPredict AI loaded.");
    
    // Add simple animation to form submission
    const form = document.querySelector('.predict-form');
    if (form) {
        form.addEventListener('submit', () => {
            const btn = form.querySelector('button[type="submit"]');
            btn.innerHTML = 'Predicting...';
            btn.style.opacity = '0.8';
        });
    }
});
